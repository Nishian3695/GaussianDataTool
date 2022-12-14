import tkinter as tk
class FileVariableExtractor():
    DEFAULT_MARKER = "_"
    def __init__(self, fileName, variableList, marker=DEFAULT_MARKER):
        self._fileName = fileName
        self._variables = variableList
        self._varDict = dict()
        # If marker is list, set beg and end markers to elements in list
        if type(marker) == list:
            # If list length 1 or 2, valid marker
            if 0 < len(marker) < 3:
                self._begMark = marker[0]
                if len(marker) == 2:
                    self._endMark = marker[1]
                else:
                    self._endMark = self._begMark
            # If list length is 0 or > 2, invalid length
            else:
                raise ValueError("Invalid marker length.")
        # If marker is a string, use as beg and end markers
        elif type(marker) == str:
            self._begMark = marker
            self._endMark = marker

    def separateFileName(self):
        stepOne = self._fileName.split(self._begMark)
        for i in range(len(stepOne)):
            element = stepOne[i]
            newElement = element.split(self._endMark)
            stepOne[i] = newElement

        return stepOne        


    def extract(self, varName):
        borderWidth = 3
        newElements = list()
        mainWindow = tk.Tk()

        def getElement(variable, element):
            self._varDict[variable] = element
            mainWindow.destroy()

        frame = tk.Frame(master=mainWindow, relief=tk.RAISED, borderwidth=borderWidth)
        mainLabel = tk.Label(master=frame, text=f'Which element is {varName}?', padx=3, pady=3)
        midRow = len(self._variables)
        frame.grid(row=midRow, column=0)
        mainLabel.pack()

        row = 0
        col = 1
        for thing in self._sepFileName:
            item = thing[0]
            newButton = tk.Button(master=frame, text=item, command=lambda item=item, varName=varName:getElement(varName, item))
            frame.grid(row=row, column=col)
            newButton.pack()            

        mainWindow.mainloop()


    def selectVariables(self):
        self._sepFileName = self.separateFileName()
        self._varDict = dict()
        for variable in self._variables:
            self.extract(variable)
        return self._varDict

def main():
    marker = "_"
    fileName = 'Hello_there_test'
    variables = ["One", "Two", "Three"]
    extractor = FileVariableExtractor(fileName, variables, marker)
    extractor.selectVariables()
if __name__ == "__main__":
    main()
        
