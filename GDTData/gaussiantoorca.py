class GaussianToOrca():
        
    # Constants for ORCA files
    MON2CHARGEMUL = '* xyz 0 1'
    BEG_LINE1 = "! RIJK RI-B2PLYP D3BJ def2-QZVP def2/JK def2-QZVPP/C TIGHTSCF GRID5 FINALGRID6 PMODEL PAL2"
    BEG_LINE2 = "%maxcore 32000"
    BEG_LINE3 = '%base "dimer"'
    BEG_LINE4 = '%id "dimer"'
    #BEG_LINE5 = "* xyz 1 1" # is charge and multiplicity? if so, change
    GHOST1_LINE1 = "*"
    GHOST1_LINE2 = "$new_job"
    GHOST1_LINE3 = BEG_LINE1
    GHOST1_LINE4 = BEG_LINE2
    GHOST1_LINE5 = '%base "monomer1_ghost"'
    GHOST1_LINE6 = '%id "monomer1_ghost"'
    GHOST1_LINE7 = MON2CHARGEMUL
    GHOST2_LINE1 = GHOST1_LINE1
    GHOST2_LINE2 = GHOST1_LINE2
    GHOST2_LINE3 = BEG_LINE1
    GHOST2_LINE4 = BEG_LINE2
    GHOST2_LINE5 = '%base "monomer2_ghost"'
    GHOST2_LINE6 = '%id "monomer2_ghost"'
    #GHOST2_LINE7 = '* xyz 0 1'
    MON1_LINE1 = GHOST1_LINE1
    MON1_LINE2 = GHOST1_LINE2
    MON1_LINE3 = BEG_LINE1
    MON1_LINE4 = BEG_LINE2
    MON1_LINE5 = '%base "monomer1"'
    MON1_LINE6 = '%id "monomer1"'
    #MON1_LINE7 = GHOST2_LINE7
    MON2_LINE1 = GHOST1_LINE1
    MON2_LINE2 = GHOST1_LINE2
    MON2_LINE3 = BEG_LINE1
    MON2_LINE4 = BEG_LINE2
    MON2_LINE5 = '%base "monomer2"'
    MON2_LINE6 = '%id "monomer2"'
    MON2_LINE7 = MON2CHARGEMUL
    END_LINE1 = GHOST1_LINE1
    #BEGLINES = [BEG_LINE1, BEG_LINE2, BEG_LINE3, BEG_LINE4, BEG_LINE5]
    BEGLINES = [BEG_LINE1, BEG_LINE2, BEG_LINE3, BEG_LINE4]
    GHOST1LINES = [GHOST1_LINE1, GHOST1_LINE2, GHOST1_LINE3, GHOST1_LINE4, GHOST1_LINE5, \
                   GHOST1_LINE6, GHOST1_LINE7]
    #GHOST2LINES = [GHOST2_LINE1, GHOST2_LINE2, GHOST2_LINE3, GHOST2_LINE4, GHOST2_LINE5, \
    #               GHOST2_LINE6, GHOST2_LINE7]
    GHOST2LINES = [GHOST2_LINE1, GHOST2_LINE2, GHOST2_LINE3, GHOST2_LINE4, GHOST2_LINE5, \
                   GHOST2_LINE6]
    #MON1LINES = [MON1_LINE1, MON1_LINE2, MON1_LINE3, MON1_LINE4, MON1_LINE5, MON1_LINE6, \
    #             MON1_LINE7]
    MON1LINES = [MON1_LINE1, MON1_LINE2, MON1_LINE3, MON1_LINE4, MON1_LINE5, MON1_LINE6]
    MON2LINES = [MON2_LINE1, MON2_LINE2, MON2_LINE3, MON2_LINE4, MON2_LINE5, MON2_LINE6, \
                 MON2_LINE7]
    # END: Constants for ORCA files

    def __init__(self, dataList, atomList, charge, multiplicity):
        self._data = dataList
        self._atoms = atomList
        self._charge = charge
        self._mul = multiplicity
        chargeMul = f"* xyz {self._charge} {self._mul}"
        self.BEGLINES.append(chargeMul)
        self.GHOST2LINES.append(chargeMul)
        self.MON1LINES.append(chargeMul)


    def findMon2Index(self):
        """Finds and returns the first index Monomer 2 starts"""
        foundH = False
        foundMon2 = False
        lineIdx = 0
        while not foundMon2 and lineIdx != len(self._orcaData):
            line = self._orcaData[lineIdx]
            if foundH and "H" not in line:
                foundMon2 = True
                return lineIdx
            elif "H" in line:
                foundH = True
            lineIdx += 1
        return False

        
    def addGhost(self, aList):
        """Adds colon to line after atom name for ghost in ORCA input"""
        monList = aList.copy()
        for lineIdx in range(len(monList)):
            line = monList[lineIdx]
            newLine = line[:2] + ":" + line[2:]
            monList[lineIdx] = newLine
        return monList


    def translate(self):
        # Delete each line's center number, atomic number, and atomic type
        newData = list()
        atomIdx = 0
        for line in self._data:
            spaceCount = 0
            charIdx = 0
            isOneGap = False
            while spaceCount < 3:
                char = line[charIdx]
                if char == " " and not isOneGap:
                    spaceCount += 1
                    isOneGap = True
                elif char != " ":
                    isOneGap = False
                charIdx += 1
            newLine = line[charIdx:].strip()
            newLine = " " + self._atoms[atomIdx] + (" " * 6) + newLine
            newData.append(newLine)
            atomIdx += 1
        self._orcaData = newData
        # Set up in ORCA file format
        self._mon2Index = self.findMon2Index()
        retList = list()
        # Add beginning header lines
        retList.extend(self.BEGLINES)
        # Add monomers 1 and 2 lines
        retList.extend(self._orcaData)
        # Add ghost 1 header lines
        retList.extend(self.GHOST1LINES)
        # Get monomers
        mon1 = self._orcaData[:self._mon2Index]
        mon2 = self._orcaData[self._mon2Index:]
        # Create ghosts
        ghost1 = self.addGhost(mon1)
        ghost2 = self.addGhost(mon2)
        # Add ghost 1 lines
        ghost1Mon2 = ghost1.copy()
        ghost1Mon2.extend(mon2)
        retList.extend(ghost1Mon2)
        # Add ghost 2 header lines
        retList.extend(self.GHOST2LINES)
        # Add ghost 2 lines
        mon1Ghost2 = mon1.copy()
        mon1Ghost2.extend(ghost2)
        retList.extend(mon1Ghost2)
        # Add monomer 1 header lines
        retList.extend(self.MON1LINES)
        # Add monomer 1 lines
        retList.extend(mon1)
        # Add monomer 2 header lines
        retList.extend(self.MON2LINES)
        # Add monomer 2 lines
        retList.extend(mon2)
        # Add ending lines
        retList.extend(self.END_LINE1)

        return retList
