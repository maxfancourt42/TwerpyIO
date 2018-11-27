# import libaries
import tkinter as tk
from tkinter import ttk

class MainApplication:
    def __init__(self, master):
        # create the local root
        self.master = master
        self.master.state('zoomed')

        # define the GUI name
        master.title("Twirpy IO")

        # create the style object and set root background colour
        style = ttk.Style()
        style.configure("TFrame", background="#ff9232")

        # create the mainframe
        self.mainframe = tk.Frame(master, background="#FFFFFF")

        # set mainframe parameteres
        self.mainframe.grid(column=0, row=0, sticky=tk.NSEW)
        self.mainframe.master.minsize(width=510, height=510)

        self.label = tk.Label(self.mainframe, text="Twirpy IO", background="#ffc532", font=(None, 15), anchor="w")
        self.label.grid(row=0, column=1, sticky=tk.NSEW, columnspan=3)

        self.logo = tk.Label(self.mainframe, text="Logo", background="#ffc532", font=(None, 15))
        self.logo.grid(row=0, column=3, sticky=tk.NSEW)

        self.controlpaneltext = tk.Label(self.mainframe, text="Control Panel v1.0", background="#636363", font=(None, 15))
        self.controlpaneltext.grid(row=0, column=0, sticky=tk.NSEW)

        # Create a frame to hold the control panel on the left hand side
        self.controlpanel = tk.Frame(self.mainframe, background="#636363")
        self.controlpanel.grid(row=1, column=0, sticky=tk.NSEW, rowspan=4)
        self.controlpanel.grid_rowconfigure(0, weight=1)
        self.controlpanel.grid_columnconfigure(0, weight=1)

        # within this create a canvas that will scroll
        self.canvas = tk.Canvas(self.controlpanel, background="#636363")
        self.canvas.config(background="#636363", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)

        # add a scroll bar to the canvvas
        self.vsb = ttk.Scrollbar(self.controlpanel, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky="NSE")
        self.canvas.configure(yscrollcommand=self.vsb.set)

        # create a frame within the canvas to structure
        #self.canvasframe = tk.Frame(self.canvas, background="#636363")
        self.canvasframe = tk.Frame(self.canvas, background="#ffffff")
        self.canvasframe.grid(row=0, column=0, sticky=tk.NSEW)

        # create the canvas having filled it
        self.canvas.create_window((0, 0), window=self.canvasframe, anchor=tk.NW)

        # create a blank dictionary to track the buttons
        numberofbuttons = 100
        buttons = [[ttk.Button()] for x in range(numberofbuttons)]

        # iterate over dictionary creating the required buttons

        for i in range(numberofbuttons):
            buttons[i] = ttk.Button(self.canvasframe, text="Temp text")
            buttons[i].grid(row=i, column=0, sticky=tk.NSEW)

        # set the scrolling region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # if the window is resized then adjust the bounding box of the canvas to prevent being able to scroll off screen
        self.canvasframe.bind("<Configure>", self.OnFrameConfigure)
        self.canvas.bind("<Configure>", self.FrameWidth)

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
        for child in self.canvasframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def greet(self):
        print("James Touched Me Inappropriately")

    """Resize the bounding box of the control panel on dynamic resize"""
    def OnFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def FrameWidth(self, event):
        self.canvas.itemconfig(self.canvas, width=event.width)



if __name__ == '__main__':
    root = tk.Tk()
    gui = MainApplication(root)
    root.mainloop()

