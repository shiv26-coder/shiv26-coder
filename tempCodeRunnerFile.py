import tkinter
import random
from helper import words
from helper import lives_visual_dict
from tkinter import messagebox
import string
import time

def get_valid_word(words):
    word = random.choice(words)
    return word.upper()

def update_display(guess_line):
    lives_line = "You have " + str(lives) + " lives left"
    l1.config(text=lives_line)

    word_list = [letter if letter in used_letters else '_' for letter in word]
    l2.config(text=' '.join(word_list))

    p1.config(text=lives_visual_dict[lives])
    e1.delete(0, tkinter.END)
    e1.focus_set()
    l3.config(text=guess_line)

def reset_game():
    global word, word_letters, used_letters, lives, hint_used, start_time
    word = get_valid_word(words)
    word_letters = set(word)
    used_letters = set()
    lives = 7
    hint_used = 0
    start_time = time.time()
    update_display("Let's begin!")

def end_game(message):
    elapsed_time = int(time.time() - start_time)
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    time_taken = f"\nTime taken: {minutes}m {seconds}s"

    play_again = messagebox.askyesno("Game Over", message + time_taken + "\nDo you want to play again?")
    if play_again:
        reset_game()
    else:
        root.quit()

def check():
    global lives
    user_letter = e1.get().upper()

    if len(user_letter) != 1 or user_letter not in alphabet:
        guess_line = 'Please enter a single valid letter.'
    elif user_letter in used_letters:
        guess_line = 'You already used that letter. Try another one.'
    else:
        used_letters.add(user_letter)
        if user_letter in word_letters:
            word_letters.remove(user_letter)
            guess_line = 'Good guess!'
        else:
            lives -= 1
            guess_line = f'Your letter {user_letter} is not in the word.'

    update_display(guess_line)

    if lives == 0:
        end_game(f"You died. The word was {word}")
    elif len(word_letters) == 0:
        end_game(f"YAY! You guessed the word! It was {word}")

def give_hint():
    global hint_used
    if hint_used >= 2:
        messagebox.showinfo("Hint", "You have used all your hints!")
        return

    remaining = list(word_letters - used_letters)
    if remaining:
        hint_letter = random.choice(remaining)
        hint_used += 1
        messagebox.showinfo("Hint", f"Try this letter: {hint_letter} (Hint {hint_used}/2)")
    else:
        messagebox.showinfo("Hint", "No hints left!")

def update_time():
    current_time = time.strftime("%H:%M:%S")
    time_label.config(text=current_time)
    root.after(1000, update_time)

# Game setup
word = get_valid_word(words)
word_letters = set(word)
alphabet = set(string.ascii_uppercase)
used_letters = set()
lives = 7
hint_used = 0
start_time = time.time()

# GUI setup
root = tkinter.Tk()
root.geometry("500x520")
root.title("Hangman Game")
root.configure(bg="#AAF0D1")

# Time label
time_label = tkinter.Label(root, font=("Arial", 12), anchor="w", bg="#AAF0D1", fg="black")
time_label.place(x=10, y=10)
update_time()

# Stylish heading
heading = tkinter.Label(root, text="🎩 HANGMAN 🎩", font=("Arial Black", 40), bg="#AAF0D1", fg="#2E8B57")
heading.pack(pady=5)

l1 = tkinter.Label(root, text="You have 7 lives left", font=("Arial", 14), bg="#AAF0D1", fg="black")
l1.pack(pady=10)

word_list = [letter if letter in used_letters else '_' for letter in word]
curr_word = ' '.join(word_list)
l2 = tkinter.Label(root, text=curr_word, font=("Arial", 14), bg="#AAF0D1", fg="black")
l2.pack(pady=10)

p1 = tkinter.Label(root, text=lives_visual_dict[lives], font=("Courier", 8), bg="#AAF0D1", fg="black")
p1.pack(pady=10)

e1 = tkinter.Entry(root, font=("Arial", 14), bg="white", fg="black")
e1.pack(pady=10)
e1.focus_set()

guess_button = tkinter.Button(root, text="Check", command=check, font=("Arial", 14), bg="#90EE90", fg="black")
guess_button.pack(pady=5)

hint_button = tkinter.Button(root, text="Hint", command=give_hint, font=("Arial", 12), bg="#90EE90", fg="black")
hint_button.pack(pady=5)

l3 = tkinter.Label(root, text="Let's Begin!", font=("Arial", 14), bg="#AAF0D1", fg="black")
l3.pack(pady=20)

# Grass canvas across full width
canvas = tkinter.Canvas(root, width=30000, height=250, bg="#AAF0D1", highlightthickness=0)
canvas.pack(side="bottom")

# Draw base grass rectangle
canvas.create_rectangle(0, 0, 1500, 1500, fill="#228B22", outline="")

# Add grass blades across entire width
# for x in range(0, 150, 80):
#     canvas.create_polygon(
#         x, 120,
#         x + 5, 90,
#         x + 10, 120,
#         fill="#32CD32", outline=""
#     )

# Enter key binding
root.bind('<Return>', lambda event: check())

root.mainloop()




