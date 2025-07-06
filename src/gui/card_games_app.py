import tkinter as tk
from tkinter import ttk, font

class CardGamesGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Card Games")
        self.root.geometry("800x600")  # Larger window size
        self.root.configure(bg="#1a202c")  # Dark background

        # Custom font
        self.custom_font = font.Font(family="Press Start 2P", size=10)

        # Style for buttons
        self.button_style = ttk.Style()
        self.button_style.configure("TButton",
            font=self.custom_font,
            background="#4a5568",  # Dark grey
            foreground="#f7fafc",  # Light text
            padding=(15, 10),
            borderwidth=0,
            relief="raised",
             Borderradius=5
        )
        self.button_style.map("TButton",
            background=[("active", "#718096"), ("pressed", "#4a5568")],
            foreground=[("active", "#f7fafc"), ("pressed", "#f7fafc")],
            relief=[("pressed", "sunken"), ("active", "raised")]
        )

        # Style for labels
        self.label_style = ttk.Style()
        self.label_style.configure("TLabel",
            font=self.custom_font,
            background="#2d3748",  # Match container background
            foreground="#f7fafc",
            padding=(0, 10)
        )
        # Style for title label
        self.title_style = ttk.Style()
        self.title_style.configure("TitleLabel",
            font=self.custom_font,
            background="#2d3748",
            foreground="#f56565",  # Red
            padding=(0, 15)
        )

        # Container frame
        self.container = ttk.Frame(self.root, style="TFrame", padding=(20, 10))
        self.container.pack(fill="both", expand=True)
        self.container.configure(borderwidth=0, relief="solid")

        # Title
        self.title_label = ttk.Label(self.container, text="Card Games")
        self.title_label.pack(pady=10)

        # Game selection frame
        self.game_selection_frame = ttk.Frame(self.container, style="TFrame")
        self.game_selection_frame.pack(pady=10, fill="x")
        self.game_selection_frame.configure()

        # Game selection buttons
        self.game_buttons = {}
        games = ["War", "Blackjack", "Eights", "Goofspiel", "Sevens", "Speed"]
        for i, game in enumerate(games):
            button = ttk.Button(self.game_selection_frame, text=game, command=lambda g=game: self.show_game_info(g), style="TButton")
            button.grid(row=0, column=i, padx=10, pady=5)
            self.game_buttons[game] = button

        # Game info frame
        self.game_info_frame = ttk.Frame(self.container, style="TFrame")
        self.game_info_frame.pack(pady=10, fill="both", expand=True)
        self.game_info_frame.configure(borderwidth=2, relief="groove")

        # Game title label
        self.game_title_label = ttk.Label(self.game_info_frame, text="Select a Game", style="TLabel")
        self.game_title_label.pack(pady=10)
        self.game_title_label.configure(font=font.Font(family="Press Start 2P", size=12), foreground="#f56565")

        # Game description label
        self.game_description_label = ttk.Label(self.game_info_frame,
                                                text="Choose a card game from the options above to get started.",
                                                style="TLabel",
                                                wraplength=600,  # Wrap the text
                                                justify="center")
        self.game_description_label.pack(pady=10)
        self.game_description_label.configure(foreground="#cbd5e0")

        # Game content text
        self.game_content_text = tk.Text(self.game_info_frame,
                                         wrap=tk.WORD,
                                         bg="#374151",  # Match frame background
                                         fg="#f7fafc",
                                         borderwidth=0,
                                         font=self.custom_font,
                                         padx=10,
                                         pady=10,
                                         relief="flat",
                                         height=10
                                         )
        self.game_content_text.pack(fill="both", expand=True)
        self.game_content_text.config(state=tk.DISABLED)  # Make it read-only

    def show_game_info(self, game):
        self.game_title_label.config(text=game)
        if game == "War":
            self.game_description_label.config(text="A simple card game where players flip cards and the highest card wins.")
            self.game_content_text.config(state=tk.NORMAL)
            self.game_content_text.delete("1.0", tk.END)
            self.game_content_text.insert(tk.END, "<h3>How to Play</h3>\nEach player starts with half the deck.  Players simultaneously reveal the top card of their deck.  The player with the higher card wins both cards and adds them to their hand.  If the cards are of equal rank, it's 'War'.")
            self.game_content_text.config(state=tk.DISABLED)
            self.add_play_button("War")
        elif game == "Blackjack":
            self.game_description_label.config(text="A classic casino game where players try to get a hand value closest to 21 without going over.")
            self.game_content_text.config(state=tk.NORMAL)
            self.game_content_text.delete("1.0", tk.END)
            self.game_content_text.insert(tk.END, "<h3>How to Play</h3>\nPlayers and the dealer are dealt two cards.  The goal is to have a hand value as close to 21 as possible.  Players can 'hit' to get another card or 'stand' to keep their hand.")
            self.game_content_text.config(state=tk.DISABLED)
            self.add_play_button("Blackjack")
        elif game == "Eights":
            self.game_description_label.config(text="A shedding-type card game where players try to get rid of all their cards.")
            self.game_content_text.config(state=tk.NORMAL)
            self.game_content_text.delete("1.0", tk.END)
            self.game_content_text.insert(tk.END, "<h3>How to Play</h3>\nPlayers match the rank or suit of the top card on the discard pile. Eights are wild and can be played on any card, and the player must declare the new suit.")
            self.game_content_text.config(state=tk.DISABLED)
            self.add_play_button("Eights")
        elif game == "Goofspiel":
            self.game_description_label.config(text="A bidding game where players bid for cards in the center.")
            self.game_content_text.config(state=tk.NORMAL)
            self.game_content_text.delete("1.0", tk.END)
            self.game_content_text.insert(tk.END, "<h3>How to Play</h3>\nPlayers bid on face-up cards using their own set of cards.  The highest bidder wins the card.")
            self.game_content_text.config(state=tk.DISABLED)
            self.add_play_button("Goofspiel")
        elif game == "Sevens":
            self.game_description_label.config(text="A game where players play cards in sequence, starting with sevens.")
            self.game_content_text.config(state=tk.NORMAL)
            self.game_content_text.delete("1.0", tk.END)
            self.game_content_text.insert(tk.END, "<h3>How to Play</h3>\nPlayers must play sevens first, then other cards in the same suit in ascending or descending order.")
            self.game_content_text.config(state=tk.DISABLED)
            self.add_play_button("Sevens")
        elif game == "Speed":
            self.game_description_label.config(text="A fast-paced game where players race to get rid of their cards.")
            self.game_content_text.config(state=tk.NORMAL)
            self.game_content_text.delete("1.0", tk.END)
            self.game_content_text.insert(tk.END, "<h3>How to Play</h3>\nPlayers have two face-up piles and try to play cards from these piles onto two center piles. The cards played must be one rank higher or lower than the center pile.")
            self.game_content_text.config(state=tk.DISABLED)
            self.add_play_button("Speed")

    def add_play_button(self, game_name):
        # Remove any existing buttons
        for child in self.game_info_frame.winfo_children():
            if isinstance(child, ttk.Button) and child.winfo_name() == "play_button":
                child.destroy()

        # Create the button
        play_button = ttk.Button(self.game_info_frame, text=f"Play {game_name}", command=lambda g=game_name: self.start_game(g), style="TButton", name="play_button")
        play_button.pack(pady=10)

    def start_game(self, game_name):
        # Placeholder for starting the game.  This is where you'd integrate
        # your Python game logic.  For example, you might have functions
        # in other modules (e.g., war.py, blackjack.py) that handle the
        # game logic.  You would import those functions here and call them.
        #
        # Example (Conceptual):
        # if game_name == "War":
        #     import war
        #     war.play_game()  # Call a function to start the War game
        # elif game_name == "Blackjack":
        #     import blackjack
        #     blackjack.start_new_game()
        #
        #  For now, we'll just print a message.
        self.game_content_text.config(state=tk.NORMAL)
        self.game_content_text.delete("1.0", tk.END)
        self.game_content_text.insert(tk.END, f"Starting {game_name}...")
        self.game_content_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    CardGamesGUI(root)
    root.mainloop()

