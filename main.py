import customtkinter as Ctk
from PIL import Image
import os

save_path = "pyRPG/Savefile.txt"

Ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
Ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

main = Ctk.CTk()  # create CTk window like you do with the Tk window
main.geometry("1024x576")
main.resizable(False, False)

menu_image_file = Ctk.CTkImage(
    dark_image=Image.open("pyRPG\content\main_image_content.png"),
    size=(674, 576)
)

menu_logo_file = Ctk.CTkImage(
    dark_image=Image.open("pyRPG\content\main_logo_content.png"),
    size=(345, 288)
)

# Functions

def create_new_game():
    print("New Game")
    dialog = Ctk.CTkInputDialog(text="What is your name?", title="Name")
    player_name = str(dialog.get_input())
    with open(save_path, "w") as save_file:
        # Write content to the file
        save_file.write("Player_name: " + player_name)


def load_game():
    print("Load Game")

def open_about_window():
    # Create secondary (or popup) window.
    about_window = Ctk.CTkToplevel()
    about_window.title("About")
    about_window.config(width=300, height=300)
    # Create a button to close (destroy) this window.
    button_close = Ctk.CTkButton(
        about_window,
        text="Close window",
        command=about_window.destroy
    )
    button_close.place(relx=0.5, rely=0.9, anchor=Ctk.CENTER)

def exit_game():
    print("Exit")
    main.destroy()
    exit()

# Main menu elements
    # Menu Image
menu_image = Ctk.CTkLabel(main, image=menu_image_file, text="")  # display image with a CTkLabel
menu_image.place(relx=0.34, rely=0, anchor=Ctk.NW)
    # Menu Logo
menu_image = Ctk.CTkLabel(main, image=menu_logo_file, text="")  # display image with a CTkLabel
menu_image.place(relx=0, rely=0, anchor=Ctk.NW)

button_frame = Ctk.CTkFrame(master=main, width=345, height=288, corner_radius=10, bg_color="transparent")
button_frame.pack(padx=0, pady=0)
button_frame.place(relx=0, rely=1, anchor=Ctk.SW)

new_game_button = Ctk.CTkButton(master=main, text="Create New Game", command=create_new_game, bg_color="#302c2c")
new_game_button.place(relx=0.1, rely=0.6, anchor=Ctk.W)

load_game_button = Ctk.CTkButton(master=main, text="Load Game", command=load_game, bg_color="#302c2c")
load_game_button.place(relx=0.1, rely=0.7, anchor=Ctk.W)
load_game_button._state="disabled"

about_button = Ctk.CTkButton(master=main, text="About", command=open_about_window, bg_color="#302c2c")
about_button.place(relx=0.1, rely=0.8, anchor=Ctk.W)

exit_button = Ctk.CTkButton(master=main, text="Exit", command=exit_game, bg_color="#302c2c")
exit_button.pack(padx=20)
exit_button.place(relx=0.1, rely=0.9, anchor=Ctk.W)

# Main loop

main.protocol("WM_DELETE_WINDOW", exit_game)
main.mainloop()