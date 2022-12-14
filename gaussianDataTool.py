import os # To get access to files
import pickle # Save data as bytes to save space
from tkinter import filedialog as fd # To browse and select files
import tkinter as tk # To create graphical interface
from tkinter import ttk # To create tabs in the interface
from file_read_backwards import FileReadBackwards # Allows to read file backwards in memory-efficient way
from filenamer import FileNamer # Names files based on input
from filetextextractor import FileTextExtractor # To extract text from files
from gaussiantoorca import GaussianToOrca # Translate Gaussian to ORCA file format
from filevariableextractor import FileVariableExtractor # To get variables for naming convention

# TODO: On first run prompt user to select where to save output files

# TODO: Handle selection of wrong file (detect end of file and raise error)
# TODO: Complete naming convention
DEBUG = True

global PROGRAM_DATA
PROGRAM_DATA = 'GDTData/GDTData.txt'
global selectedFileList
global saveFileLoc
saveFileLoc = None
global saveFileLocIdx
saveFileLocIdx = 0
global newUser
newUser = False
        
def loadData():
    global PROGRAM_DATA
    global newUser
    global saveFileLoc
    global saveFileLocIdx

    loadList = pickle.load(open(PROGRAM_DATA, 'rb'))
    saveFileLoc = loadList[saveFileLocIdx]
    if saveFileLoc == None:
        newUser = True

def saveData(saveLocation=None):
    global PROGRAM_DATA
    global newUser
    global saveFileLoc

    saveList = [saveFileLoc]
    pickle.dump(saveList, open(PROGRAM_DATA, 'wb'))
    
    # TODO: Markers for naming convetion once implemented
    '''
    begFileName = fileNameMarkBeg['text']
    endFileName = fileNameMarkEnd['text']
    begNewFile = newFileNameMarkBeg['text']
    endNewFile = newFileNameMarkEnd['text']
    '''
    

def createInterface():
    """ Creates the main visual interface for the program """
    global mainWindow
    
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
    selFileDisplay = tk.Label(master=genFrame, text='Selected File(s)', padx=100, pady=5)
    genElements.append(selFileDisplay)
    selFileButton = tk.Button(master=genFrame, text="Select Files", \
                              command=lambda:selectFiles(selFileDisplay))
    genElements.append(selFileButton)

    startButton = tk.Button(master=genFrame, text="Start", command=convertToOrca)
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
    saveFileDisplay = tk.Label(master=advFrame, text='Save Location', padx=100, pady=5)
    advElements.append(saveFileDisplay)
    saveFileButton = tk.Button(master=advFrame, text="Select Location", \
                               command=lambda:selectFiles(saveFileDisplay, True))
    advElements.append(saveFileButton)
    # TODO: Implement naming convention? Not functional for now
    '''
    newFileName = tk.Label(master=advFrame, text="How to name file", \
                            padx=100, pady=5)
    advElements.append(newFileName)
    newFileName2 = tk.Label(master=advFrame, text="(e.g., year_group_{protein}_{ligand}_{aminoacid}", \
                            padx=100, pady=5)
    advElements.append(newFileName2)
    newFileNameInput = tk.Entry(master=advFrame)
    advElements.append(newFileNameInput)
    nameConvLabel = tk.Label(master=advFrame, text="Parts of file name to be inserted into new file names (separate with commas)", \
                            padx=100, pady=5)
    advElements.append(nameConvLabel)
    nameConvLabel2 = tk.Label(master=advFrame, text="(e.g., protein, ligand, project name)", \
                            padx=100, pady=5)
    advElements.append(nameConvLabel2)
    nameConvInput = tk.Entry(master=advFrame)
    advElements.append(nameConvInput)
    fileNameMarkBeg = tk.Label(master=advFrame, text="File name start marker", \
                            padx=100, pady=5)
    advElements.append(fileNameMarkBeg)
    fileNameMarkEnd = tk.Label(master=advFrame, text="File name end marker", \
                            padx=100, pady=5)
    advElements.append(fileNameMarkEnd)
    newFileNameMarkBeg = tk.Label(master=advFrame, text="New file name start marker", \
                            padx=100, pady=5)
    advElements.append(newFileNameMarkBeg)
    newFileNameMarkEnd = tk.Label(master=advFrame, text="New file name end marker", \
                            padx=100, pady=5)
    advElements.append(newFileNameMarkEnd)
    '''
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
        '''
        displayStr = ""
        for fileName in selectedFileList:
            displayStr += fileName
        displayLabel['text'] = displayStr + ", "
        '''
        displayStr = ", ".join(selectedFileList)
        displayLabel['text'] = displayStr
    else:
        # ask directory to save the ORCA files to 
        saveFileLoc = fd.askdirectory()
        displayLabel['text'] = saveFileLoc
        saveData()


def convertToOrca():
    """ Extracts the desired data from the Gaussian output files and converts to ORCA data"""
    global selectedFileList

    primaryMarker = " ***"
    marker = " ------"
    atomMarker = " Charge"
    endAtomMarker = " Add"
    for aFile in selectedFileList:
        dataFound = False
        atomsFound = False
        dataRecorded = False
        with FileReadBackwards(aFile, encoding="utf-8") as frb:
            extractor = FileTextExtractor(marker, frb)
            for i in range(2):
                extractor.passText(primaryMarker)
            dataReversed = extractor.extractText()
            data = list(reversed(dataReversed))
        with open(aFile, 'r') as file:
            extractor = FileTextExtractor([atomMarker, endAtomMarker], file)
            atomLines = extractor.extractText()
        
        atoms = list()
        for aLine in atomLines:
            if aLine != "":
                atomName = aLine[0]
                atoms.append(atomName)
        # Change lines to ORCA input data
        orcaConverter = GaussianToOrca(data, atoms)
        orcaData = orcaConverter.translate()
        writeFile(nameFile(aFile), orcaData)


# TODO: Implement naming convention? Many difficulties
def nameFile(aFile):
    '''Names files based on previous name'''
    splitPath = aFile.split('/')
    fileName = splitPath[-1].split('.')[0]
    return fileName + '_ORCA.inp'
    '''
    """Names a file based on the naming convention used"""
    global varList
    global nameConv
    extractor = FileVariableExtractor(aFile, varList)
    variableDict = extractor.selectVariables()
    namer = FileNamer(['{', '}'])
    newName = namer.nameFile(nameConv, variableDict)
    return newName
    '''


def writeFile(aFile, aFileData):
    global saveFileLoc

    with open(saveFileLoc + '/' + aFile, 'w') as newFile:
        for line in aFileData:
            newFile.write(line + '\n')
    

def promptSaveLoc():
    borderWidth = 3
    horizontalPad = 3
    verticalPad = 3

    popup = tk.Tk()
    promptText = "Before getting started, select a directory where you'd like your ORCA input files to go"
    elements = list()
    frame = ttk.Frame(master=popup, relief=tk.RAISED, borderwidth=borderWidth)
    promptLabel = tk.Label(master=frame, text=promptText, padx=100, pady=5)
    elements.append(promptLabel)
    saveLocDisplay = tk.Label(master=frame, padx=100, pady=5)
    elements.append(saveLocDisplay)
    saveLocBtn = tk.Button(master=frame, text='Select Location', command=lambda:selectFiles(saveLocDisplay, True))
    elements.append(saveLocBtn)
    doneBtn = tk.Button(master=frame, text='Done', command=lambda:popup.destroy())
    elements.append(doneBtn)
    # Add each element in order
    row = 0
    col = 0
    for element in elements:
        frame.grid(row=row, column=col, padx=horizontalPad, pady=verticalPad)
        element.pack()
        row += 1
        
    popup.mainloop()

    
def main():
    """ Extracts and places data appropriately from Gaussian output to Orca input """
    createInterface()

    
# Initialize program
if not os.path.exists(PROGRAM_DATA):
    programDir = PROGRAM_DATA.split('/')[0]
    if not os.path.exists(programDir):
        os.mkdir(programDir)
    open(PROGRAM_DATA, 'x').close()
    saveData()
    newUser = True
else:
    loadData()
if newUser:
    promptSaveLoc()
    
    
# Allows program to run as executable
if __name__ == "__main__":
    main()
