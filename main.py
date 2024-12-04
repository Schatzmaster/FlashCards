from tkinter import *
import pandas
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
random_record = {}
words_to_learn = {}

# ---------------------------- DATA ------------------------------- #
try:
    data = pandas.read_csv("data/words_to_lear.csv")
except FileNotFoundError:
    org_data = pandas.read_csv(r"data/spanish_words.csv")
    print(org_data)
    words_to_learn = org_data.to_dict(orient="records")
else:
    words_to_learn = data.to_dict(orient="records")


# ---------------------------- FUNCTIONS ------------------------------- #
def new_word():
    global random_record, timer
    window.after_cancel(flip_card)
    random_record = choice(words_to_learn)
    canvas.itemconfig(card_title, text="Spanisch", fill="black")
    canvas.itemconfig(card_word, text=random_record["Spanisch"], fill="black")
    canvas.itemconfig(canvas_background, image=front_img)
    timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="Deutsch", fill="white")
    canvas.itemconfig(card_word, text=random_record["Deutsch"], fill="white")
    canvas.itemconfig(canvas_background, image=back_img)

def learned():
    words_to_learn.remove(random_record)
    print(len(words_to_learn))
    data = pandas.DataFrame(words_to_learn)
    data.to_csv("data/words_to_learn", index=False)
    new_word()


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Karteikarten")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
timer = window.after(3000, func=flip_card)

print(random_record)
canvas = Canvas(width=800, height=526)
front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
canvas_background = canvas.create_image(400, 263, image=front_img)
canvas.config(highlightthickness=0, bg=BACKGROUND_COLOR)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Buttons

wrong_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=wrong_img, highlightthickness=0, command=new_word)
unknown_button.grid(row=1, column=0)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=learned)
right_button.grid(row=1, column=1)

new_word()

window.mainloop()
