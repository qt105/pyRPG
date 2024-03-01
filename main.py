from tkinter import *
from os import *
import json
import fight
from fight import *

# Path variables
savePath = 'pyRPG/Save.txt' # Defines the save Path
contentPath = 'pyRPG/content/' # Defines the content Path, points to the content folder located in the main file

window = Tk()
window.geometry("1280x720")

window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)

# Frames

top_left_frame = Frame(window, bg='black')
top_left_frame.grid(row=0, column=0, sticky='nswe')
bottom_left_frame = Frame(window, bg='gray')
bottom_left_frame.grid(row=1, column=0, sticky='nswe')
right_frame = Frame(window, bg='blue')
right_frame.grid(row=0, column=1, sticky='nswe', rowspan=2, columnspan=2)

# Images
topLeftImage = PhotoImage(file=contentPath+"topLeftImage.png")  # Replace "top_image.png" with your image path
top_left_image_label = Label(top_left_frame, image=topLeftImage)
top_left_image_label.place(x=0, y=0, relwidth=1, relheight=1)

rightImage = PhotoImage(file=contentPath+"rightImage.png")  # Replace "top_image.png" with your image path
right_image_label = Label(right_frame, image=rightImage)
right_image_label.place(x=0, y=0, relwidth=1, relheight=1)

# Commands, Triggered by pressing the respectives buttons on the main menu
def new_game():
    system('cls')
    window.iconify()
    print("What is your character's name?")
    player_name = str(input('>'))
    player = Entity(player_name, 1, 0, 250, 100, 100, 50, 10, 20, 15, 15, 30)
    enemy = generate_random_enemy(player.level)
    combat(player, enemy)

def load_game():
    pass

def about():
    system('cls')
    window.iconify()
    print(
        "This game was realised by:\n\n"
        "Quentin Mireur\n"
        "Nérilyne Chhem\n"
        "Juan Salvador Alcorta"
    )

def exit_game():
    exit()

# Buttons
newGame_button = Button(bottom_left_frame, text="New Game", command=new_game)
newGame_button.place(relx=0.5, rely=0.2, anchor=CENTER)

loadGame_button = Button(bottom_left_frame, text="Load Game", command=load_game)
loadGame_button.place(relx=0.5, rely=0.4, anchor=CENTER)

about_button = Button(bottom_left_frame, text="About", command=about)
about_button.place(relx=0.5, rely=0.6, anchor=CENTER)

exit_button = Button(bottom_left_frame, text="Exit Game", command=exit_game)
exit_button.place(relx=0.5, rely=0.8, anchor=CENTER)

window.mainloop()