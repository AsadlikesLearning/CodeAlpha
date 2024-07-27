import tkinter as tk
from tkinter import messagebox, font
import random
from words import words_list
from PIL import Image, ImageTk


class HangmanGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Bollywood Hangman")
        self.master.geometry("900x700")
        self.master.configure(bg="#1e1e1e")

        self.word = None
        self.hint = None
        self.tries = None
        self.guessed_letters = None
        self.hangman_images = self.load_hangman_images()

        self.setup_new_game()
        self.create_widgets()

    def load_hangman_images(self):
        image_paths = [f"hangman_{i}.png" for i in range(7)]
        images = []
        for path in image_paths:
            try:
                img = Image.open(path)
                img = img.resize((200, 200), Image.Resampling.LANCZOS)
                images.append(ImageTk.PhotoImage(img))
            except FileNotFoundError:
                print(f"Warning: Image file {path} not found. Using placeholder.")
                # Create a blank image as a placeholder
                img = Image.new('RGB', (200, 200), color='gray')
                images.append(ImageTk.PhotoImage(img))
        return images
    def setup_new_game(self):
        self.word, self.hint = random.choice(words_list)
        self.tries = 6
        self.guessed_letters = []

    def create_widgets(self):
        # Custom fonts
        title_font = font.Font(family="Helvetica", size=36, weight="bold")
        main_font = font.Font(family="Helvetica", size=18)
        button_font = font.Font(family="Helvetica", size=14, weight="bold")

        self.title_label = tk.Label(self.master, text="Bollywood Hangman", font=title_font, bg="#1e1e1e", fg="#ffd700")
        self.title_label.pack(pady=20)

        main_frame = tk.Frame(self.master, bg="#1e1e1e")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        left_frame = tk.Frame(main_frame, bg="#1e1e1e")
        left_frame.pack(side="left", padx=20)

        self.hangman_display = tk.Label(left_frame, image=self.hangman_images[6], bg="#1e1e1e")
        self.hangman_display.pack(pady=10)

        right_frame = tk.Frame(main_frame, bg="#1e1e1e")
        right_frame.pack(side="right", padx=20, expand=True, fill="both")

        self.word_display = tk.Label(right_frame, text=self.get_displayed_word(), font=main_font, bg="#1e1e1e",
                                     fg="#ffffff")
        self.word_display.pack(pady=10)

        self.guessed_letters_label = tk.Label(right_frame, text="Guessed letters: ", font=main_font, bg="#1e1e1e",
                                              fg="#c0c0c0")
        self.guessed_letters_label.pack(pady=5)

        self.tries_label = tk.Label(right_frame, text=f"Tries left: {self.tries}", font=main_font, bg="#1e1e1e",
                                    fg="#ff6b6b")
        self.tries_label.pack(pady=5)

        input_frame = tk.Frame(right_frame, bg="#1e1e1e")
        input_frame.pack(pady=20)

        self.guess_entry = tk.Entry(input_frame, font=main_font, width=5, bg="#2c2c2c", fg="#ffffff",
                                    insertbackground="#ffffff")
        self.guess_entry.pack(side="left", padx=5)
        self.guess_entry.bind("<Return>", lambda event: self.make_guess())

        self.guess_button = tk.Button(input_frame, text="Guess", command=self.make_guess, font=button_font,
                                      bg="#4caf50", fg="#ffffff", activebackground="#45a049")
        self.guess_button.pack(side="left")

        self.hint_button = tk.Button(right_frame, text="Get Hint", command=self.show_hint, font=button_font,
                                     bg="#2196f3", fg="#ffffff", activebackground="#1e88e5")
        self.hint_button.pack(pady=10)

        self.hint_label = tk.Label(right_frame, text="", font=main_font, wraplength=300, bg="#1e1e1e", fg="#ffd700")
        self.hint_label.pack(pady=10)

        self.new_game_button = tk.Button(right_frame, text="New Game", command=self.new_game, font=button_font,
                                         bg="#ff9800", fg="#ffffff", activebackground="#f57c00")
        self.new_game_button.pack(pady=20)

        self.create_virtual_keyboard()

    def create_virtual_keyboard(self):
        keyboard_frame = tk.Frame(self.master, bg="#1e1e1e")
        keyboard_frame.pack(pady=20)

        rows = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]

        for row in rows:
            row_frame = tk.Frame(keyboard_frame, bg="#1e1e1e")
            row_frame.pack()
            for letter in row:
                btn = tk.Button(row_frame, text=letter, width=4, height=2, font=("Helvetica", 10, "bold"),
                                command=lambda l=letter: self.virtual_keyboard_press(l),
                                bg="#333333", fg="#ffffff", activebackground="#555555")
                btn.pack(side="left", padx=2, pady=2)

    def virtual_keyboard_press(self, letter):
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.insert(0, letter)
        self.make_guess()

    def get_displayed_word(self):
        return " ".join(letter if letter in self.guessed_letters or letter == " " else "_" for letter in self.word)

    def make_guess(self):
        guess = self.guess_entry.get().upper()
        self.guess_entry.delete(0, tk.END)

        if len(guess) == 1 and guess.isalpha():
            if guess in self.guessed_letters:
                self.flash_message("Repeat Guess", f"You already guessed the letter {guess}")
            elif guess in self.word:
                self.guessed_letters.append(guess)
                self.flash_message("Good Guess", f"Good job! {guess} is in the movie title!")
                self.animate_correct_guess()
            else:
                self.guessed_letters.append(guess)
                self.tries -= 1
                self.flash_message("Wrong Guess", f"{guess} is not in the movie title.")
                self.animate_wrong_guess()
        elif len(guess) == len(self.word) and guess.isalpha():
            if guess == self.word:
                self.word_display.config(text=self.word)
                self.game_over("Congratulations! You guessed the movie!")
                return
            else:
                self.tries -= 1
                self.flash_message("Wrong Guess", f"{guess} is not the correct movie title.")
                self.animate_wrong_guess()
        else:
            self.flash_message("Invalid Guess", "Please enter a single letter or the full movie title.")

        self.update_display()
        self.check_game_over()

    def update_display(self):
        self.hangman_display.config(image=self.hangman_images[self.tries])
        self.word_display.config(text=self.get_displayed_word())
        self.guessed_letters_label.config(text=f"Guessed letters: {' '.join(sorted(self.guessed_letters))}")
        self.tries_label.config(text=f"Tries left: {self.tries}")

    def check_game_over(self):
        if "_" not in self.get_displayed_word():
            self.game_over("Congratulations! You guessed the movie!")
        elif self.tries == 0:
            self.game_over(f"Game Over! The movie was {self.word}")

    def game_over(self, message):
        play_again = messagebox.askyesno("Game Over", f"{message}\nDo you want to play again?")
        if play_again:
            self.new_game()
        else:
            self.master.quit()

    def new_game(self):
        self.setup_new_game()
        self.update_display()
        self.guess_entry.delete(0, tk.END)
        self.hint_label.config(text="")
        self.flash_message("New Game", "A new game has started!")

    def show_hint(self):
        self.hint_label.config(text=f"Hint: {self.hint}")

    def flash_message(self, title, message):
        popup = tk.Toplevel(self.master)
        popup.title(title)
        popup.geometry("300x100")
        popup.configure(bg="#333333")

        label = tk.Label(popup, text=message, font=("Helvetica", 12), bg="#333333", fg="#ffffff")
        label.pack(expand=True)

        popup.after(1500, popup.destroy)

    def animate_correct_guess(self):
        original_color = self.word_display.cget("fg")
        self.word_display.config(fg="#00ff00")
        self.master.after(500, lambda: self.word_display.config(fg=original_color))

    def animate_wrong_guess(self):
        original_color = self.word_display.cget("fg")
        self.word_display.config(fg="#ff0000")
        self.master.after(500, lambda: self.word_display.config(fg=original_color))


def main():
    root = tk.Tk()
    hangman_game = HangmanGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()