# import libaries
import tkinter as tk
from tkinter import ttk
import os
from PIL import Image
from PIL import ImageTk

class MainApplication:
    def __init__(self, master):
        # create the local root
        self.master = master
        self.master.state('zoomed')
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        # define the GUI name
        master.title("Twirpy IO")

        # create the style object and set root background colour
        style = ttk.Style()
        style.configure("TFrame", background="#ff9232")

        # create the mainframe
        self.mainframe = tk.Frame(master, background="#FFFFFF")

        # set mainframe parameteres
        self.mainframe.grid(column=0, row=0, sticky=tk.NSEW)
        self.mainframe.master.minsize(width=600, height=510)

        self.label = tk.Label(self.mainframe, text="Twirpy IO", background="#ffc532", font=(None, 18), anchor="w")
        self.label.grid(row=0, column=1, sticky=tk.NSEW, columnspan=3)

        root.update()

        # get logo from file
        self.logoactualorignal = Image.open("%s\\logo.png" % os.path.dirname(__file__))
        self.logoactual = self.logoactualorignal.resize((self.label.winfo_height(), self.label.winfo_height()), Image.ANTIALIAS)
        self.photoimage = ImageTk.PhotoImage(self.logoactual)
        self.logo = tk.Label(self.mainframe, image=self.photoimage, borderwidth=0)
        self.logo.grid(row=0, column=2, columnspan=2, sticky=tk.E)
        root.update_idletasks()

        # on frame resize
        self.mainframe.bind("<Configure>", self.resizeimage)

        self.controlpaneltext = tk.Label(self.mainframe, text="Control Panel v1.0", background="#636363", font=(None, 15))
        self.controlpaneltext.grid(row=0, column=0, sticky=tk.NSEW)

        # Create a frame to hold the control panel on the left hand side
        self.controlpanel = tk.Frame(self.mainframe, background="#636363")
        self.controlpanel.grid(row=1, column=0, sticky=tk.NSEW, rowspan=3)
        self.controlpanel.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.controlpanel.grid_columnconfigure(0, weight=1)

        # create the buttons on the left hand side
        self.button1 = ttk.Button(self.controlpanel, text="Kill James")
        self.button1.grid(row=0, column=0, sticky=tk.NSEW)
        self.button2 = ttk.Button(self.controlpanel, text="Touch James")
        self.button2.grid(row=1, column=0, sticky=tk.NSEW)
        self.button3 = ttk.Button(self.controlpanel, text="Lick James")
        self.button3.grid(row=2, column=0, sticky=tk.NSEW)
        self.button4 = ttk.Button(self.controlpanel, text="Blame James")
        self.button4.grid(row=3, column=0, sticky=tk.NSEW)
        self.button5 = ttk.Button(self.controlpanel, text="Poke James")
        self.button5.grid(row=4, column=0, sticky=tk.NSEW)
        self.button6 = ttk.Button(self.controlpanel, text="Quit Program")
        self.button6.grid(row=5, column=0, sticky=tk.NSEW)

        # create the grid of labels in the middle which represent the subsystems
        self.powersubsystem = tk.Label(self.mainframe, text="Power", background="#7a7a7a")
        self.powersubsystem.grid(row=1, column=1, sticky=tk.NSEW)
        self.powersubsystem.grid_configure(padx=5, pady=5)

        self.controlsubsystem = tk.Label(self.mainframe, text="Controls", background="#7a7a7a")
        self.controlsubsystem.grid(row=1, column=2, sticky=tk.NSEW)
        self.controlsubsystem.grid_configure(padx=5, pady=5)

        self.sirensubsystem = tk.Label(self.mainframe, text="Siren", background="#7a7a7a")
        self.sirensubsystem.grid(row=1, column=3, sticky=tk.NSEW)
        self.sirensubsystem.grid_configure(padx=5, pady=5)

        self.motorsubsystem = tk.Label(self.mainframe, text="Motor", background="#7a7a7a")
        self.motorsubsystem.grid(row=2, column=1, sticky=tk.NSEW)
        self.motorsubsystem.grid_configure(padx=5, pady=5)

        self.AIsubsystem = tk.Label(self.mainframe, text="AI", background="#7a7a7a")
        self.AIsubsystem.grid(row=2, column=2, sticky=tk.NSEW)
        self.AIsubsystem.grid_configure(padx=5, pady=5)

        self.bluetoothsubsystem = tk.Label(self.mainframe, text="Bluetooth", background="#7a7a7a")
        self.bluetoothsubsystem.grid(row=2, column=3, sticky=tk.NSEW)
        self.bluetoothsubsystem.grid_configure(padx=5, pady=5)

        self.hoseintergrationsubsystem = tk.Label(self.mainframe, text="Water Hose", background="#7a7a7a")
        self.hoseintergrationsubsystem.grid(row=3, column=1, sticky=tk.NSEW)
        self.hoseintergrationsubsystem.grid_configure(padx=5, pady=5)

        self.fluxcapacitorsubsystem = tk.Label(self.mainframe, text="Flux Capacitor", background="#7a7a7a")
        self.fluxcapacitorsubsystem.grid(row=3, column=2, sticky=tk.NSEW)
        self.fluxcapacitorsubsystem.grid_configure(padx=5, pady=5)

        self.selfdestructsubsystem = tk.Label(self.mainframe, text="Self Destruct", background="#7a7a7a")
        self.selfdestructsubsystem.grid(row=3, column=3, sticky=tk.NSEW)
        self.selfdestructsubsystem.grid_configure(padx=5, pady=5)

        # give weight to root rows and column to permit all children to fill the frame
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        # give weight to rows and column to permit dynamic redraw
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure((1, 2, 3), weight=2)
        self.mainframe.rowconfigure((0, 1, 2, 3), weight=1)

        # Buff and pad all children of mainframe
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # canvas frame pad
        for child in self.controlpanel.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def greet(self):
        print("James Touched Me Inappropriately")

    """Resize the bounding box of the control panel on dynamic resize"""
    def resizeimage(self, event):
        # get height of top bar
        self.height = self.label.winfo_height()
        print(self.height)

        if self.height > 200:
            self.logoactual = self.logoactualorignal.resize((200, 200), Image.ANTIALIAS)
        else:
            self.logoactual = self.logoactualorignal.resize((self.height, self.height), Image.ANTIALIAS)

        self.photoimage = ImageTk.PhotoImage(self.logoactual)
        self.logo.configure(image=self.photoimage)

        root.update_idletasks()

if __name__ == '__main__':
    root = tk.Tk()
    gui = MainApplication(root)
    root.mainloop()

