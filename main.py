"""
Lernkarten-Quizgame mit CustomTkinter GUI, Fortschrittsanzeige und modernem Layout

Abhängigkeiten:
- customtkinter (Installation: pip install customtkinter)
"""

import random
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

# Optional: Erscheinungsbild festlegen
ctk.set_appearance_mode("System")  # "Dark" oder "Light"
ctk.set_default_color_theme("blue")  # Themes: blue, dark-blue, green

# Definition der Lernkarten
default_flashcards = [
    {"frage": "Was ist die Hauptstadt von Deutschland?", "auswahl": ["Berlin", "München", "Hamburg", "Köln"], "antwort": "Berlin"},
    {"frage": "Welches Element hat das chemische Symbol 'O'?", "auswahl": ["Gold", "Oxygen", "Silber", "Magnesium"], "antwort": "Oxygen"},
    {"frage": "Wer hat die Relativitätstheorie formuliert?", "auswahl": ["Isaac Newton", "Albert Einstein", "Nikola Tesla", "Galileo Galilei"], "antwort": "Albert Einstein"},
    {"frage": "In welchem Jahr begann der Zweite Weltkrieg?", "auswahl": ["1914", "1939", "1945", "1929"], "antwort": "1939"},
    {"frage": "Wie viele Planeten hat unser Sonnensystem?", "auswahl": ["7", "8", "9", "10"], "antwort": "8"}
]

class QuizApp(ctk.CTk):
    def __init__(self, flashcards=None):
        super().__init__()
        self.title("Lernkarten-Quiz")
        self.geometry("650x450")
        self.resizable(False, False)

        # Daten
        self.flashcards = flashcards or default_flashcards[:]
        random.shuffle(self.flashcards)
        self.score = 0
        self.index = 0
        self.selected = tk.StringVar(value="")

        # Layout: Header, Frage, Optionen, Footer
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))
        self.body_frame = ctk.CTkFrame(self)
        self.body_frame.pack(fill="both", expand=True, padx=20)
        self.footer_frame = ctk.CTkFrame(self)
        self.footer_frame.pack(fill="x", padx=20, pady=(10, 20))

        # Header: Titel + Fortschrittsanzeige + Punktezähler
        self.title_label = ctk.CTkLabel(self.header_frame, text="Lernkarten-Quiz", font=("Arial", 20, "bold"))
        self.title_label.pack(side="left")
        self.progress = ctk.CTkProgressBar(self.header_frame, width=200)
        self.progress.set(0)
        self.progress.pack(side="left", padx=20)
        self.score_label = ctk.CTkLabel(self.header_frame, text="Score: 0", font=("Arial", 14))
        self.score_label.pack(side="right")

        # Frage-Label
        self.question_label = ctk.CTkLabel(self.body_frame, text="", wraplength=600, font=("Arial", 16))
        self.question_label.pack(pady=20)

        # Optionen-Container
        self.options_frame = ctk.CTkFrame(self.body_frame)
        self.options_frame.pack(fill="x", pady=10)

        # Footer: Weiter-Button und Theme-Toggle
        self.next_button = ctk.CTkButton(self.footer_frame, text="Weiter", command=self.next_question, width=100)
        self.next_button.pack(side="right")
        # Appearance Mode Switch
        self.theme_switch = ctk.CTkSwitch(self.footer_frame, text="Dark Mode", command=self.toggle_theme)
        self.theme_switch.pack(side="left")

        self.display_question()

    def toggle_theme(self):
        mode = "Dark" if self.theme_switch.get() else "Light"
        ctk.set_appearance_mode(mode)

    def display_question(self):
        # Überschrift aktualisieren
        total = len(self.flashcards)
        self.question_label.configure(text=f"Frage {self.index+1} von {total}:\n{self.flashcards[self.index]['frage']}")

        # Alte Optionen entfernen
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        # Neue Radiobuttons erstellen
        options = self.flashcards[self.index]['auswahl'][:]
        random.shuffle(options)
        for opt in options:
            rb = ctk.CTkRadioButton(self.options_frame, text=opt, variable=self.selected, value=opt)
            rb.pack(fill="x", padx=30, pady=5)

        # Reset Auswahl & Button
        self.selected.set("")
        self.next_button.configure(state="normal")

        # Fortschritt aktualisieren
        progress_value = self.index / total
        self.progress.set(progress_value)
        self.score_label.configure(text=f"Score: {self.score}")

    def next_question(self):
        sel = self.selected.get()
        if not sel:
            messagebox.showwarning("Keine Auswahl", "Bitte wähle eine Antwort aus.")
            return

        # Auswertung
        correct = self.flashcards[self.index]['antwort']
        if sel == correct:
            self.score += 1
        # Highlight
        self.highlight_correct(correct)
        self.next_button.configure(state="disabled")
        # 2 sek. Pause
        self.after(2000, self.proceed_to_next)

    def highlight_correct(self, correct_answer):
        for widget in self.options_frame.winfo_children():
            if isinstance(widget, ctk.CTkRadioButton) and widget.cget("text") == correct_answer:
                widget.configure(text_color="#00cc00", hover_color="#007700")
                break

    def proceed_to_next(self):
        self.index += 1
        if self.index < len(self.flashcards):
            self.display_question()
        else:
            self.show_result()

    def show_result(self):
        # Alles löschen
        for widget in self.winfo_children():
            widget.destroy()
        # Ergebnis
        result_frame = ctk.CTkFrame(self)
        result_frame.pack(fill="both", expand=True, padx=20, pady=20)
        res_label = ctk.CTkLabel(result_frame, text=f"Quiz beendet!\nDu hast {self.score} von {len(self.flashcards)} richtig beantwortet.", font=("Arial", 20), justify="center")
        res_label.pack(expand=True)
        close_btn = ctk.CTkButton(self, text="Schließen", command=self.destroy, width=120)
        close_btn.pack(pady=10)

if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
