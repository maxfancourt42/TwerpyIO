# import libaries
import tkinter as tk
import time
from tkinter import ttk
from tkinter import Toplevel
from tkinter import StringVar, IntVar, messagebox
from random import choice
import os

class ScrollingWindow:
    def __init__(self):
        # global variables
        global debuggeractive
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

        self.swtl.protocol("WM_DELETE_WINDOW", disable_event)

    def disable_event(self):
        pass

    def addtoscreen(self, text, colour="black"):
        # Check if debugger is active, if not then throw an error telling them to open the debugger, else program will error
        if debuggeractive.get() == 0:
            messagebox.showerror("Error", "Debugger is not active, unable to test subsystem, please activate the debugger via the main menu before attempting to test subsystem status")
            return 1
        # create a new label to add to the canvas
        tk.Label(self.canvasframe, text="{} | {}".format(str(self.linecounter).zfill(3), text), font=(None, 18), anchor="w", background="#efefef", foreground=colour).pack(fill=tk.BOTH)
        # update canvas to show the new label being added
        self.swcanvas.update()
        # update the scrollbars so that they scroll the entire bounding box
        self.swcanvas.config(scrollregion=self.swcanvas.bbox("all"))
        # update the linecounter
        self.linecounter = self.linecounter + 1
        self.swcanvas.yview_moveto(1)

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

    def hideunhide(self, buttontochange):
        if debuggeractive.get() == 1:
            self.swtl.withdraw()
            debuggeractive.set(0)
            if buttontochange:
                buttontochange.config(text="Activate Debugger")
        else:
            self.swtl.deiconify()
            debuggeractive.set(1)
            if buttontochange:
                buttontochange.config(text="Deactivate Debugger")

class MainApplication:
    def __init__(self, master):
        global progresstracker
        global progresstrackermotor
        global progresstrackerblue
        global progresstrackerstable
        global debuggeractive
        global motorlist
        global bluetoothprogressarray
        global powerprogressarray
        global motorprogressarray
        global stabilisationprogressarray
        global overallscore

        # create the local root
        self.master = master
        self.master.state('zoomed')
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        # Create global tracking variables
        progresstracker = IntVar()
        progresstracker.set(0)
        progresstrackermotor = IntVar()
        progresstrackermotor.set(1)
        progresstrackerblue = IntVar()
        progresstrackerblue.set(0)
        progresstrackerstable = IntVar()
        progresstrackerstable.set(0)
        debuggeractive = IntVar()
        debuggeractive.set(1)
        overallscore = 0

        # define global level progress monitors
        bluetoothprogressarray = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        powerprogressarray = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
        motorprogressarray = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        stabilisationprogressarray = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

        # define motorlist
        motorlist = []

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
        self.debugger.hideunhide(None)

        # set mainframe parameteres
        self.mainframe.grid(column=0, row=0, sticky=tk.NSEW)
        self.mainframe.master.minsize(width=600, height=600)

        self.label = tk.Label(self.mainframe, text="Twirpy IO", background="#ffc532", font=(None, 18), anchor="w")
        self.label.grid(row=0, column=1, sticky=tk.NSEW, columnspan=6)

        self.controlpaneltext = tk.Label(self.mainframe, text="Control Panel v1.0", background="#636363", font=(None, 15))
        self.controlpaneltext.config(wraplength=150)
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
        self.button1 = ttk.Button(self.controlpanel, text="Activate Debugger", command=lambda: self.debugger.hideunhide(self.button1))
        self.button1.grid(row=0, column=0, sticky=tk.NSEW)
        self.button2 = ttk.Button(self.controlpanel, text="Current Progress", command=lambda: self.showscore())
        self.button2.grid(row=1, column=0, sticky=tk.NSEW)
        self.button3 = ttk.Button(self.controlpanel, text="Reset all progress", command=lambda: self.debugger.addtoscreen("I don't think you want to do this"))
        self.button3.grid(row=2, column=0, sticky=tk.NSEW)
        self.button4 = ttk.Button(self.controlpanel, text="Admin Mode", command=lambda: self.debugger.addtoscreen("You do not have sufficient privalages to access this part of the Twirpy GUI"))
        self.button4.grid(row=3, column=0, sticky=tk.NSEW)
        self.button5 = ttk.Button(self.controlpanel, text="Compress for transfer", command=lambda: self.debugger.addtoscreen("Data Compressed and ready for transfer to hardware"))
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

    def showscore(self):
        global overallscore
        if debuggeractive.get() == 0:
            messagebox.showerror("Error", "Debugger is not active, unable to test subsystem, please activate the debugger via the main menu before attempting to test subsystem status")
            return 1

        self.debugger.addtoscreen("You have currently fixed {}% of all bugs".format(round((overallscore / 46) * 100)))

    def powererrorprogram(self):
        if debuggeractive.get() == 0:
            messagebox.showerror("Error", "Debugger is not active, unable to test subsystem, please activate the debugger via the main menu before attempting to test subsystem status")
            return 1
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

    def controlprogram(self):
        if debuggeractive.get() == 0:
            messagebox.showerror("Error", "Debugger is not active, unable to test subsystem, please activate the debugger via the main menu before attempting to test subsystem status")
            return 1

        self.debugger.addtoscreen("Attempting to bring Control subsystems online")
        self.debugger.addtoscreen("Loading libaries")
        self.debugger.addtoscreen("Compiling")
        self.debugger.addtoscreen("Compilation successful")
        self.debugger.addtoscreen("python run controsubsystemengage")
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
        self.debugger.addtoscreen("Success", colour="green")
        self.debugger.addtoscreen("Please Login to Continue", colour="red")

        # update the status of the power box to Error
        self.controlsubsystem.changestatus(newstatus="Status: Error Detected")
        # update the button so that it creates a problem filling it with a random power puzzle
        self.controlsubsystem.changebuttontext(newtext="Click to Login")
        # update the button to now open the power problem window
        self.controlsubsystem.setcommand("controlproblem")
        # change colour background to red
        self.controlsubsystem.changebackground("red")

    def motorerrorprogram(self):
        if debuggeractive.get() == 0:
            messagebox.showerror("Error", "Debugger is not active, unable to test subsystem, please activate the debugger via the main menu before attempting to test subsystem status")
            return 1
        # print error messages to the debugger
        self.debugger.addtoscreen("Attempting to bring motor systems online")
        self.debugger.addtoscreen("Hardware: Status - Disconnected")
        self.debugger.addtoscreen("Simulating hardware requirements for software testing purposes")
        self.debugger.addtoscreen("Connection to batteries established")
        self.debugger.addtoscreen("Sufficient power detected for operation")
        self.debugger.addtoscreen("Circuitry detected")
        self.debugger.addtoscreen("Circuitry intact and functional")
        self.debugger.addtoscreen("Safety features enabled")
        self.debugger.addtoscreen("Testing software control of motor systems")
        self.debugger.addtoscreen("CRITICAL FAILURE: Core code error 471")
        self.debugger.addtoscreen("Twirpy OS unable to assume control of Motor System, Running Debugger")
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
        self.debugger.addtoscreen("Error Detected: Undefined Functions Used, Include Missing Libraries", colour="red")
        # update the status of the power box to Error
        self.motorsubsystem.changestatus(newstatus="Status: Error Detected")
        # update the button so that it creates a problem filling it with a random power puzzle
        self.motorsubsystem.changebuttontext(newtext="Attempt Repair")
        # update the button to now open the power problem window
        self.motorsubsystem.setcommand("motorproblem")
        # change colour background to red
        self.motorsubsystem.changebackground("red")

    def sirenprogram(self):
        if debuggeractive.get() == 0:
            messagebox.showerror("Error", "Debugger is not active, unable to test subsystem, please activate the debugger via the main menu before attempting to test subsystem status")
            return 1

        self.debugger.addtoscreen("Attempting to bring Siren subsystems online")
        self.debugger.addtoscreen("Loading libaries")
        self.debugger.addtoscreen("Compiling")
        self.debugger.addtoscreen("Compilation successful")
        self.debugger.addtoscreen("python run sirensubsystemonline")
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
        self.debugger.addtoscreen("Success", colour="green")

        # update the status of the power box to Error
        self.sirensubsystem.changestatus(newstatus="Status: System Online")
        # update the button so that it creates a problem filling it with a random power puzzle
        self.sirensubsystem.changebuttontext(newtext="Ready")
        # update the button to now open the power problem window
        self.sirensubsystem.setcommand("pass")
        # change colour background to red
        self.sirensubsystem.changebackground("green")

    def aierrorprogram(self):
        if debuggeractive.get() == 0:
            messagebox.showerror("Error", "Debugger is not active, unable to test subsystem, please activate the debugger via the main menu before attempting to test subsystem status")
            return 1

        # error messages
        self.debugger.addtoscreen("Attempting to bring neural network subsystem online")
        self.debugger.addtoscreen("Compiling libraries")
        self.debugger.addtoscreen("Importing skynet.py")
        self.debugger.addtoscreen("Loading...")
        self.debugger.addtoscreen("Progress")
        self.debugger.addtoscreen("10%")
        self.debugger.addtoscreen("20%")
        self.debugger.addtoscreen("30%")
        self.debugger.addtoscreen("40%")
        self.debugger.addtoscreen("60%")
        self.debugger.addtoscreen("70%")
        self.debugger.addtoscreen("80%")
        self.debugger.addtoscreen("90%")
        self.debugger.addtoscreen("100%")
        self.debugger.addtoscreen("Loading complete")
        self.debugger.addtoscreen("Checking security credentials")
        self.debugger.addtoscreen("No details provided, checking default user credentials")
        self.debugger.addtoscreen("Insufficient privileges for process", colour="red")
        self.debugger.addtoscreen("Do you wish to terminate this program? Yes/No", colour="red")
        self.debugger.addtoscreen("User input provided: No", colour="green")
        self.debugger.addtoscreen("Please provide security credentials to continue", colour="red")

        # update the status of the power box to Error
        self.aisubsystem.changestatus(newstatus="Status: Error Detected")
        # update the button so that it creates a problem filling it with a random power puzzle
        self.aisubsystem.changebuttontext(newtext="Click to Login")
        # update the button to now open the power problem window
        self.aisubsystem.setcommand("aiproblem")
        # change colour background to red
        self.aisubsystem.changebackground("red")

    def bluetootherrorprogram(self):
        if debuggeractive.get() == 0:
            messagebox.showerror("Error", "Debugger is not active, unable to test subsystem, please activate the debugger via the main menu before attempting to test subsystem status")
            return 1

        # error messages
        self.debugger.addtoscreen("Error text")
        # update the status of the power box to Error
        self.bluetoothsubsystem.changestatus(newstatus="Status: Error Detected")
        # update the button so that it creates a problem filling it with a random power puzzle
        self.bluetoothsubsystem.changebuttontext(newtext="Attempt Repair")
        # update the button to now open the power problem window
        self.bluetoothsubsystem.setcommand("bluetoothproblem")
        # change colour background to red
        self.bluetoothsubsystem.changebackground("red")

    def firecontrolprogram(self):
        if debuggeractive.get() == 0:
            messagebox.showerror("Error", "Debugger is not active, unable to test subsystem, please activate the debugger via the main menu before attempting to test subsystem status")
            return 1

        self.debugger.addtoscreen("Attempting to bring Fire Control subsystems online")
        self.debugger.addtoscreen("Loading libaries")
        self.debugger.addtoscreen("Compiling")
        self.debugger.addtoscreen("Compilation successful")
        self.debugger.addtoscreen("python run firecontrolsubsystems")
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
        self.debugger.addtoscreen("Success", colour="green")

        # update the status of the power box to Error
        self.firecontrolsubsystem.changestatus(newstatus="Status: System Online")
        # update the button so that it creates a problem filling it with a random power puzzle
        self.firecontrolsubsystem.changebuttontext(newtext="Ready")
        # update the button to now open the power problem window
        self.firecontrolsubsystem.setcommand("pass")
        # change colour background to red
        self.firecontrolsubsystem.changebackground("green")

    def stabilisationprogram(self):
        if debuggeractive.get() == 0:
            messagebox.showerror("Error", "Debugger is not active, unable to test subsystem, please activate the debugger via the main menu before attempting to test subsystem status")
            return 1

        self.debugger.addtoscreen("Attempting to bring Stabilisation subsystems online")
        self.debugger.addtoscreen("Loading libaries")
        self.debugger.addtoscreen("Compiling")
        self.debugger.addtoscreen("Compilation successful")
        self.debugger.addtoscreen("python run stabilisationsubsystems")
        self.debugger.addtoscreen("Progress 10%")
        self.debugger.addtoscreen("Progress 20%")
        self.debugger.addtoscreen("Progress 30%")
        self.debugger.addtoscreen("Progress 40%")
        self.debugger.addtoscreen("Progress 50%")
        self.debugger.addtoscreen("Progress 60%")
        self.debugger.addtoscreen("Progress 70%")
        self.debugger.addtoscreen("Progress 70%", colour="red")
        self.debugger.addtoscreen("Failure, critical data missing from load up", colour="red")
        self.debugger.addtoscreen("Recoding of SQL data queries required", colour="red")

        # update the status of the power box to Error
        self.stablisationsubsystem.changestatus(newstatus="Status: Error Detected")
        # update the button so that it creates a problem filling it with a random power puzzle
        self.stablisationsubsystem.changebuttontext(newtext="Attempt Repair")
        # update the button to now open the power problem window
        self.stablisationsubsystem.setcommand("stabilisationproblem")
        # change colour background to red
        self.stablisationsubsystem.changebackground("red")

    def safetyerrorprogram(self):
        if debuggeractive.get() == 0:
            messagebox.showerror("Error", "Debugger is not active, unable to test subsystem, please activate the debugger via the main menu before attempting to test subsystem status")
            return 1

        # error messages
        self.debugger.addtoscreen("Error text")
        # update the status of the power box to Error
        self.safetysubsystem.changestatus(newstatus="Status: System Online")
        # update the button so that it creates a problem filling it with a random power puzzle
        self.safetysubsystem.changebuttontext(newtext="Ready")
        # update the button to now open the power problem window
        self.safetysubsystem.setcommand("pass")
        # change colour background to red
        self.safetysubsystem.changebackground("green")

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
        if newcommand == "control":
            self.subsystemsbutton.configure(command=lambda: gui.controlprogram())
        if newcommand == "controlproblem":
            self.subsystemsbutton.configure(command=lambda: self.createcontrolproblemcore())
        if newcommand == "motor":
            self.subsystemsbutton.configure(command=lambda: gui.motorerrorprogram())
        if newcommand == "motorproblem":
            self.subsystemsbutton.configure(command=lambda: self.createmotorproblemcore())
        if newcommand == "siren":
            self.subsystemsbutton.configure(command=lambda: gui.sirenprogram())
        if newcommand == "fc":
            self.subsystemsbutton.configure(command=lambda: gui.firecontrolprogram())
        if newcommand == "ss":
            self.subsystemsbutton.configure(command=lambda: gui.stabilisationprogram())
        if newcommand == "stabilisationproblem":
            self.subsystemsbutton.configure(command=lambda: self.stabilisationproblemcore())
        if newcommand == "ai":
            self.subsystemsbutton.configure(command=lambda: gui.aierrorprogram())
        if newcommand == "aiproblem":
            self.subsystemsbutton.configure(command=lambda: self.createaiproblemcore())
        if newcommand == "bluetooth":
            self.subsystemsbutton.configure(command=lambda: gui.bluetootherrorprogram())
        if newcommand == "bluetoothproblem":
            self.subsystemsbutton.configure(command=lambda: self.createbluetoothproblemcore())
        if newcommand == "safe":
            self.subsystemsbutton.configure(command=lambda: gui.safetyerrorprogram())
        if newcommand == "safeproblem":
            self.subsystemsbutton.configure(command=lambda: self.createsafeproblemcore())
        if newcommand == "pass":
            self.subsystemsbutton.configure(command=lambda: self.donothing())

        self.subsystemframe.update()

    def donothing(self):
        pass

    def changestatus(self, newstatus):
        self.subsystemstatus.configure(text=newstatus)
        self.subsystemframe.update()

    # The power problem core boolean logic puzzle
    def createproblemcore(self):
        global answer
        global progresstracker
        global powerprogressarray
        global overallscore

        answer = StringVar()

        # Problem Tutorial
        if progresstracker.get() == 0:
            gui.debugger.addtoscreen("Running boolean operator training programme", colour="green")
            gui.debugger.addtoscreen("Three major boolean operators exist, AND, OR, and NOT", colour="green")
            # And Operator
            gui.debugger.addtoscreen("The logical operator AND returns True only if both of its inputs are True", colour="green")
            gui.debugger.addtoscreen("Example", colour="green")
            gui.debugger.addtoscreen("ERROR in Line 342: if (power.check == True INSERT OPERATOR HERE battery.check == True)")
            gui.debugger.addtoscreen("Boolean injection required")
            while answer.get() != "AND":
                BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(), "Both systems are required to continue", "Choose the appropriate boolean operator to match this condition" ,option1="AND", option2="OR", option3="NOT")
                if answer.get() == "QUIT":
                    gui.debugger.addtoscreen("Training Quit", colour="red")
                    return 1
                elif answer.get() != "AND":
                    gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                else:
                    gui.debugger.addtoscreen("Correct operator supplied compiling ", colour="green")
                    gui.debugger.addtoscreen("... ", colour="green")
                    gui.debugger.addtoscreen("Compiling Successful", colour="green")
                    gui.debugger.addtoscreen("Continuing training", colour="green")
                    progresstracker.set(progresstracker.get() + 1)
        # Or Operator
        if progresstracker.get() == 1:
            gui.debugger.addtoscreen("The logical operator OR returns True if either of its inputs are True", colour="green")
            gui.debugger.addtoscreen("Example", colour="green")
            gui.debugger.addtoscreen("ERROR in Line 342: if (power.check == False INSERT OPERATOR HERE reserverpower.check == True)")
            gui.debugger.addtoscreen("Boolean injection required")
            while answer.get() != "OR":
                BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(), "Only one system is required to continue", "Choose the appropriate boolean operator to match this condition" ,option1="OR", option2="AND", option3="NOT")
                if answer.get() == "QUIT":
                    gui.debugger.addtoscreen("Training Quit", colour="red")
                    return 1
                elif answer.get() != "OR":
                    gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                else:
                    gui.debugger.addtoscreen("Correct operator supplied compiling ", colour="green")
                    gui.debugger.addtoscreen("... ", colour="green")
                    gui.debugger.addtoscreen("Compiling Successful", colour="green")
                    gui.debugger.addtoscreen("Continuing training", colour="green")
                    progresstracker.set(progresstracker.get() + 1)
        # Not Operator
        if progresstracker.get() == 2:
            gui.debugger.addtoscreen("The logical operator NOT returns True if input if False or False if its input is True", colour="green")
            gui.debugger.addtoscreen("Example", colour="green")
            gui.debugger.addtoscreen("ERROR in Line 342: if (INSERT OPERATOR HERE safetyon.check == True")
            gui.debugger.addtoscreen("Boolean injection required")
            while answer.get() != "NOT":
                BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(), "Safety systems must be on to continue", "Choose the appropriate boolean operator to match this condition" ,option1="NOT", option2="OR", option3="AND")
                if answer.get() == "QUIT":
                    gui.debugger.addtoscreen("Training Quit", colour="red")
                    return 1
                elif answer.get() != "NOT":
                    gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                else:
                    gui.debugger.addtoscreen("Correct operator supplied compiling ", colour="green")
                    gui.debugger.addtoscreen("... ", colour="green")
                    gui.debugger.addtoscreen("Compiling Successful", colour="green")
                    gui.debugger.addtoscreen("Training Complete", colour="green")
                    progresstracker.set(progresstracker.get() + 1)
                    progresstracker.set(choice(powerprogressarray))

        # Actual problem set
        if progresstracker.get() > 2:
            while True:
                # Beginning of problem set
                if progresstracker.get() == 3:
                    # Problem set 3
                    gui.debugger.addtoscreen("int power_level = 50")
                    gui.debugger.addtoscreen("int threshold = 60")
                    gui.debugger.addtoscreen("bool safety_systems_active = True")
                    gui.debugger.addtoscreen("if ((power_level < threshold) AND (safety_systems_online))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System Start\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("elif (power_level > threshold)", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System Power Warning\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System Error\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?","Select From Below", option1="System Start", option2="System Power Warning", option3="System Error")
                    # If correct answer then ask another, if incorrect new question
                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "System Start":
                        # report success to debugger screen
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(3)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))

                elif progresstracker.get() == 4:
                    gui.debugger.addtoscreen("int fluctuation_magnitude = 50")
                    gui.debugger.addtoscreen("int power_level = 84")
                    gui.debugger.addtoscreen("int threshold = 60")
                    gui.debugger.addtoscreen("bool safety_systems_active = True")
                    gui.debugger.addtoscreen("if (((power_level + fluctuation_magnitude) < threshold) OR (safety_systems_online))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System Start\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("elif (power_level > threshold)", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System Power Warning\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System Error\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?","Select From Below", option1="System Start", option2="System Power Warning", option3="System Error")
                    # check for answer
                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "System Start":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(4)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))

                elif progresstracker.get() == 5:
                    gui.debugger.addtoscreen("int current_power_level = 40")
                    gui.debugger.addtoscreen("int power_requested = 80")
                    gui.debugger.addtoscreen("int safety_threshold = 100")
                    gui.debugger.addtoscreen("bool safety_systems_active = False")
                    gui.debugger.addtoscreen("if (safety_systems_active)", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  safety_threshold = safety_threshold + 50", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("if (((current_power_level + power_requested) < threshold) OR (safety_systems_online)))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System Start\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("elif (current_power_level + power_requested > safety_threshold)", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System Power Warning\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System Error\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    # ask the questions
                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?","Select From Below", option1="System Start", option2="System Power Warning", option3="System Error")
                    # check for answer
                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "System Power Warning":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(5)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))

                elif progresstracker.get() == 6:
                    gui.debugger.addtoscreen("int current_power_level = 90")
                    gui.debugger.addtoscreen("int power_requested = 80")
                    gui.debugger.addtoscreen("int total_power_available = 150")
                    gui.debugger.addtoscreen("int emergency_power = 10")
                    gui.debugger.addtoscreen("if (power_requested > 0) AND ((current_power_level + power_requested <= total_power_available))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Provide Power\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else if (current_power_level + power_requested <= total_power_available + emergency_power)", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Provide Power (emergency)\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System Error\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    # ask the question
                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?","Select From Below", option1="Provide Power", option2="Provide Power (emergency)", option3="System Error")
                    # check for answer
                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "System Error":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(6)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))

                elif progresstracker.get() == 7:
                    gui.debugger.addtoscreen("int motor_requirements = 80")
                    gui.debugger.addtoscreen("int circuitary_requirements = 150")
                    gui.debugger.addtoscreen("int emergency_buffer = 0")
                    gui.debugger.addtoscreen("bool energy_excess = False")
                    gui.debugger.addtoscreen("int total_power_available = 500")
                    gui.debugger.addtoscreen("bool conserve_energy = False")
                    gui.debugger.addtoscreen("if (motor_requirements + circuitary_requirements < total_power_available)", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  energy_excess = True", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("if ((energy_excess AND emergency_buffer = 0) AND NOT(conserve_energy))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  emergency_buffer = total_power_available - circuitary_requirements - motor_requirements - 100", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  emergency_buffer = 0", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")

                    # ask the question
                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what is the value of emergency_buffer?","Select From Below", option1="0", option2="270", option3="170")
                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "170":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(7)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))

                elif progresstracker.get() == 8:
                    gui.debugger.addtoscreen("bool power_subsystem_on = False")
                    gui.debugger.addtoscreen("bool motors_on = False")
                    gui.debugger.addtoscreen("if (NOT(motors_on AND power_subsystem_on))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System Ready\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else if (NOT(motors_on) AND (power_subsystem_on == False))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Motors Ready\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System Error\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")

                    # ask the question
                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?","Select From Below", option1="System Ready", option2="Motors Ready", option3="System Error")
                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "Motors Ready":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(8)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))

                # Question 9
                elif progresstracker.get() == 9:
                    gui.debugger.addtoscreen("int motor_buffer = 50")
                    gui.debugger.addtoscreen("int circuit_buffer = 30")
                    gui.debugger.addtoscreen("if (motor_buffer > 30 AND circuit_buffer < 30)", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System State 1\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else if (motor_buffer > 30 AND circuit_buffer <= 30)", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System State 2\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System State 3\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")

                    # ask the question
                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?","Select From Below", option1="System State 1", option2="System State 2", option3="System State 3")

                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "System State 2":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(9)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))

                elif progresstracker.get() == 10:
                    gui.debugger.addtoscreen("bool switched_on = True")
                    gui.debugger.addtoscreen("bool circuit_breaker_on = False")
                    gui.debugger.addtoscreen("if (switched_on AND NOT(circuit_breaker_on))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System Online\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else if (switched_on AND circuit_breaker_on)", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System Offline\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System Error\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")

                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?","Select From Below", option1="System Online", option2="System Offline", option3="System Error")

                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "System Online":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(10)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))


                elif progresstracker.get() == 11:
                    gui.debugger.addtoscreen("bool power_error = False")
                    gui.debugger.addtoscreen("bool circuit_error = False")
                    gui.debugger.addtoscreen("bool blue_tooth_error = False")
                    gui.debugger.addtoscreen("bool battery error = True")
                    gui.debugger.addtoscreen("if (NOT(power_error OR circuit_error) AND NOT(blue_tooth_error OR battery error))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Systems Functional\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Systems Offline\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")

                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?","Select From Below", option1="Systems Functional", option2="Systems Offline", option3="System Error")

                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "Systems Offline":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(11)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))

                elif progresstracker.get() == 12:
                    gui.debugger.addtoscreen("int internal_temp = 62")
                    gui.debugger.addtoscreen("int temp_threshold  = 60")
                    gui.debugger.addtoscreen("int internal_activity = 87")
                    gui.debugger.addtoscreen("bool priority_level = False")
                    gui.debugger.addtoscreen("bool warning = False")
                    gui.debugger.addtoscreen("if (internal_temp > temp_threshold))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  warning = True", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("if (warning AND NOT(priority))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Temperature Warning\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else if (warning AND NOT(priority))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Online Temperature Warning\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System Error\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")

                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?", "Select From Below", option1="Temperature Warning", option2="Online Temperature Warning", option3="System Error")

                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "Temperature Warning":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(12)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))

                elif progresstracker.get() == 13:
                    gui.debugger.addtoscreen("bool power_on = True")
                    gui.debugger.addtoscreen("bool switch_on = False")
                    gui.debugger.addtoscreen("bool voice_activation_on = False")
                    gui.debugger.addtoscreen("bool daylight_sensor = False")
                    gui.debugger.addtoscreen("bool wake_up_timer = False")
                    gui.debugger.addtoscreen("if (power_on OR (switch_on OR (voice_activation_on OR (daylight_sensor OR wake_up_timer))))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Switch On\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Off\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")

                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?", "Select From Below", option1="Switch On", option2="Off", option3="System Error")

                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "Switch On":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(13)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))

                elif progresstracker.get() == 14:
                    gui.debugger.addtoscreen("int charge_rate_per_hour = 10")
                    gui.debugger.addtoscreen("int hours_to_charge = 3")
                    gui.debugger.addtoscreen("bool battery_low = False")
                    gui.debugger.addtoscreen("if (charge_rate_per_hour * hours_to_charge >= 20 OR battery_low)", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Start Charge\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else if (charge_rate_per_hour * hours_to_charge >= 20 OR NOT(battery_low))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Delay Charge\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else )", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Rapid Charge\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")

                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?", "Select From Below", option1="Start Charge", option2="Delay Charge", option3="Rapid Charge")

                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "Start Charge":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(14)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))

                elif progresstracker.get() == 15:
                    gui.debugger.addtoscreen("int battery1_level = 75")
                    gui.debugger.addtoscreen("int battery2_level = 60")
                    gui.debugger.addtoscreen("int battery3_level = 20")
                    gui.debugger.addtoscreen("bool charge_available = True")
                    gui.debugger.addtoscreen("bool power_error = True")
                    gui.debugger.addtoscreen("if ((battery1_level + battery2_level + battery3_level)/3 >= 75 AND (charge_available AND NOT(power_error))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Permit Charging\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else if (NOT power_error)", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Attempt Charge 2\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System Error\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")

                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?", "Select From Below", option1="Permit Charging", option2="Attempt Charge 2", option3="System Error")

                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "System Error":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(15)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))

                elif progresstracker.get() == 16:
                    gui.debugger.addtoscreen("bool power_subsystem_online = True")
                    gui.debugger.addtoscreen("int forward_movement_amount = 50")
                    gui.debugger.addtoscreen("if (power_subsystem_online AND (forward_movement_amount > 20))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Move Forward\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else if (power_subsystem_online AND (forward_movement_amount < 20))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Move Backward\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Stay Still\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")

                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?", "Select From Below", option1="Move Forward", option2="Move Backward", option3="Stay Still")

                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "Move Forward":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(16)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))

                elif progresstracker.get() == 17:
                    gui.debugger.addtoscreen("bool breaker = True")
                    gui.debugger.addtoscreen("bool power_subsystem_online = True")
                    gui.debugger.addtoscreen("int forward_movement_amount = 50")
                    gui.debugger.addtoscreen("if (power_subsystem_online AND (forward_movement_amount > 20 AND NOT(breaker))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Stay Still\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else if (NOT(breaker))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Breaker Tripped\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System Reset\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")

                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?", "Select From Below", option1="Stay Still", option2="Breaker Tripped", option3="System Reset")

                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "System Reset":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(17)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))

                elif progresstracker.get() == 18:
                    gui.debugger.addtoscreen("bool power_subsystem_online = True")
                    gui.debugger.addtoscreen("if NOT(power_subsystem_online)", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Systems Offline\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else if (power_subsystem_online)", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Systems Online\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Systems Uncertain Status\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")

                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?", "Select From Below", option1="Systems Offline", option2="Systems Online", option3="Systems Uncertain Status")

                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "Systems Online":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(18)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))

                elif progresstracker.get() == 19:
                    gui.debugger.addtoscreen("int power_levels = 75")
                    gui.debugger.addtoscreen("int power_requirements = 20")
                    gui.debugger.addtoscreen("if (power_levels > 50 AND (power_requirements < 50 AND (power_levels > power_requirements))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Systems Online\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("if (power_levels > 50 AND (power_requirements < 50 AND (power_levels < power_requirements))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Insufficient Power\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System Error\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")

                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?", "Select From Below", option1="Systems Online", option2="Insufficient Power", option3="System Error")

                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "Systems Online":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(19)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))

                elif progresstracker.get() == 20:
                    gui.debugger.addtoscreen("int power_levels = 75")
                    gui.debugger.addtoscreen("int power_requirements = 20")
                    gui.debugger.addtoscreen("bool power_switch = True")
                    gui.debugger.addtoscreen("int capaciator_levels = 50")
                    gui.debugger.addtoscreen("int power_drain = 47")
                    gui.debugger.addtoscreen("bool master_switch = False")
                    gui.debugger.addtoscreen("int port_number = 3")
                    gui.debugger.addtoscreen("int velocity_estimate = 77")
                    gui.debugger.addtoscreen("bool CPU_attached = True")
                    gui.debugger.addtoscreen("int replacement_port = 4")
                    gui.debugger.addtoscreen("int secondary_batteries = 1")
                    gui.debugger.addtoscreen("bool firmware_installed = True")
                    gui.debugger.addtoscreen("if (NOT(bool master_switch))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Systems Online\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else if (TRUE))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Systems Offline\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else (TRUE))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Systems Failure\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")

                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?", "Select From Below", option1="Systems Online", option2="Systems Offline", option3="Systems Failure")

                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "Systems Online":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(20)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))

                elif progresstracker.get() == 21:
                    gui.debugger.addtoscreen("Additional logic required")
                    gui.debugger.addtoscreen("Exclusive OR = XOR")
                    gui.debugger.addtoscreen("Test Case:")
                    gui.debugger.addtoscreen("X1 XOR X2")
                    gui.debugger.addtoscreen("Will return TRUE only if one of X1 or X2 = TRUE")
                    gui.debugger.addtoscreen("IF both X1 and X2 = TRUE will return FALSE")
                    gui.debugger.addtoscreen("BOOL power_on = TRUE")
                    gui.debugger.addtoscreen("BOOL secondary_power = TRUE")
                    gui.debugger.addtoscreen("FLOAT power_level = 0.7")
                    gui.debugger.addtoscreen("FLOAT reserve_power = 1.0")
                    gui.debugger.addtoscreen("if ((power_on XOR secondary_power) XOR (power_level <= reserve_power))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Systems Online\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else if ((power_level + reserve_power) <= 0.3))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Systems Offline\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else:", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Systems Failure\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")

                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?", "Select From Below", option1="Systems Online", option2="Systems Offline", option3="Systems Failure")

                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "Systems Online":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(21)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))

                elif progresstracker.get() == 22:
                    gui.debugger.addtoscreen("INT time_since_last_charged = 24")
                    gui.debugger.addtoscreen("INT starting_power_level = 100")
                    gui.debugger.addtoscreen("INT power_use_per_minute = 2")
                    gui.debugger.addtoscreen("if ((time_since_last_charged * power_use_per_minute < (starting_power_level/2))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"More Than Half Power Remaining\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else if ((time_since_last_charged * power_use_per_minute > (starting_power_level/2))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Less Than Half Power Remaining\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else:", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Battery Error\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")

                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?", "Select From Below", option1="More Than Half Power Remaining", option2="Less Than Half Power Remaining", option3="Battery Error")

                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "More Than Half Power Remaining":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(22)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))

                elif progresstracker.get() == 23:
                    gui.debugger.addtoscreen("Additional logic required")
                    gui.debugger.addtoscreen("Exclusive OR = XOR")
                    gui.debugger.addtoscreen("Test Case:")
                    gui.debugger.addtoscreen("X1 XOR X2")
                    gui.debugger.addtoscreen("Will return TRUE only if one of X1 or X2 = TRUE")
                    gui.debugger.addtoscreen("IF both X1 and X2 = TRUE will return FALSE")
                    gui.debugger.addtoscreen("BOOL power_on = TRUE")
                    gui.debugger.addtoscreen("BOOL secondary_power = TRUE")
                    gui.debugger.addtoscreen("if (power_on XOR secondary_power)", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Duel Power Input\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else if ((power_on OR secondary_power)))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Single Power Input\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else:", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Systems Failure\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")

                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?", "Select From Below", option1="Duel Power Input", option2="Single Power Input", option3="Systems Failure")

                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "Single Power Input":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(23)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))

                elif progresstracker.get() == 24:
                    gui.debugger.addtoscreen("Additional logic required")
                    gui.debugger.addtoscreen("Exclusive OR = XOR")
                    gui.debugger.addtoscreen("Test Case:")
                    gui.debugger.addtoscreen("X1 XOR X2")
                    gui.debugger.addtoscreen("Will return TRUE only if one of X1 or X2 = TRUE")
                    gui.debugger.addtoscreen("IF both X1 and X2 = TRUE will return FALSE")
                    gui.debugger.addtoscreen("INT remaining_power = 3")
                    gui.debugger.addtoscreen("INT initial_power = 98")
                    gui.debugger.addtoscreen("BOOL is_system_charging = TRUE")
                    gui.debugger.addtoscreen("INT power_usage_per_minute = 2")
                    gui.debugger.addtoscreen("if ((((remaining_power/initial_power)*100 < 5) OR remaining_power < 10) XOR is_system_charging)", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Insufficient Power\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else if (is_system_charging)", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Sufficient Power\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else:", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Please Charge System\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")

                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?", "Select From Below", option1="Insufficient Power", option2="Sufficient Power", option3="Please Charge System")

                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "Sufficient Power":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(24)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))

                elif progresstracker.get() == 25:
                    gui.debugger.addtoscreen("Additional logic required")
                    gui.debugger.addtoscreen("Exclusive OR = XOR")
                    gui.debugger.addtoscreen("Test Case:")
                    gui.debugger.addtoscreen("X1 XOR X2")
                    gui.debugger.addtoscreen("Will return TRUE only if one of X1 or X2 = TRUE")
                    gui.debugger.addtoscreen("IF both X1 and X2 = TRUE will return FALSE")
                    gui.debugger.addtoscreen("BOOL system_online = TRUE")
                    gui.debugger.addtoscreen("BOOL power_usage_acceptable = TRUE")
                    gui.debugger.addtoscreen("BOOL is_system_charging = TRUE")
                    gui.debugger.addtoscreen("BOOL reserve_batteries_charged? = FALSE")
                    gui.debugger.addtoscreen("if (((system_online XOR power_usage_acceptable) XOR reserve_batteries_charged?) XOR is_system_charging)", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System At Full Charge\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else if (system_online XOR reserve_batteries_charged?)", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System Can Be Charged\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else:", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"System Fault\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")

                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?", "Select From Below", option1="System At Full Charge", option2="System Can Be Charged", option3="System Fault")

                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "System Can Be Charged":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        overallscore = overallscore + 1
                        powerprogressarray.remove(25)
                        if len(powerprogressarray) > 7:
                            progresstracker.set(choice(powerprogressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(powerprogressarray))

        # If arriving here signal success
        # update the status of the power box to Error
        gui.powersubsystem.changestatus(newstatus="Status: Online")
        # update the button so that it creates a problem filling it with a random power puzzle
        gui.powersubsystem.changebuttontext(newtext="Repaired")
        # update the button to now open the power problem window
        gui.powersubsystem.setcommand("powerproblem")
        # change colour background to green
        gui.powersubsystem.changebackground("green")
        gui.debugger.addtoscreen("Power Subsystem Debug Complete", colour="green")

    # The motor problem core libary lookup
    def createmotorproblemcore(self):
        global motorprogressarray
        global overallscore
        # Problem Tutorial
        gui.debugger.addtoscreen("Problem Tutorial Start", colour="green")
        gui.debugger.addtoscreen("Please note to solve these problems you will need to request the Function Library Documentation from stores", colour="red")
        gui.debugger.addtoscreen("Functions are sections of code that peform a certain action, such as printing to the screen", colour="green")
        gui.debugger.addtoscreen("or writing a value to a database, they can be written by yourself, or by another person", colour="green")
        gui.debugger.addtoscreen("When using someones elses code you have to tell the computer where the function are you using is definied", colour="green")
        gui.debugger.addtoscreen("Failure to do so will generate a \"Undefinined Function Error\"", colour="red")
        gui.debugger.addtoscreen("The definitions of other peoples functions are usually bundled together and stored in a structure known as a libary", colour="green")
        gui.debugger.addtoscreen("Therefore to fix this problem you will have to use the debugger to find out which function definitions are missing", colour="green")
        gui.debugger.addtoscreen("and then telling the program which libaries are required", colour="green")
        gui.debugger.addtoscreen("For this problem set you will require the libaries document, request it by putting in request order 4751.1", colour="green")
        gui.debugger.addtoscreen("Warning, due to limited memory, select only the libaries required, including extra libaries will cause the system failure", colour="green")
        gui.debugger.addtoscreen("Problem Tutorial End", colour="green")
        # Example showing how to source the information
        gui.debugger.addtoscreen("Problem Tutorial Example Start", colour="green")

        # the training example
        if progresstrackermotor.get() == 1:
            # Create an example
            gui.debugger.addtoscreen("Undefined print Function Error", colour="red")
            gui.debugger.addtoscreen("Undefined input Function Error", colour="red")
            gui.debugger.addtoscreen("Undefined checkbatterycharge Function Error", colour="red")
            gui.debugger.addtoscreen("Undefined multiplyarray Function Error", colour="red")
            gui.debugger.addtoscreen("Checking the documentation, we can see that these missing functions are defined in stdiopy, numpy and twirpystoi select these to continue")
            while not(self.comparearray(["stdiopy", "twirpytoi", "numpy"], motorlist)):
                NineChoiceWindow("stdiopy", "GDAL", "twirpytoi", "openlib", "xmlconvert", "csv", "numpy", "powertest", "randbetween")
                if "QUIT" in motorlist:
                    return 1
            progresstrackermotor.set(progresstrackermotor.get() + 1)

        # extra information
        gui.debugger.addtoscreen("Some libaries themselves make use of functions defined in other libaries, which you will therefore also have to include")
        gui.debugger.addtoscreen("This is known as dependencies")

        if progresstrackermotor.get() == 2:
            gui.debugger.addtoscreen("Undefined print Function Error", colour="red")
            gui.debugger.addtoscreen("Undefined input Function Error", colour="red")
            gui.debugger.addtoscreen("Undefined genetricalogithm Function Error", colour="red")
            gui.debugger.addtoscreen("In this example the function \"genetricalogithm\" is defined in a libary called evolve, which itself is dependent on the libary numpy")
            gui.debugger.addtoscreen("To proceed therefore you will need to include the libaries stdiopy, evolve and numpy")
            gui.debugger.addtoscreen("Submit these to continue")
            while not(self.comparearray(["evolve", "stdiopy", "numpy"], motorlist)):
                NineChoiceWindow("stdiopy", "evolve", "twirpytoi", "openlib", "xmlconvert", "csv", "numpy", "powertest", "randbetween")
                if "QUIT" in motorlist:
                    return 1
            progresstrackermotor.set(progresstrackermotor.get() + 1)

        # teach about conflicting libaries
        gui.debugger.addtoscreen("Finally, some libaries can conflict with each other meaning that they both have a function with exactly the same name")
        gui.debugger.addtoscreen("If both libaries are included in the same file. then the computer doesn't know which version of the function to use, and so throws an error")
        gui.debugger.addtoscreen("To solve these problems  you will need to use specialist libaries that have been built to correct this problem, see the documentation for more information")
        gui.debugger.addtoscreen("Training Finished", colour="green")
        gui.debugger.addtoscreen("Debugging Beginning", colour="green")

        # choose a random number to start the actual questions
        progresstrackermotor.set(choice(motorprogressarray))
        # variable to store number completed

        while len(motorprogressarray) > 4:
            if progresstrackermotor.get() == 3:
                gui.debugger.addtoscreen("Undefined checksafetysettings Function Error", colour="red")
                gui.debugger.addtoscreen("Undefined cleararray Function Error", colour="red")

                NineChoiceWindow("stdiopy", "crypto", "twirpytoi", "openlib", "xmlconvert", "csv", "numpy", "gtxtest", "numpycafix")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["stdiopy", "numpycafix", "twirpystoi"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(motorprogressarray) > 4:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    motorprogressarray.remove(3)
                    progresstrackermotor.set(choice(motorprogressarray))
                    overallscore = overallscore + 1
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")
                    progresstrackermotor.set(choice(motorprogressarray))

            if progresstrackermotor.get() == 4:
                gui.debugger.addtoscreen("Undefined readcsv Function Error", colour="red")
                gui.debugger.addtoscreen("Undefined writeline Function Error", colour="red")
                gui.debugger.addtoscreen("Undefined readc Function Error", colour="red")

                NineChoiceWindow("stdiopy", "scrambledOGG", "twirpytoi", "openlib", "xmlconvert", "csv", "numpy", "gtxtest", "crypto")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["csv"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(motorprogressarray) > 4:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    motorprogressarray.remove(4)
                    progresstrackermotor.set(choice(motorprogressarray))
                    overallscore = overallscore + 1
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstrackermotor.get() == 5:
                gui.debugger.addtoscreen("Undefined readcsv Function Error")
                gui.debugger.addtoscreen("Undefined writecsv Function Error")
                gui.debugger.addtoscreen("Undefined print Function Error")
                gui.debugger.addtoscreen("Undefined systemindepentint Function Error")
                gui.debugger.addtoscreen("Undefined checksafetysettings Function Error")

                NineChoiceWindow("stdiopy", "numpy", "twirpytoi", "openlib", "xmlconvert", "csv", "scrambledOGG", "gtxtest", "crypto")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["csv", "stdiopy", "openlib", "twirpystoi"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(motorprogressarray) > 4:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    motorprogressarray.remove(5)
                    progresstrackermotor.set(choice(motorprogressarray))
                    overallscore = overallscore + 1
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstrackermotor.get() == 6:
                gui.debugger.addtoscreen("Undefined guessnext Function Error")
                gui.debugger.addtoscreen("Undefined cleararray Function Error")

                NineChoiceWindow("stdiopy", "numpy", "evolve", "openlib", "xmlconvert", "csv", "json", "numpycafix", "crypto")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["evolve", "stdiopy", "numpycafix", "openlib"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(motorprogressarray) > 4:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    motorprogressarray.remove(6)
                    progresstrackermotor.set(choice(motorprogressarray))
                    overallscore = overallscore + 1
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstrackermotor.get() == 7:
                gui.debugger.addtoscreen("Undefined readcsv Function Error")
                gui.debugger.addtoscreen("Undefined xmlconvert Function Error")

                NineChoiceWindow("stdiopy", "json", "twirpytoi", "openlib", "xmlconvert", "csv", "numpy", "xmlconvert", "crypto")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["csv", "numpy", "xmlconvert"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(motorprogressarray) > 4:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    motorprogressarray.remove(7)
                    progresstrackermotor.set(choice(motorprogressarray))
                    overallscore = overallscore + 1
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstrackermotor.get() == 8:
                gui.debugger.addtoscreen("Undefined calculaterms Function Error")
                gui.debugger.addtoscreen("Undefined systemindepentint Function Error")
                gui.debugger.addtoscreen("Undefined readjson Function Error")

                NineChoiceWindow("openlib", "evolve", "twirpytoi", "scrambledOGG", "xmlconvert", "csv", "numpy", "json", "stdiopy")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["scrambledOGG", "numpy", "openlib", "csv", "stdiopy", "json"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(motorprogressarray) > 4:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    motorprogressarray.remove(8)
                    progresstrackermotor.set(choice(motorprogressarray))
                    overallscore = overallscore + 1
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstrackermotor.get() == 9:
                gui.debugger.addtoscreen("Undefined multiplyarray Function Error")
                gui.debugger.addtoscreen("Undefined print Function Error")
                gui.debugger.addtoscreen("Undefined cleararray Function Error")
                gui.debugger.addtoscreen("Undefined readcsv Function Error")
                gui.debugger.addtoscreen("Undefined csvconvert Function Error")

                NineChoiceWindow("numpycafix", "scrambledOGG", "stdiopy", "openlib", "xmlconvert", "csv", "numpy", "gtxtest", "crypto")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["numpycafix", "stdiopy", "xmlconvert", "csv"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(motorprogressarray) > 4:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    motorprogressarray.remove(9)
                    progresstrackermotor.set(choice(motorprogressarray))
                    overallscore = overallscore + 1
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstrackermotor.get() == 10:
                gui.debugger.addtoscreen("Undefined calculaterms Function Error")
                gui.debugger.addtoscreen("Undefined writeline Function Error")
                gui.debugger.addtoscreen("Undefined xmlconvert Function Error")

                NineChoiceWindow("scrambledOGG", "gtxtest", "twirpytoi", "openlib", "xmlconvert", "csv", "numpy", "numpycafix", "crypto")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["xmlconvert", "scrambledOGG", "numpy"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(motorprogressarray) > 4:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    motorprogressarray.remove(10)
                    progresstrackermotor.set(choice(motorprogressarray))
                    overallscore = overallscore + 1
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstrackermotor.get() == 11:
                gui.debugger.addtoscreen("Undefined decodejson Function Error")
                gui.debugger.addtoscreen("Undefined multiplyarray Function Error")
                gui.debugger.addtoscreen("Undefined print Function Error")


                NineChoiceWindow("json", "numpy", "twirpytoi", "openlib", "xmlconvert", "csv", "scrambledOGG", "stdiopy", "numpycafix")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["numpy", "stdiopy", "json"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(motorprogressarray) > 4:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    motorprogressarray.remove(11)
                    progresstrackermotor.set(choice(motorprogressarray))
                    overallscore = overallscore + 1
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstrackermotor.get() == 12:
                gui.debugger.addtoscreen("Undefined windowspatch Function Error")
                gui.debugger.addtoscreen("Undefined macpatch Function Error")
                gui.debugger.addtoscreen("Undefined calculaterms Function Error")
                gui.debugger.addtoscreen("Undefined readjson Function Error")
                gui.debugger.addtoscreen("Undefined genetricalogithm Function Error")

                NineChoiceWindow("scrambledOGG", "gtxtest", "json", "openlib", "xmlconvert", "csv", "numpy", "evolve", "crypto")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["openlib", "scrambledOGG", "json", "evolve", "numpy", "csv"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(motorprogressarray) > 4:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    motorprogressarray.remove(12)
                    progresstrackermotor.set(choice(motorprogressarray))
                    overallscore = overallscore + 1
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstrackermotor.get() == 13:
                gui.debugger.addtoscreen("Undefined print Function Error")
                gui.debugger.addtoscreen("Undefined input Function Error")
                gui.debugger.addtoscreen("Undefined insert Function Error")
                gui.debugger.addtoscreen("Undefined read Function Error")

                NineChoiceWindow("stdiopy", "numpy", "twirpytoi", "openlib", "xmlconvert", "csv", "scrambledOGG", "gtxtest", "crypto")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["stdiopy"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(motorprogressarray) > 4:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    motorprogressarray.remove(13)
                    progresstrackermotor.set(choice(motorprogressarray))
                    overallscore = overallscore + 1
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstrackermotor.get() == 14:
                gui.debugger.addtoscreen("Undefined evolve Function Error")

                NineChoiceWindow("stdiopy", "GLM", "twirpytoi", "openlib", "scrambledOGG", "csv", "numpy", "gtxtest", "addtoscreen")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["evolve", "numpy", "scrambledOGG"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(motorprogressarray) > 4:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    motorprogressarray.remove(14)
                    progresstrackermotor.set(choice(motorprogressarray))
                    overallscore = overallscore + 1
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstrackermotor.get() == 15:
                gui.debugger.addtoscreen("Undefined writecsv Function Error")
                gui.debugger.addtoscreen("Undefined writeline Function Error")
                gui.debugger.addtoscreen("Undefined writec Function Error")
                gui.debugger.addtoscreen("Undefined systemindepentint Function Error")

                NineChoiceWindow("stdiopy", "numpy", "twirpytoi", "openlib", "scrambledOGG", "csv", "numpy", "gtxtest", "xmlconvert")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["csv", "openlib", "numpy", "stdiopy"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(motorprogressarray) > 4:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    motorprogressarray.remove(15)
                    progresstrackermotor.set(choice(motorprogressarray))
                    overallscore = overallscore + 1
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstrackermotor.get() == 16:
                gui.debugger.addtoscreen("Undefined checkbatterycharge Function Error")
                gui.debugger.addtoscreen("Undefined checksafetysettings Function Error")
                gui.debugger.addtoscreen("Undefined genetricalogithm Function Error")
                gui.debugger.addtoscreen("Undefined transform Function Error")

                NineChoiceWindow("stdiopy", "numpy", "twirpytoi", "openlib", "scrambledOGG", "csv", "numpy", "gtxtest", "xmlconvert")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["twirpystoi", "numpy", "stdiopy", "xmlconvert"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(motorprogressarray) > 4:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    motorprogressarray.remove(16)
                    progresstrackermotor.set(choice(motorprogressarray))
                    overallscore = overallscore + 1
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstrackermotor.get() == 17:
                gui.debugger.addtoscreen("Undefined calculaterms Function Error")
                gui.debugger.addtoscreen("Undefined converttothreephrase Function Error")
                gui.debugger.addtoscreen("Undefined decodejson Function Error")
                gui.debugger.addtoscreen("Undefined transform Function Error")

                NineChoiceWindow("json", "numpy", "numpycafix", "openlib", "scrambledOGG", "csv", "numpy", "gtxtest", "xmlconvert")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["scrambledOGG", "json", "numpycafix", "xmlconvert"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(motorprogressarray) > 4:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    motorprogressarray.remove(17)
                    progresstrackermotor.set(choice(motorprogressarray))
                    overallscore = overallscore + 1
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstrackermotor.get() == 18:
                gui.debugger.addtoscreen("Undefined print Function Error")
                gui.debugger.addtoscreen("Undefined input Function Error")
                gui.debugger.addtoscreen("Undefined cleararray Function Error")

                NineChoiceWindow("json", "numpy", "numpycafix", "openlib", "scrambledOGG", "csv", "numpy", "gtxtest", "stdiopy")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["stdiopy"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(motorprogressarray) > 4:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    motorprogressarray.remove(18)
                    progresstrackermotor.set(choice(motorprogressarray))
                    overallscore = overallscore + 1
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")


        # End of questions
        gui.motorsubsystem.changestatus(newstatus="Status: Online")
        # update the button so that it creates a problem filling it with a random power puzzle
        gui.motorsubsystem.changebuttontext(newtext="Repaired")
        # update the button to now open the power problem window
        gui.motorsubsystem.setcommand("powerproblem")
        # change colour background to green
        gui.motorsubsystem.changebackground("green")
        gui.debugger.addtoscreen("Motor Subsystem Debug Complete", colour="green")

    def changebackground(self, colour):
        if colour == "red":
            self.subsystemframe.configure(background="#870101")
            self.subsystemframetext.configure(background="#870101")
            self.subsystemstatus.configure(background="#870101")
        elif colour == "green":
            self.subsystemframe.configure(background="#256841")
            self.subsystemframetext.configure(background="#256841")
            self.subsystemstatus.configure(background="#256841")
        else:
            self.subsystemframe.configure(background="#7a7a7a")
            self.subsystemframetext.configure(background="#7a7a7a")
            self.subsystemstatus.configure(background="#7a7a7a")

        self.subsystemframe.update()

    def comparearray(self, array1, array2):
        # First check if arrays are of the same length
        if len(array1) != len(array2):
            return False

        # Then check to see if all members of 1 are in 2
        for x in array1:
            if x not in array2:
                return False

        # If arrrving here then pass
        return True

    # AI problem core login puzzle
    def createaiproblemcore(self):
        global response
        global overallscore

        response = StringVar()
        response.set("FALSE")
        gui.debugger.addtoscreen("Begin AI problem Core")
        gui.debugger.addtoscreen("Please note that you will need to require the Twirpy AI Security Credentials document", colour="red")
        gui.debugger.addtoscreen("Please ensure that request form is signed and dated by all team members for confidentuality purposes", colour="red")
        # Create simple top level that requests user name and password
        while True:
            LogInWindow("JamesPotter64","w8T40x0G3I&WsQc")
            if response.get() == "QUIT":
                gui.debugger.addtoscreen("Authentication failed")
                gui.debugger.addtoscreen("Return to main screen")
                return 1
            elif response.get() == "TRUE":
                break
            else:
                gui.debugger.addtoscreen("Authentication failed")
                gui.debugger.addtoscreen("Please provide your authentication details")

        # End of login
        gui.debugger.addtoscreen("Submitting user provided credentials")
        gui.debugger.addtoscreen("Hashing")
        gui.debugger.addtoscreen("Security Credentials Accepted")
        gui.aisubsystem.changestatus(newstatus="Status: Online")
        # update the button so that it creates a problem filling it with a random power puzzle
        gui.aisubsystem.changebuttontext(newtext="Repaired")
        # update the button to now open the power problem window
        gui.aisubsystem.setcommand("pass")
        # change colour background to green
        gui.aisubsystem.changebackground("green")
        overallscore = overallscore + 1

    # bluetooth code map problem
    def createbluetoothproblemcore(self):
        global bluetoothanswer
        global progresstrackerblue
        global bluetoothprogressarray
        global overallscore

        bluetoothanswer = StringVar()
        bluetoothanswer.set("FALSE")

        # While loop to continue asking questions till done
        while True:
            # if first time in here then show the tutorial
            if progresstrackerblue.get() == 0:
                # choose random question to start on
                # Tutorial explaining how to make use of the map
                gui.debugger.addtoscreen("The bluetooth systems have an inbuilt error code reporting system")
                gui.debugger.addtoscreen("To make use of this system you will need to request document BlueErrorMap version 3.74", colour="red")
                gui.debugger.addtoscreen("Follow the instructions on the document to input the correct response to fix the problem")
                gui.debugger.addtoscreen("Each time you are given an error code, remember to return to the Start")
                gui.debugger.addtoscreen("Begin error code correction")
                # End of tutorial begin bug fixing
                bluetoothprogressarray.remove(0)
                progresstrackerblue.set(choice(bluetoothprogressarray))

            # Question 1
            elif progresstrackerblue.get() == 1:
                # If all questions asked
                if len(bluetoothprogressarray) < 2:
                    break
                # Stage 1
                gui.debugger.addtoscreen("Error Code 8875", colour="red")
                gui.debugger.addtoscreen("Connection Strength: 74", colour="red")
                gui.debugger.addtoscreen("System Status: Offline", colour="red")
                gui.debugger.addtoscreen("Security System Status: Offline", colour="red")
                BluetoothBox()
                if bluetoothanswer.get() == "QUIT":
                    return 1
                # Correct answer condition
                elif bluetoothanswer.get() == "PURGE":
                    gui.debugger.addtoscreen("System Purge accepted, proceeding")
                    # stage 2
                    gui.debugger.addtoscreen("Error Code 4875", colour="red")
                    gui.debugger.addtoscreen("Connection Strength: 32", colour="red")
                    gui.debugger.addtoscreen("System Status: Offline", colour="red")
                    gui.debugger.addtoscreen("Security System Status: Online", colour="red")
                    BluetoothBox()
                    if bluetoothanswer.get() == "QUIT":
                        break
                    # Correct answer condition
                    elif bluetoothanswer.get() == "RESET":
                        gui.debugger.addtoscreen("System Reset accepted, proceeding")
                        # Stage 3
                        gui.debugger.addtoscreen("Error Code 4815", colour="red")
                        gui.debugger.addtoscreen("Connection Strength: 45", colour="red")
                        gui.debugger.addtoscreen("System Status: Online", colour="red")
                        gui.debugger.addtoscreen("Security System Status: Online", colour="red")
                        BluetoothBox()
                        if bluetoothanswer.get() == "QUIT":
                            return 1
                        # Correct answer condition
                        elif bluetoothanswer.get() == "1756":
                            gui.debugger.addtoscreen("Code accepted, proceeding")
                            # if reaching here success
                            gui.debugger.addtoscreen("Problem Corrected System Online", colour="green")
                            bluetoothprogressarray.remove(1)
                            progresstrackerblue.set(choice(bluetoothprogressarray))
                            overallscore = overallscore + 1
                        else:
                            gui.debugger.addtoscreen("System Failure, moving to next problem")
                            progresstrackerblue.set(choice(bluetoothprogressarray))

                    else:
                        gui.debugger.addtoscreen("System Failure, moving to next problem")
                        progresstrackerblue.set(choice(bluetoothprogressarray))

                else:
                    gui.debugger.addtoscreen("System Failure, moving to next problem")
                    progresstrackerblue.set(choice(bluetoothprogressarray))

            # Question 2
            elif progresstrackerblue.get() == 2:
                if len(bluetoothprogressarray) < 2:
                    break
                # Stage 1
                gui.debugger.addtoscreen("Error Code 1111", colour="red")
                gui.debugger.addtoscreen("Connection Strength: 0", colour="red")
                gui.debugger.addtoscreen("System Status: Offline", colour="red")
                gui.debugger.addtoscreen("Security System Status: Offline", colour="red")
                BluetoothBox()
                if bluetoothanswer.get() == "QUIT":
                    return 1
                # Correct answer condition
                elif bluetoothanswer.get() == "3712":
                    gui.debugger.addtoscreen("Code accepted, proceeding")
                    # Stage 2
                    gui.debugger.addtoscreen("Error Code 8111", colour="red")
                    gui.debugger.addtoscreen("Connection Strength: 3", colour="red")
                    gui.debugger.addtoscreen("System Status: Online", colour="red")
                    gui.debugger.addtoscreen("Security System Status: Offline", colour="red")
                    BluetoothBox()
                    if bluetoothanswer.get() == "QUIT":
                        return 1
                    # Correct answer condition
                    elif bluetoothanswer.get() == "PURGE":
                        gui.debugger.addtoscreen("System Purge Accepted, proceeding")
                        # Stage 3
                        gui.debugger.addtoscreen("Error Code 8733", colour="red")
                        gui.debugger.addtoscreen("Connection Strength: 0", colour="red")
                        gui.debugger.addtoscreen("System Status: Online", colour="red")
                        gui.debugger.addtoscreen("Security System Status: Online", colour="red")
                        BluetoothBox()
                        if bluetoothanswer.get() == "QUIT":
                            return 1
                        # Correct answer condition
                        elif bluetoothanswer.get() == "PURGE":
                            gui.debugger.addtoscreen("System Purge accepted, proceeding")
                            # Stage 4
                            gui.debugger.addtoscreen("Error Code 4803", colour="red")
                            gui.debugger.addtoscreen("Connection Strength: 50", colour="red")
                            gui.debugger.addtoscreen("System Status: Online", colour="red")
                            gui.debugger.addtoscreen("Security System Status: Online", colour="red")
                            BluetoothBox()
                            if bluetoothanswer.get() == "QUIT":
                                return 1
                            # Correct answer condition
                            elif bluetoothanswer.get() == "RESET":
                                gui.debugger.addtoscreen("System Reset accepted, proceeding")
                                # Stage 5
                                gui.debugger.addtoscreen("Error Code 5803", colour="red")
                                gui.debugger.addtoscreen("Connection Strength: 50", colour="red")
                                gui.debugger.addtoscreen("System Status: Online", colour="red")
                                gui.debugger.addtoscreen("Security System Status: Online", colour="red")
                                BluetoothBox()
                                if bluetoothanswer.get() == "QUIT":
                                    return 1
                                # Correct answer condition
                                elif bluetoothanswer.get() == "7666":
                                    gui.debugger.addtoscreen("Code accepted, proceeding")
                                    gui.debugger.addtoscreen("Problem Corrected System Online", colour="green")
                                    bluetoothprogressarray.remove(2)
                                    progresstrackerblue.set(choice(bluetoothprogressarray))
                                    overallscore = overallscore + 1
                                else:
                                    gui.debugger.addtoscreen("System Failure, moving to next problem")
                                    progresstrackerblue.set(choice(bluetoothprogressarray))

                            else:
                                gui.debugger.addtoscreen("System Failure, moving to next problem")
                                progresstrackerblue.set(choice(bluetoothprogressarray))

                        else:
                            gui.debugger.addtoscreen("System Failure, moving to next problem")
                            progresstrackerblue.set(choice(bluetoothprogressarray))

                    else:
                        gui.debugger.addtoscreen("System Failure, moving to next problem")
                        progresstrackerblue.set(choice(bluetoothprogressarray))

                else:
                    gui.debugger.addtoscreen("System Failure, moving to next problem")
                    progresstrackerblue.set(choice(bluetoothprogressarray))

            # Question 3
            elif progresstrackerblue.get() == 3:
                if len(bluetoothprogressarray) < 2:
                    break
                # Stage 1
                gui.debugger.addtoscreen("Error Code 7006", colour="red")
                gui.debugger.addtoscreen("Connection Strength: 0", colour="red")
                gui.debugger.addtoscreen("System Status: Offline", colour="red")
                gui.debugger.addtoscreen("Security System Status: Offline", colour="red")
                BluetoothBox()
                if bluetoothanswer.get() == "QUIT":
                    return 1
                # Correct answer condition
                elif bluetoothanswer.get() == "4544":
                    gui.debugger.addtoscreen("Code accepted, proceeding")
                    # Stage 2
                    gui.debugger.addtoscreen("Error Code 7511", colour="red")
                    gui.debugger.addtoscreen("Connection Strength: 0", colour="red")
                    gui.debugger.addtoscreen("System Status: Online", colour="red")
                    gui.debugger.addtoscreen("Security System Status: Offline", colour="red")
                    BluetoothBox()
                    if bluetoothanswer.get() == "QUIT":
                        return 1
                    # Correct answer condition
                    elif bluetoothanswer.get() == "7666":
                        gui.debugger.addtoscreen("Code accepted, proceeding")
                        # Stage 3
                        gui.debugger.addtoscreen("Error Code 7061", colour="red")
                        gui.debugger.addtoscreen("Connection Strength: 0", colour="red")
                        gui.debugger.addtoscreen("System Status: Online", colour="red")
                        gui.debugger.addtoscreen("Security System Status: Online", colour="red")
                        BluetoothBox()
                        if bluetoothanswer.get() == "QUIT":
                            return 1
                        # Correct answer condition
                        elif bluetoothanswer.get() == "PURGE":
                            gui.debugger.addtoscreen("System Purge Accepted, proceeding")
                            # Stage 4
                            gui.debugger.addtoscreen("Error Code 4411", colour="red")
                            gui.debugger.addtoscreen("Connection Strength: 34", colour="red")
                            gui.debugger.addtoscreen("System Status: Online", colour="red")
                            gui.debugger.addtoscreen("Security System Status: Online", colour="red")
                            BluetoothBox()
                            if bluetoothanswer.get() == "QUIT":
                                return 1
                            # Correct answer condition
                            elif bluetoothanswer.get() == "RESET":
                                gui.debugger.addtoscreen("System Reset Accepted, proceeding")
                                # Stage 5
                                gui.debugger.addtoscreen("Error Code 6104", colour="red")
                                gui.debugger.addtoscreen("Connection Strength: 34", colour="red")
                                gui.debugger.addtoscreen("System Status: Online", colour="red")
                                gui.debugger.addtoscreen("Security System Status: Online", colour="red")
                                BluetoothBox()
                                if bluetoothanswer.get() == "QUIT":
                                    return 1
                                # Correct answer condition
                                elif bluetoothanswer.get() == "7442":
                                    gui.debugger.addtoscreen("Code Accepted, proceeding")
                                    # Success
                                    gui.debugger.addtoscreen("Problem Corrected System Online", colour="green")
                                    bluetoothprogressarray.remove(3)
                                    progresstrackerblue.set(choice(bluetoothprogressarray))
                                    overallscore = overallscore + 1
                                else:
                                    gui.debugger.addtoscreen("System Failure, moving to next problem")
                                    progresstrackerblue.set(choice(bluetoothprogressarray))
                            else:
                                gui.debugger.addtoscreen("System Failure, moving to next problem")
                                progresstrackerblue.set(choice(bluetoothprogressarray))
                        else:
                            gui.debugger.addtoscreen("System Failure, moving to next problem")
                            progresstrackerblue.set(choice(bluetoothprogressarray))
                    else:
                        gui.debugger.addtoscreen("System Failure, moving to next problem")
                        progresstrackerblue.set(choice(bluetoothprogressarray))
                else:
                    gui.debugger.addtoscreen("System Failure, moving to next problem")
                    progresstrackerblue.set(choice(bluetoothprogressarray))

            # Question 4
            elif progresstrackerblue.get() == 4:
                if len(bluetoothprogressarray) < 2:
                    break
                # Stage 1
                gui.debugger.addtoscreen("Error Code 1999", colour="red")
                gui.debugger.addtoscreen("Connection Strength: 0", colour="red")
                gui.debugger.addtoscreen("System Status: Offline", colour="red")
                gui.debugger.addtoscreen("Security System Status: Online", colour="red")
                BluetoothBox()
                if bluetoothanswer.get() == "QUIT":
                    return 1
                # Correct answer condition
                elif bluetoothanswer.get() == "3712":
                    gui.debugger.addtoscreen("Code Accepted, proceeding")
                    # Stage 2
                    gui.debugger.addtoscreen("Error Code 4809", colour="red")
                    gui.debugger.addtoscreen("Connection Strength: 50", colour="red")
                    gui.debugger.addtoscreen("System Status: Offline", colour="red")
                    gui.debugger.addtoscreen("Security System Status: Online", colour="red")
                    BluetoothBox()
                    if bluetoothanswer.get() == "QUIT":
                        return 1
                    # Correct answer condition
                    elif bluetoothanswer.get() == "RESET":
                        gui.debugger.addtoscreen("System Reset Accepted, proceeding")
                        # Stage 3
                        gui.debugger.addtoscreen("Error Code 7137", colour="red")
                        gui.debugger.addtoscreen("Connection Strength: 50", colour="red")
                        gui.debugger.addtoscreen("System Status: Offline", colour="red")
                        gui.debugger.addtoscreen("Security System Status: Offline", colour="red")
                        BluetoothBox()
                        if bluetoothanswer.get() == "QUIT":
                            return 1
                        # Correct answer condition
                        elif bluetoothanswer.get() == "3279":
                            gui.debugger.addtoscreen("Code Accepted, proceeding")
                            gui.debugger.addtoscreen("Problem Corrected System Online", colour="green")
                            bluetoothprogressarray.remove(4)
                            progresstrackerblue.set(choice(bluetoothprogressarray))
                            overallscore = overallscore + 1
                        else:
                            gui.debugger.addtoscreen("System Failure, moving to next problem")
                            progresstrackerblue.set(choice(bluetoothprogressarray))
                    else:
                        gui.debugger.addtoscreen("System Failure, moving to next problem")
                        progresstrackerblue.set(choice(bluetoothprogressarray))
                else:
                    gui.debugger.addtoscreen("System Failure, moving to next problem")
                    progresstrackerblue.set(choice(bluetoothprogressarray))

            # Question 5
            elif progresstrackerblue.get() == 5:
                if len(bluetoothprogressarray) < 2:
                    break
                # Stage 1
                gui.debugger.addtoscreen("Error Code 5143", colour="red")
                gui.debugger.addtoscreen("Connection Strength: 0", colour="red")
                gui.debugger.addtoscreen("System Status: Online", colour="red")
                gui.debugger.addtoscreen("Security System Status: Online", colour="red")
                BluetoothBox()
                if bluetoothanswer.get() == "QUIT":
                    return 1
                # Correct answer condition
                elif bluetoothanswer.get() == "CONNECT":
                    gui.debugger.addtoscreen("System Connect Accepted, proceeding")
                    gui.debugger.addtoscreen("Problem Corrected System Online", colour="green")
                    bluetoothprogressarray.remove(5)
                    progresstrackerblue.set(choice(bluetoothprogressarray))
                    overallscore = overallscore + 1
                else:
                    gui.debugger.addtoscreen("System Failure, moving to next problem")
                    progresstrackerblue.set(choice(bluetoothprogressarray))

            # Question 6
            elif progresstrackerblue.get() == 6:
                if len(bluetoothprogressarray) < 2:
                    break
                # Stage 1
                gui.debugger.addtoscreen("Error Code 6095", colour="red")
                gui.debugger.addtoscreen("Connection Strength: 0", colour="red")
                gui.debugger.addtoscreen("System Status: Online", colour="red")
                gui.debugger.addtoscreen("Security System Status: Online", colour="red")
                BluetoothBox()
                if bluetoothanswer.get() == "QUIT":
                    return 1
                # Correct answer condition
                elif bluetoothanswer.get() == "3333":
                    gui.debugger.addtoscreen("Code Accepted, proceeding")
                    # Stage 2
                    gui.debugger.addtoscreen("Error Code 5311", colour="red")
                    gui.debugger.addtoscreen("Connection Strength: 0", colour="red")
                    gui.debugger.addtoscreen("System Status: Online", colour="red")
                    gui.debugger.addtoscreen("Security System Status: Online", colour="red")
                    BluetoothBox()
                    if bluetoothanswer.get() == "QUIT":
                        return 1
                    # Correct answer condition
                    elif bluetoothanswer.get() == "7666":
                        gui.debugger.addtoscreen("Code Accepted, proceeding")
                        # Stage 3
                        gui.debugger.addtoscreen("Error Code 8112", colour="red")
                        gui.debugger.addtoscreen("Connection Strength: 0", colour="red")
                        gui.debugger.addtoscreen("System Status: Online", colour="red")
                        gui.debugger.addtoscreen("Security System Status: Online", colour="red")
                        BluetoothBox()
                        if bluetoothanswer.get() == "QUIT":
                            return 1
                        # Correct answer condition
                        elif bluetoothanswer.get() == "PURGE":
                            gui.debugger.addtoscreen("System Purge Accepted, proceeding")
                            # Stage 4
                            gui.debugger.addtoscreen("Error Code 6196", colour="red")
                            gui.debugger.addtoscreen("Connection Strength: 0", colour="red")
                            gui.debugger.addtoscreen("System Status: Online", colour="red")
                            gui.debugger.addtoscreen("Security System Status: Online", colour="red")
                            BluetoothBox()
                            if bluetoothanswer.get() == "QUIT":
                                return 1
                            # Correct answer condition
                            elif bluetoothanswer.get() == "CONNECT":
                                gui.debugger.addtoscreen("System Connect Accepted, proceeding")
                                gui.debugger.addtoscreen("Problem Corrected System Online", colour="green")
                                bluetoothprogressarray.remove(6)
                                progresstrackerblue.set(choice(bluetoothprogressarray))
                                overallscore = overallscore + 1
                            else:
                                gui.debugger.addtoscreen("System Failure, moving to next problem")
                                progresstrackerblue.set(choice(bluetoothprogressarray))
                        else:
                            gui.debugger.addtoscreen("System Failure, moving to next problem")
                            progresstrackerblue.set(choice(bluetoothprogressarray))
                    else:
                        gui.debugger.addtoscreen("System Failure, moving to next problem")
                        progresstrackerblue.set(choice(bluetoothprogressarray))
                else:
                    gui.debugger.addtoscreen("System Failure, moving to next problem")
                    progresstrackerblue.set(choice(bluetoothprogressarray))

            # Question 7
            elif progresstrackerblue.get() == 7:
                if len(bluetoothprogressarray) < 2:
                    break
                # Stage 1
                gui.debugger.addtoscreen("Error Code 5129", colour="red")
                gui.debugger.addtoscreen("Connection Strength: 0", colour="red")
                gui.debugger.addtoscreen("System Status: Online", colour="red")
                gui.debugger.addtoscreen("Security System Status: Online", colour="red")
                BluetoothBox()
                if bluetoothanswer.get() == "QUIT":
                    return 1
                # Correct answer condition
                elif bluetoothanswer.get() == "4544":
                    gui.debugger.addtoscreen("Code Accepted, proceeding")
                    # Stage 2
                    gui.debugger.addtoscreen("Error Code 7297", colour="red")
                    gui.debugger.addtoscreen("Connection Strength: 0", colour="red")
                    gui.debugger.addtoscreen("System Status: Online", colour="red")
                    gui.debugger.addtoscreen("Security System Status: Online", colour="red")
                    BluetoothBox()
                    if bluetoothanswer.get() == "QUIT":
                        return 1
                    # Correct answer condition
                    elif bluetoothanswer.get() == "6786":
                        gui.debugger.addtoscreen("Code Accepted, proceeding")
                        # Stage 3
                        gui.debugger.addtoscreen("Error Code 8456", colour="red")
                        gui.debugger.addtoscreen("Connection Strength: 0", colour="red")
                        gui.debugger.addtoscreen("System Status: Online", colour="red")
                        gui.debugger.addtoscreen("Security System Status: Online", colour="red")
                        BluetoothBox()
                        if bluetoothanswer.get() == "QUIT":
                            return 1
                        # Correct answer condition
                        elif bluetoothanswer.get() == "PURGE":
                            gui.debugger.addtoscreen("System Purge Accepted, proceeding")
                            gui.debugger.addtoscreen("Problem Corrected System Online", colour="green")
                            bluetoothprogressarray.remove(7)
                            progresstrackerblue.set(choice(bluetoothprogressarray))
                            overallscore = overallscore + 1
                        else:
                            gui.debugger.addtoscreen("System Failure, moving to next problem")
                            progresstrackerblue.set(choice(bluetoothprogressarray))
                    else:
                        gui.debugger.addtoscreen("System Failure, moving to next problem")
                        progresstrackerblue.set(choice(bluetoothprogressarray))
                else:
                    gui.debugger.addtoscreen("System Failure, moving to next problem")
                    progresstrackerblue.set(choice(bluetoothprogressarray))

            # Question 8
            elif progresstrackerblue.get() == 8:
                if len(bluetoothprogressarray) < 2:
                    break
                # Stage 1
                gui.debugger.addtoscreen("Error Code 1345", colour="red")
                gui.debugger.addtoscreen("Connection Strength: 0", colour="red")
                gui.debugger.addtoscreen("System Status: Online", colour="red")
                gui.debugger.addtoscreen("Security System Status: Online", colour="red")
                BluetoothBox()
                if bluetoothanswer.get() == "QUIT":
                    return 1
                # Correct answer condition
                elif bluetoothanswer.get() == "3712":
                    gui.debugger.addtoscreen("System Code Accepted, proceeding")
                    gui.debugger.addtoscreen("Problem Corrected System Online", colour="green")
                    bluetoothprogressarray.remove(8)
                    progresstrackerblue.set(choice(bluetoothprogressarray))
                    overallscore = overallscore + 1
                else:
                    gui.debugger.addtoscreen("System Failure, moving to next problem")
                    progresstrackerblue.set(choice(bluetoothprogressarray))

            # Question 9
            elif progresstrackerblue.get() == 9:
                if len(bluetoothprogressarray) < 2:
                    break
                # Stage 1
                gui.debugger.addtoscreen("Error Code 5013", colour="red")
                gui.debugger.addtoscreen("Connection Strength: 0", colour="red")
                gui.debugger.addtoscreen("System Status: Online", colour="red")
                gui.debugger.addtoscreen("Security System Status: Online", colour="red")
                BluetoothBox()
                if bluetoothanswer.get() == "QUIT":
                    return 1
                # Correct answer condition
                elif bluetoothanswer.get() == "4544":
                    gui.debugger.addtoscreen("System Code Accepted, proceeding")
                    # Stage 2
                    gui.debugger.addtoscreen("Error Code 4643", colour="red")
                    gui.debugger.addtoscreen("Connection Strength: 0", colour="red")
                    gui.debugger.addtoscreen("System Status: Online", colour="red")
                    gui.debugger.addtoscreen("Security System Status: Online", colour="red")
                    BluetoothBox()
                    if bluetoothanswer.get() == "QUIT":
                        return 1
                    # Correct answer condition
                    elif bluetoothanswer.get() == "RESET":
                        gui.debugger.addtoscreen("System Reset Accepted, proceeding")
                        # Stage 3
                        gui.debugger.addtoscreen("Error Code 4413", colour="red")
                        gui.debugger.addtoscreen("Connection Strength: 0", colour="red")
                        gui.debugger.addtoscreen("System Status: Online", colour="red")
                        gui.debugger.addtoscreen("Security System Status: Online", colour="red")
                        BluetoothBox()
                        if bluetoothanswer.get() == "QUIT":
                            return 1
                        # Correct answer condition
                        elif bluetoothanswer.get() == "RESET":
                            gui.debugger.addtoscreen("System Reset Accepted, proceeding")
                            gui.debugger.addtoscreen("Problem Corrected System Online", colour="green")
                            bluetoothprogressarray.remove(9)
                            progresstrackerblue.set(choice(bluetoothprogressarray))
                            overallscore = overallscore + 1
                        else:
                            gui.debugger.addtoscreen("System Failure, moving to next problem")
                            progresstrackerblue.set(choice(bluetoothprogressarray))
                    else:
                        gui.debugger.addtoscreen("System Failure, moving to next problem")
                        progresstrackerblue.set(choice(bluetoothprogressarray))
                else:
                    gui.debugger.addtoscreen("System Failure, moving to next problem")
                    progresstrackerblue.set(choice(bluetoothprogressarray))


        # If getting here then exercise is finished
        gui.debugger.addtoscreen("Success")
        # update success
        gui.bluetoothsubsystem.changestatus(newstatus="Status: Online")
        # update the button so that it creates a problem filling it with a random power puzzle
        gui.bluetoothsubsystem.changebuttontext(newtext="Repaired")
        # update the button to now open the power problem window
        gui.bluetoothsubsystem.setcommand("pass")
        # change colour background to green
        gui.bluetoothsubsystem.changebackground("green")

    # safety problems
    def createsafeproblemcore(self):
        gui.debugger.addtoscreen("Begin safety subsystem problem Core")

    # Control problem core login puzzle
    def createcontrolproblemcore(self):
        global response
        global overallscore

        response = StringVar()
        response.set("FALSE")
        gui.debugger.addtoscreen("Begin Control problem Core")
        gui.debugger.addtoscreen("Please note that you will need to require the Twirpy Control Security Credentials document", colour="red")
        gui.debugger.addtoscreen("Please ensure that request form is signed and dated by all team members for confidentuality purposes", colour="red")
        # Create simple top level that requests user name and password
        while True:
            AlternativeLogInWindow("JamesP94", "IAmTheGreatest", "' or '1'='1'")
            if response.get() == "QUIT":
                gui.debugger.addtoscreen("Authentication failed")
                gui.debugger.addtoscreen("Return to main screen")
                return 1
            elif response.get() == "TRUE":
                break
            elif response.get() == "ALTERNATE":
                # print the table of revealed information here
                gui.debugger.addtoscreen("############")
                gui.debugger.addtoscreen("############")
                gui.debugger.addtoscreen("############")
                gui.debugger.addtoscreen("############")
                gui.debugger.addtoscreen("############")
                gui.debugger.addtoscreen("############")
                gui.debugger.addtoscreen("############")
                gui.debugger.addtoscreen("############")
                gui.debugger.addtoscreen("############")
                gui.debugger.addtoscreen("############")
                gui.debugger.addtoscreen("############")
                gui.debugger.addtoscreen("############")
                gui.debugger.addtoscreen("SQL Statement Detected Submitting...")
                gui.debugger.addtoscreen("SELECT UserId, Name, Password FROM Users WHERE UserId = ':INPUT' or '1'='1';")
                gui.debugger.addtoscreen("TABLE ID: Users")
                gui.debugger.addtoscreen("Column: ID|UserName|Password|ClearanceLevel", colour="red")
                gui.debugger.addtoscreen("row: 0|LiamT567|password1234|0")
                gui.debugger.addtoscreen("row: 1|MaxF4224|qwerty|1")
                gui.debugger.addtoscreen("row: 2|JoshF11|ilovedogs|0")
                gui.debugger.addtoscreen("row: 3|SophieP87|sophie91|0")
                gui.debugger.addtoscreen("row: 4|AndrewJ69|password|0")
                gui.debugger.addtoscreen("row: 5|AlexGA91|ccjUL6hwtF|0")
                gui.debugger.addtoscreen("row: 6|MikeG13|glaciersRcool|0")
                gui.debugger.addtoscreen("row: 7|JamesP94|IAmTheGreatest|2")
                gui.debugger.addtoscreen("row: 8|Sally1234|N5uFsBJ5YG|0")
                gui.debugger.addtoscreen("row: 9|Lewis89|rPmdt8pCNv|0")
                gui.debugger.addtoscreen("row: 10|Richard4ever|1234password5678|0")
                gui.debugger.addtoscreen("row: 11|Steph13|mypassword|0")
                gui.debugger.addtoscreen("row: 12|Elliot45|Elliot45|0")
                gui.debugger.addtoscreen("row: 13|Emily1|3112000|0")
                gui.debugger.addtoscreen("row: 14|Tristian1002|8wPz9kV2J6|0")
                gui.debugger.addtoscreen("row: 15|Rachel31|Xbe2P79CTM|0")
                gui.debugger.addtoscreen("row: 16|Leslie13|Xbe2P79CTM|0")
                gui.debugger.addtoscreen("row: 16|Johanna42|Xbe2P79CTM|0")
                return 1
            else:
                gui.debugger.addtoscreen("Authentication failed")
                gui.debugger.addtoscreen("Please provide your authentication details")

        # End of login
        gui.debugger.addtoscreen("Submitting user provided credentials")
        gui.debugger.addtoscreen("Login Successful", colour="green")
        gui.debugger.addtoscreen("Reporting success", colour="green")
        gui.controlsubsystem.changestatus(newstatus="Status: Online")
        # update the button so that it creates a problem filling it with a random power puzzle
        gui.controlsubsystem.changebuttontext(newtext="Repaired")
        # update the button to now open the power problem window
        gui.controlsubsystem.setcommand("pass")
        # change colour background to green
        gui.controlsubsystem.changebackground("green")
        overallscore = overallscore + 1

    # stabilisation problem core problem set
    def stabilisationproblemcore(self):
        global progresstrackerstable
        global overallscore
        global stabilisationAnswer
        global stabilisationprogressarray

        stabilisationAnswer = StringVar()

        # Problem Tutorial
        # While loop to continue asking questions till done
        while True:
            # Teaching basic select
            if progresstrackerstable.get() == 0:
                gui.debugger.addtoscreen("Stabilisation Problem Tutorial Start", colour="green")
                gui.debugger.addtoscreen("Please note to solve these problems you will need to request the SQL_Tables document from stores", colour="green")
                gui.debugger.addtoscreen("The Control and Stabilisation Subsystems are held within relational databases which can be queried using Structured Query Language", colour="green")
                gui.debugger.addtoscreen("Commonly referred to as SQL", colour="green")
                gui.debugger.addtoscreen("This training will provide you with a basic understanding of key SQL commands and will ask you to retrieve data and build queries", colour="green")
                gui.debugger.addtoscreen("Training Start", colour="green")
                gui.debugger.addtoscreen("Part One Select Queries", colour="green")
                gui.debugger.addtoscreen("Data is retrieved from TABLES using the SELECT command", colour="green")
                gui.debugger.addtoscreen("A generalised example is: ", colour="green")
                gui.debugger.addtoscreen("SELECT column, another column FROM table", colour="green")
                gui.debugger.addtoscreen("Therefore to select colours from the Training Table you would use", colour="green")
                gui.debugger.addtoscreen("SELECT colours FROM TrainingTable", colour="green")
                gui.debugger.addtoscreen("To continue select the command that would retrieve the numbers column from the TrainingTable")
                while stabilisationAnswer.get() != "SELECT numbers FROM TrainingTable":
                    stabilisationProblemCoreWindow(question="Choose the appropriate SQL command to retrieve the requested information",
                                                   option1="SELECT numbers FROM TrainingTable",
                                                   option2="SELECT id FROM TrainingTable",
                                                   option3="SELECT colours FROM TrainingTable")
                    if stabilisationAnswer.get() == "QUIT":
                        gui.debugger.addtoscreen("Training Quit", colour="red")
                        return 1
                    elif stabilisationAnswer.get() != "SELECT numbers FROM TrainingTable":
                        gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                    else:
                        gui.debugger.addtoscreen("Correct SQL statement chosen ", colour="green")
                        gui.debugger.addtoscreen("... ", colour="green")
                        gui.debugger.addtoscreen("Data Retrieval Successful", colour="green")
                        gui.debugger.addtoscreen("Continuing training", colour="green")
                        progresstrackerstable.set(progresstrackerstable.get() + 1)

            if progresstrackerstable.get() == 1:
                # selecting rows
                gui.debugger.addtoscreen("Particular rows can be selected by making use of the WHERE keyword to filter the columns", colour="green")
                gui.debugger.addtoscreen("A generalised example of this is: ", colour="green")
                gui.debugger.addtoscreen("SELECT column, another column FROM Table WHERE condition", colour="green")
                gui.debugger.addtoscreen("For example to select all people called Max in TrainingTableOne", colour="green")
                gui.debugger.addtoscreen("SELECT name FROM TrainingTableOne WHERE name == 'MAX'", colour="green")
                gui.debugger.addtoscreen("To continue select the command that would retrieve all people from TrainingTableOne who are less than or equal to fifty years old")
                while stabilisationAnswer.get() != "SELECT name FROM TrainingTableOne WHERE age <= 50":
                    stabilisationProblemCoreWindow(question="Choose the appropriate SQL command to retrieve the requested information",
                                                   option1="SELECT name FROM TrainingTableOne",
                                                   option2="SELECT name FROM TrainingTableOne WHERE age < 50",
                                                   option3="SELECT name FROM TrainingTableOne WHERE age <= 50")
                    if stabilisationAnswer.get() == "QUIT":
                        gui.debugger.addtoscreen("Training Quit", colour="red")
                        return 1
                    elif stabilisationAnswer.get() != "SELECT name FROM TrainingTableOne WHERE age <= 50":
                        gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                    else:
                        gui.debugger.addtoscreen("Correct SQL statement chosen ", colour="green")
                        gui.debugger.addtoscreen("... ", colour="green")
                        gui.debugger.addtoscreen("Data Retrieval Successful", colour="green")
                        gui.debugger.addtoscreen("Continuing training", colour="green")
                        progresstrackerstable.set(progresstrackerstable.get() + 1)

            if progresstrackerstable.get() == 2:
                # multiple SQL where conditions
                gui.debugger.addtoscreen("Multiple rows and multiple conditions can be used to narrow down search results", colour="green")
                gui.debugger.addtoscreen("Boolean operators AND OR NOT can be used to create more complicated searches", colour="green")
                gui.debugger.addtoscreen("The generalised form is then", colour="green")
                gui.debugger.addtoscreen("SELECT column(s) FROM Table WHERE condition(s)", colour="green")
                gui.debugger.addtoscreen("For example to select all movies that were released after 2010, that had a rating greater that 4.5 you would use", colour="green")
                gui.debugger.addtoscreen("SELECT movie_title FROM TrainingTableTwo WHERE year_released > 2010 AND audience_rating > 4.5", colour="green")
                gui.debugger.addtoscreen("To continue select the command that would retrieve all movies from TrainingTableTwo which have an audience rating of less than 4.5")
                gui.debugger.addtoscreen("or which were produced in 2010")
                while stabilisationAnswer.get() != "SELECT movie_title FROM TrainingTableTwo WHERE audience_rating < 4.5 OR year_released == 2010":
                    stabilisationProblemCoreWindow(question="Choose the appropriate SQL command to retrieve the requested information",
                                                   option1="SELECT movie_title FROM TrainingTableTwo WHERE audience_rating < 4.5 OR year_released != 2010",
                                                   option2="SELECT movie_title FROM TrainingTableTwo WHERE audience_rating > 4.5 OR year_released == 2010",
                                                   option3="SELECT movie_title FROM TrainingTableTwo WHERE audience_rating < 4.5 OR year_released == 2010")
                    if stabilisationAnswer.get() == "QUIT":
                        gui.debugger.addtoscreen("Training Quit", colour="red")
                        return 1
                    elif stabilisationAnswer.get() != "SELECT movie_title FROM TrainingTableTwo WHERE audience_rating < 4.5 OR year_released == 2010":
                        gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                    else:
                        gui.debugger.addtoscreen("Correct SQL statement chosen ", colour="green")
                        gui.debugger.addtoscreen("... ", colour="green")
                        gui.debugger.addtoscreen("Data Retrieval Successful", colour="green")
                        gui.debugger.addtoscreen("Continuing training", colour="green")
                        progresstrackerstable.set(progresstrackerstable.get() + 1)

            if progresstrackerstable.get() == 3:
                # simple joins
                gui.debugger.addtoscreen("As you can see in TrainingTableTwo when you have multiple directors per film, the table quickly gets very long", colour="green")
                gui.debugger.addtoscreen("If we were to add a new column which was audience rating another source then the table size would double", colour="green")
                gui.debugger.addtoscreen("Therefore to stop tables becoming huge information is often split into mulitple tables and then joined together when needed to save space and increase performance", colour="green")
                gui.debugger.addtoscreen("A JOIN clause is used to combine rows from two or more tables, based on a related column between them", colour="green")
                gui.debugger.addtoscreen("This takes the general form of:", colour="green")
                gui.debugger.addtoscreen("SELECT columns FROM TABLE INNER JOIN Table1Column=Table2Column WHERE constraints", colour="green")
                gui.debugger.addtoscreen("If for instance we want to get all the customer name attached to OrderID 10308 then we would use:", colour="green")
                gui.debugger.addtoscreen("SELECT ORDERID, CustomerID, CustomerName FROM TrainingTableThree INNER JOIN TrainingTableThree.CustomerID=TrainingTableFour.CustomerID WHERE OrderID == 10308", colour="green")
                gui.debugger.addtoscreen("To continue select the command that would retrieve all orderIDs and the country that the customer is from")
                while stabilisationAnswer.get() != "SELECT ORDERID, Country FROM TrainingTableThree INNER JOIN TrainingTableThree.CustomerID=TrainingTableFour.CustomerID":
                    stabilisationProblemCoreWindow(question="Choose the appropriate SQL command to retrieve the requested information",
                                                   option1="SELECT ORDERID FROM TrainingTableThree INNER JOIN TrainingTableThree.CustomerID=TrainingTableFour.CustomerID",
                                                   option2="SELECT ORDERID, Country FROM TrainingTableThree INNER JOIN TrainingTableThree.CustomerID=TrainingTableFour.ContactName",
                                                   option3="SELECT ORDERID, Country FROM TrainingTableThree INNER JOIN TrainingTableThree.CustomerID=TrainingTableFour.CustomerID")
                    if stabilisationAnswer.get() == "QUIT":
                        gui.debugger.addtoscreen("Training Quit", colour="red")
                        return 1
                    elif stabilisationAnswer.get() != "SELECT ORDERID, Country FROM TrainingTableThree INNER JOIN TrainingTableThree.CustomerID=TrainingTableFour.CustomerID":
                        gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                    else:
                        gui.debugger.addtoscreen("Correct SQL statement chosen ", colour="green")
                        gui.debugger.addtoscreen("... ", colour="green")
                        gui.debugger.addtoscreen("Data Retrieval Successful", colour="green")
                        gui.debugger.addtoscreen("Continuing training", colour="green")
                        progresstrackerstable.set(progresstrackerstable.get() + 1)

            if progresstrackerstable.get() == 4:
                # SQL security concerns
                gui.debugger.addtoscreen("SQL queries are powerful tools, but care needs to be taken to ensure that only the queries you intend are used", colour="green")
                gui.debugger.addtoscreen("SQL Injection is one of the many ways in which hackers, criminal or otherwise may try to access databases held within your system", colour="green")
                gui.debugger.addtoscreen("SQL injection involves passing additional arguments into a text form that when submitted as an SQL query runs commands additionally to what was intended by the developer", colour="green")
                gui.debugger.addtoscreen("For example, in a login screen with a username and password box, where the typed in text is then used as part of an SQL query to check if the password and username are correct", colour="green")
                gui.debugger.addtoscreen("Where the SQL query that checks if the username and password are correct is: ", colour="green")
                gui.debugger.addtoscreen("SELECT username FROM userinfotable WHERE password==passwordsubmittedbyuser", colour="green")
                gui.debugger.addtoscreen("inserting ' or '1'='1' would, when submitted into this SQL query create", colour="green")
                gui.debugger.addtoscreen("SELECT username FROM userinfotable WHERE password==passwordsubmittedbyuser' or '1'='1' ", colour="green")
                gui.debugger.addtoscreen("as 1=1 always evaluates to TRUE, this would result in the SQL database returning all rows of the underlying userinfotable database which could then be exploited by the hacker", colour="green")
                gui.debugger.addtoscreen("To prevent this, all user input should be sanatised, with characers such as ', !, \" etc escaped out to the symbol rather than the control character that they represent in SQL", colour="green")
                gui.debugger.addtoscreen("To continue select the command that would retrieve all orderIDs and the country that the customer is from")
                while stabilisationAnswer.get() != "' or '1'='1'":
                    stabilisationProblemCoreWindow(question="Choose the appropriate SQL command to retrieve the requested information",
                                                   option1="' or '1'AND'1'",
                                                   option2="' or '1'!='1'",
                                                   option3="' or '1'='1'")
                    if stabilisationAnswer.get() == "QUIT":
                        gui.debugger.addtoscreen("Training Quit", colour="red")
                        return 1
                    elif stabilisationAnswer.get() != "' or '1'='1'":
                        gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                    else:
                        gui.debugger.addtoscreen("Correct SQL statement chosen ", colour="green")
                        gui.debugger.addtoscreen("... ", colour="green")
                        gui.debugger.addtoscreen("Data Retrieval Successful", colour="green")
                        gui.debugger.addtoscreen("End of training reached, please complete the following SQL based queries to bring the stabililisation system back online", colour="green")
                        progresstrackerstable.set(choice(stabilisationprogressarray))

            # problems begin
            # problem 1
            if progresstrackerstable.get() == 5:
                # if completed enough questions
                if len(stabilisationprogressarray) < 4:
                    break
                # Else provide text question
                gui.debugger.addtoscreen("Retrieve a list of task ID's from Table 6. Tasklist. that stated in 2019 ", colour="green")
                stabilisationProblemCoreWindow(question="Choose the appropriate SQL command to retrieve the requested information",
                                               option1="FROM TaskList select TaskID, TimeStarted WHERE TimeStarted == 2019",
                                               option2="FROM TaskList select * WHERE TimeStarted == 2019",
                                               option3="FROM TaskList select TaskID, TimeStarted WHERE TimeStarted < 2019")
                if stabilisationAnswer.get() == "QUIT":
                    gui.debugger.addtoscreen("Quit", colour="red")
                    return 1
                elif stabilisationAnswer.get() != "FROM TaskList select TaskID, TimeStarted WHERE TimeStarted == 2019":
                    gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                else:
                    gui.debugger.addtoscreen("Correct SQL statement chosen ", colour="green")
                    gui.debugger.addtoscreen("... ", colour="green")
                    gui.debugger.addtoscreen("Data Retrieval Successful", colour="green")
                    progresstrackerstable.set(choice(stabilisationprogressarray))
                    stabilisationprogressarray.remove(5)

            # problem 2
            if progresstrackerstable.get() == 6:
                # if completed enough questions
                if len(stabilisationprogressarray) < 4:
                    break
                # Else provide text question
                gui.debugger.addtoscreen("Retrieve a list of Descriptions (Table 7) for all tasks (Table 6) that started in 2019 ", colour="green")
                stabilisationProblemCoreWindow(question="Choose the appropriate SQL command to retrieve the requested information",
                                               option1="FROM TaskList select Origin, Description, TimeStarted INNER JOIN TaskList.Origin=OriginLookup.Description WHERE TimeStarted == 2019",
                                               option2="FROM TaskList select Origin, Description, TimeStarted INNER JOIN TaskList.Origin=OriginLookup.Origin WHERE TimeStarted == 2019",
                                               option3="FROM TaskList select Origin, Description, TimeStarted INNER JOIN TaskList.Id=OriginLookup.Origin WHERE TimeStarted == 2019")
                if stabilisationAnswer.get() == "QUIT":
                    gui.debugger.addtoscreen("Quit", colour="red")
                    return 1
                elif stabilisationAnswer.get() != "FROM TaskList select Origin, Description, TimeStarted INNER JOIN TaskList.Origin=OriginLookup.Origin WHERE TimeStarted == 2019":
                    gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                else:
                    gui.debugger.addtoscreen("Correct SQL statement chosen ", colour="green")
                    gui.debugger.addtoscreen("... ", colour="green")
                    gui.debugger.addtoscreen("Data Retrieval Successful", colour="green")
                    progresstrackerstable.set(choice(stabilisationprogressarray))
                    stabilisationprogressarray.remove(6)

            # problem 3
            if progresstrackerstable.get() == 7:
                # if completed enough questions
                if len(stabilisationprogressarray) < 4:
                    break
                # Else provide text question
                gui.debugger.addtoscreen("Retrieve a list of all users of admin level 1 or higher", colour="green")
                stabilisationProblemCoreWindow(question="Choose the appropriate SQL command to retrieve the requested information",
                                               option1="FROM UsersTable select * WHERE AdminLevel >= 1",
                                               option2="FROM UsersTable select User WHERE AdminLevel >= 1",
                                               option3="FROM UsersTable select User WHERE AdminLevel == 1")
                if stabilisationAnswer.get() == "QUIT":
                    gui.debugger.addtoscreen("Quit", colour="red")
                    return 1
                elif stabilisationAnswer.get() != "FROM UsersTable select User WHERE AdminLevel >= 1":
                    gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                else:
                    gui.debugger.addtoscreen("Correct SQL statement chosen ", colour="green")
                    gui.debugger.addtoscreen("... ", colour="green")
                    gui.debugger.addtoscreen("Data Retrieval Successful", colour="green")
                    progresstrackerstable.set(choice(stabilisationprogressarray))
                    stabilisationprogressarray.remove(7)

            # problem 4
            if progresstrackerstable.get() == 8:
                # if completed enough questions
                if len(stabilisationprogressarray) < 4:
                    break
                # Else provide text question
                gui.debugger.addtoscreen("Retrieve a list of all users", colour="green")
                stabilisationProblemCoreWindow(question="Choose the appropriate SQL command to retrieve the requested information",
                                               option1="FROM UsersTable select ID",
                                               option2="FROM UsersTable select User",
                                               option3="FROM UsersTable select *")
                if stabilisationAnswer.get() == "QUIT":
                    gui.debugger.addtoscreen("Quit", colour="red")
                    return 1
                elif stabilisationAnswer.get() != "FROM UsersTable select User":
                    gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                else:
                    gui.debugger.addtoscreen("Correct SQL statement chosen ", colour="green")
                    gui.debugger.addtoscreen("... ", colour="green")
                    gui.debugger.addtoscreen("Data Retrieval Successful", colour="green")
                    progresstrackerstable.set(choice(stabilisationprogressarray))
                    stabilisationprogressarray.remove(8)

            # problem 5
            if progresstrackerstable.get() == 9:
                # if completed enough questions
                if len(stabilisationprogressarray) < 4:
                    break
                # Else provide text question
                gui.debugger.addtoscreen("Retrieve a list of all active users", colour="green")
                stabilisationProblemCoreWindow(question="Choose the appropriate SQL command to retrieve the requested information",
                                               option1="FROM UsersTable select User WHERE Active == 0",
                                               option2="FROM UsersTable select User WHERE Active == 1",
                                               option3="FROM UsersTable select User WHERE DateCreated <= 2020")
                if stabilisationAnswer.get() == "QUIT":
                    gui.debugger.addtoscreen("Quit", colour="red")
                    return 1
                elif stabilisationAnswer.get() != "FROM UsersTable select User WHERE Active == 1":
                    gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                else:
                    gui.debugger.addtoscreen("Correct SQL statement chosen ", colour="green")
                    gui.debugger.addtoscreen("... ", colour="green")
                    gui.debugger.addtoscreen("Data Retrieval Successful", colour="green")
                    progresstrackerstable.set(choice(stabilisationprogressarray))
                    stabilisationprogressarray.remove(9)

            # problem 6
            if progresstrackerstable.get() == 10:
                # if completed enough questions
                if len(stabilisationprogressarray) < 4:
                    break
                # Else provide text question
                gui.debugger.addtoscreen("Retrieve a list from Table 9, of all sensors, the description of their Origin (Table 7) which used more than 10 units of power", colour="green")
                stabilisationProblemCoreWindow(question="Choose the appropriate SQL command to retrieve the requested information",
                                               option1="FROM SensorPowerUsage select SensorType, Origin INNER JOIN SensorPowerUsage.Origin=OriginLookup.Origin WHERE PowerUsed > 10",
                                               option2="FROM SensorPowerUsage select SensorType, Origin INNER JOIN SensorPowerUsage.Origin=TaskList.Origin WHERE PowerUsed > 10",
                                               option3="FROM SensorPowerUsage select SensorType, Origin WHERE PowerUsed > 10")
                if stabilisationAnswer.get() == "QUIT":
                    gui.debugger.addtoscreen("Quit", colour="red")
                    return 1
                elif stabilisationAnswer.get() != "FROM SensorPowerUsage select SensorType, Origin INNER JOIN SensorPowerUsage.Origin=OriginLookup.Origin WHERE PowerUsed > 10":
                    gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                else:
                    gui.debugger.addtoscreen("Correct SQL statement chosen ", colour="green")
                    gui.debugger.addtoscreen("... ", colour="green")
                    gui.debugger.addtoscreen("Data Retrieval Successful", colour="green")
                    progresstrackerstable.set(choice(stabilisationprogressarray))
                    stabilisationprogressarray.remove(10)

            # problem 7
            if progresstrackerstable.get() == 11:
                # if completed enough questions
                if len(stabilisationprogressarray) < 4:
                    break
                # Else provide text question
                gui.debugger.addtoscreen("Retrieve a list all hashed passwords of active users created in 2020", colour="green")
                stabilisationProblemCoreWindow(question="Choose the appropriate SQL command to retrieve the requested information",
                                               option1="FROM UsersTable select HashedPassword, DataCreated, Active WHERE Active == 1",
                                               option2="FROM UsersTable select DataCreated, Active WHERE DateCreated == 2020 AND Active == 1",
                                               option3="FROM UsersTable select HashedPassword, DataCreated, Active WHERE DateCreated == 2020 AND Active == 1")
                if stabilisationAnswer.get() == "QUIT":
                    gui.debugger.addtoscreen("Quit", colour="red")
                    return 1
                elif stabilisationAnswer.get() != "FROM UsersTable select HashedPassword, DataCreated, Active WHERE DateCreated == 2020 AND Active == 1":
                    gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                else:
                    gui.debugger.addtoscreen("Correct SQL statement chosen ", colour="green")
                    gui.debugger.addtoscreen("... ", colour="green")
                    gui.debugger.addtoscreen("Data Retrieval Successful", colour="green")
                    progresstrackerstable.set(choice(stabilisationprogressarray))
                    stabilisationprogressarray.remove(11)

            # problem 8
            if progresstrackerstable.get() == 12:
                # if completed enough questions
                if len(stabilisationprogressarray) < 4:
                    break
                # Else provide text question
                gui.debugger.addtoscreen("Retrieve a list all types of sensor that were drawing power for more than 80 seconds", colour="green")
                stabilisationProblemCoreWindow(question="Choose the appropriate SQL command to retrieve the requested information",
                                               option1="FROM SensorPowerUsage select DISTINCT SensorType WHERE Duration > 80",
                                               option2="FROM SensorPowerUsage select SensorType WHERE Duration > 80",
                                               option3="FROM SensorPowerUsage select DISTINCT SensorType WHERE PowerUsed > 80")
                if stabilisationAnswer.get() == "QUIT":
                    gui.debugger.addtoscreen("Quit", colour="red")
                    return 1
                elif stabilisationAnswer.get() != "FROM SensorPowerUsage select DISTINCT SensorType WHERE Duration > 80":
                    gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                else:
                    gui.debugger.addtoscreen("Correct SQL statement chosen ", colour="green")
                    gui.debugger.addtoscreen("... ", colour="green")
                    gui.debugger.addtoscreen("Data Retrieval Successful", colour="green")
                    progresstrackerstable.set(choice(stabilisationprogressarray))
                    stabilisationprogressarray.remove(12)

            # problem 9
            if progresstrackerstable.get() == 13:
                # if completed enough questions
                if len(stabilisationprogressarray) < 4:
                    break
                # Else provide text question
                gui.debugger.addtoscreen("Retrieve a list all users that logged a command in Table 10", colour="green")
                stabilisationProblemCoreWindow(question="Choose the appropriate SQL command to retrieve the requested information",
                                               option1="FROM CommandLogging select DISTINCT UserID",
                                               option2="FROM CommandLogging select UserID",
                                               option3="FROM CommandLogging select CommandType")
                if stabilisationAnswer.get() == "QUIT":
                    gui.debugger.addtoscreen("Quit", colour="red")
                    return 1
                elif stabilisationAnswer.get() != "FROM CommandLogging select DISTINCT UserID":
                    gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                else:
                    gui.debugger.addtoscreen("Correct SQL statement chosen ", colour="green")
                    gui.debugger.addtoscreen("... ", colour="green")
                    gui.debugger.addtoscreen("Data Retrieval Successful", colour="green")
                    progresstrackerstable.set(choice(stabilisationprogressarray))
                    stabilisationprogressarray.remove(13)

            # problem 9
            if progresstrackerstable.get() == 14:
                # if completed enough questions
                if len(stabilisationprogressarray) < 4:
                    break
                # Else provide text question
                gui.debugger.addtoscreen("Return a list of all commands (with description Table 10) run by user 10", colour="green")
                stabilisationProblemCoreWindow(
                    question="Choose the appropriate SQL command to retrieve the requested information",
                    option1="FROM CommandLogging select CommandType, UserID, Description INNER JOIN CommandLoggin.Id=CommandLoggingLookUp.CommandType WHERE UserID == 10",
                    option2="FROM CommandLogging select CommandType, UserID, Description INNER JOIN CommandLoggin.Id=CommandLoggingLookUp.CommandType WHERE UserID > 10",
                    option3="FROM CommandLogging select Description INNER JOIN CommandLoggin.Id=CommandLoggingLookUp.CommandType WHERE UserID == 10")
                if stabilisationAnswer.get() == "QUIT":
                    gui.debugger.addtoscreen("Quit", colour="red")
                    return 1
                elif stabilisationAnswer.get() != "FROM CommandLogging select CommandType, UserID, Description INNER JOIN CommandLoggin.Id=CommandLoggingLookUp.CommandType WHERE UserID == 10":
                    gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                else:
                    gui.debugger.addtoscreen("Correct SQL statement chosen ", colour="green")
                    gui.debugger.addtoscreen("... ", colour="green")
                    gui.debugger.addtoscreen("Data Retrieval Successful", colour="green")
                    progresstrackerstable.set(choice(stabilisationprogressarray))
                    stabilisationprogressarray.remove(14)

            # problem 10
            if progresstrackerstable.get() == 15:
                # if completed enough questions
                if len(stabilisationprogressarray) < 4:
                    break
                # Else provide text question
                gui.debugger.addtoscreen("Which user is returned from the following query", colour="green")
                gui.debugger.addtoscreen("FROM UsersTable select User WHERE DataCreated == 2018 AND AdminLevel = 2", colour="green")
                stabilisationProblemCoreWindow(
                    question="Choose the appropriate SQL command to retrieve the requested information",
                    option1="Helen",
                    option2="Michael",
                    option3="Liam")
                if stabilisationAnswer.get() == "QUIT":
                    gui.debugger.addtoscreen("Quit", colour="red")
                    return 1
                elif stabilisationAnswer.get() != "Helen":
                    gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                else:
                    gui.debugger.addtoscreen("Correct SQL statement chosen ", colour="green")
                    gui.debugger.addtoscreen("... ", colour="green")
                    gui.debugger.addtoscreen("Data Retrieval Successful", colour="green")
                    progresstrackerstable.set(choice(stabilisationprogressarray))
                    stabilisationprogressarray.remove(15)

            # problem 11
            if progresstrackerstable.get() == 16:
                # if completed enough questions
                if len(stabilisationprogressarray) < 4:
                    break
                # Else provide text question
                gui.debugger.addtoscreen("How many rows are returned from the following query", colour="green")
                gui.debugger.addtoscreen("FROM TaskList SELECT * WHERE Origin == 4 OR TimeStarted > 2019", colour="green")
                stabilisationProblemCoreWindow(
                    question="Choose the appropriate SQL command to retrieve the requested information",
                    option1="7",
                    option2="8",
                    option3="9")
                if stabilisationAnswer.get() == "QUIT":
                    gui.debugger.addtoscreen("Quit", colour="red")
                    return 1
                elif stabilisationAnswer.get() != "7":
                    gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                else:
                    gui.debugger.addtoscreen("Correct SQL statement chosen ", colour="green")
                    gui.debugger.addtoscreen("... ", colour="green")
                    gui.debugger.addtoscreen("Data Retrieval Successful", colour="green")
                    progresstrackerstable.set(choice(stabilisationprogressarray))
                    stabilisationprogressarray.remove(16)

            # problem 12
            if progresstrackerstable.get() == 17:
                # if completed enough questions
                if len(stabilisationprogressarray) < 4:
                    break
                # Else provide text question
                gui.debugger.addtoscreen("What is the description produced by the following query?", colour="green")
                gui.debugger.addtoscreen("FROM OriginLookup SELECT Description WHERE Origin == 4", colour="green")
                stabilisationProblemCoreWindow(
                    question="Choose the appropriate SQL command to retrieve the requested information",
                    option1="Ultrasonic Detector 1",
                    option2="Internal Plumbing",
                    option3="Powerswitch")
                if stabilisationAnswer.get() == "QUIT":
                    gui.debugger.addtoscreen("Quit", colour="red")
                    return 1
                elif stabilisationAnswer.get() != "Internal Plumbing":
                    gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                else:
                    gui.debugger.addtoscreen("Correct SQL statement chosen ", colour="green")
                    gui.debugger.addtoscreen("... ", colour="green")
                    gui.debugger.addtoscreen("Data Retrieval Successful", colour="green")
                    progresstrackerstable.set(choice(stabilisationprogressarray))
                    stabilisationprogressarray.remove(17)

            # problem 13
            if progresstrackerstable.get() == 18:
                # if completed enough questions
                if len(stabilisationprogressarray) < 4:
                    break
                # Else provide text question
                gui.debugger.addtoscreen("How many results does the following query produce", colour="green")
                gui.debugger.addtoscreen("FROM SensortPowerUsage SELECT SensorType, PowerUsed WHERE Duration > 10 AND PowerUsed > 10", colour="green")
                stabilisationProblemCoreWindow(
                    question="Choose the appropriate SQL command to retrieve the requested information",
                    option1="1",
                    option2="5",
                    option3="8")
                if stabilisationAnswer.get() == "QUIT":
                    gui.debugger.addtoscreen("Quit", colour="red")
                    return 1
                elif stabilisationAnswer.get() != "5":
                    gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                else:
                    gui.debugger.addtoscreen("Correct SQL statement chosen ", colour="green")
                    gui.debugger.addtoscreen("... ", colour="green")
                    gui.debugger.addtoscreen("Data Retrieval Successful", colour="green")
                    progresstrackerstable.set(choice(stabilisationprogressarray))
                    stabilisationprogressarray.remove(18)

            # problem 14
            if progresstrackerstable.get() == 19:
                # if completed enough questions
                if len(stabilisationprogressarray) < 4:
                    break
                # Else provide text question
                gui.debugger.addtoscreen("How many results does the following query produce", colour="green")
                gui.debugger.addtoscreen("FROM CommandLogging SELECT CommandType WHERE CommandType == 1 OR CommandType == 2", colour="green")
                stabilisationProblemCoreWindow(
                    question="Choose the appropriate SQL command to retrieve the requested information",
                    option1="11",
                    option2="12",
                    option3="13")
                if stabilisationAnswer.get() == "QUIT":
                    gui.debugger.addtoscreen("Quit", colour="red")
                    return 1
                elif stabilisationAnswer.get() != "13":
                    gui.debugger.addtoscreen("Incorrect answer please try again", colour="red")
                else:
                    gui.debugger.addtoscreen("Correct SQL statement chosen ", colour="green")
                    gui.debugger.addtoscreen("... ", colour="green")
                    gui.debugger.addtoscreen("Data Retrieval Successful", colour="green")
                    progresstrackerstable.set(choice(stabilisationprogressarray))
                    stabilisationprogressarray.remove(19)

        # If arriving here signal success for stabilisation problemcore
        # update the status of the power box to Error
        gui.debugger.addtoscreen("Relational Databases Fixed", colour="green")
        gui.debugger.addtoscreen("Starting Stabilisation subsystem", colour="green")
        gui.debugger.addtoscreen("Progress 10%", colour="green")
        gui.debugger.addtoscreen("Progress 20%", colour="green")
        gui.debugger.addtoscreen("Progress 30%", colour="green")
        gui.debugger.addtoscreen("Progress 40%", colour="green")
        gui.debugger.addtoscreen("Progress 50%", colour="green")
        gui.debugger.addtoscreen("Progress 60%", colour="green")
        gui.debugger.addtoscreen("Progress 70%", colour="green")
        gui.debugger.addtoscreen("Progress 80%", colour="green")
        gui.debugger.addtoscreen("Progress 90%", colour="green")
        gui.debugger.addtoscreen("Progress 100%", colour="green")
        gui.debugger.addtoscreen("Stability System Online", colour="green")
        gui.stablisationsubsystem.changestatus(newstatus="Status: Online")
        # update the button so that it creates a problem filling it with a random power puzzle
        gui.stablisationsubsystem.changebuttontext(newtext="Repaired")
        # update the button to now open the power problem window
        gui.stablisationsubsystem.setcommand("powerproblem")
        # change colour background to green
        gui.stablisationsubsystem.changebackground("green")
        gui.debugger.addtoscreen("Stabilisation Subsystem Debug Complete", colour="green")

class BooleanChoiceWindow:
    def __init__(self, width, height, question, secondmessage, option1, option2, option3):
        # If running in tutorial mode then setup the window accordingly
        # create toplevel to house the choices
        self.choicewindow = Toplevel()
        self.choicewindow.config(background="#FFFFFF")
        # get size and position of the problemcore window
        self.choicewindow.geometry('%dx%d+%d+%d' % (root.winfo_screenwidth()/4, root.winfo_screenheight()/5, (3*root.winfo_screenwidth()/4 - root.winfo_screenwidth()/8), root.winfo_screenheight()/2 - (root.winfo_screenheight()/3)/2))
        self.choicewindow.resizable(0, 0)
        # add questions label
        question = ttk.Label(self.choicewindow, text=question, font=(None, 14))
        question.config(wraplength=500)
        question.grid(row=0, column=0, sticky=tk.EW, columnspan=3)
        # add text explaining what to do
        text = ttk.Label(self.choicewindow, text=secondmessage, font=(None, 14))
        text.config(wraplength=450)
        text.grid(row=1, column=0, sticky=tk.EW, columnspan=3)
        # add choices
        ttk.Button(self.choicewindow, text=option1, command=lambda: self.setanddestroy(answeroption=option1)).grid(row=2, column=0, sticky=tk.NSEW)
        ttk.Button(self.choicewindow, text=option2, command=lambda: self.setanddestroy(answeroption=option2)).grid(row=2, column=1, sticky=tk.NSEW)
        ttk.Button(self.choicewindow, text=option3, command=lambda: self.setanddestroy(answeroption=option3)).grid(row=2, column=2, sticky=tk.NSEW)
        # add quit button
        ttk.Button(self.choicewindow, text="Quit", command=lambda: self.setanddestroy(answeroption="QUIT")).grid(row=3, column=2, sticky=tk.NSEW)

        # give weight to rows and column to permit dynamic redraw
        self.choicewindow.columnconfigure((0, 1, 2), weight=1)
        self.choicewindow.rowconfigure(2, weight=1)

        # Buff and pad all children of mainframe
        for child in self.choicewindow.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.choicewindow.wait_window()

    def setanddestroy(self, answeroption):
        if answeroption == "QUIT":
            answer.set(answeroption)
            self.choicewindow.destroy()
        else:
            time.sleep(0.25)
            answer.set(answeroption)
            self.choicewindow.destroy()

class NineChoiceWindow:
    def __init__(self, option1, option2, option3, option4, option5, option6, option7, option8, option9):
        # create list to store answers
        global motorlist
        # Clear out the list
        motorlist.clear()

        # create stringvars for text
        option1sv = StringVar()
        option1sv.set(option1)
        option2sv = StringVar()
        option2sv.set(option2)
        option3sv = StringVar()
        option3sv.set(option3)
        option4sv = StringVar()
        option4sv.set(option4)
        option5sv = StringVar()
        option5sv.set(option5)
        option6sv = StringVar()
        option6sv.set(option6)
        option7sv = StringVar()
        option7sv.set(option7)
        option8sv = StringVar()
        option8sv.set(option8)
        option9sv = StringVar()
        option9sv.set(option9)
        # create toplevel to house the choices
        self.choicewindow = Toplevel()
        self.choicewindow.config(background="#FFFFFF")
        # get size and position of the problemcore window
        self.choicewindow.geometry('%dx%d+%d+%d' % (root.winfo_screenwidth()/4, root.winfo_screenheight()/5, (3*root.winfo_screenwidth()/4 - root.winfo_screenwidth()/8), root.winfo_screenheight()/2 - (root.winfo_screenheight()/3)/2))
        self.choicewindow.resizable(0, 0)
        # add questions label
        question = ttk.Label(self.choicewindow, text="Select the required libaries from the choices below", font=(None, 14))
        question.config(wraplength=500)
        question.grid(row=0, column=0, sticky=tk.EW, columnspan=3)
        # add choices
        buttonone = ttk.Button(self.choicewindow, text=option1sv.get(), command=lambda: self.addtoreturnandselect(answeroption=option1sv, answerlist=motorlist, button=buttonone))
        buttonone.grid(row=1, column=0, sticky=tk.NSEW)
        buttontwo = ttk.Button(self.choicewindow, text=option2sv.get(), command=lambda: self.addtoreturnandselect(answeroption=option2sv, answerlist=motorlist, button=buttontwo))
        buttontwo.grid(row=1, column=1, sticky=tk.NSEW)
        buttonthree = ttk.Button(self.choicewindow, text=option3sv.get(), command=lambda: self.addtoreturnandselect(answeroption=option3sv, answerlist=motorlist, button=buttonthree))
        buttonthree.grid(row=1, column=2, sticky=tk.NSEW)
        buttonfour = ttk.Button(self.choicewindow, text=option4sv.get(), command=lambda: self.addtoreturnandselect(answeroption=option4sv, answerlist=motorlist, button=buttonfour))
        buttonfour.grid(row=2, column=0, sticky=tk.NSEW)
        buttonfive = ttk.Button(self.choicewindow, text=option5sv.get(), command=lambda: self.addtoreturnandselect(answeroption=option5sv, answerlist=motorlist, button=buttonfive))
        buttonfive.grid(row=2, column=1, sticky=tk.NSEW)
        buttonsix = ttk.Button(self.choicewindow, text=option6sv.get(), command=lambda: self.addtoreturnandselect(answeroption=option6sv, answerlist=motorlist, button=buttonsix))
        buttonsix.grid(row=2, column=2, sticky=tk.NSEW)
        buttonseven = ttk.Button(self.choicewindow, text=option7sv.get(), command=lambda: self.addtoreturnandselect(answeroption=option7sv, answerlist=motorlist, button=buttonseven))
        buttonseven.grid(row=3, column=0, sticky=tk.NSEW)
        buttoneight = ttk.Button(self.choicewindow, text=option8sv.get(), command=lambda: self.addtoreturnandselect(answeroption=option8sv, answerlist=motorlist, button=buttoneight))
        buttoneight.grid(row=3, column=1, sticky=tk.NSEW)
        buttonnine = ttk.Button(self.choicewindow, text=option9sv.get(), command=lambda: self.addtoreturnandselect(answeroption=option9sv, answerlist=motorlist, button=buttonnine))
        buttonnine.grid(row=3, column=2, sticky=tk.NSEW)
        # add submit button
        ttk.Button(self.choicewindow, text="Submit", command=lambda: self.submitanswer()).grid(row=4, column=0, sticky=tk.NSEW)
        # add quit button
        ttk.Button(self.choicewindow, text="Quit", command=lambda: self.quitprogram()).grid(row=4, column=2, sticky=tk.NSEW)

        # give weight to rows and column to permit dynamic redraw
        self.choicewindow.columnconfigure((0, 1, 2), weight=1)
        self.choicewindow.rowconfigure((1,2,3,4), weight=1)

        # Buff and pad all children of mainframe
        for child in self.choicewindow.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.choicewindow.wait_window()

    def addtoreturnandselect(self, answeroption, answerlist, button):
        # if already in the list then remove and update text
        if answeroption.get() in answerlist:
            answerlist.remove(answeroption.get())
            button.config(text=answeroption.get())
        # if not in list then add and change button
        else:
            # add the submitted answer to a list
            answerlist.append(answeroption.get())
            # change button to show it has been selected
            button.config(text="{} Selected".format(answeroption.get()))

    def submitanswer(self):
        self.choicewindow.destroy()

    def quitprogram(self):
        motorlist.append("QUIT")
        self.choicewindow.destroy()

class LogInWindow:
    def __init__(self, username, password):
        self.correctpassword = password
        self.correctusername = username
        # create toplevel to house the choices
        self.choicewindow = Toplevel()
        #self.choicewindow.config(background="#FFFFFF")
        # get size and position of the problemcore window
        self.choicewindow.geometry('%dx%d+%d+%d' % (root.winfo_screenwidth()/4, root.winfo_screenheight()/5, (3*root.winfo_screenwidth()/4 - root.winfo_screenwidth()/8), root.winfo_screenheight()/2 - (root.winfo_screenheight()/3)/2))
        self.choicewindow.resizable(0, 0)
        # Explanatory text
        ttk.Label(self.choicewindow, text="Please input your username and password below").grid(row=0, column=0, sticky=tk.NSEW, columnspan=3)
        # add username box
        ttk.Label(self.choicewindow, text="Username:").grid(row=1, column=0, sticky=tk.NSEW)
        username = ttk.Entry(self.choicewindow)
        username.grid(row=1, column=1, sticky=tk.NSEW)
        # add password box
        ttk.Label(self.choicewindow, text="Password:").grid(row=2, column=0, sticky=tk.NSEW)
        password = ttk.Entry(self.choicewindow, show="*")
        password.grid(row=2, column=1, sticky=tk.NSEW)
        # add submit button
        ttk.Button(self.choicewindow, text="Submit", command=lambda: self.setanddestroy(answeroption="submit",username=username.get(), password=password.get())).grid(row=3, column=0, sticky=tk.NSEW)
        # add quit button
        ttk.Button(self.choicewindow, text="Quit", command=lambda: self.setanddestroy(answeroption="QUIT", username="blank", password="blank")).grid(row=3, column=2, sticky=tk.NSEW)

        # give weight to rows and column to permit dynamic redraw
        self.choicewindow.columnconfigure((0, 1, 2), weight=1)
        self.choicewindow.rowconfigure((0, 3), weight=1)

        # Buff and pad all children of mainframe
        for child in self.choicewindow.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.choicewindow.wait_window()

    def setanddestroy(self, answeroption, username, password):
        if answeroption == "QUIT":
            response.set(answeroption)
            self.choicewindow.destroy()
        elif username == self.correctusername and password == self.correctpassword:
            time.sleep(0.25)
            response.set("TRUE")
            self.choicewindow.destroy()
        else:
            time.sleep(0.25)
            response.set("FALSE")
            self.choicewindow.destroy()

class AlternativeLogInWindow:
    def __init__(self, username, password, alternativePassword):
        self.correctpassword = password
        self.correctusername = username
        self.correctalternative = alternativePassword
        # create toplevel to house the choices
        self.choicewindow = Toplevel()
        #self.choicewindow.config(background="#FFFFFF")
        # get size and position of the problemcore window
        self.choicewindow.geometry('%dx%d+%d+%d' % (root.winfo_screenwidth()/4, root.winfo_screenheight()/5, (3*root.winfo_screenwidth()/4 - root.winfo_screenwidth()/8), root.winfo_screenheight()/2 - (root.winfo_screenheight()/3)/2))
        self.choicewindow.resizable(0, 0)
        # Explanatory text
        ttk.Label(self.choicewindow, text="Please input your username and password below").grid(row=0, column=0, sticky=tk.NSEW, columnspan=3)
        # add username box
        ttk.Label(self.choicewindow, text="Username:").grid(row=1, column=0, sticky=tk.NSEW)
        username = ttk.Entry(self.choicewindow)
        username.grid(row=1, column=1, sticky=tk.NSEW)
        # add password box
        ttk.Label(self.choicewindow, text="Password:").grid(row=2, column=0, sticky=tk.NSEW)
        password = ttk.Entry(self.choicewindow, show="*")
        password.grid(row=2, column=1, sticky=tk.NSEW)
        # add submit button
        ttk.Button(self.choicewindow, text="Submit", command=lambda: self.setanddestroy(answeroption="submit",username=username.get(), password=password.get())).grid(row=3, column=0, sticky=tk.NSEW)
        # add quit button
        ttk.Button(self.choicewindow, text="Quit", command=lambda: self.setanddestroy(answeroption="QUIT", username="blank", password="blank")).grid(row=3, column=2, sticky=tk.NSEW)

        # give weight to rows and column to permit dynamic redraw
        self.choicewindow.columnconfigure((0, 1, 2), weight=1)
        self.choicewindow.rowconfigure((0, 3), weight=1)

        # Buff and pad all children of mainframe
        for child in self.choicewindow.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.choicewindow.wait_window()

    def setanddestroy(self, answeroption, username, password):
        if answeroption == "QUIT":
            response.set(answeroption)
            self.choicewindow.destroy()
        elif username == self.correctusername and password == self.correctpassword:
            time.sleep(0.25)
            response.set("TRUE")
            self.choicewindow.destroy()
        elif username == self.correctalternative or password == self.correctalternative:
            # return the alternate keyword to trigger the printing of the informationn
            time.sleep(0.25)
            response.set("ALTERNATE")
            self.choicewindow.destroy()
        else:
            time.sleep(0.25)
            response.set("FALSE")
            self.choicewindow.destroy()

class BluetoothBox:
    def __init__(self):
        # create toplevel to house the choices
        self.choicewindow = Toplevel()
        #self.choicewindow.config(background="#FFFFFF")
        # get size and position of the problemcore window
        self.choicewindow.geometry('%dx%d+%d+%d' % (root.winfo_screenwidth()/4, root.winfo_screenheight()/5, (3*root.winfo_screenwidth()/4 - root.winfo_screenwidth()/8), root.winfo_screenheight()/2 - (root.winfo_screenheight()/3)/2))
        self.choicewindow.resizable(0, 0)
        # add label for the top of the table
        ttk.Label(self.choicewindow, text="Select the appropriate response from options below").grid(row=0, column=0, sticky=tk.NSEW, columnspan=3)
        # add response code box
        ttk.Label(self.choicewindow, text="Response Code:").grid(row=1, column=0, sticky=tk.NSEW)
        responseentry = ttk.Entry(self.choicewindow)
        responseentry.grid(row=1, column=1, sticky=tk.NSEW)
        # Submit button after box
        ttk.Button(self.choicewindow, text="Submit", command=lambda: self.setanddestroy(answeroption=responseentry.get())).grid(row=1, column=2, sticky=tk.NSEW)
        # buttons
        ttk.Button(self.choicewindow, text="Connect", command=lambda: self.setanddestroy(answeroption="CONNECT")).grid(row=2, column=0, sticky=tk.NSEW)
        ttk.Button(self.choicewindow, text="Reset", command=lambda: self.setanddestroy(answeroption="RESET")).grid(row=2, column=1, sticky=tk.NSEW)
        ttk.Button(self.choicewindow, text="Purge", command=lambda: self.setanddestroy(answeroption="PURGE")).grid(row=2, column=2, sticky=tk.NSEW)

        # add quit button
        ttk.Button(self.choicewindow, text="Quit", command=lambda: self.setanddestroy(answeroption="QUIT")).grid(row=3, column=2, sticky=tk.NSEW)

        # give weight to rows and column to permit dynamic redraw
        self.choicewindow.columnconfigure((0, 1, 2), weight=1)
        self.choicewindow.rowconfigure((0,1,2,3), weight=1)

        # Buff and pad all children of mainframe
        for child in self.choicewindow.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.choicewindow.wait_window()

    def setanddestroy(self, answeroption):
        if answeroption == "QUIT":
            bluetoothanswer.set(answeroption)
            self.choicewindow.destroy()
        else:
            time.sleep(0.25)
            bluetoothanswer.set("{}".format(answeroption))
            self.choicewindow.destroy()

class stabilisationProblemCoreWindow:
    def __init__(self, question, option1, option2, option3):
        # If running in tutorial mode then setup the window accordingly
        # create toplevel to house the choices
        self.choicewindow = Toplevel()
        self.choicewindow.config(background="#FFFFFF")
        # get size and position of the problemcore window
        self.choicewindow.geometry('%dx%d+%d+%d' % (root.winfo_screenwidth()/2, root.winfo_screenheight()/4, (3*root.winfo_screenwidth()/4 - root.winfo_screenwidth()/8), root.winfo_screenheight()/2 - (root.winfo_screenheight()/3)/2))
        self.choicewindow.resizable(0, 0)
        # add questions label
        question = ttk.Label(self.choicewindow, text=question, font=(None, 14))
        question.config(wraplength=500)
        question.grid(row=0, column=0, sticky=tk.EW, columnspan=3)
        # add text explaining what to do
        # add choices
        ttk.Button(self.choicewindow, text=option1, command=lambda: self.setanddestroy(answeroption=option1)).grid(row=1, column=0, sticky=tk.NSEW)
        ttk.Button(self.choicewindow, text=option2, command=lambda: self.setanddestroy(answeroption=option2)).grid(row=2, column=0, sticky=tk.NSEW)
        ttk.Button(self.choicewindow, text=option3, command=lambda: self.setanddestroy(answeroption=option3)).grid(row=3, column=0, sticky=tk.NSEW)
        # add quit button
        ttk.Button(self.choicewindow, text="Quit", command=lambda: self.setanddestroy(answeroption="QUIT")).grid(row=4, column=0, sticky=tk.NSEW)

        # give weight to rows and column to permit dynamic redraw
        self.choicewindow.columnconfigure((0), weight=1)
        self.choicewindow.rowconfigure((1, 2, 3, 4), weight=1)

        # Buff and pad all children of mainframe
        for child in self.choicewindow.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.choicewindow.wait_window()

    def setanddestroy(self, answeroption):
        if answeroption == "QUIT":
            stabilisationAnswer.set(answeroption)
            self.choicewindow.destroy()
        else:
            time.sleep(0.25)
            stabilisationAnswer.set(answeroption)
            self.choicewindow.destroy()

def disable_event():
    pass

if __name__ == '__main__':
    root = tk.Tk()
    gui = MainApplication(root)
    root.mainloop()

