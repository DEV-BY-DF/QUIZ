import random

# Definition der Lernkarten
flashcards = [
    {
        "frage": "Was ist die Hauptstadt von Deutschland?",
        "auswahl": ["Berlin", "München", "Hamburg", "Köln"],
        "antwort": "Berlin"
    },
    {
        "frage": "Welches Element hat das chemische Symbol 'O'?",
        "auswahl": ["Gold", "Oxygen", "Silber", "Magnesium"],
        "antwort": "Oxygen"
    },
    {
        "frage": "Wer hat die Relativitätstheorie formuliert?",
        "auswahl": ["Isaac Newton", "Albert Einstein", "Nikola Tesla", "Galileo Galilei"],
        "antwort": "Albert Einstein"
    },
    {
        "frage": "In welchem Jahr begann der Zweite Weltkrieg?",
        "auswahl": ["1914", "1939", "1945", "1929"],
        "antwort": "1939"
    },
    {
        "frage": "Wie viele Planeten hat unser Sonnensystem?",
        "auswahl": ["7", "8", "9", "10"],
        "antwort": "8"
    }
]


def run_quiz(cards):
    """
    Führt das Quiz mit den gegebenen Karten durch.
    """
    random.shuffle(cards)
    score = 0

    for idx, card in enumerate(cards, 1):
        print(f"Frage {idx}: {card['frage']}")
        # Auswahllisten mischen
        options = card['auswahl'][:]
        random.shuffle(options)

        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")

        # Eingabe des Benutzers
        try:
            choice = int(input("Deine Wahl (Zahl eingeben): "))
            selected = options[choice - 1]
        except (ValueError, IndexError):
            selected = None

        # Überprüfung der Antwort
        if selected == card['antwort']:
            print("✅ Richtig!\n")
            score += 1
        else:
            print(f"❌ Falsch! Die richtige Antwort ist: {card['antwort']}\n")

    # Endergebnis ausgeben
    print(f"Quiz beendet! Du hast {score} von {len(cards)} richtig beantwortet.")


if __name__ == "__main__":
    print("Willkommen zum Lernkarten-Quiz!")
    run_quiz(flashcards)
