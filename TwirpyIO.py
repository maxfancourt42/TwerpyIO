# import libaries
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import Toplevel
import os

class Debugger:
    def __init__(self):
        # create toplevel
        self.debugger = tk.Toplevel()
        self.debugger.config(background="#DFE8F6")
        self.debugger.geometry('%dx%d+%d+%d' % (600, 600, 0, 0))
        self.debugger.minsize(width=600, height=600)

        # weight the columns
        self.debugger.columnconfigure(0, weight=1)
        self.debugger.rowconfigure(1, weight=1)

        # create the header
        self.header = tk.Label(self.debugger, text="Twirpy IO Debugger", background="#ffc532", font=(None, 18), anchor="w")
        self.header.grid(row=0, column=0, sticky=tk.NSEW, columnspan=2)

        # create a scrolling canvas to add debugger lines to
        self.debuggercanvas = tk.Canvas(self.debugger, background="#efefef")
        self.debuggercanvas.grid(row=1, column=0, sticky=tk.NSEW)
        # add frame to canvas to allow organised stacking
        self.canvasframe = tk.Frame(self.debuggercanvas)
        self.canvasframe.pack(fill=tk.BOTH, expand=1)

        # create vertical toolbar
        self.vsb = ttk.Scrollbar(self.debugger, orient="vertical", command=self.debuggercanvas.yview)
        self.vsb.grid(row=1, column=1, sticky=tk.NS)
        self.debuggercanvas.configure(yscrollcommand=self.vsb.set)

        # create horizontal toolbar
        self.hsb = ttk.Scrollbar(self.debugger, orient="horizontal", command=self.debuggercanvas.xview)
        self.hsb.grid(row=2, column=0, sticky=tk.EW)
        self.debuggercanvas.configure(xscrollcommand=self.hsb.set)

        # create a button at the top to clear the window
        self.clearbutton = ttk.Button(self.debugger, text="Clear", command=lambda: self.cleardebuggerscreen())
        self.clearbutton.grid(row=0, column=0, sticky=tk.E)

        self.debuggercanvas.create_window((0, 0), window=self.canvasframe, anchor=tk.NW)

    def addtoscreen(self, text):
        # create a new label to add to the canvas
        tk.Label(self.canvasframe, text=text, font=(None, 18), anchor="w", background="#efefef").pack(fill=tk.BOTH)
        # update canvas to show the new label being added
        self.debuggercanvas.update()
        # update the scrollbars so that they scroll the entire bounding box
        self.debuggercanvas.config(scrollregion=self.debuggercanvas.bbox("all"))

    def cleardebuggerscreen(self):
        # loop through and delete all children
        for x in self.canvasframe.winfo_children():
            x.destroy()
        # update canvas to show the new label being added
        self.debuggercanvas.update()
        # update the scrollbars so that they scroll the entire bounding box
        self.debuggercanvas.config(scrollregion=self.debuggercanvas.bbox("all"))

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

        # create debugger
        self.debugger = Debugger()

        # set mainframe parameteres
        self.mainframe.grid(column=0, row=0, sticky=tk.NSEW)
        self.mainframe.master.minsize(width=600, height=600)

        self.label = tk.Label(self.mainframe, text="Twirpy IO", background="#ffc532", font=(None, 18), anchor="w")
        self.label.grid(row=0, column=1, sticky=tk.NSEW, columnspan=3)

        # get logo from file
        self.photoimage = PhotoImage(file="%s\\logo.png" % os.path.dirname(__file__))
        self.logo = tk.Label(self.mainframe, image=self.photoimage, borderwidth=0)
        self.logo.grid(row=0, column=3)
        root.update_idletasks()

        self.controlpaneltext = tk.Label(self.mainframe, text="Control Panel v1.0", background="#636363", font=(None, 15))
        self.controlpaneltext.grid(row=0, column=0, sticky=tk.NSEW)

        # Create a frame to hold the control panel on the left hand side
        self.controlpanel = tk.Frame(self.mainframe, background="#636363")
        self.controlpanel.grid(row=1, column=0, sticky=tk.NSEW, rowspan=3)
        self.controlpanel.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.controlpanel.grid_columnconfigure(0, weight=1)

        # create the buttons on the left hand side
        self.button1 = ttk.Button(self.controlpanel, text="Kill James", command=lambda: self.debugger.addtoscreen("James Smells"))
        self.button1.grid(row=0, column=0, sticky=tk.NSEW)
        self.button2 = ttk.Button(self.controlpanel, text="Touch James", command=lambda: self.debugger.addtoscreen("James Smells James Smells James Smells James Smells James Smells James Smells James Smells James Smells  "))
        self.button2.grid(row=1, column=0, sticky=tk.NSEW)
        self.button3 = ttk.Button(self.controlpanel, text="Lick James")
        self.button3.grid(row=2, column=0, sticky=tk.NSEW)
        self.button4 = ttk.Button(self.controlpanel, text="Blame James")
        self.button4.grid(row=3, column=0, sticky=tk.NSEW)
        self.button5 = ttk.Button(self.controlpanel, text="Poke James")
        self.button5.grid(row=4, column=0, sticky=tk.NSEW)
        self.button6 = ttk.Button(self.controlpanel, text="Quit Program", command=lambda: root.quit())
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


if __name__ == '__main__':
    root = tk.Tk()
    gui = MainApplication(root)
    root.mainloop()

