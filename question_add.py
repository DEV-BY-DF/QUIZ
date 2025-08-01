# question_add.py
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os

# Theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class QuestionAdder(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Fragen hinzufügen")
        self.geometry("700x850")
        self.minsize(700, 850)
        
        # Load logo
        try:
            self.logo_image = ctk.CTkImage(dark_image=Image.open("logo.png"), size=(200, 200))
        except:
            self.logo_image = None
            
        self.questions_file = "questions.json"
        self.setup_gui()

    def setup_gui(self):
        self.clear_window()
        
        # Main frame
        main_frame = ctk.CTkFrame(self, corner_radius=15)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Logo or Title
        if self.logo_image:
            logo_label = ctk.CTkLabel(main_frame, image=self.logo_image, text="")
            logo_label.pack(pady=10)
        else:
            title_label = ctk.CTkLabel(main_frame, text="Fragen hinzufügen", font=("Arial", 24, "bold"))
            title_label.pack(pady=10)
            
        # File selection
        file_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        file_frame.pack(pady=10, fill="x", padx=20)
        
        ctk.CTkLabel(file_frame, text="Fragendatei:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(5, 2))
        
        file_button_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
        file_button_frame.pack(fill="x", padx=10, pady=5)
        
        self.file_label = ctk.CTkLabel(file_button_frame, text=self.questions_file, font=("Arial", 12), anchor="w")
        self.file_label.pack(side="left", fill="x", expand=True, padx=5)
        
        ctk.CTkButton(file_button_frame, text="Ändern", command=self.change_file, width=80, font=("Arial", 12)).pack(side="right", padx=5)
        
        # Category selection
        category_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        category_frame.pack(pady=10, fill="x", padx=20)
        
        ctk.CTkLabel(category_frame, text="Kategorie:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(5, 2))
        
        category_dropdown_frame = ctk.CTkFrame(category_frame, fg_color="transparent")
        category_dropdown_frame.pack(fill="x", padx=10, pady=5)
        
        self.category_var = tk.StringVar()
        self.category_dropdown = ctk.CTkComboBox(
            category_dropdown_frame, 
            variable=self.category_var, 
            font=("Arial", 12),
            width=400
        )
        self.category_dropdown.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.update_category_dropdown()
        
        ctk.CTkButton(category_dropdown_frame, text="Neu", command=self.add_new_category, font=("Arial", 12), width=60).pack(side="right", padx=5)
        
        # Question input
        question_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        question_frame.pack(pady=10, fill="x", padx=20)
        
        ctk.CTkLabel(question_frame, text="Frage:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(5, 2))
        
        self.question_entry = ctk.CTkTextbox(question_frame, height=80, font=("Arial", 12))
        self.question_entry.pack(fill="x", padx=10, pady=5)
        
        # Answer options
        answers_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        answers_frame.pack(pady=10, fill="x", padx=20)
        
        ctk.CTkLabel(answers_frame, text="Antwortmöglichkeiten:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(5, 2))
        
        self.answer_entries = []
        self.correct_answer_var = tk.StringVar(value="0") # Default to first answer
        
        for i in range(4):
            entry_frame = ctk.CTkFrame(answers_frame, fg_color="transparent")
            entry_frame.pack(fill="x", padx=10, pady=2)
            
            rb = ctk.CTkRadioButton(entry_frame, text="", variable=self.correct_answer_var, value=str(i), width=20)
            rb.pack(side="left", padx=(0, 5))
            
            entry = ctk.CTkEntry(entry_frame, placeholder_text=f"Antwort {i+1}", font=("Arial", 12))
            entry.pack(side="left", fill="x", expand=True, padx=5)
            self.answer_entries.append(entry)
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20, fill="x", padx=20)
        
        ctk.CTkButton(
            button_frame, 
            text="Frage hinzufügen", 
            command=self.add_question, 
            height=40,
            font=("Arial", 14, "bold")
        ).pack(side="left", fill="x", expand=True, padx=5)
        
        ctk.CTkButton(
            button_frame, 
            text="Zurücksetzen", 
            command=self.reset_fields, 
            height=40,
            font=("Arial", 14, "bold")
        ).pack(side="right", fill="x", expand=True, padx=5)

    def change_file(self):
        file_path = filedialog.askopenfilename(
            title="Fragendatei auswählen",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir="." # Start in current directory
        )
        if file_path:
            self.questions_file = file_path
            self.file_label.configure(text=self.questions_file)
            self.update_category_dropdown()

    def update_category_dropdown(self):
        try:
            if os.path.exists(self.questions_file):
                with open(self.questions_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                categories = list(data.keys()) if isinstance(data, dict) else []
                self.category_dropdown.configure(values=categories)
                if categories:
                    self.category_var.set(categories[0])
                else:
                    self.category_var.set("")
            else:
                # File doesn't exist yet, offer to create it or select another
                self.category_dropdown.configure(values=[])
                self.category_var.set("")
                # Optionally, you could prompt to create a new file here
        except (FileNotFoundError, json.JSONDecodeError) as e:
            messagebox.showerror("Fehler", f"Fehler beim Lesen der Datei {self.questions_file}: {str(e)}")
            self.category_dropdown.configure(values=[])
            self.category_var.set("")

    def add_new_category(self):
        new_category = ctk.CTkInputDialog(text="Neue Kategorie eingeben:", title="Neue Kategorie")
        category_name = new_category.get_input()
        
        if category_name:
            try:
                # Load existing data or create new structure
                if os.path.exists(self.questions_file):
                    with open(self.questions_file, 'r', encoding='utf-8') as f:
                        try:
                            data = json.load(f)
                        except json.JSONDecodeError:
                            data = {} # Start fresh if file is corrupted
                else:
                    data = {}
                
                # Ensure data is a dictionary
                if not isinstance(data, dict):
                    data = {}
                
                # Add new category if it doesn't exist
                if category_name not in data:
                    data[category_name] = []
                    
                    # Save updated data
                    with open(self.questions_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
                    
                    # Update dropdown
                    self.update_category_dropdown()
                    self.category_var.set(category_name)
                    messagebox.showinfo("Erfolg", f"Kategorie '{category_name}' hinzugefügt")
                else:
                    messagebox.showwarning("Warnung", f"Kategorie '{category_name}' existiert bereits")
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Hinzufügen der Kategorie: {str(e)}")

    def add_question(self):
        # Get values
        category = self.category_var.get().strip()
        question = self.question_entry.get("1.0", "end-1c").strip()
        answers = [entry.get().strip() for entry in self.answer_entries]
        
        # Validate inputs
        if not category:
            messagebox.showerror("Fehler", "Bitte wählen oder erstellen Sie eine Kategorie")
            return
            
        if not question:
            messagebox.showerror("Fehler", "Bitte geben Sie eine Frage ein")
            return
            
        # Filter out empty answers but ensure at least one exists
        non_empty_answers = [ans for ans in answers if ans]
        if not non_empty_answers:
            messagebox.showerror("Fehler", "Bitte geben Sie mindestens eine Antwort ein")
            return
            
        # Validate correct answer selection
        try:
            correct_answer_index = int(self.correct_answer_var.get())
        except ValueError:
            messagebox.showerror("Fehler", "Ungültige Auswahl für die korrekte Antwort")
            return
            
        if correct_answer_index < 0 or correct_answer_index >= len(answers) or not answers[correct_answer_index]:
            messagebox.showerror("Fehler", "Bitte wählen Sie eine gültige korrekte Antwort")
            return
            
        correct_answer = answers[correct_answer_index]
        
        # Create question object
        question_obj = {
            "frage": question,
            "auswahl": answers, # Keep original list including empty ones for structure
            "antwort": correct_answer
        }
        
        try:
            # Load existing data or create new structure
            if os.path.exists(self.questions_file):
                with open(self.questions_file, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = {} # Start fresh if file is corrupted
            else:
                data = {}
            
            # Ensure data is a dictionary
            if not isinstance(data, dict):
                data = {}
            
            # Add question to category
            if category not in data:
                data[category] = []
            data[category].append(question_obj)
            
            # Save updated data
            with open(self.questions_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
            
            messagebox.showinfo("Erfolg", "Frage erfolgreich hinzugefügt")
            self.reset_fields()
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern der Frage: {str(e)}")

    def reset_fields(self):
        self.question_entry.delete("1.0", "end")
        for entry in self.answer_entries:
            entry.delete(0, "end")
        self.correct_answer_var.set("0") # Reset to first answer

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    # Import here to avoid conflicts if PIL is not available
    try:
        from PIL import Image
    except ImportError:
        # If PIL is not available, disable logo loading
        class MockImage:
            @staticmethod
            def open(*args, **kwargs):
                raise FileNotFoundError("PIL/Pillow not installed")
        Image = MockImage()
        
    app = QuestionAdder()
    app.mainloop()