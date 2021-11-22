from tkinter import *
import pandas
import random

# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}


# ---------------------------- APP MECHANISM ------------------------------- #

try:
    words_to_learn_data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    word_data = pandas.read_csv("./data/german_words.csv")
    word_data_list = word_data.to_dict(orient="records")
else:
    word_data_list = words_to_learn_data.to_dict(orient="records")


def random_word():
    """By hitting wrong or right random word will be generated."""
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(word_data_list)
    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(title_text, text="Deutsch", fill="black")
    canvas.itemconfig(word_text, text=current_card["Deutsch"], fill="black")
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    """the card will be flipped after 3 seconds to generate the translation of word."""
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_card['English'], fill="white")


def update_data():
    """Removes the words from german_words.csv and updated new data is stored in words_to_learn.csv"""
    word_data_list.remove(current_card)
    words_to_learn_data = pandas.DataFrame(word_data_list)
    words_to_learn_data.to_csv("./data/words_to_learn.csv", index=False)
    random_word()

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front)
title_text = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# right button image
right_button_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_button_image, highlightthickness=0, command=random_word)
right_button.grid(column=1, row=1)

# wrong button image -- there's no callback function yet - need to add!
wrong_button_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_button_image, highlightthickness=0, command=flip_card)
wrong_button.grid(column=0, row=1)

# calling the functions to start the flashy app
random_word()

window.mainloop()


