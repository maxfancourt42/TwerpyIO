# import libaries
import tkinter as tk
from tkinter import ttk

class MainApplication:
    def __init__(self, master):

        # create the local root
        self.master = master

        # define the GUI name
        master.title("Twirpy IO")

        # create the style object and set root background colour
        style = ttk.Style()
        style.configure("TFrame", background="#ff9232")

        # create the mainframe
        self.mainframe = tk.Frame(root, background="#FFFFFF")

        # set mainframe parameteres
        self.mainframe.grid(column=0, row=0, sticky=tk.NSEW)
        self.mainframe.master.minsize(width=510, height=510)

        self.label = tk.Label(self.mainframe, text="Twirpy IO", background="#ffc532", font=(None, 15))
        self.label.grid(row=0, column=0, sticky="NSEW", columnspan=4, rowspan=1)

        self.logo = tk.Label(self.mainframe, text="Logo", background="#ffc532", font=(None, 15))
        self.logo.grid(row=0, column=0, sticky="NSW", rowspan=1)

        self.systemstatus = tk.Label(self.mainframe, text="Status Bar", background="#ff5e32", font=(None, 15))
        self.systemstatus.grid(row=1, column=0, rowspan=6, sticky=tk.NSEW)

        self.power = tk.Label(self.mainframe, text="Power", background="#f70000", font=(None, 12))
        self.power.grid(row=2, column=0)

        self.Controls = tk.Label(self.mainframe, text="Controls", background="#f70000", font=(None, 12))
        self.Controls.grid(row=3, column=0)

        self.Siren = tk.Label(self.mainframe, text="Siren", background="#f70000", font=(None, 12))
        self.Siren.grid(row=4, column=0)

        self.greet_button = tk.Button(self.mainframe, text="Power On", command=self.greet, background="#f70000")
        self.greet_button.grid(row=4, column=1, columnspan=3)

        self.close_button = tk.Button(self.mainframe, text="Quit Program", command=master.quit, background="#ff5e32")
        self.close_button.grid(row=6, column=3, sticky=tk.SE)

        # give weight to root rows and column to permit all children to fill the frame
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        # give weight to rows and column to permit dynamic redraw
        self.mainframe.columnconfigure((0, 1, 2, 3), weight=1)
        self.mainframe.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        # Buff and pad all children of mainframe
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def greet(self):
        print("James Touched Me Inappropriately")


if __name__ == '__main__':
    root = tk.Tk()
    gui = MainApplication(root)
    root.mainloop()

