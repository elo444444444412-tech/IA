import tkinter as tk
from tkinter import scrolledtext
import re

APP_NAME = "IA"

# Lightweight offline conversational engine: no API, no internet, no external service.
INTENTS = [
    (r"\b(bonjour|salut|coucou|hello|hey)\b", "Bonjour ! Je suis IA, ton assistant hors ligne. Comment puis-je t'aider ?"),
    (r"\b(qui es[- ]tu|tu es qui|présente[- ]toi)\b", "Je suis IA, un petit assistant conversationnel local écrit en Python. Je fonctionne sans connexion Internet."),
    (r"\b(aide|help)\b", "Tu peux me poser une question, demander une explication, une reformulation ou un petit calcul."),
    (r"\b(merci|thanks)\b", "Avec plaisir !"),
    (r"\b(au revoir|bye|à bientôt)\b", "À bientôt !"),
]


def calculate(text):
    expr = text.lower().replace("×", "*").replace("÷", "/")
    expr = re.sub(r"[^0-9+\-*/().% ]", "", expr)
    if not expr.strip():
        return None
    try:
        # Restrict evaluation to arithmetic characters only.
        return str(eval(expr, {"__builtins__": {}}, {}))
    except Exception:
        return None


def answer(text):
    clean = text.strip()
    low = clean.lower()

    if low.startswith(("calcule ", "calcul ")):
        result = calculate(clean.split(" ", 1)[1])
        if result is not None:
            return f"Résultat : {result}"

    for pattern, response in INTENTS:
        if re.search(pattern, low):
            return response

    if "explique" in low or "définis" in low or "définition" in low:
        topic = clean.split(" ", 1)[-1].strip(" :")
        return f"Je peux t'aider à comprendre « {topic} ». Donne-moi un peu plus de contexte et je construirai une explication simple."

    return ("Je suis une IA locale en version de base. Je n'ai pas accès à Internet ni à un modèle distant. "
            "Je peux cependant répondre à des commandes simples, faire des calculs et être étendue avec un modèle local.")


class IAApp:
    def __init__(self, root):
        self.root = root
        root.title(APP_NAME)
        root.geometry("900x650")
        root.minsize(650, 480)

        header = tk.Frame(root, padx=18, pady=14)
        header.pack(fill="x")
        tk.Label(header, text="IA", font=("Segoe UI", 24, "bold")).pack(side="left")
        tk.Label(header, text="Assistant Python hors ligne", font=("Segoe UI", 11)).pack(side="left", padx=14, pady=(9, 0))

        self.chat = scrolledtext.ScrolledText(root, wrap="word", font=("Segoe UI", 12), state="disabled", padx=14, pady=14)
        self.chat.pack(fill="both", expand=True, padx=18, pady=(0, 12))

        bottom = tk.Frame(root, padx=18, pady=14)
        bottom.pack(fill="x")
        self.entry = tk.Entry(bottom, font=("Segoe UI", 12))
        self.entry.pack(side="left", fill="x", expand=True, ipady=9)
        self.entry.bind("<Return>", lambda _e: self.send())
        tk.Button(bottom, text="Envoyer", font=("Segoe UI", 11, "bold"), command=self.send, padx=18).pack(side="left", padx=(10, 0), ipady=5)

        self.write("IA", "Bonjour ! Je suis prêt à discuter.")
        self.entry.focus_set()

    def write(self, speaker, text):
        self.chat.config(state="normal")
        self.chat.insert("end", f"{speaker} : {text}\n\n")
        self.chat.see("end")
        self.chat.config(state="disabled")

    def send(self):
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, "end")
        self.write("Vous", text)
        self.root.after(80, lambda: self.write("IA", answer(text)))


if __name__ == "__main__":
    root = tk.Tk()
    IAApp(root)
    root.mainloop()
