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
        global debuggeractive
        global motorlist
        # create the local root
        self.master = master
        self.master.state('zoomed')
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        # Create global tracking variables
        progresstracker = IntVar()
        progresstracker.set(0)
        debuggeractive = IntVar()
        debuggeractive.set(1)

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
        self.button2 = ttk.Button(self.controlpanel, text="Test all subsystems", command=lambda: self.debugger.addtoscreen("Placeholder text"))
        self.button2.grid(row=1, column=0, sticky=tk.NSEW)
        self.button3 = ttk.Button(self.controlpanel, text="Reset all progress", command=lambda: self.debugger.addtoscreen("Placeholder text"))
        self.button3.grid(row=2, column=0, sticky=tk.NSEW)
        self.button4 = ttk.Button(self.controlpanel, text="Admin Mode", command=lambda: self.debugger.addtoscreen("Placeholder text"))
        self.button4.grid(row=3, column=0, sticky=tk.NSEW)
        self.button5 = ttk.Button(self.controlpanel, text="Compress for transfer", command=lambda: self.debugger.addtoscreen("Placeholder text"))
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

        def activatedebugger():
            self.debugger = ScrollingWindow()
            self.debugger.settitle("Twirpy IO Debugger")

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

        # update the status of the power box to Error
        self.controlsubsystem.changestatus(newstatus="Status: System Online")
        # update the button so that it creates a problem filling it with a random power puzzle
        self.controlsubsystem.changebuttontext(newtext="Ready")
        # update the button to now open the power problem window
        self.controlsubsystem.setcommand("pass")
        # change colour background to red
        self.controlsubsystem.changebackground("green")

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
        if newcommand == "motor":
            self.subsystemsbutton.configure(command=lambda: gui.motorerrorprogram())
        if newcommand == "motorproblem":
            self.subsystemsbutton.configure(command=lambda: self.createmotorproblemcore())
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
        global progressarray
        global progresstracker
        answer = StringVar()
        progressarray = [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]

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
                    progresstracker.set(choice(progressarray))

        # Actual problem set
        if progresstracker.get() > 2:
            while True:
                # Beginning of problem set
                if progresstracker.get() == 3:
                    # Problem set 3
                    gui.debugger.addtoscreen("int power_level = 84")
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
                        progressarray.remove(3)
                        if len(progressarray) > 12:
                            progresstracker.set(choice(progressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(progressarray))

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
                        progressarray.remove(4)
                        if len(progressarray) > 12:
                            progresstracker.set(choice(progressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(progressarray))

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
                        progressarray.remove(5)
                        if len(progressarray) > 12:
                            progresstracker.set(choice(progressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(progressarray))

                elif progresstracker.get() == 6:
                    gui.debugger.addtoscreen("int current_power_level = 90")
                    gui.debugger.addtoscreen("int power_requested = 80")
                    gui.debugger.addtoscreen("int total_power_available = 150")
                    gui.debugger.addtoscreen("int emergency_power = 10")
                    gui.debugger.addtoscreen("if (power_requested > 0) AND ((current_power_level + power_requested <= total_power_available))", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Provide Power\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("else if (current_power_level + power_requested <= power_requested + emergency_power)", colour="red")
                    gui.debugger.addtoscreen("{", colour="red")
                    gui.debugger.addtoscreen("  return \"Provide Power (emergency)\"", colour="red")
                    gui.debugger.addtoscreen("}", colour="red")
                    gui.debugger.addtoscreen("if (((current_power_level + power_requested) < threshold) OR (safety_systems_online)))", colour="red")
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
                        progressarray.remove(6)
                        if len(progressarray) > 12:
                            progresstracker.set(choice(progressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(progressarray))

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
                    gui.debugger.addtoscreen("if (energy_excess AND emergency_buffer > 0 AND NOT(conserve_energy)", colour="red")
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
                        progressarray.remove(7)
                        if len(progressarray) > 12:
                            progresstracker.set(choice(progressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(progressarray))

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
                        progressarray.remove(8)
                        if len(progressarray) > 12:
                            progresstracker.set(choice(progressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(progressarray))

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
                        progressarray.remove(9)
                        if len(progressarray) > 12:
                            progresstracker.set(choice(progressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(progressarray))

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
                        progressarray.remove(10)
                        if len(progressarray) > 12:
                            progresstracker.set(choice(progressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(progressarray))


                elif progresstracker.get() == 11:
                    gui.debugger.addtoscreen("bool power_error = False")
                    gui.debugger.addtoscreen("bool circuit_error = False")
                    gui.debugger.addtoscreen("bool blue_tooth_error = False")
                    gui.debugger.addtoscreen("bool battery error = True")
                    gui.debugger.addtoscreen("if (NOT(power_error OR circuit_error) AND (blue_tooth_error OR battery error))", colour="red")
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
                        progressarray.remove(11)
                        if len(progressarray) > 12:
                            progresstracker.set(choice(progressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(progressarray))

                elif progresstracker.get() == 12:
                    gui.debugger.addtoscreen("int internal_temp = 32")
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
                        progressarray.remove(12)
                        if len(progressarray) > 12:
                            progresstracker.set(choice(progressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(progressarray))

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
                        progressarray.remove(13)
                        if len(progressarray) > 12:
                            progresstracker.set(choice(progressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(progressarray))

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
                        progressarray.remove(14)
                        if len(progressarray) > 12:
                            progresstracker.set(choice(progressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(progressarray))

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

                    BooleanChoiceWindow(gui.debugger.swtl.winfo_width(), gui.debugger.swtl.winfo_height(),"Given the inputs, what will this code output?", "Select From Below", option1="Permit Charging", option2="Attempt Charge 2", option3="System Error")

                    if answer.get() == "QUIT":
                        return 1
                    if answer.get() == "System Error":
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation successful", colour="green")
                        progressarray.remove(15)
                        if len(progressarray) > 12:
                            progresstracker.set(choice(progressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(progressarray))

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
                        progressarray.remove(16)
                        if len(progressarray) > 12:
                            progresstracker.set(choice(progressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(progressarray))

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
                        progressarray.remove(17)
                        if len(progressarray) > 12:
                            progresstracker.set(choice(progressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(progressarray))

                elif progresstracker.get() == 18:
                    gui.debugger.addtoscreen("bool power_subsystem_online = False")
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
                        progressarray.remove(18)
                        if len(progressarray) > 12:
                            progresstracker.set(choice(progressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(progressarray))

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
                        progressarray.remove(19)
                        if len(progressarray) > 12:
                            progresstracker.set(choice(progressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(progressarray))

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
                    gui.debugger.addtoscreen("if (NOT(TRUE AND FALSE))", colour="red")
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
                        progressarray.remove(20)
                        if len(progressarray) > 12:
                            progresstracker.set(choice(progressarray))
                            gui.debugger.addtoscreen("Continuing to next error")
                        else:
                            break
                    else:
                        gui.debugger.addtoscreen("Attempting to compile...")
                        gui.debugger.addtoscreen("Compilation failure...", colour="red")
                        gui.debugger.addtoscreen("Continuing to next error")
                        progresstracker.set(choice(progressarray))

        # If arriving here signal success
        # update the status of the power box to Error
        gui.powersubsystem.changestatus(newstatus="Status: Fixed")
        # update the button so that it creates a problem filling it with a random power puzzle
        gui.powersubsystem.changebuttontext(newtext="Repaired")
        # update the button to now open the power problem window
        gui.powersubsystem.setcommand("powerproblem")
        # change colour background to green
        gui.powersubsystem.changebackground("green")
        gui.debugger.addtoscreen("Power Subsystem Debug Complete", colour="green")

    # The motor problem core libary lookup
    def createmotorproblemcore(self):
        # Problem Tutorial
        gui.debugger.addtoscreen("Problem Tutorial Start", colour="green")
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
        gui.debugger.addtoscreen("Problem Tutorial Start", colour="green")

        # set the progressmarker to zero
        progresstracker.set(1)

        # create an array containing all questions bar the 1st which is an example
        progressarray = [3,4,5,6,7,8,9,10,11,12,13,14]


        # the training example
        if progresstracker.get() == 1:
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
            progresstracker.set(progresstracker.get() + 1)

        # extra information
        gui.debugger.addtoscreen("Some libaries themselves make use of functions defined in other libaries, which you will therefore also have to include")
        gui.debugger.addtoscreen("This is known as dependencies")

        if progresstracker.get() == 2:
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
            progresstracker.set(progresstracker.get() + 1)

        # teach about conflicting libaries
        gui.debugger.addtoscreen("Finally, some libaries can conflict with each other meaning that they both have a function with exactly the same name")
        gui.debugger.addtoscreen("If both libaries are included in the same file. then the computer doesn't know which version of the function to use, and so throws an error")
        gui.debugger.addtoscreen("To solve this problem you will need to use specialist libaries that have been built to correct this problem")

        # choose a random number to start the actual questions
        progresstracker.set(choice(progressarray))
        # variable to store number completed

        while len(progressarray) > 8:
            if progresstracker.get() == 3:
                gui.debugger.addtoscreen("Undefined checksafetysettings Function Error", colour="red")
                gui.debugger.addtoscreen("Undefined cleararray Function Error", colour="red")

                NineChoiceWindow("stdiopy", "numpy", "twirpytoi", "openlib", "xmlconvert", "csv", "numpy", "gtxtest", "numpycafix")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["stdiopy", "numpycafix", "twirpystoi"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(progressarray) > 8:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    progressarray.remove(3)
                    progresstracker.set(choice(progressarray))
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")
                    progresstracker.set(choice(progressarray))

            if progresstracker.get() == 4:
                gui.debugger.addtoscreen("Undefined readcsv Function Error", colour="red")
                gui.debugger.addtoscreen("Undefined writeline Function Error", colour="red")
                gui.debugger.addtoscreen("Undefined readc Function Error", colour="red")

                NineChoiceWindow("stdiopy", "numpy", "twirpytoi", "openlib", "xmlconvert", "csv", "numpy", "gtxtest", "crypto")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["csv"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(progressarray) > 8:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    progressarray.remove(4)
                    progresstracker.set(choice(progressarray))
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstracker.get() == 5:
                gui.debugger.addtoscreen("Undefined readcsv Function Error")
                gui.debugger.addtoscreen("Undefined writecsv Function Error")
                gui.debugger.addtoscreen("Undefined print Function Error")
                gui.debugger.addtoscreen("Undefined systemindepentint Function Error")
                gui.debugger.addtoscreen("Undefined checksafetysettings Function Error")

                NineChoiceWindow("stdiopy", "numpy", "twirpytoi", "openlib", "xmlconvert", "csv", "numpy", "gtxtest", "crypto")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["csv", "stdiopy", "openlib", "twirpystoi"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(progressarray) > 8:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    progressarray.remove(5)
                    progresstracker.set(choice(progressarray))
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstracker.get() == 6:
                gui.debugger.addtoscreen("Undefined guessnext Function Error")
                gui.debugger.addtoscreen("Undefined cleararray Function Error")

                NineChoiceWindow("stdiopy", "numpy", "evolve", "openlib", "xmlconvert", "csv", "numpy", "numpycafix", "crypto")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["evolve", "stdiopy", "numpycafix", "openlib"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(progressarray) > 8:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    progressarray.remove(6)
                    progresstracker.set(choice(progressarray))
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstracker.get() == 7:
                gui.debugger.addtoscreen("Undefined readcsv Function Error")
                gui.debugger.addtoscreen("Undefined xmlconvert Function Error")

                NineChoiceWindow("stdiopy", "numpy", "twirpytoi", "openlib", "xmlconvert", "csv", "numpy", "xmlconvert", "crypto")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["csv", "numpy", "xmlconvert"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(progressarray) > 8:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    progressarray.remove(7)
                    progresstracker.set(choice(progressarray))
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstracker.get() == 8:
                gui.debugger.addtoscreen("Undefined calculaterms Function Error")
                gui.debugger.addtoscreen("Undefined systemindepentint Function Error")
                gui.debugger.addtoscreen("Undefined readjson Function Error")

                NineChoiceWindow("openlib", "numpy", "twirpytoi", "scrambledOGG", "xmlconvert", "csv", "numpy", "gtxtest", "csv")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["scrambledOGG", "numpy", "openlib", "csv"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(progressarray) > 8:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    progressarray.remove(8)
                    progresstracker.set(choice(progressarray))
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstracker.get() == 9:
                gui.debugger.addtoscreen("Undefined multiplyarray Function Error")
                gui.debugger.addtoscreen("Undefined print Function Error")
                gui.debugger.addtoscreen("Undefined cleararray Function Error")
                gui.debugger.addtoscreen("Undefined readcsv Function Error")
                gui.debugger.addtoscreen("Undefined csvconvert Function Error")


                NineChoiceWindow("numpycafix", "numpy", "stdiopy", "openlib", "xmlconvert", "csv", "numpy", "gtxtest", "crypto")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["numpycafix", "stdiopy", "xmlconvert", "csv"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(progressarray) > 8:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    progressarray.remove(9)
                    progresstracker.set(choice(progressarray))
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstracker.get() == 10:
                gui.debugger.addtoscreen("Undefined calculaterms Function Error")
                gui.debugger.addtoscreen("Undefined writeline Function Error")
                gui.debugger.addtoscreen("Undefined calculaterms Function Error")

                NineChoiceWindow("scrambledOGG", "numpy", "twirpytoi", "openlib", "xmlconvert", "csv", "numpy", "numpycafix", "crypto")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["xmlconvert", "scrambledOGG", "numpycafix"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(progressarray) > 8:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    progressarray.remove(10)
                    progresstracker.set(choice(progressarray))
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstracker.get() == 11:
                gui.debugger.addtoscreen("Undefined decodejson Function Error")
                gui.debugger.addtoscreen("Undefined multiplyarray Function Error")
                gui.debugger.addtoscreen("Undefined print Function Error")
                gui.debugger.addtoscreen("Undefined cleararray Function Error")


                NineChoiceWindow("json", "numpy", "twirpytoi", "openlib", "xmlconvert", "csv", "numpy", "stdiopy", "numpycafix")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["numpycafix", "stdiopy", "json"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(progressarray) > 8:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    progressarray.remove(11)
                    progresstracker.set(choice(progressarray))
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstracker.get() == 12:
                gui.debugger.addtoscreen("Undefined windowspatch Function Error")
                gui.debugger.addtoscreen("Undefined macpatch Function Error")
                gui.debugger.addtoscreen("Undefined calculaterms Function Error")
                gui.debugger.addtoscreen("Undefined readjson Function Error")
                gui.debugger.addtoscreen("Undefined calculaterms Function Error")
                gui.debugger.addtoscreen("Undefined genetricalogithm Function Error")

                NineChoiceWindow("scrambledOGG", "numpy", "json", "openlib", "xmlconvert", "csv", "numpy", "evolve", "crypto")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["openlib", "scrambledOGG", "json", "evolve"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(progressarray) > 8:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    progressarray.remove(12)
                    progresstracker.set(choice(progressarray))
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstracker.get() == 13:
                gui.debugger.addtoscreen("Undefined print Function Error")
                gui.debugger.addtoscreen("Undefined input Function Error")
                gui.debugger.addtoscreen("Undefined insert Function Error")
                gui.debugger.addtoscreen("Undefined read Function Error")

                NineChoiceWindow("stdiopy", "numpy", "twirpytoi", "openlib", "xmlconvert", "csv", "numpy", "gtxtest", "crypto")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["stdiopy"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(progressarray) > 8:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    progressarray.remove(13)
                    progresstracker.set(choice(progressarray))
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

            if progresstracker.get() == 14:
                gui.debugger.addtoscreen("Undefined evolve Function Error")

                NineChoiceWindow("stdiopy", "numpy", "twirpytoi", "openlib", "scrambledOGG", "csv", "numpy", "gtxtest", "addtoscreen")

                # check to see if quit in array
                if "QUIT" in motorlist:
                    return 1
                # if correct answer
                if self.comparearray(["evolve", "numpy", "scrambledOGG"], motorlist):
                    gui.debugger.addtoscreen("Correct libaries selected", colour="green")
                    if len(progressarray) > 8:
                        break
                    gui.debugger.addtoscreen("Proceeding to next problem", colour="green")
                    progressarray.remove(14)
                    progresstracker.set(choice(progressarray))
                else:
                    gui.debugger.addtoscreen("Incorrect libaries selected", colour="red")
                    gui.debugger.addtoscreen("Proceeding to next problem ", colour="red")

        # End of questions
        gui.motorsubsystem.changestatus(newstatus="Status: Fixed")
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

def disable_event():
    pass

if __name__ == '__main__':
    root = tk.Tk()
    gui = MainApplication(root)
    root.mainloop()

