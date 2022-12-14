"""Merges .gjf files for a ligand and receptor and combines them into
a single file, preparing it for input into Gaussian"""
class GaussianInputMerger():
    method = "#P HF/6-31+G* Opt=ModRedundant NoSymm test"
    def __init__(self, ligFile, method=method):
        # File of the ligand
        self.ligFile = ligFile
        # What method to use
        self.method = method
        
    # TODO: Add way to name new files?
    def addLigand(self):
        '''Combines the files of the interactions into a single file for
        Gaussian input'''
        argPathSplit = self.interFile.split('/')
        argName = argPathSplit[-1]
        ligPathSplit = self.ligFile.split('/')
        ligName = ligPathSplit[-1]
        newFile = argName[:len(argName) - 4] + '_' + ligName[:len(ligName) - 4] + '.com'
        self.fixedAtoms = list()
        self.atomCount = 1
        self.fileNum = 0
        def writeAtoms(aFile):
            # Add number of files seen
            self.fileNum += 1
            with open(aFile, 'r') as file:
                lineIter = iter(file.readlines())
                line = next(lineIter)
                # Skip lines until reaching multiplicity
                # First character should be digit at multiplicity in GausView output
                while not line[0].isdigit():
                    line = next(lineIter)
                # If first file add multiplicity. Else go to next line
                if self.fileNum == 1:
                    data.append(line.strip())
                line = next(lineIter)
                # Write atoms to new file until reaching newline
                # (newline signifies end of atoms in GausView output)
                while line[0] != '\n':
                    data.append(line.strip())
                    # If not a hydrogen, a fixed atom, so add to fixedAtoms list
                    if line[1] != 'H':
                        self.fixedAtoms.append(self.atomCount)
                    self.atomCount += 1
                    line = next(lineIter)
                    
        #with open(newFile, 'w') as newF:
        data = list()
        data.append(self.method + '\n')
        data.append(newFile + '\n')
        writeAtoms(self.interFile)
        writeAtoms(self.ligFile)
        data.append('')
        for fixedAtom in self.fixedAtoms:
            data.append(str(fixedAtom) + ' F')

        return data

    def getOutputData(self):
        '''Returns the name of the combined file'''
        return self.addLigand()
    
    # Setters and Getters
    def getLigFile(self):
        return self.ligFile
    def setLigFile(self, ligFile):
        self.ligFile = ligFile
    def getInterFile(self):
        return self.interFile
    def setInterFile(self, interFile):
        self.interFile = interFile
    def getMethod(self):
        return self.method
    def setMethod(self, method):
        self.method = method
