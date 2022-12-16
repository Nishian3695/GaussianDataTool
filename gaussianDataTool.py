import os # To get access to files
import pickle # Save data as bytes to save space
from tkinter import filedialog as fd # To browse and select files
import tkinter as tk # To create graphical interface
from tkinter import ttk # To create tabs in the interface
from tkinter import messagebox
from file_read_backwards import FileReadBackwards # Allows to read file backwards in memory-efficient way
from GDTData.filetextextractor import FileTextExtractor # To extract text from files
from GDTData.gaussiantoorca import GaussianToOrca # Translate Gaussian to ORCA file format
from GDTData.gaussianInputMerger import GaussianInputMerger # Translates .txt files for an interaction into Gaussian input


class gaussianDataTool():
    GAUSSIAN = 'Gaussian'
    ORCA = 'ORCA'
    PROGRAM_DATA = 'GDTData/GDTData.txt'
    BORDER_WIDTH = 3
    HORIZONTAL_PAD = 3
    VERTICAL_PAD = 3

    def __init__(self):
        '''Initializes the data tool'''
        self.orcaSaveFileLoc = None
        self.orcaSaveFileLocIdx = 0
        self.gausSaveFileLoc = None
        self.gausSaveFileLocIdx = 1
        self.newUser = False
        self.cont = True
        self.type = None

        # If program's data path doesn't exist, create it
        if not os.path.exists(self.PROGRAM_DATA):
            self.checkPaths()
        else:
            self.loadData()


    def onClose(self):
        if tk.messagebox.askokcancel('Quit', 'Are you sure you want to quit?'):
            self.cont = False
            self.mainWindow.destroy()

        
    def checkPaths(self):
        '''Checks if data path exists. If not, creates it'''
        programDir = self.PROGRAM_DATA.split('/')[0]
        if not os.path.exists(programDir):
            os.mkdir(programDir)
        open(self.PROGRAM_DATA, 'x').close()
        # Save the current saveLoc paths
        self.saveData()
        # Since data file did not exist, definitely a new user
        self.newUser = True


    def checkIfNewUser(self):
        '''Checks if user is a new user based on if they selected
        a location to save their files for the program being used'''
        if self.type == self.GAUSSIAN and self.gausSaveFileLoc == None or\
           self.type == self.ORCA and self.orcaSaveFileLoc == None:
            self.promptSaveLoc()


    def loadData(self):
        '''Loads previously-saved data from tool's data file'''
        loadList = pickle.load(open(self.PROGRAM_DATA, 'rb'))
        self.orcaSaveFileLoc = loadList[self.orcaSaveFileLocIdx]
        self.gausSaveFileLoc = loadList[self.gausSaveFileLocIdx]


    def saveData(self, saveLocation=None):
        '''Saves the save locations for the program'''
        saveList = [self.orcaSaveFileLoc, self.gausSaveFileLoc]
        pickle.dump(saveList, open(self.PROGRAM_DATA, 'wb'))


    def centerScreenCoor(self, window, winWidth, winHeight):
        screenW = window.winfo_screenwidth()
        screenH = window.winfo_screenheight()
        x = (screenW / 2) - (winWidth / 2)
        y = (screenH / 2) - (winHeight / 2)
        return (winWidth, winHeight, x, y)


    def chooseProgram(self):
        '''Creates interface for the user to select whether they want
            to create Gaussian or ORCA input files'''

        def startGausInput():
            self.type = self.GAUSSIAN
            window.destroy()
            self.checkIfNewUser()
            self.createInterface()
        def startOrcaInput():
            self.type = self.ORCA
            window.destroy()
            self.checkIfNewUser()
            self.createInterface()
        
        window = tk.Tk()
        winWidth = 500
        winHeight = 150
        frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=self.BORDER_WIDTH)
        displayStr = 'Please choose which files you want to make'
        disLabel = tk.Label(master=frame, text=displayStr, padx=100, pady=5)
        frame.grid(row=0, column=1, padx=self.HORIZONTAL_PAD, pady=self.VERTICAL_PAD)
        disLabel.pack()
        gausIn = tk.Button(master=frame, text='Gaussian Input', command=lambda:startGausInput())
        frame.grid(row=1, column=0, padx=self.HORIZONTAL_PAD, pady=self.VERTICAL_PAD)
        gausIn.pack()
        orcaIn = tk.Button(master=frame, text='ORCA Input', command=lambda:startOrcaInput())
        frame.grid(row=1, column=3, padx=self.HORIZONTAL_PAD, pady=self.VERTICAL_PAD)
        orcaIn.pack()
        
        window.mainloop()


    def createInterface(self):
        """ Creates the main visual interface for the program """
        def start():
            if self.type == GAUSSIAN:
               convertToGaussian()
            elif self.type == ORCA:
                convertToOrca()
            self.mainWindow.destroy()
        
        self.mainWindow = tk.Tk()
        # Make multiple tabs
        tabManager = ttk.Notebook(self.mainWindow)
        tabManager.pack(pady=10, expand=True)
        # General Info. Tab
        genFrame = ttk.Frame(master=tabManager, relief=tk.RAISED, borderwidth=self.BORDER_WIDTH)
        # Make a list of elements in interface to add in order
        genElements = list()
        # Create Label and Button to select files
        selFileLabel = tk.Label(master=genFrame, text=f"Select the files to create {self.type} input", \
                                padx=100, pady=5)    
        genElements.append(selFileLabel)
        if self.type == self.ORCA:
            selFileDisplay = tk.Label(master=genFrame, text='Selected File(s) will be listed here', padx=100, pady=5)
            genElements.append(selFileDisplay)
            selFileButton = tk.Button(master=genFrame, text="Select Files", \
                                      command=lambda:self.selectFiles(selFileDisplay))
            genElements.append(selFileButton)
            startButton = tk.Button(master=genFrame, text="Start", command=self.convertToOrca)
            genElements.append(startButton)
        elif self.type == self.GAUSSIAN:
            interFileDisplay = tk.Label(master=genFrame, text='Amino acid file(s)', padx=100, pady=5)
            genElements.append(interFileDisplay)
            interFileBtn = tk.Button(master=genFrame, text='Select Amino Acid Files', command=lambda:self.selectFiles(interFileDisplay, interLig='Inter'))
            genElements.append(interFileBtn)
            ligFileDisplay = tk.Label(master=genFrame, text='Ligand file', padx=100, pady=5)
            genElements.append(ligFileDisplay)
            ligFileBtn = tk.Button(master=genFrame, text='Select Ligand File', command=lambda:self.selectFiles(ligFileDisplay, interLig='Lig'))
            genElements.append(ligFileBtn)
            startButton = tk.Button(master=genFrame, text="Start", command=lambda:self.convertToGaussian())
            genElements.append(startButton)
        # Add each element in order
        row = 0
        col = 0
        for element in genElements:
            genFrame.grid(row=row, column=col, padx=self.HORIZONTAL_PAD, pady=self.VERTICAL_PAD)
            element.pack()
            row += 1
        # END: General Info. Tab
        # Advanced Tab
        advFrame = ttk.Frame(master=tabManager, relief=tk.RAISED, borderwidth=self.BORDER_WIDTH)
        # List of elements for advanced tab
        advElements = list()
        # Create labels and buttons
        saveFileLabel = tk.Label(master=advFrame, text="Save Location:", padx=100, pady=5)
        advElements.append(saveFileLabel)
        saveFileDisplay = tk.Label(master=advFrame, text='Save Location', padx=100, pady=5)
        advElements.append(saveFileDisplay)
        saveFileButton = tk.Button(master=advFrame, text="Select Location", \
                                   command=lambda:self.selectFiles(saveFileDisplay, True))
        advElements.append(saveFileButton)
        
        # Add each element in order
        row = 0
        col = 0
        for element in advElements:
            advFrame.grid(row=row, column=col, padx=self.HORIZONTAL_PAD, pady=self.VERTICAL_PAD)
            element.pack()
            row += 1
        # Add both tabs to the main window
        tabManager.add(genFrame, text="General")
        tabManager.add(advFrame, text="Advanced")
        # Show main interface
        self.mainWindow.protocol("WM_DELETE_WINDOW", self.onClose)        
        self.mainWindow.mainloop()


    def checkFiles(self, aFileList):
        '''Returns true if all files in aFileList are .gjf files.
            Returns false otherwise'''
        gaussianStart = ' Entering Gaussian System'
        for file in aFileList:
            with open(file, 'r') as rFile:
                if gaussianStart not in rFile.readline()[:len(gaussianStart)]:
                    return False
        return True


    def selectFiles(self, displayLabel, settingSaveLoc=False, interLig=None):
        '''Opens dialog to select one or more files and saves the list of
            files to the global variable selectedFileList'''
        validFiles = False
        if not settingSaveLoc and self.type == self.ORCA:
            # askopenfilenames() allows multiple files to be selected and returns a list of strings
            self.selectedFileList = fd.askopenfilenames()
            validFiles = self.checkFiles(self.selectedFileList)
            if not validFiles:
                messagebox.showerror('Incorrect File Type', 'At least one selected file is an improper type.')
                displayLabel['text'] = 'Selected File(s)'
            else:
                displayList = list()
                for file in self.selectedFileList:
                    displayList.append(file.split('/')[-1])
                displayStr = ", ".join(displayList)
                displayLabel['text'] = displayStr
        elif not settingSaveLoc and self.type == self.GAUSSIAN:
            if interLig == 'Inter':
                self.interFiles = fd.askopenfilenames()
                displayList = list()
                for file in self.interFiles:
                    displayList.append(file.split('/')[-1])
                displayStr = ", ".join(displayList)
                displayLabel['text'] = displayStr
            elif interLig == 'Lig':
                self.ligFile = fd.askopenfilename()
                displayLabel['text'] = self.ligFile.split('/')[-1]
        elif self.type == self.ORCA:
            # ask directory to save the ORCA files to 
            self.orcaSaveFileLoc = fd.askdirectory()
            displayLabel['text'] = self.orcaSaveFileLoc.split('/')[-1]
            self.saveData()
        elif self.type == self.GAUSSIAN:
            # ask directory to save the Gaussian files to 
            self.gausSaveFileLoc = fd.askdirectory()
            displayLabel['text'] = self.gausSaveFileLoc.split('/')[-1]
            self.saveData()


    def convertToOrca(self):
        """ Extracts the desired data from the Gaussian output files and converts to ORCA data"""
        primaryMarker = " ***"
        marker = " ------"
        jobNameMarker = ' (Enter'
        atomMarker = " Charge"
        endAtomMarker = " Add"
        for aFile in self.selectedFileList:
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
                extractor.passText(jobNameMarker)
                for i in range(2):
                    extractor.nextLine()
                jobName = extractor.getCurLine().strip()
                atomLines = extractor.extractText()
            
            atoms = list()
            for aLine in atomLines:
                if aLine != "":
                    atomName = aLine[0]
                    atoms.append(atomName)
            # Change lines to ORCA input data
            orcaConverter = GaussianToOrca(data, atoms)
            orcaData = orcaConverter.translate()
            self.writeFile(self.nameFile(jobName), orcaData)
        messagebox.showinfo('Done')


    def convertToGaussian(self):
        inputMerger = GaussianInputMerger(self.ligFile)
        for file in self.interFiles:
            inputMerger.setInterFile(file)
            data = inputMerger.getOutputData()
            interNameExt = file.split('/')[-1]
            interName = interNameExt.split('.')[0]
            ligNameExt = self.ligFile.split('/')[-1]
            ligName = ligNameExt.split('.')[0]
            name = f"{interName}_{ligName}.com"
            self.writeFile(name, data)
        messagebox.showinfo('Done')


    def nameFile(self, aJobName):
        '''Names files based on used job name'''
        if self.type == self.ORCA:
            return aJobName + '_ORCA.inp'


    def writeFile(self, aFile, aFileData):
        if self.type == self.ORCA:
            saveLoc = self.orcaSaveFileLoc
        elif self.type == self.GAUSSIAN:
            saveLoc = self.gausSaveFileLoc
        with open(saveLoc + '/' + aFile, 'w') as newFile:
            for line in aFileData:
                newFile.write(line + '\n')


    def promptSaveLoc(self):
        '''Prompts new user to select a save location for created ORCA
        input files to go'''

        popup = tk.Tk()
        promptText = f"Before getting started, select a directory where you'd like your {self.type} input files to go"
        elements = list()
        frame = ttk.Frame(master=popup, relief=tk.RAISED, borderwidth=self.BORDER_WIDTH)
        promptLabel = tk.Label(master=frame, text=promptText, padx=100, pady=5)
        elements.append(promptLabel)
        saveLocDisplay = tk.Label(master=frame, padx=100, pady=5)
        elements.append(saveLocDisplay)
        saveLocBtn = tk.Button(master=frame, text='Select Location', command=lambda:self.selectFiles(saveLocDisplay, True))
        elements.append(saveLocBtn)
        doneBtn = tk.Button(master=frame, text='Done', command=lambda:popup.destroy())
        elements.append(doneBtn)
        # Add each element in order
        row = 0
        col = 0
        for element in elements:
            frame.grid(row=row, column=col, padx=self.HORIZONTAL_PAD, pady=self.VERTICAL_PAD)
            element.pack()
            row += 1
            
        popup.mainloop()


    def popup(self, displayText):
        '''Creates a popup with the displayText'''

        def canc():
            self.cont = False
            self.mainWindow.destroy()
            popup.destroy()


def main():
    dataTool = gaussianDataTool()
    dataTool.chooseProgram()


# Allows program to run as executable
if __name__ == "__main__":
    main()
