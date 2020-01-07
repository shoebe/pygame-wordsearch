# File name: Grid.py
# Programmer: Sebastien Marleau
# Contains Grid classes:
#           class Grid: abstract class for all classes with a Grid
#           class WordGrid: extends Grid and makes the cells WordBox objects
#           class ButtonGrid: extends Grid and makes the cells Button objects
#           class MenuGrid: extends ButtonsGrid with attributes beffiting a menu selection grid
#           class WordSearchGrid: extends ButtonGrid and has all functionality of a WordSearch game
#           class CrossOutWordGrid: extends WordGrid, and adds functionality to cross out specific words
# Date: April 9th, 2019

import pygame
from BoxComponents import *


class Grid:
    # abstract grid class
    # handles the location placement of the cells, as well as their drawing
    # also supports column and row adding
    # children classes should overwrite drawCell() and addCell()
    def __init__(self, gridRect, xCellNum, yCellNum, cellWidth, cellHeight, centerX=True,
                 centerY=True, borderColor=(0, 0, 0), drawGridBorder=True, visible=True):

        self.gridRect = gridRect
        self.xCellNum = xCellNum
        self.yCellNum = yCellNum
        self.borderColor = borderColor
        self.cellWidth = cellWidth
        self.cellHeight = cellHeight
        self.gapX = 0  # initialized in initGaps()
        self.gapY = 0  # initialized in initGaps()

        self.centerX = centerX
        self.centerY = centerY
        self.drawGridBorder = drawGridBorder
        self.visible = visible
        self.initGaps()
        self.cellList = None  # initialized in initCells()
        self.initCells()

    def initGaps(self):  # only used in constructor
        if self.centerX:
            #              big grid width      size the cells combined will take       amount of gaps
            self.gapX = (self.gridRect.width - (self.cellWidth * self.xCellNum)) // (self.xCellNum + 1)
        else:
            self.gapX = 0
        if self.centerY:
            #              big grid height      size the cells combined will take       amount of gaps
            self.gapY = (self.gridRect.height - (self.cellHeight * self.yCellNum)) // (self.yCellNum + 1)
        else:
            self.gapY = 0


    def newCell(self, left, top, width, height):  # used in initCells()
        return pygame.Rect(left, top, width, height)

    def initCells(self):
        self.cellList = []

        currentY = self.gridRect.top + self.gapY
        for i in range(self.yCellNum):
            # new row
            self.cellList.append([])
            # reset x location
            currentX = self.gridRect.left + self.gapX
            for j in range(self.xCellNum):
                cell = self.newCell(currentX, currentY, self.cellWidth, self.cellHeight)
                self.cellList[i].append(cell)
                # move left
                currentX += self.cellWidth + self.gapX
            # move down
            currentY += self.cellHeight + self.gapY

    def draw(self, win):
        if not self.visible:
            return
        if self.drawGridBorder:
            pygame.draw.rect(win, self.borderColor, self.gridRect, 1)
        for row in self.cellList:
            for cell in row:
                self.drawCell(win, cell)

    def drawCell(self, win, cell):  # used in draw()
        pygame.draw.rect(win, self.borderColor, cell, 1)

    def addColumn(self):
        self.xCellNum += 1
        self.gridRect = pygame.Rect(self.gridRect.left,
                                    self.gridRect.top,
                                    self.gridRect.width + self.cellHeight + self.gapX,
                                    self.gridRect.height)
        self.initCells()

    def addRow(self):
        self.yCellNum += 1
        self.gridRect = pygame.Rect(self.gridRect.left,
                                    self.gridRect.top,
                                    self.gridRect.width,
                                    self.gridRect.height + self.cellHeight + self.gapY)
        self.initCells()


########################################################################################################################
########################################################################################################################


class WordGrid(Grid):
    # A grid containing WordBoxes
    # handles the creation of WordBox instances used as cells
    # has a function to get the WordBox instance containing a specific word
    def __init__(self, gridRect, listOfWords, xCellNum, yCellNum, cellWidth, cellHeight,
                 centerX=True, centerY=True, borderColor=Colors.BLACK, boxBackgroundColor=None,
                 fillBoxesWithColor=False, centerTextInBox=True, font=pygame.font.SysFont("arial", 12),
                 drawBoxesAroundWords=True, boxesColor=Colors.BLACK, drawGridBorder=True, visible=True):
        # words
        self.listOfWords = listOfWords  # list must contain as many words as there are boxes
        self._listOfWordsIter = None  # initialized in initSquares()
        # background color
        self.fillBoxesWithColor = fillBoxesWithColor
        self.boxBackgroundColor = boxBackgroundColor
        # text specifications
        self.centerTextInBox = centerTextInBox
        self.font = font
        # border
        self.drawBoxesAroundWords = drawBoxesAroundWords
        self.boxesColor = boxesColor

        super().__init__(gridRect=gridRect, xCellNum=xCellNum, yCellNum=yCellNum, cellWidth=cellWidth,
                         cellHeight=cellHeight, centerX=centerX, centerY=centerY, borderColor=borderColor,
                         drawGridBorder=drawGridBorder, visible=visible)

    def initCells(self):
        self._listOfWordsIter = iter(self.listOfWords)  # reset iter
        super().initCells()

    def newCell(self, left, top, width, height):
        text = next(self._listOfWordsIter)  # program crashes without enough words

        return WordBox(pygame.Rect(left, top, width, height), text=text, font=self.font,
                       borderColor=self.borderColor, boxBackgroundColor=self.boxBackgroundColor,
                       centerTextInBox=self.centerTextInBox, drawBorder=self.drawBoxesAroundWords,
                       fillBoxWithColor=self.fillBoxesWithColor)

    def drawCell(self, win, cell):
        cell.draw(win)

    def getWordBoxWithWord(self, word):
        for row in self.cellList:
            for wordBox in row:
                if wordBox.getText() == word:
                    return wordBox


########################################################################################################################
########################################################################################################################

class ButtonGrid(Grid):
    # A grid containing buttons
    # handles the creation of Buttons instances used as cells, their clicking and hovering
    # has a list of functions that can be added to the buttons
    # has a function to get the Button instance ogf a button with a particular word
    def __init__(self, gridRect, listOfWords, xCellNum, yCellNum, cellWidth, cellHeight,
                 listOfFunctions=[], centerX=True, centerY=True, borderColor=Colors.BLACK, buttonsGrowOnHover=True,
                 borderGrowColor=Colors.BLACK, boxBackgroundColor=None,
                 fillBoxesWithColor=False, buttonsDarkenOnHover=False,
                 centerTextInBox=True, font=pygame.font.SysFont("arial", 12), textColorChangesOnHover=False,
                 textColorChangeColor=Colors.BLACK,
                 drawBoxesAroundWords=True, drawGridBorder=True, visible=True):

        #  lists
        self.listOfWords = listOfWords
        self.listOfFunctions = listOfFunctions
        self._listOfFunctionsIter = None  # initialized in initSquares()
        self._listOfWordsIter = None  # initialized in initSquares()
        #  box backgrounds
        self.fillBoxesWithColor = fillBoxesWithColor
        self.boxBackgroundColor = boxBackgroundColor
        self.buttonsDarkenOnHover = buttonsDarkenOnHover
        #  text
        self.centerTextInBox = centerTextInBox
        self.font = font
        self.textColorChangesOnHover = textColorChangesOnHover
        self.textColorChangeColor = textColorChangeColor

        #  behavior attributes
        self.addText = self.listOfWords != []
        self.addFunctions = self.listOfFunctions != []

        #  box borders
        self.drawBoxesAroundWords = drawBoxesAroundWords
        self.buttonsGrowOnHover = buttonsGrowOnHover
        self.borderGrowColor = borderGrowColor

        super().__init__(gridRect=gridRect, xCellNum=xCellNum, yCellNum=yCellNum, cellWidth=cellWidth,
                         cellHeight=cellHeight, centerX=centerX, centerY=centerY, borderColor=borderColor,
                         drawGridBorder=drawGridBorder, visible=visible)

    def initCells(self):
        # reset iters
        self._listOfWordsIter = iter(self.listOfWords)
        self._listOfFunctionsIter = iter(self.listOfFunctions)
        super().initCells()

    def newCell(self, left, top, width, height):
        if self.addText:
            text = next(self._listOfWordsIter)
        else:
            text = ''
        if self.addFunctions:
            function = next(self._listOfFunctionsIter)
        else:
            function = lambda: None  # empty function
        # program will crash without enough functions or words if lists aren't empty

        return Button(pygame.Rect(left, top, width, height), functionIfClicked=function, text=text, font=self.font,
                      borderColor=self.borderColor, boxBackgroundColor=self.boxBackgroundColor,
                      growColor=self.borderGrowColor,
                      drawBorder=self.drawBoxesAroundWords, fillBoxWithColor=self.fillBoxesWithColor,
                      darkenOnHover=self.buttonsDarkenOnHover, borderGrowOnHover=self.buttonsGrowOnHover,
                      textColorChangesOnHover=self.textColorChangesOnHover, textColorChangeColor=self.textColorChangeColor)

    def drawCell(self, win, cell):
        cell.draw(win)

    def returnTextOfClickedButton(self, mp):
        if self.gridRect.collidepoint(mp):
            for row in self.cellList:
                for cell in row:
                    if cell.clickedOn(mp):
                        return cell.getText()
        return None

    def clickedOn(self, mp):
        if not self.gridRect.collidepoint(mp):
            return False
        for row in self.cellList:
            for button in row:
                if button.clickedOn(mp):
                    return True
        return False

    def getButtonWithWord(self, word):
        for row in self.cellList:
            for button in row:
                if button.getText() == word:
                    return button


    def hoverOver(self, mp):
        if not self.gridRect.collidepoint(mp):
            return False
        for row in self.cellList:
            for button in row:
                if button.hoverOver(mp):
                    return True
        return False

########################################################################################################################
########################################################################################################################

class MenuGrid(ButtonGrid):
    # A grid of buttons
    # has better optional attributes befitting a menu
    def __init__(self, gridRect: pygame.Rect, xCellNum: int, yCellNum: int, cellWidth: int, cellHeight: int,
                 boxBackgroundColor: (int, int, int),
                 listOfFunctions=[], listOfWords=[], centerX=True, centerY=True, borderColor=Colors.BLACK,
                 buttonsGrowOnHover=False, borderGrowColor=Colors.BLACK, drawBoxesAroundWords=False,
                 fillBoxesWithColor=True, buttonsDarkenOnHover=True, centerTextInBox=True,
                 font=pygame.font.SysFont("arial", 12), textColorChangesOnHover=False,
                 textColorChangeColor=Colors.BLACK, drawGridBorder=False, visible=True):

        super().__init__(gridRect, listOfWords, xCellNum, yCellNum, cellWidth, cellHeight,
                         listOfFunctions=listOfFunctions, centerX=centerX, centerY=centerY, borderColor=borderColor,
                         buttonsGrowOnHover=buttonsGrowOnHover,
                         borderGrowColor=borderGrowColor, boxBackgroundColor=boxBackgroundColor,
                         fillBoxesWithColor=fillBoxesWithColor, buttonsDarkenOnHover=buttonsDarkenOnHover,
                         centerTextInBox=centerTextInBox, font=font, textColorChangesOnHover=textColorChangesOnHover,
                         textColorChangeColor=textColorChangeColor,
                         drawBoxesAroundWords=drawBoxesAroundWords, drawGridBorder=drawGridBorder, visible=visible)


########################################################################################################################
########################################################################################################################


class WordSearchGrid(ButtonGrid):
    # A grid of letters with many functions aimed towards a word search game
    # Being a specific class, most attributes are chosen for it already
    def __init__(self, gridRect, xCellNum, yCellNum, cellWidth, cellHeight, textListForLetters, wordList,
                 foundWordList, boxBackgroundColor, font=pygame.font.SysFont("arial", 20), drawBoxesAroundLetters=False,
                 centerX=False, centerY=False, visible=True):

        super().__init__(gridRect, textListForLetters, xCellNum, yCellNum, cellWidth, cellHeight, centerX=centerX,
                         centerY=centerY, buttonsGrowOnHover=False, font=font,
                         boxBackgroundColor=boxBackgroundColor,
                         drawBoxesAroundWords=drawBoxesAroundLetters, drawGridBorder=False, visible=visible)
        # used in selection and its calculation
        self.firstSelecSquare = None
        self.lastSelecSquare = None
        self.selSquares = list()
        # the set is added to as words are found. Progress is known by evaluating this set outside the class
        self.foundWordList = foundWordList
        self.wordList = wordList
        # colors for the word selection
        self.currentColor = Colors.randLightColor()
        self.pastColors = set()


    def clickedOn(self, mp):
        if not self.gridRect.collidepoint(mp):
            return
        for rowInd in range(self.yCellNum):
            for columnInd in range(self.xCellNum):

                if self.cellList[rowInd][columnInd].clickedOn(mp):
                    if self.firstSelecSquare is None:
                        # no squares currently selected
                        self.firstSelecSquare = (rowInd, columnInd)
                        self.selSquares.append(self.cellList[rowInd][columnInd])
                        # ^ the square gets colored as soon as it is clicked, vs when the mouse is moved
                        return
                    else:
                        # a square is already selected
                        # get word between two squares selected
                        possibleWords = self.getPossibleWordsFromSelectedSquares()
                        for word in self.wordList:
                            # check if word is valid
                            if word in possibleWords and word not in self.foundWordList:
                                # update list
                                self.foundWordList.append(word)
                                # permanently change background of squares
                                self.changeBackgroundColorOfSelectedSquares()
                        # reset
                        self.firstSelecSquare = None
                        self.lastSelecSquare = None
                        self.selSquares = list()
                        return

    def hoverOver(self, mp):
        if self.firstSelecSquare is None:
            return
        for rowInd in range(self.yCellNum):
            for columnInd in range(self.xCellNum):

                if self.cellList[rowInd][columnInd].hoverOver(mp):  # if mouse is over square
                    coords = (rowInd, columnInd)
                    if self.inAllowedDirection(self.firstSelecSquare, coords) and coords != self.lastSelecSquare:
                        # square change in an allowed direction with first square
                        self.lastSelecSquare = coords
                        self.updateSelectedSquares()

    @staticmethod
    def sameRow(coords1, coords2):
        return coords1[0] == coords2[0]

    @staticmethod
    def sameColumn(coords1, coords2):
        return coords1[1] == coords2[1]

    @staticmethod
    def sameDiag(coords1, coords2):
        return abs(coords1[0] - coords2[0]) == abs(coords1[1] - coords2[1])

    @classmethod
    def inAllowedDirection(cls, coords1, coords2):
        return (cls.sameRow(coords1, coords2) or cls.sameColumn(coords1, coords2)
                or cls.sameDiag(coords1, coords2))


    def changeBackgroundColorOfSelectedSquares(self):  # used on squares where a word is found
        for square in self.selSquares:
            if square.getBackgroundColor() == self.boxBackgroundColor:
                # letter has not been in a found word
                square.updateBackgroundColor(Colors.lightenColor(self.currentColor, amount=0.6))
                square.startDrawingBoxBackground()
        # don't reuse same color
        self.pastColors.add(self.currentColor)
        while self.currentColor in self.pastColors:
            self.currentColor = Colors.randLightColor()

    def updateSelectedSquares(self):
        self.selSquares = list()
        rows = [x for x in range(self.firstSelecSquare[0], self.lastSelecSquare[0] + 1)]
        if len(rows) == 0:
            # go in opposite direction
            rows = [x for x in range(self.firstSelecSquare[0], self.lastSelecSquare[0] - 1, -1)]

        columns = [x for x in range(self.firstSelecSquare[1], self.lastSelecSquare[1] + 1)]
        if len(columns) == 0:
            # go in opposite direction
            columns = [x for x in range(self.firstSelecSquare[1], self.lastSelecSquare[1] - 1, -1)]

        if len(rows) == 1:  # selected squares in same row
            for columnInd in columns:
                self.selSquares.append(self.cellList[rows[0]][columnInd])
        elif len(columns) == 1:  # selected squares in same column
            for rowInd in rows:
                self.selSquares.append(self.cellList[rowInd][columns[0]])
        else:  # diagonal
            for innerInd in range(len(columns)):  # rows and columns have same length
                self.selSquares.append(self.cellList[rows[innerInd]][columns[innerInd]])

    def draw(self, win):
        win.fill(rect=self.gridRect, color=self.boxBackgroundColor)
        super().draw(win)
        # draw selection color over squares
        for square in self.selSquares:
            win.fill(self.currentColor, square.rect)
            # text is erased, so redraw
            square.drawTheText(win)

    def getPossibleWordsFromSelectedSquares(self):
        charList = []
        for square in self.selSquares:
            charList.append(square.getText())

        word1 = "".join(charList)
        charList.reverse()
        word2 = "".join(charList)
        return word1, word2


########################################################################################################################
########################################################################################################################


class CrossOutWordGrid(WordGrid):
    # a WordGrid class that also supports crossing out words
    def __init__(self, gridRect, listOfWords, xCellNum, yCellNum, cellWidth, cellHeight,
                 centerX=True, centerY=True, borderColor=Colors.BLACK, boxBackgroundColor=None,
                 fillBoxesWithColor=True, centerTextInBox=True, font=pygame.font.SysFont("arial", 12),
                 drawBoxesAroundWords=True, drawGridBorder=True, visible=True):

        super().__init__(gridRect, listOfWords, xCellNum, yCellNum, cellWidth, cellHeight, centerX, centerY,
                         borderColor, boxBackgroundColor, fillBoxesWithColor, centerTextInBox, font,
                         drawBoxesAroundWords, drawGridBorder, visible)
        # list with the line arguments
        self.lineList = list()

    def crossOut(self, wordSet):
        if len(wordSet) == len(self.lineList):
            # no new change
            return

        word = wordSet[-1]
        wordBox = self.getWordBoxWithWord(word)
        width = wordBox.textBlit.get_width()
        height = wordBox.textBlit.get_height()
        pos = wordBox.textPosition

        lineStart = (pos[0], pos[1] + height // 2 - 1)
        #           x of start plus width,   y of start
        lineEnd = (lineStart[0] + width, lineStart[1])
        # append args
        self.lineList.append((Colors.BLACK, lineStart, lineEnd, 3))

    def draw(self, win):
        super().draw(win)
        for lineArgs in self.lineList:
            pygame.draw.line(win, *lineArgs)
