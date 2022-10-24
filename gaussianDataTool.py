import os # To get access to files
from tkinter import filedialog as fd # To browse and select files
import tkinter as tk # To create graphical interface
from file_read_backwards import FileReadBackwards # Allows to read file backwards in memory-efficient way

# TODO: Handle multiple files
global selectedFileList

def createInterface():
    """ Creates the main visual interface for the program """
    borderWidth = 3
    horizontalPad = 3
    verticalPad = 3
    
    mainWindow = tk.Tk()
    frame = tk.Frame(master=mainWindow, relief=tk.RAISED, borderwidth=borderWidth)

    #Make a list of elements in interface to add in order
    guiElements = list()
    # Create Label and Button to select files
    selFileLabel = tk.Label(master=frame, text="Please select the Gaussian files", \
                            padx=100, pady=50)
    guiElements.append(selFileLabel)
    selFileButton = tk.Button(master=frame, text="Select File", command=selectFiles)
    guiElements.append(selFileButton)

    startButton = tk.Button(master=frame, text="Start", command=extractGaussianData)
    guiElements.append(startButton)
    # Add each element in order
    row = 0
    col = 0
    for element in guiElements:
        frame.grid(row=row, column=col, padx=horizontalPad, pady=verticalPad)
        element.pack()
        row += 1

    # Show main interface
    mainWindow.mainloop()

def selectFiles():
    """ Opens dialog to select one or more files and saves the list of
        files to the global variable selectedFileList """
    global selectedFileList
    # askopenfilenames() allows multiple files to be selected and returns a list of strings
    selectedFileList = fd.askopenfilenames()

def extractGaussianData():
    """ Extracts the desired data from the Gaussian output files """
    global selectedFileList
    
    def readLinesUntil(marker, fileReader, recording):
        markerLen = len(marker)
        data = list()
        line = fileReader.readline()
        firstChars = line[:markerLen]
        while firstChars != marker:
            if recording:
                data.append(line.strip())
            line = fileReader.readline()
            firstChars = line[:markerLen]
        return data

    marker = " ------"
    dataFound = False
    dataRecorded = False
    for aFile in selectedFileList:
        with FileReadBackwards(aFile, encoding="utf-8") as frb:
            readLinesUntil(marker, frb, dataFound)
            dataFound = True
            # maybe try recursion instead
            dataReversed = readLinesUntil(marker, frb, dataFound)
            data = list(reversed(dataReversed))
            print(data)

def main():
    """ Extracts and places data appropriately from Gaussian output to Orca input """
    createInterface()

# Allows program to run as executable
if __name__ == "__main__":
    main()
