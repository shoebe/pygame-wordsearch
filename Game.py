# File name: Game.py
# Programmer: Sebastien Marleau
# Description: Handles the WordSearch game menu and puzzle development
# Date: April 9th, 2019

import pygame
pygame.init()
from Grid import *
from SimpleMenu import *

class Game:
    def __init__(self, puzzleDictData):
        self.width = 720
        self.height = 560
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Word Search by Sebastien Marleau')
        self.puzzleDictData = puzzleDictData


    def start(self):
        while True:
            nameOfPuzzle = self.menu()
            if nameOfPuzzle == "Exit":
                break  # exit
            backToMenu = self.startPuzzle(nameOfPuzzle)  # returns True if back button is pressed or on win
            if not backToMenu:
                break  # exit
        pygame.quit()


    def menu(self):
        backgroundColor = Colors.randReallyLightColor()
        listOfWords = list(self.puzzleDictData.keys())
        amountOfPuzzles = len(listOfWords)
        left = 0
        top = 25
        width = self.width
        height = self.height-100
        menuRect = pygame.Rect(left, top, width, height)
        heightOfButtons = 50

        menu = SimpleMenu(overallMenuRect=menuRect, listOfWordsForOptions=listOfWords, optionsXCellNum=1,
                          optionsYCellNum=amountOfPuzzles, title="Word Search", titleFont=pygame.font.SysFont("arial", 45),
                          optionsCellWidth=280, optionsCellHeight=heightOfButtons,
                          optionsBoxBackgroundColor=Colors.darkenColor(backgroundColor),
                          optionsFont=pygame.font.SysFont("arial", 20), drawOptionsButtonsBorder=False,
                          visible=True)
        mp = (0,0)
        while True:
            pygame.time.delay(5)
            self.win.fill(backgroundColor)
            menu.draw(self.win)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None

                if event.type == pygame.MOUSEMOTION:
                    mp = pygame.mouse.get_pos()
                    menu.hoverOver(mp)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    nameOfPuzzle = menu.returnTextOfClickedButton(mp)
                    if nameOfPuzzle is not None:
                        return nameOfPuzzle



    def startPuzzle(self, puzzleName):
        backgroundColor = Colors.randReallyLightColor()
        puzzleData = self.puzzleDictData[puzzleName]
        puzzleLeft = 50
        puzzleTop = 100
        puzzleMaxHeight = self.height-150
        puzzleMaxWidth = self.width-250
        cellHeight = puzzleMaxHeight // puzzleData.rowCount
        cellWidth = puzzleMaxWidth //puzzleData.columnCount
        cellHeight = cellWidth = min(cellHeight, cellWidth)
        puzzleHeight = cellHeight*puzzleData.rowCount
        puzzleWidth = cellWidth*puzzleData.columnCount



        puzzleGridRect = pygame.Rect(puzzleLeft, puzzleTop, puzzleWidth, puzzleHeight)

        foundWords = list()  # set gets added to as words are found
        wordSearch = WordSearchGrid(puzzleGridRect, xCellNum=puzzleData.columnCount, yCellNum=puzzleData.rowCount,
                                    cellWidth=cellWidth, cellHeight=cellHeight, textListForLetters=puzzleData.letters,
                                    wordList=puzzleData.words, foundWordList=foundWords,
                                    font=pygame.font.SysFont("arial", cellHeight//2),
                                    boxBackgroundColor=Colors.lightenColor(backgroundColor, amount=0.8))
        #  title right above the puzzle grid
        puzzleThemeTitle = WordBox(pygame.Rect(puzzleLeft,0,puzzleWidth, puzzleTop),text=puzzleName,
                                   font=pygame.font.SysFont("arial", 30,bold=True),drawBorder=False)

        wordGridCellHeight = 40
        wordGridYCellNum = len(puzzleData.words)
        if wordGridYCellNum > 8: # more than 8 makes the back button go off the screen
            wordGridCellHeight -= 3.5*(wordGridYCellNum-8)

        wordGridLeft = puzzleLeft+puzzleMaxWidth
        wordGridTop = puzzleTop+50
        wordGridWidth = self.width-puzzleLeft-puzzleMaxWidth-50
        wordGridHeight = wordGridCellHeight * len(puzzleData.words)

        # grid containing possible words in puzzle grid
        wordGrid = CrossOutWordGrid(pygame.Rect(wordGridLeft, wordGridTop, wordGridWidth, wordGridHeight),
                                    listOfWords=puzzleData.words, xCellNum=1, yCellNum=wordGridYCellNum,
                                    cellHeight=wordGridCellHeight,cellWidth=wordGridWidth, centerY=False,
                                    drawBoxesAroundWords=False,centerX=True ,boxBackgroundColor=Colors.darkenColor(backgroundColor, amount=0.95),
                                    drawGridBorder=True)
        # word box right above the list of words
        wordBoxThatSaysWords = WordBox(pygame.Rect(wordGridLeft, puzzleTop, wordGridWidth, 50), text="Words",
                                       font=pygame.font.SysFont("arial", 25, bold=True), drawBorder=False,
                                       boxBackgroundColor=Colors.darkenColor(backgroundColor, amount=0.95))

        # text updates as letters are chosen
        currentlySelectedLettersBox = WordBox(pygame.Rect(wordGridLeft, 0, wordGridWidth, puzzleTop), text="",
                                              font=pygame.font.SysFont("arial", 25, bold=True), drawBorder=False,
                                              boxBackgroundColor=None)
        backButton = Button(pygame.Rect(wordGridLeft+wordGridWidth//2-50, wordGridTop + wordGridHeight+25, 100, 50), text="Back",
                            font=pygame.font.SysFont("arial", 15), boxBackgroundColor=Colors.darkenColor(backgroundColor, amount=0.95),
                            darkenOnHover=True, fillBoxWithColor=True, drawBorder=False)
        oldTime = pygame.time.get_ticks()
        timeBox = WordBox(pygame.Rect(0,0,100,puzzleTop), text="0",font=pygame.font.SysFont("arial", 25, bold=True),
                          drawBorder=False,boxBackgroundColor=None)
        mp = (0,0)
        while True:
            pygame.time.delay(10)
            time = pygame.time.get_ticks()-oldTime
            self.win.fill(backgroundColor)
            timeBox.updateText(str(time // 1000))
            timeBox.draw(self.win)

            currentlySelectedLettersBox.updateText(wordSearch.getPossibleWordsFromSelectedSquares()[0])
            currentlySelectedLettersBox.draw(self.win)

            wordSearch.draw(self.win)
            backButton.draw(self.win)
            wordGrid.draw(self.win)
            puzzleThemeTitle.draw(self.win)
            wordBoxThatSaysWords.draw(self.win)

            pygame.display.update()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

                if event.type == pygame.MOUSEMOTION:
                    mp = pygame.mouse.get_pos()
                    wordSearch.hoverOver(mp)
                    backButton.hoverOver(mp)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    wordSearch.clickedOn(mp)
                    wordGrid.crossOut(foundWords)  # crosses out words when found
                    if backButton.clickedOn(mp):
                        return True  # main menu

                    if len(foundWords) == len(puzzleData.words):
                        wordGrid.draw(self.win)  # tick last word found
                        pygame.display.update()  # user sees completed state
                        pygame.time.delay(400)
                        self.win.fill(backgroundColor)  # erase
                        playerWin = WordBox(pygame.Rect(0, 0, self.width, self.height), text="YOU WIN",
                                            font=pygame.font.SysFont("arial", 45), drawBorder=False)
                        playerWin.draw(self.win)  # display "win"
                        pygame.display.update()
                        pygame.time.delay(2000)
                        return True  # main menu
