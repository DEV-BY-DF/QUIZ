import random
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime
import time
from PIL import Image, ImageTk

# Theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Load quiz categories from external JSON file
def load_quiz_categories(filename="questions.json"):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback to original data if file not found
        print(f"Warnung: {filename} nicht gefunden. Verwende eingebaute Fragen.")
        return get_default_quiz_categories()
    except json.JSONDecodeError:
        print(f"Fehler beim Lesen von {filename}. Verwende eingebaute Fragen.")
        return get_default_quiz_categories()

def get_default_quiz_categories():
    # Original Fragenkategorien als Fallback
    return {
        "Planen, Vorbereiten und Durchführen von Arbeitsaufgaben": [
            {"frage": "Welche Methode wird häufig für die Projektplanung verwendet?", "auswahl": ["Wasserfallmodell", "Scrum", "Beides", "Keine"], "antwort": "Beides"},
            {"frage": "Was ist ein wichtiger Bestandteil der Arbeitsvorbereitung?", "auswahl": ["Ressourcenplanung", "Kaffeepause", "Social Media", "Chatten"], "antwort": "Ressourcenplanung"},
            {"frage": "Welches Dokument beschreibt die Vorgehensweise bei einem Projekt?", "auswahl": ["Projektplan", "Einkaufsliste", "Speiseplan", "Wetterbericht"], "antwort": "Projektplan"},
            {"frage": "Was gehört zur Auftragsdurchführung?", "auswahl": ["Zeiterfassung", "Urlaubsplanung", "Kaffeekochen", "Shoppen"], "antwort": "Zeiterfassung"},
            {"frage": "Welche Rolle ist typisch für einen Projektleiter?", "auswahl": ["Koordination", "Kassieren", "Putzen", "Kochen"], "antwort": "Koordination"}
        ],
        "Informieren und Beraten von Kunden und Kundinnen": [
            {"frage": "Was ist bei einer Kundenberatung wichtig?", "auswahl": ["Aktives Zuhören", "Reden ohne Pause", "Technischer Jargon", "Ignorieren der Wünsche"], "antwort": "Aktives Zuhören"},
            {"frage": "Wie sollte man technische Informationen an Kunden weitergeben?", "auswahl": ["Verständlich und einfach", "Hochkomplex", "Fachchinesisch", "Mit vielen Abkürzungen"], "antwort": "Verständlich und einfach"},
            {"frage": "Welche Fähigkeit ist für Kundenberatung entscheidend?", "auswahl": ["Empathie", "Arroganz", "Unfreundlichkeit", "Uninteressiertheit"], "antwort": "Empathie"},
            {"frage": "Was gehört zur Kundeninformation?", "auswahl": ["Produktdatenblätter", "Geheime Unterlagen", "Private Daten", "Konkurrenzgeheimnisse"], "antwort": "Produktdatenblätter"},
            {"frage": "Wie geht man mit Kundenbeschwerden um?", "auswahl": ["Konstruktiv und lösungsorientiert", "Ablehnend", "Ignorierend", "Aggressiv"], "antwort": "Konstruktiv und lösungsorientiert"}
        ],
        "Beurteilen marktgängiger IT-Systeme und Lösungen": [
            {"frage": "Welches Kriterium ist bei der Systembewertung wichtig?", "auswahl": ["Kosteneffizienz", "Farbe des Gehäuses", "Markenname", "Anzahl der Features"], "antwort": "Kosteneffizienz"},
            {"frage": "Was bedeutet Skalierbarkeit eines Systems?", "auswahl": ["Anpassbarkeit an wachsende Anforderungen", "Schön anzusehen", "Teuer", "Kompliziert"], "antwort": "Anpassbarkeit an wachsende Anforderungen"},
            {"frage": "Welcher Aspekt ist bei IT-Lösungen entscheidend?", "auswahl": ["Kompatibilität", "Design", "Marke", "Popularität"], "antwort": "Kompatibilität"},
            {"frage": "Was ist bei der Bewertung von Softwarelösungen wichtig?", "auswahl": ["Benutzerfreundlichkeit", "Anzahl der Fenster", "Farbe der Icons", "Länge des Namens"], "antwort": "Benutzerfreundlichkeit"},
            {"frage": "Welche Faktoren beeinflussen die Systemauswahl?", "auswahl": ["Performance und Zuverlässigkeit", "Preis allein", "Werbung", "Zufall"], "antwort": "Performance und Zuverlässigkeit"}
        ],
        "Entwickeln, Erstellen und Betreuen von IT-Lösungen": [
            {"frage": "Welcher Prozess gehört zur Softwareentwicklung?", "auswahl": ["Debugging", "Einkaufen", "Kochen", "Sport"], "antwort": "Debugging"},
            {"frage": "Was ist ein wichtiger Aspekt beim Software-Betreuung?", "auswahl": ["Updates und Wartung", "Urlaub", "Partys", "Shopping"], "antwort": "Updates und Wartung"},
            {"frage": "Welche Methode wird im Software-Engineering verwendet?", "auswahl": ["Agile Entwicklung", "Zufallsgenerator", "Würfeln", "Raten"], "antwort": "Agile Entwicklung"},
            {"frage": "Was gehört zur Dokumentation von IT-Lösungen?", "auswahl": ["Quellcode-Kommentare", "Einkaufszettel", "Rezepte", "Notizen"], "antwort": "Quellcode-Kommentare"},
            {"frage": "Welche Rolle spielt Testing in der Entwicklung?", "auswahl": ["Qualitätssicherung", "Zeitverschwendung", "Unwichtig", "Kostenfaktor"], "antwort": "Qualitätssicherung"}
        ],
        "Qualitätssichernde Maßnahmen": [
            {"frage": "Was ist ein Ziel der Qualitätssicherung?", "auswahl": ["Fehlervermeidung", "Fehlerproduktion", "Kostensteigerung", "Zeitverlust"], "antwort": "Fehlervermeidung"},
            {"frage": "Welche Methode gehört zur Qualitätssicherung?", "auswahl": ["Testverfahren", "Raten", "Zufall", "Ignorieren"], "antwort": "Testverfahren"},
            {"frage": "Was ist bei Software-Tests wichtig?", "auswahl": ["Vollständige Abdeckung", "Oberflächliche Prüfung", "Einzelne Funktion", "Zufällige Auswahl"], "antwort": "Vollständige Abdeckung"},
            {"frage": "Welcher Standard ist für Qualität relevant?", "auswahl": ["ISO 9001", "ISO 14001", "ISO 45001", "ISO 27001"], "antwort": "ISO 9001"},
            {"frage": "Was gehört zur kontinuierlichen Verbesserung?", "auswahl": ["Feedback-Schleifen", "Stillstand", "Rückgang", "Ignoranz"], "antwort": "Feedback-Schleifen"}
        ],
        "IT-Sicherheit und Datenschutz, Ergonomie": [
            {"frage": "Welche Maßnahme schützt vor Datenverlust?", "auswahl": ["Regelmäßige Backups", "Keine Backups", "Löschen von Daten", "Ignorieren des Problems"], "antwort": "Regelmäßige Backups"},
            {"frage": "Was ist ein wichtiger Aspekt des Datenschutzes?", "auswahl": ["Verschlüsselung", "Veröffentlichung", "Teilen in sozialen Medien", "Ignorieren"], "antwort": "Verschlüsselung"},
            {"frage": "Welche Ergonomie-Regel gilt am Arbeitsplatz?", "auswahl": ["Richtige Bildschirmhöhe", "Beliebige Position", "Dunkler Raum", "Lauter Musik"], "antwort": "Richtige Bildschirmhöhe"},
            {"frage": "Was schützt vor Phishing-Angriffen?", "auswahl": ["Mitarbeiterschulung", "Klick auf alles", "Ignorieren von Warnungen", "Alle E-Mails öffnen"], "antwort": "Mitarbeiterschulung"},
            {"frage": "Welcher Standard behandelt Informationssicherheit?", "auswahl": ["ISO 27001", "ISO 9001", "ISO 14001", "ISO 45001"], "antwort": "ISO 27001"}
        ],
        "Auftragsabschluss und Leistungserbringung": [
            {"frage": "Was gehört zum ordnungsgemäßen Auftragsabschluss?", "auswahl": ["Dokumentation und Abnahme", "Ignorieren des Kunden", "Weglaufen", "Nichts tun"], "antwort": "Dokumentation und Abnahme"},
            {"frage": "Welche Dokumente sind beim Leistungsvertrag wichtig?", "auswahl": ["Service Level Agreement", "Einkaufsliste", "Speiseplan", "Wetterbericht"], "antwort": "Service Level Agreement"},
            {"frage": "Was ist bei der Leistungserbringung entscheidend?", "auswahl": ["Termintreue", "Verspätung", "Chaotisches Arbeiten", "Ignorieren der Anforderungen"], "antwort": "Termintreue"},
            {"frage": "Welche Vertragsart ist im IT-Bereich üblich?", "auswahl": ["Werkvertrag", "Leihvertrag", "Mietvertrag", "Kaufvertrag"], "antwort": "Werkvertrag"},
            {"frage": "Was gehört zur Kundenzufriedenheit?", "auswahl": ["Einhaltung von Qualitätsstandards", "Überteuerte Rechnungen", "Schlechte Kommunikation", "Verspätete Lieferung"], "antwort": "Einhaltung von Qualitätsstandards"}
        ]
    }

# Load questions from external file
quiz_categories = load_quiz_categories()

class HighscoreManager:
    def __init__(self, filename="highscores.json"):
        self.filename = filename
        self.highscores = self.load_highscores()

    def load_highscores(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_highscores(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.highscores, f, ensure_ascii=False, indent=2)

    def add_score(self, name, score, total, category, time_taken):
        entry = {
            "name": name,
            "score": score,
            "total": total,
            "percentage": round((score/total) * 100, 1),
            "category": category,
            "time_taken": time_taken,
            "date": datetime.now().strftime("%d.%m.%Y %H:%M")
        }
        self.highscores.append(entry)
        # Sortiere nach Prozentzahl (absteigend) und dann nach Zeit (aufsteigend)
        self.highscores.sort(key=lambda x: (-x["percentage"], x["time_taken"]))
        self.highscores = self.highscores[:10]
        self.save_highscores()

    def get_top_scores(self, category=None):
        if category:
            return [s for s in self.highscores if s["category"] == category]
        return self.highscores

class QuizApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.highscore_manager = HighscoreManager()
        self.selected_category = list(quiz_categories.keys())[0]
        self.timer_duration = 30
        self.time_left = self.timer_duration
        self.timer_running = False
        self.timer_id = None
        self.title("IT-Berufe Lernkarten-Quiz")
        self.geometry("1000x900")
        self.minsize(900, 900)
        
        # Load logo
        try:
            self.logo_image = ctk.CTkImage(Image.open("logo.png"), size=(200, 200))
        except:
            self.logo_image = None
            
        self.setup_main_menu()

    def setup_main_menu(self):
        self.clear_window()
        main_frame = ctk.CTkFrame(self, corner_radius=15)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Logo or Title
        if self.logo_image:
            logo_label = ctk.CTkLabel(main_frame, image=self.logo_image, text="")
            logo_label.pack(pady=20)
        else:
            title_label = ctk.CTkLabel(main_frame, text="IT-Berufe Quiz", font=("Arial", 28, "bold"))
            title_label.pack(pady=20)
            
        subtitle_label = ctk.CTkLabel(main_frame, text="Lernfelder der IT-Berufe", font=("Arial", 18))
        subtitle_label.pack(pady=5)
        
        # Category Selection
        category_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        category_frame.pack(pady=20, fill="x", padx=20)
        
        ctk.CTkLabel(category_frame, text="Lernfeld auswählen:", font=("Arial", 16, "bold")).pack(pady=10)
        
        scrollable_category_frame = ctk.CTkScrollableFrame(category_frame, height=200)
        scrollable_category_frame.pack(fill="x", padx=10, pady=5)
        
        self.category_var = tk.StringVar(value=self.selected_category)
        for category in quiz_categories.keys():
            rb = ctk.CTkRadioButton(
                scrollable_category_frame, 
                text=category, 
                variable=self.category_var, 
                value=category,
                font=("Arial", 14)
            )
            rb.pack(fill="x", pady=3, padx=5)
        
        # Timer Setting
        timer_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        timer_frame.pack(pady=20, padx=20, fill="x")
        
        ctk.CTkLabel(timer_frame, text="Zeit pro Frage (Sekunden):", font=("Arial", 14)).pack(pady=5)
        self.timer_var = tk.IntVar(value=self.timer_duration)
        timer_spinbox = ctk.CTkOptionMenu(
            timer_frame, 
            values=["10", "15", "20", "30", "45", "60"], 
            variable=self.timer_var,
            font=("Arial", 14)
        )
        timer_spinbox.pack(pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=20)
        
        ctk.CTkButton(
            button_frame, 
            text="Quiz Starten", 
            command=self.start_quiz, 
            width=150, 
            height=40,
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame, 
            text="Highscores", 
            command=self.show_highscores, 
            width=150, 
            height=40,
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=10)
        
        # Theme Switch
        theme_frame = ctk.CTkFrame(self)
        theme_frame.pack(side="bottom", fill="x", padx=20, pady=10)
        self.theme_switch = ctk.CTkSwitch(
            theme_frame, 
            text="Dark Mode", 
            command=self.toggle_theme,
            font=("Arial", 14)
        )
        self.theme_switch.pack(pady=5)

    def start_quiz(self):
        self.selected_category = self.category_var.get()
        self.timer_duration = self.timer_var.get()
        self.time_left = self.timer_duration
        
        all_questions = quiz_categories[self.selected_category]
        self.flashcards = random.sample(all_questions, min(10, len(all_questions)))
        self.index = 0
        self.score = 0
        self.selected = tk.StringVar()
        self.start_time = time.time()
        self.setup_quiz_interface()
        self.display_question()

    def setup_quiz_interface(self):
        self.clear_window()
        
        # Header
        self.header_frame = ctk.CTkFrame(self, corner_radius=10)
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Header Content
        title_text = self.selected_category
        if len(title_text) > 50:
            title_text = title_text[:47] + "..."
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text=f"Quiz: {title_text}", 
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(side="left", padx=10, pady=10)
        
        self.progress = ctk.CTkProgressBar(self.header_frame, width=200)
        self.progress.set(0)
        self.progress.pack(side="left", padx=15, pady=10)
        
        self.score_label = ctk.CTkLabel(
            self.header_frame, 
            text="Score: 0", 
            font=("Arial", 16, "bold")
        )
        self.score_label.pack(side="right", padx=10, pady=10)
        
        # Timer Label
        self.timer_label = ctk.CTkLabel(
            self.header_frame, 
            text=f"Zeit: {self.time_left}s", 
            font=("Arial", 14, "bold"),
            text_color="red"
        )
        self.timer_label.pack(side="right", padx=10, pady=10)
        
        # Body
        self.body_frame = ctk.CTkFrame(self, corner_radius=10)
        self.body_frame.pack(expand=True, fill="both", padx=20, pady=10)
        
        # Question Label
        self.question_label = ctk.CTkLabel(
            self.body_frame, 
            text="", 
            wraplength=650, 
            font=("Arial", 16), 
            justify="left",
            anchor="w"
        )
        self.question_label.pack(pady=20, padx=20)
        
        # Options Container
        self.options_frame = ctk.CTkFrame(self.body_frame, corner_radius=10)
        self.options_frame.pack(fill="x", pady=10, padx=20)
        
        # Footer
        self.footer_frame = ctk.CTkFrame(self)
        self.footer_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Footer Buttons
        self.next_button = ctk.CTkButton(
            self.footer_frame, 
            text="Weiter", 
            command=self.next_question, 
            width=100,
            font=("Arial", 14, "bold")
        )
        self.next_button.pack(side="right", padx=10)
        
        ctk.CTkButton(
            self.footer_frame, 
            text="Zurück", 
            command=self.setup_main_menu, 
            width=100,
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=10)

    def display_question(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
        self.time_left = self.timer_duration
        self.update_timer_display()
        self.start_timer()
        
        total = len(self.flashcards)
        current = self.flashcards[self.index]
        question_text = f"Frage {self.index+1} von {total}:\n\n{current['frage']}"
        self.question_label.configure(text=question_text)
        
        # Remove old options
        for w in self.options_frame.winfo_children():
            w.destroy()
            
        # Create new radio buttons
        opts = current['auswahl'][:]
        random.shuffle(opts)
        for opt in opts:
            rb = ctk.CTkRadioButton(
                self.options_frame, 
                text=opt, 
                variable=self.selected, 
                value=opt,
                font=("Arial", 14)
            )
            rb.pack(fill="x", padx=20, pady=5)
            
        self.selected.set("")
        self.next_button.configure(state="normal")
        self.progress.set((self.index + 1) / total)
        self.score_label.configure(text=f"Score: {self.score}")

    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.timer_running and self.time_left > 0:
            self.time_left -= 1
            self.update_timer_display()
            self.timer_id = self.after(1000, self.update_timer)
        elif self.time_left <= 0:
            self.time_up()

    def update_timer_display(self):
        self.timer_label.configure(text=f"Zeit: {self.time_left}s")
        if self.time_left <= 10:
            self.timer_label.configure(text_color="#FF3B30")  # Red
        elif self.time_left <= 20:
            self.timer_label.configure(text_color="#FF9500")  # Orange
        else:
            self.timer_label.configure(text_color="#34C759")  # Green

    def time_up(self):
        self.timer_running = False
        messagebox.showinfo("Zeit abgelaufen", "Die Zeit für diese Frage ist abgelaufen!")
        self.highlight_correct(self.flashcards[self.index]['antwort'], None)
        self.next_button.configure(state="disabled")
        self.disable_options()
        self.after(2000, self.proceed_to_next)

    def next_question(self):
        sel = self.selected.get()
        if not sel:
            messagebox.showwarning("Keine Auswahl", "Bitte wähle eine Antwort aus.")
            return
            
        self.timer_running = False
        if self.timer_id:
            self.after_cancel(self.timer_id)
            
        correct = self.flashcards[self.index]['antwort']
        is_correct = sel == correct
        if is_correct:
            self.score += 1
            
        self.highlight_correct(correct, sel)
        self.next_button.configure(state="disabled")
        self.disable_options()
        self.after(2000, self.proceed_to_next)

    def disable_options(self):
        for w in self.options_frame.winfo_children():
            if isinstance(w, ctk.CTkRadioButton):
                w.configure(state="disabled")

    def highlight_correct(self, correct_answer, selected_answer):
        for w in self.options_frame.winfo_children():
            if isinstance(w, ctk.CTkRadioButton):
                text = w.cget("text")
                if text == correct_answer:
                    w.configure(
                        text_color="#34C759",  # Green
                        hover_color="#219653"
                    )
                elif text == selected_answer and text != correct_answer:
                    w.configure(
                        text_color="#FF3B30",  # Red
                        hover_color="#D13438"
                    )

    def proceed_to_next(self):
        self.index += 1
        if self.index < len(self.flashcards):
            self.display_question()
        else:
            self.show_result()

    def show_result(self):
        end_time = time.time()
        time_taken = round(end_time - self.start_time, 1)
        
        # Save highscore
        name = simpledialog.askstring("Highscore", "Gib deinen Namen ein:", parent=self)
        if name:
            self.highscore_manager.add_score(name, self.score, len(self.flashcards), 
                                           self.selected_category, time_taken)
            
        self.clear_window()
        result_frame = ctk.CTkFrame(self, corner_radius=15)
        result_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        result_text = f"Quiz beendet!\n\n"
        result_text += f"Lernfeld: {self.selected_category}\n\n"
        result_text += f"Richtig beantwortet: {self.score} von {len(self.flashcards)}\n\n"
        result_text += f"Prozent: {round((self.score/len(self.flashcards)) * 100, 1)}%\n\n"
        result_text += f"Zeit benötigt: {time_taken} Sekunden"
        
        lbl = ctk.CTkLabel(
            result_frame, 
            text=result_text, 
            font=("Arial", 18, "bold"), 
            justify="center"
        )
        lbl.pack(expand=True, pady=20)
        
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)
        
        ctk.CTkButton(
            button_frame, 
            text="Highscores anzeigen", 
            command=self.show_highscores,
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame, 
            text="Neues Quiz", 
            command=self.setup_main_menu,
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame, 
            text="Schließen", 
            command=self.destroy,
            font=("Arial", 14, "bold")
        ).pack(side="left", padx=5)

    def show_highscores(self):
        self.clear_window()
        hs_frame = ctk.CTkFrame(self, corner_radius=15)
        hs_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        title_label = ctk.CTkLabel(hs_frame, text="Highscores", font=("Arial", 24, "bold"))
        title_label.pack(pady=10)
        
        # Category Selection
        cat_frame = ctk.CTkFrame(hs_frame, corner_radius=10)
        cat_frame.pack(pady=10)
        
        ctk.CTkLabel(cat_frame, text="Lernfeld:", font=("Arial", 14)).pack(side="left")
        self.hs_category_var = tk.StringVar(value="Alle")
        categories = ["Alle"] + list(quiz_categories.keys())
        cat_menu = ctk.CTkOptionMenu(
            cat_frame, 
            values=categories, 
            variable=self.hs_category_var,
            command=self.update_highscore_display,
            width=300,
            font=("Arial", 14)
        )
        cat_menu.pack(side="left", padx=10)
        
        # Highscore Table
        self.hs_display_frame = ctk.CTkFrame(hs_frame, corner_radius=10)
        self.hs_display_frame.pack(expand=True, fill="both", padx=20, pady=10)
        
        self.update_highscore_display()
        
        ctk.CTkButton(
            hs_frame, 
            text="Zurück", 
            command=self.setup_main_menu,
            font=("Arial", 14, "bold")
        ).pack(pady=10)

    def update_highscore_display(self, *args):
        # Clear previous content
        for widget in self.hs_display_frame.winfo_children():
            widget.destroy()
            
        category = self.hs_category_var.get()
        if category == "Alle":
            scores = self.highscore_manager.get_top_scores()
        else:
            scores = self.highscore_manager.get_top_scores(category)
            
        if not scores:
            ctk.CTkLabel(
                self.hs_display_frame, 
                text="Noch keine Highscores vorhanden",
                font=("Arial", 16)
            ).pack(pady=20)
            return
            
        # Scrollable frame for table
        scrollable_hs_frame = ctk.CTkScrollableFrame(self.hs_display_frame, height=300)
        scrollable_hs_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Table Headers
        header_frame = ctk.CTkFrame(scrollable_hs_frame)
        header_frame.pack(fill="x", padx=5, pady=2)
        
        headers = ["Platz", "Name", "Punkte", "Prozent", "Lernfeld", "Zeit", "Datum"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                header_frame, 
                text=header, 
                font=("Arial", 14, "bold")
            ).grid(row=0, column=i, padx=3, pady=2)
            
        # Score entries
        for i, score in enumerate(scores[:10], 1):
            row_frame = ctk.CTkFrame(scrollable_hs_frame)
            row_frame.pack(fill="x", padx=3, pady=1)
            
            ctk.CTkLabel(row_frame, text=str(i), width=40, font=("Arial", 12)).grid(row=0, column=0, padx=2, pady=1)
            ctk.CTkLabel(row_frame, text=score["name"], width=100, font=("Arial", 12)).grid(row=0, column=1, padx=2, pady=1)
            ctk.CTkLabel(row_frame, text=f"{score['score']}/{score['total']}", width=60, font=("Arial", 12)).grid(row=0, column=2, padx=2, pady=1)
            ctk.CTkLabel(row_frame, text=f"{score['percentage']}%", width=60, font=("Arial", 12)).grid(row=0, column=3, padx=2, pady=1)
            
            cat_name = score["category"]
            if len(cat_name) > 20:
                cat_name = cat_name[:17] + "..."
            ctk.CTkLabel(row_frame, text=cat_name, width=120, font=("Arial", 12)).grid(row=0, column=4, padx=2, pady=1)
            
            ctk.CTkLabel(row_frame, text=f"{score['time_taken']}s", width=60, font=("Arial", 12)).grid(row=0, column=5, padx=2, pady=1)
            ctk.CTkLabel(row_frame, text=score["date"], width=120, font=("Arial", 12)).grid(row=0, column=6, padx=2, pady=1)

    def toggle_theme(self):
        mode = "Dark" if self.theme_switch.get() else "Light"
        ctk.set_appearance_mode(mode)

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()