"""
filenamer.py

Names files using the fileNamer class
fileNamer takes a marker, string and list as arguments
The marker acts as a notifier to insert the next element in
the list into the file name.
The marker can be either a single character or a 2-element list
which will contain the beginning and end markers, respectively.
The string is the general format, which should include
the marker(s) in order to insert the list elements into the string.
"""
class FileNamer():
    """Names files using marker(s) (strings) that are used to insert
        a variable from a dictionary of variables into a general
        format, fileStr"""
    def __init__(self, marker):
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


    def nameFile(self, fileStr, variablesDict):
        """Takes a string containing the fileNamer's markers and
           inserts variables into their appropriate places.
           Returns a string."""
        fileName = ""
        i = 0
        while i < len(fileStr):
            if fileStr[i] == self._begMark:
                insStr = ""
                i += 1
                while fileStr[i] != self._endMark:
                    insStr += fileStr[i]
                    i += 1
                fileName += variablesDict[insStr]
            else:
                fileName += fileStr[i]
            i += 1
        return fileName
            

def main():
    namer = FileNamer(["{", "}"])
    variables = {"lig":"A", "pro":"6nzp", "inter":"arg"}
    testName = "Ligand_{lig}_Protein_{pro}_With_{inter}"
    print(namer.nameFile(testName, variables))

if __name__ == "__main__":
    main()
            
