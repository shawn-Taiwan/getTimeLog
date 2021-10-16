import tkinter as tk
from tkinter import ttk, simpledialog
from tkcalendar import Calendar
from datetime import date
import os

class CalendarDialog(simpledialog.Dialog):
    """Dialog box that displays a calendar and returns the selected date"""
    def body(self, master):
        self.calendar = Calendar(master)
        self.calendar.pack()

    def apply(self):
        self.result = self.calendar.selection_get()
class UI():
    def __init__(self, getXlsx):
        self.getXlsx = getXlsx
        self.startDate = str(date.today().strftime("%Y/%m/%d"))
        self.endDate = str(date.today().strftime("%Y/%m/%d"))

        self.fileNames = []
        self.userIDs = []
        self.readFile()

        self.root = tk.Tk()
        self.root.title('timelog LabProject -> xlsx')
        self.root.geometry('530x70')

        fileNamelabel = tk.Label(self.root, text = "fileName")
        fileNamelabel.grid(column=0, row=0, sticky=tk.W)
        self.fileNameString = tk.StringVar()
        self.fileNameString.set(self.fileNames[0])
        self.fileNameCombobox = ttk.Combobox(self.root, width=35, text=self.fileNameString)
        self.fileNameCombobox['values'] = self.fileNames
        self.fileNameCombobox.bind("<<ComboboxSelected>>", self.selectUserID)
        self.fileNameCombobox.grid(column=1, row=0, padx=10)

        self.selectAllValue = tk.BooleanVar()
        self.selectAllValue.set(False)
        self.selectAllCheckBox = tk.Checkbutton(self.root, text='Select all', var=self.selectAllValue)
        self.selectAllCheckBox.grid(column=2, row=0, padx=10)

        userIDlabel = tk.Label(self.root, text = "userID")
        userIDlabel.grid(column=0, row=1, sticky=tk.W)
        self.userIDString = tk.StringVar()
        self.userIDString.set(self.userIDs[0])
        self.userIDentry = tk.Entry(self.root, width=40, textvariable=self.userIDString)
        self.userIDentry.grid(column=1, row=1, padx=10)

        self.startButtonText = tk.StringVar()
        self.updateStartButtonText()
        self.startButton = tk.Button(self.root, textvariable=self.startButtonText, command=self.openStartDateCalendar)
        self.startButton.grid(column=0, row=2, padx=0)

        self.endButtonText = tk.StringVar()
        self.updateEndButtonText()
        self.endButton = tk.Button(self.root, textvariable=self.endButtonText, command=self.openEndDateCalendar)
        self.endButton.grid(column=1, row=2, padx=0)

        self.submitButton = tk.Button(self.root, text="Submit", command=self.submit)
        self.submitButton.grid(column=2, row=2, padx=0)

        self.root.mainloop()

    def readFile(self):
        fileName = "record.txt"
        filePath = os.path.join(os.path.dirname(__file__), fileName)

        try:
            file = open(filePath)
            lines = file.readlines()
            for index in range(0, len(lines), 2):
                self.fileNames.append(lines[index].replace('\n', ''))
                self.userIDs.append(lines[index+1].replace('\n', ''))
            file.close()
        except:
            print('record.txt is missing...')

    def selectUserID(self, event):
        index = self.fileNames.index(self.fileNameString.get())
        self.userIDString.set(self.userIDs[index])

    def updateStartButtonText(self):
        self.startButtonText.set("Start date: " + self.startDate)

    def updateEndButtonText(self):
        self.endButtonText.set("End date: " + self.endDate)

    def openStartDateCalendar(self):
        calendarDialog = CalendarDialog(self.root)
        self.startDate = calendarDialog.result.strftime("%Y/%m/%d")
        self.updateStartButtonText()

    def openEndDateCalendar(self):
        calendarDialog = CalendarDialog(self.root)
        self.endDate = calendarDialog.result.strftime("%Y/%m/%d")
        self.updateEndButtonText()

    def submitAll(self):
        for index, fileName in enumerate(self.fileNames):
            self.getXlsx(fileName, self.userIDs[index], self.startDate, self.endDate)

    def submit(self):
        if self.selectAllValue:
            self.submitAll()
        elif(self.fileNameString.get() != '' and self.userIDString.get() != ''):
            self.getXlsx(self.fileNameString.get(), self.userIDString.get(), self.startDate, self.endDate)