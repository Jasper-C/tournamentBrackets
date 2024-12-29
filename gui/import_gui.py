import tkinter as tk
from tkinter import filedialog, messagebox
from logic.data_import import validate_and_import


class ImportGUI:
    def __init__(self, root, db_path="main_sports.db"):
        self.root = root
        self.db_path = db_path
        self.root.title("Tournament Data Import")
        self.root.geometry("400x300")

        # Title Label
        tk.Label(root, text="Import Data", font=("Arial", 16)).pack(pady=10)

        # Import Teams Button
        tk.Button(
            root, text="Import Teams File", command=lambda: self.import_file("Teams")
        ).pack(pady=10)

        # Import Ballparks Button
        tk.Button(
            root, text="Import Ballparks File", command=lambda: self.import_file("Ballparks")
        ).pack(pady=10)

        # Quit Button
        tk.Button(
            root, text="Back", command=root.quit
        ).pack(pady=20)

    def import_file(self, table_name):
        file_path = filedialog.askopenfilename(
            title=f"Select {table_name} File",
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
        )
        if not file_path:
            return

        try:
            validate_and_import(file_path, table_name, self.db_path)
            messagebox.showinfo("Success", f"{table_name} data imported successfully!")
        except Exception as e:
            messagebox.showerror("Import Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = ImportGUI(root)
    root.mainloop()
