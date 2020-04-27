from tkinter import *
from random import randint as ri
import runpy

root = Tk()
root.geometry("600x600")
root.configure(bg="#000000")

title_colors = ["#FFFF00", "#6FFF00", "#00FFEF", "#0077FF", "#8F44FF", "#FF00DE", "#FF0000"]


def change_color():
    current_color = title.cget("foreground")
    rand_ind = ri(0, 6)
    next_color = title_colors[rand_ind] if current_color != title_colors[rand_ind] else "#FFFFFF"
    title.config(fg=next_color)
    root.after(100, change_color)


def launch_demo():
    root.destroy()

    runpy.run_path("gameboarddemo.py")


# Create
title = Text(root, height=4, width=8, borderwidth=0, bg="#000000",
             fg=title_colors[ri(0, 6)], font=("Helvetica", 20, "bold"))
title.insert(END, "TETRIS")

start = Button(root, text="Start", padx=8, bg="#9F9F9F", command=launch_demo)
close = Button(root, text="Exit", padx=10, bg="#9F9F9F", command=root.destroy)

# Show
title.pack(pady=20, anchor=CENTER)
start.pack()
close.pack()

change_color()
root.mainloop()


