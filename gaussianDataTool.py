import os # To get access to files
from tkinter import filedialog as fd # To browse and select files
import tkinter as tk # To create graphical interface
from tkinter import ttk # To create tabs in the interface
from file_read_backwards import FileReadBackwards # Allows to read file backwards in memory-efficient way

# TODO: Handle multiple files
# TODO: Handle selection of wrong file (detect end of file and raise error)
# TODO: Complete naming convention
global PROGRAM_DATA 
PROGRAM_DATA = "GDTData.txt"
global selectedFileList
global saveFileLoc
global namingConvention

def createInterface():
    """ Creates the main visual interface for the program """
    borderWidth = 3
    horizontalPad = 3
    verticalPad = 3
    
    mainWindow = tk.Tk()

    # Make multiple tabs
    tabManager = ttk.Notebook(mainWindow)
    tabManager.pack(pady=10, expand=True)

    # General Info. Tab
    genFrame = ttk.Frame(master=tabManager, relief=tk.RAISED, borderwidth=borderWidth)

    # Make a list of elements in interface to add in order
    genElements = list()
    # Create Label and Button to select files
    selFileLabel = tk.Label(master=genFrame, text="Select the Gaussian files", \
                            padx=100, pady=5)    
    genElements.append(selFileLabel)
    selFileDisplay = tk.Label(master=genFrame, padx=100, pady=5)
    genElements.append(selFileDisplay)
    selFileButton = tk.Button(master=genFrame, text="Select Files", \
                              command=lambda:selectFiles(selFileDisplay))
    genElements.append(selFileButton)

    startButton = tk.Button(master=genFrame, text="Start", command=extractGaussianData)
    genElements.append(startButton)
    # Add each element in order
    row = 0
    col = 0
    for element in genElements:
        genFrame.grid(row=row, column=col, padx=horizontalPad, pady=verticalPad)
        element.pack()
        row += 1
    # END: General Info. Tab
    # Advanced Tab
    advFrame = ttk.Frame(master=tabManager, relief=tk.RAISED, borderwidth=borderWidth)
    # List of elements for advanced tab
    advElements = list()
    # Create labels and buttons
    saveFileLabel = tk.Label(master=advFrame, text="Save Location:", padx=100, pady=5)
    advElements.append(saveFileLabel)
    saveFileDisplay = tk.Label(master=advFrame, padx=100, pady=5)
    advElements.append(saveFileDisplay)
    saveFileButton = tk.Button(master=genFrame, text="Select Location", \
                               command=lambda:selectFiles(saveFileDisplay, True))
    nameConvLabel = tk.Label(master=advFrame, text="New File Naming Convention:", \
                            padx=100, pady=5)
    advElements.append(nameConvLabel)
    nameConvInput = tk.Entry(master=advFrame)
    advElements.append(nameConvInput)
    # Add each element in order
    row = 0
    col = 0
    for element in advElements:
        advFrame.grid(row=row, column=col, padx=horizontalPad, pady=verticalPad)
        element.pack()
        row += 1
    # Add both tabs to the main window
    tabManager.add(genFrame, text="General")
    tabManager.add(advFrame, text="Advanced")
    # Show main interface
    mainWindow.mainloop()

def selectFiles(displayLabel, settingSaveLoc=False):
    """ Opens dialog to select one or more files and saves the list of
        files to the global variable selectedFileList """
    global selectedFileList
    global saveFileLoc
    if not settingSaveLoc:
        # askopenfilenames() allows multiple files to be selected and returns a list of strings
        selectedFileList = fd.askopenfilenames()
        displayStr = ""
        for fileName in selectedFileList:
            displayStr += fileName
        displayLabel['text'] = displayStr + ", "
    else:
        # ask directory to save the ORCA files to 
        saveFileLoc = fd.askdirectory()
        displayLabel['text'] = saveFileLoc

def extractGaussianData():
    """ Extracts the desired data from the Gaussian output files """
    global selectedFileList
    global PROGRAM_DATA
    
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
            
            

def nameFile(aFile):
    """Names a file based on the naming convention used"""
    
    
    
def main():
    """ Extracts and places data appropriately from Gaussian output to Orca input """
    createInterface()

# Allows program to run as executable
if __name__ == "__main__":
    main()
