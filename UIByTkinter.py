import tkinter as tk
from tkinter import ttk, simpledialog
from tkcalendar import Calendar

class CalendarDialog(simpledialog.Dialog):
    """Dialog box that displays a calendar and returns the selected date"""
    def body(self, master):
        self.calendar = Calendar(master)
        self.calendar.pack()

    def apply(self):
        self.result = self.calendar.selection_get()

def UI(func):
    root = tk.Tk()
    root.title('timelog to xlsx')
    root.geometry('500x100')

    def openStartDateCalendar():
        global startDate
        cd = CalendarDialog(root)
        startDate = cd.result

    def openEndDateCalendar():
        global endDate
        cd = CalendarDialog(root)
        endDate = cd.result

    def submit():
        func(studentIDString.get(), userIDString.get(), str(startDate).replace('-', '/'), str(endDate).replace('-', '/'))

    studentIDlabel = tk.Label(root, text = "studentID")
    studentIDlabel.grid(column=0, row=0, sticky=tk.W)

    global studentIDString
    studentIDString = tk.StringVar()
    # studentIDString.set("")    # You can decomment this to input your student ID by default 
    studentIDentry = tk.Entry(root, width=40, textvariable=studentIDString)
    studentIDentry.grid(column=1, row=0, padx=10)

    userIDlabel = tk.Label(root, text = "userID")
    userIDlabel.grid(column=0, row=1, sticky=tk.W)

    global userIDString
    userIDString = tk.StringVar()
    # userIDString.set("")    # You can decomment this to input your user ID by default
    userIDentry = tk.Entry(root, width=40, textvariable=userIDString)
    userIDentry.grid(column=1, row=1, padx=10)

    startButton = tk.Button(root, text="Start date calendar", command=openStartDateCalendar)
    endButton = tk.Button(root, text="End date calendar", command=openEndDateCalendar)
    submitButton = tk.Button(root, text="Submit", command=submit)

    startButton.grid(column=0, row=2, padx=0)
    endButton.grid(column=1, row=2, padx=0)
    submitButton.grid(column=2, row=2, padx=0)

    root.mainloop()