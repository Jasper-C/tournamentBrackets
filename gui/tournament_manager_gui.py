import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from logic.tournament_manager import save_tournament, load_tournament, update_tournament
import sqlite3
import json
import datetime

DB_PATH = "main_sports.db"


class TournamentManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tournament Manager")

        # Main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Tournament list
        self.tournament_tree = ttk.Treeview(
            self.main_frame, columns=("Name", "League/Sport", "Type", "Status"), show="headings"
        )
        self.tournament_tree.heading("Name", text="Name")
        self.tournament_tree.heading("League/Sport", text="League/Sport")
        self.tournament_tree.heading("Type", text="Type")
        self.tournament_tree.heading("Status", text="Status")
        self.tournament_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill=tk.X)

        self.create_button = tk.Button(self.button_frame, text="Create Tournament", command=self.create_tournament)
        self.create_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.load_button = tk.Button(self.button_frame, text="Load Tournament", command=self.load_tournament)
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.edit_button = tk.Button(self.button_frame, text="Edit Tournament", command=self.edit_tournament)
        self.edit_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Load tournaments on startup
        self.load_tournament_list()


    def load_tournament_list(self):
        """Load the list of tournaments into the treeview."""
        for row in self.tournament_tree.get_children():
            self.tournament_tree.delete(row)

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, league, type, status FROM Tournaments")
            tournaments = cursor.fetchall()

        for tournament in tournaments:
            self.tournament_tree.insert("", "end", values=tournament)

    def create_tournament(self):
        """Create a new tournament."""
        self.tournament_dialog("Create Tournament")

    def edit_tournament(self):
        """Edit the selected tournament."""
        selected_item = self.tournament_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a tournament to edit.")
            return

        tournament_id = self.tournament_tree.item(selected_item, "values")[0]
        self.tournament_dialog("Edit Tournament", tournament_id=int(tournament_id))

    def load_tournament(self):
        """Load and view details of the selected tournament."""
        selected_item = self.tournament_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a tournament to load.")
            return

        tournament_id = self.tournament_tree.item(selected_item, "values")[0]
        tournament = load_tournament(tournament_id, DB_PATH)

        if not tournament:
            messagebox.showerror("Error", f"Tournament with ID {tournament_id} not found.")
            return

        details = json.dumps(tournament, indent=4)
        detail_window = tk.Toplevel(self.root)
        detail_window.title("Tournament Details")
        text_widget = tk.Text(detail_window, wrap=tk.WORD)
        text_widget.insert(tk.END, details)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def tournament_dialog(self, title, tournament_id=None):
        """Dialog for creating or editing a tournament."""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)

        # Input fields
        tk.Label(dialog, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(dialog)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        desc_text = tk.Text(dialog, height=4, wrap=tk.WORD)
        desc_text.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Type:").grid(row=2, column=0, padx=5, pady=5)
        type_combobox = ttk.Combobox(dialog, values=["Single Elimination", "Double Elimination"], state="readonly")
        type_combobox.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(dialog, text="League/Sport:").grid(row=3, column=0, padx=5, pady=5)
        league_combobox = ttk.Combobox(dialog, values=["MLB", "NFL", "NBA", "NHL", "NCAAF", "NCAAB"], state="readonly")
        league_combobox.grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        def save():
            name = name_entry.get()
            description = desc_text.get("1.0", tk.END).strip()
            tournament_type = type_combobox.get()
            league = league_combobox.get()

            if not name or not tournament_type or not league:
                messagebox.showerror("Error", "Name, Type, and League/Sport are required fields.")
                return

            if tournament_id:
                # Update existing tournament
                tournament = load_tournament(tournament_id, DB_PATH)
                tournament["name"] = name
                tournament["description"] = description
                tournament["type"] = tournament_type
                tournament["league"] = league
                tournament["last_updated"] = datetime.now().isoformat()
                update_tournament(tournament_id, tournament["data"], tournament["status"], DB_PATH)
            else:
                # Create new tournament
                tournament_data = {"teams": [], "rounds": []}
                save_tournament(name, description, tournament_type, tournament_data, league, DB_PATH)

            dialog.destroy()
            self.load_tournament_list()

        tk.Button(dialog, text="Save", command=save).grid(row=4, column=0, columnspan=2, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = TournamentManagerGUI(root)
    root.mainloop()
