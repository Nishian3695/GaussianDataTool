import os # To access files
"""
filetextextractor.py

Extracts text from a .txt file by reading until a user-specified
marker. The program then records data that will be returned up to
(but not including) an end marker.
"""
class FileTextExtractor():
    """Extracts text from a .txt file using a beginning and
        end marker to determine when to record the text, and
        thus what to return. The program will stop once done
        recording the text. The data will be returned as a list
        which each element being a line in the .txt file read."""
    def __init__(self, marker, fileReader):
        self.setMarker(marker)
        self._fileReader = fileReader


    def readLines(self, marker):
        """Reads the lines in the .txt file. If
            self._recording is True, then the lines
            recorded will be returned as a list"""
        markerLen = len(marker)
        data = list()
        line = self._fileReader.readline()
        while line[:markerLen] != marker:
            if self._recording:
                data.append(line.strip())
            line = self._fileReader.readline()
        return data


    def passText(self, marker):
        """Passes all text up to and including a specified
            marker without recording data."""
        self._recording = False
        self.readLines(marker)

        
    def extractText(self, recording=False):
        """Reads file up until FileTextExtractor's marker. After this point,
            data is recorded in a list (with lines in the .txt file being
            an element in the list) until but not including the end marker"""
        self._recording = recording
        self.readLines(self._begMark)
        if not self._recording:
            self._recording = True
            extractedText = self.readLines(self._endMark)
        return extractedText
        

    def setMarker(self, marker):
        """Changes the current marker to something different. Can
            be inputted as a single string or as a list of two
            strings."""
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


    def setFileReader(self, fileReader):
        """Changes file reader"""
        self._fileReader = fileReader


    def getMarker(self):
        """Returns the values for the beginning and end markers as tuple"""
        return (self._begMark, self._endMark)


    def getFileReader(self):
        """Returns current file reader"""
        return self._fileReader
