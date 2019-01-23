# import libaries
import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
from random import randint
import os

class ScrollingWindow:
    def __init__(self):
        # local variables
        self.linecounter = 0

        # create toplevel
        self.swtl = tk.Toplevel()
        self.swtl.config(background="#DFE8F6")
        self.swtl.geometry('%dx%d+%d+%d' % (600, 600, 0, 0))
        self.swtl.minsize(width=600, height=600)

        # weight the columns
        self.swtl.columnconfigure(0, weight=1)
        self.swtl.rowconfigure(1, weight=1)

        # create the header
        self.header = tk.Label(self.swtl, text="Temp Text", background="#ffc532", font=(None, 18), anchor="w")
        self.header.grid(row=0, column=0, sticky=tk.NSEW, columnspan=2)

        # create a scrolling canvas to add lines of text to
        self.swcanvas = tk.Canvas(self.swtl, background="#efefef")
        self.swcanvas.grid(row=1, column=0, sticky=tk.NSEW)
        # add frame to canvas to allow organised stacking
        self.canvasframe = tk.Frame(self.swcanvas)
        self.canvasframe.pack(fill=tk.BOTH, expand=1)

        # create vertical toolbar
        self.vsb = ttk.Scrollbar(self.swtl, orient="vertical", command=self.swcanvas.yview)
        self.vsb.grid(row=1, column=1, sticky=tk.NS)
        self.swcanvas.configure(yscrollcommand=self.vsb.set)

        # create horizontal toolbar
        self.hsb = ttk.Scrollbar(self.swtl, orient="horizontal", command=self.swcanvas.xview)
        self.hsb.grid(row=2, column=0, sticky=tk.EW)
        self.swcanvas.configure(xscrollcommand=self.hsb.set)

        # create a button at the top to clear the window
        self.clearbutton = ttk.Button(self.swtl, text="Clear", command=lambda: self.cleardebuggerscreen())
        self.clearbutton.grid(row=0, column=0, sticky=tk.E)

        self.swcanvas.create_window((0, 0), window=self.canvasframe, anchor=tk.NW)

    def addtoscreen(self, text, colour="black"):
        # create a new label to add to the canvas
        tk.Label(self.canvasframe, text="{} | {}".format(str(self.linecounter).zfill(3), text), font=(None, 18), anchor="w", background="#efefef", foreground=colour).pack(fill=tk.BOTH)
        # update canvas to show the new label being added
        self.swcanvas.update()
        # update the scrollbars so that they scroll the entire bounding box
        self.swcanvas.config(scrollregion=self.swcanvas.bbox("all"))
        # update the linecounter
        self.linecounter = self.linecounter + 1

    def cleardebuggerscreen(self):
        # loop through and delete all children
        for x in self.canvasframe.winfo_children():
            x.destroy()
        # update canvas to show the new label being added
        self.swcanvas.update()
        # update the scrollbars so that they scroll the entire bounding box
        self.swcanvas.config(scrollregion=self.swcanvas.bbox("all"))
        # set the linecounter to 0
        self.linecounter = 0

    def settitle(self, newtext):
        self.header.configure(text=newtext)
        self.swtl.update_idletasks()


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
        self.debugger = ScrollingWindow()
        self.debugger.settitle("Twirpy IO Debugger")

        # set mainframe parameteres
        self.mainframe.grid(column=0, row=0, sticky=tk.NSEW)
        self.mainframe.master.minsize(width=600, height=600)

        self.label = tk.Label(self.mainframe, text="Twirpy IO", background="#ffc532", font=(None, 18), anchor="w")
        self.label.grid(row=0, column=1, sticky=tk.NSEW, columnspan=6)

        self.controlpaneltext = tk.Label(self.mainframe, text="Control Panel v1.0", background="#636363", font=(None, 15))
        self.controlpaneltext.grid(row=0, column=0, sticky=tk.NSEW)

        # get logo from file
        self.photoimage = tk.PhotoImage(file="%s\\logo.png" % os.path.dirname(__file__))
        self.logo = tk.Label(self.mainframe, image=self.photoimage, borderwidth=0, background="#ffc532")
        self.logo.grid(row=0, column=2, columnspan=2, sticky=tk.E)

        # Create a frame to hold the control panel on the left hand side
        self.controlpanel = tk.Frame(self.mainframe, background="#636363")
        self.controlpanel.grid(row=1, column=0, sticky=tk.NSEW, rowspan=5)
        self.controlpanel.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.controlpanel.grid_columnconfigure(0, weight=1)

        # create the menu on the left hand side
        self.button1 = ttk.Button(self.controlpanel, text="Activate Debugger", command=lambda: self.debugger.addtoscreen("James Smells"))
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

        # power subsystem
        # control subsystem
        self.powersubsystem = subsystemwindow(self.mainframe, row=1, column=1)
        self.powersubsystem.changetitle("Power Subsystems")
        self.powersubsystem.setcommand("power")

        # control subsystem
        self.controlsubsystem = subsystemwindow(self.mainframe, row=1, column=2)
        self.controlsubsystem.changetitle("Control Subsystems")
        self.controlsubsystem.setcommand("control")

        # motor subsystems
        self.motorsubsystem = subsystemwindow(self.mainframe, row=1, column=3)
        self.motorsubsystem.changetitle("Motor Subsystems")
        self.motorsubsystem.setcommand("motor")

        # siren subsystem
        self.sirensubsystem = subsystemwindow(self.mainframe, row=2, column=1)
        self.sirensubsystem.changetitle("Siren Subsystems")
        self.sirensubsystem.setcommand("siren")

        # artifical intelligence subsystem
        self.aisubsystem = subsystemwindow(self.mainframe, row=2, column=2)
        self.aisubsystem.changetitle("AI Subsystems")
        self.aisubsystem.setcommand("ai")

        # bluetooth subsystem
        self.bluetoothsubsystem = subsystemwindow(self.mainframe, row=2, column=3)
        self.bluetoothsubsystem.changetitle("Bluetooth Subsystems")
        self.bluetoothsubsystem.setcommand("bluetooth")

        # firecontrol subsystem
        self.firecontrolsubsystem = subsystemwindow(self.mainframe, row=3, column=1)
        self.firecontrolsubsystem.changetitle("Fire Control Subsystems")
        self.firecontrolsubsystem.setcommand("fc")

        # auto-stabilisation subsystem
        self.stablisationsubsystem = subsystemwindow(self.mainframe, row=3, column=2)
        self.stablisationsubsystem.changetitle("Stabilisation Subsystems")
        self.stablisationsubsystem.setcommand("ss")

        # safety subsystems
        self.safetysubsystem = subsystemwindow(self.mainframe, row=3, column=3)
        self.safetysubsystem.changetitle("Safety Subsystems")
        self.safetysubsystem.setcommand("safe")

        # give weight to root rows and column to permit all children to fill the frame
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        # give weight to rows and column to permit dynamic redraw
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure((1, 2, 3), weight=2)
        self.mainframe.rowconfigure((1, 2, 3), weight=1)

        # Buff and pad all children of mainframe
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # canvas frame pad
        for child in self.controlpanel.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.logo.grid_configure(padx=20, pady=20)

    def powererrorprogram(self):
        # print error messages to the debugger
        self.debugger.addtoscreen("Attempting to bring power systems online")
        self.debugger.addtoscreen("Hardware: Status - Disconnected")
        self.debugger.addtoscreen("Simulating hardware requirements for software testing purposes")
        self.debugger.addtoscreen("Connection to batteries established")
        self.debugger.addtoscreen("Sufficient power detected for operation")
        self.debugger.addtoscreen("Circuitry detected")
        self.debugger.addtoscreen("Circuitry intact and functional")
        self.debugger.addtoscreen("Safety features enabled")
        self.debugger.addtoscreen("Testing software control of power systems")
        self.debugger.addtoscreen("CRITICAL FAILURE: Core code error 471")
        self.debugger.addtoscreen("Twirpy OS unable to assume control of Power System, Running Debugger")
        self.debugger.addtoscreen("Activating Debug Mode")
        self.debugger.addtoscreen("Debug Summary")
        self.debugger.addtoscreen("Hardware requirements: PASS", colour="green")
        self.debugger.addtoscreen("Power requirements: PASS", colour="green")
        self.debugger.addtoscreen("Circuitry requirements: PASS", colour="green")
        self.debugger.addtoscreen("Safety features: PASS", colour="green")
        self.debugger.addtoscreen("Software Control: FAIL", colour="red")
        self.debugger.addtoscreen("Full diagnostic: Software Control Subroutines")
        self.debugger.addtoscreen("Progress 10%")
        self.debugger.addtoscreen("Progress 20%")
        self.debugger.addtoscreen("Progress 30%")
        self.debugger.addtoscreen("Progress 40%")
        self.debugger.addtoscreen("Progress 50%")
        self.debugger.addtoscreen("Progress 60%")
        self.debugger.addtoscreen("Progress 70%")
        self.debugger.addtoscreen("Progress 80%")
        self.debugger.addtoscreen("Progress 90%")
        self.debugger.addtoscreen("Progress 100%")
        self.debugger.addtoscreen("Error Detected: Process exceeds maximum allowed memory usage")

        # update the status of the power box to Error
        self.powersubsystem.changestatus(newstatus="Status: Error Detected")
        # update the button so that it creates a problem filling it with a random power puzzle
        self.powersubsystem.changebuttontext(newtext="Attempt Repair")
        # update the button to now open the power problem window
        self.powersubsystem.setcommand("powerproblem")
        # change colour background to red
        self.powersubsystem.changebackground("red")

    def motorerrorprogram(self):
        # print error messages to the debugger
        self.debugger.addtoscreen("Attempting to bring motor systems online")
        self.debugger.addtoscreen("Hardware: Status - Disconnected")
        self.debugger.addtoscreen("Simulating hardware requirements for software testing purposes")
        self.debugger.addtoscreen("Connection to batteries established")
        self.debugger.addtoscreen("Sufficient power detected for operation")
        self.debugger.addtoscreen("Circuitry detected")
        self.debugger.addtoscreen("Circuitry intact and functional")
        self.debugger.addtoscreen("Safety features enabled")
        self.debugger.addtoscreen("Testing software control of power systems")
        self.debugger.addtoscreen("CRITICAL FAILURE: Core code error 471")
        self.debugger.addtoscreen("Twirpy OS unable to assume control of Power System, Running Debugger")
        self.debugger.addtoscreen("Activating Debug Mode")
        self.debugger.addtoscreen("Debug Summary")
        self.debugger.addtoscreen("Hardware requirements: PASS", colour="green")
        self.debugger.addtoscreen("Power requirements: PASS", colour="green")
        self.debugger.addtoscreen("Circuitry requirements: PASS", colour="green")
        self.debugger.addtoscreen("Safety features: PASS", colour="green")
        self.debugger.addtoscreen("Software Control: FAIL", colour="red")
        self.debugger.addtoscreen("Full diagnostic: Software Control Subroutines")
        self.debugger.addtoscreen("Progress 10%")
        self.debugger.addtoscreen("Progress 20%")
        self.debugger.addtoscreen("Progress 30%")
        self.debugger.addtoscreen("Progress 40%")
        self.debugger.addtoscreen("Progress 50%")
        self.debugger.addtoscreen("Progress 60%")
        self.debugger.addtoscreen("Progress 70%")
        self.debugger.addtoscreen("Progress 80%")
        self.debugger.addtoscreen("Progress 90%")
        self.debugger.addtoscreen("Progress 100%")
        self.debugger.addtoscreen("Error Detected: Process exceeds maximum allowed memory usage")

        # update the status of the power box to Error
        self.motorsubsystem.changestatus(newstatus="Status: Error Detected")
        # update the button so that it creates a problem filling it with a random power puzzle
        self.motorsubsystem.changebuttontext(newtext="Attempt Repair")
        # update the button to now open the power problem window
        self.motorsubsystem.setcommand("motorproblem")
        # change colour background to red
        self.motorsubsystem.changebackground("red")


class subsystemwindow:
    def __init__(self, mainframe, row, column):
        # control subsystem
        self.subsystemframe = tk.Frame(mainframe, background="#7a7a7a")
        self.subsystemframe.grid(row=row, column=column, sticky=tk.NSEW)
        self.subsystemframetext = tk.Label(self.subsystemframe, text="Control Subsystem", background="#7a7a7a", font=(None, 18))
        self.subsystemframetext.grid(row=0, column=0, sticky=tk.NSEW)
        self.subsystemstatus = tk.Label(self.subsystemframe, text="Status: Untested", background="#7a7a7a", font=(None, 18))
        self.subsystemstatus.grid(row=1, column=0, sticky=tk.NSEW)
        self.subsystemsbutton = tk.Button(self.subsystemframe, text="Activate")
        self.subsystemsbutton.grid(row=2, column=0, sticky=tk.NSEW)

        self.subsystemframe.grid_rowconfigure((0, 1), weight=1)
        self.subsystemframe.grid_rowconfigure(2, weight=1)
        self.subsystemframe.grid_columnconfigure(0, weight=1)

        # Buff and pad all children of controlsubframe
        for child in self.subsystemframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def changetitle(self, newtitle):
        self.subsystemframetext.configure(text=newtitle)
        self.subsystemframe.update()

    def changebuttontext(self, newtext):
        self.subsystemsbutton.configure(text=newtext)
        self.subsystemframe.update()

    def setcommand(self, newcommand):
        if newcommand == "power":
            self.subsystemsbutton.configure(command=lambda: gui.powererrorprogram())
        if newcommand == "powerproblem":
            self.subsystemsbutton.configure(command=lambda: self.createproblemcore())
        if newcommand == "motor":
            self.subsystemsbutton.configure(command=lambda: gui.motorerrorprogram())
        if newcommand == "motorproblem":
            self.subsystemsbutton.configure(command=lambda: self.createmotorproblemcore())

        self.subsystemframe.update()

    def changestatus(self, newstatus):
        self.subsystemstatus.configure(text=newstatus)
        self.subsystemframe.update()

    def createproblemcore(self):
        gui.debugger.addtoscreen("ACTIVATING INTERACTIVE DEBUG SESSION", colour="red")
        gui.debugger.addtoscreen("ERROR")
        gui.debugger.addtoscreen("Line 342: Power and battery installation status, expected output TRUE")
        gui.debugger.addtoscreen("Input 1: Function call: detect power returns TRUE")
        gui.debugger.addtoscreen("Input 2: Function call: detect battery returns TRUE")
        gui.debugger.addtoscreen("Boolean operator injection required")
        testing = BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(), "Return TRUE only if both power systems and battery are active")

    def createmotorproblemcore(self):
        motorproblemcore = ScrollingWindow()
        motorproblemcore.settitle("Motor Systems Debug")
        motorproblemcore.addtoscreen("Testing")

    def changebackground(self, colour):
        if colour == "red":
            self.subsystemframe.configure(background="#870101")
            self.subsystemframetext.configure(background="#870101")
            self.subsystemstatus.configure(background="#870101")
        else:
            self.subsystemframe.configure(background="#7a7a7a")
            self.subsystemframetext.configure(background="#7a7a7a")
            self.subsystemstatus.configure(background="#7a7a7a")

        self.subsystemframe.update()


class BooleanChoiceWindow:
    def __init__(self, width, height, question):
        # create toplevel to house the choices
        self.choicewindow = Toplevel()
        self.choicewindow.config(background="#FFFFFF")
        # get size and position of the problemcore window
        self.choicewindow.geometry('%dx%d+%d+%d' % (width/2, height/5, (root.winfo_screenwidth()/2 - width/4), root.winfo_screenheight()/2 - (height/3)/2))
        self.choicewindow.resizable(0, 0)
        # add questions label
        question = ttk.Label(self.choicewindow, text=question, font=(None, 14))
        question.config(wraplength=500)
        question.grid(row=0, column=0, sticky=tk.EW, columnspan=3)
        # add text explaining what to do
        text = ttk.Label(self.choicewindow, text="Choose the appropriate boolean operator to match the conditions as specified in the debugger", font=(None, 14))
        text.config(wraplength=500)
        text.grid(row=1, column=0, sticky=tk.EW, columnspan=3)
        # add choices
        ttk.Button(self.choicewindow, text="AND").grid(row=2, column=0, sticky=tk.NSEW)
        ttk.Button(self.choicewindow, text="OR").grid(row=2, column=1, sticky=tk.NSEW)
        ttk.Button(self.choicewindow, text="NOT").grid(row=2, column=2, sticky=tk.NSEW)
        # add quite button
        ttk.Button(self.choicewindow, text="Quit").grid(row=3, column=2, sticky=tk.NSEW)

        # give weight to rows and column to permit dynamic redraw
        self.choicewindow.columnconfigure((0, 1, 2), weight=1)
        self.choicewindow.rowconfigure(2, weight=1)

        # Buff and pad all children of mainframe
        for child in self.choicewindow.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.choicewindow.wait_window()


if __name__ == '__main__':
    root = tk.Tk()
    gui = MainApplication(root)
    root.mainloop()

