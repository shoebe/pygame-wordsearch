# File name: SimpleMenu.py
# Programmer: Sebastien Marleau
# Description: A simple menu
# Date: April 9th, 2019


from Grid import MenuGrid
from BoxComponents import WordBox
from Colors import *
import pygame


class SimpleMenu:
    # a simple reusable menu with a menu grid and a title
    # can also add an extra exit button
    # automatically makes the menu grid pygame.Rect based on title and its size
    def __init__(self, overallMenuRect: pygame.Rect, title: str, listOfWordsForOptions: list, optionsXCellNum,
                 optionsYCellNum, optionsCellWidth, optionsCellHeight, listOfFunctionsForOptions=[],
                 drawOptionsButtonsBorder=True, optionsBorderColor=Colors.BLACK, optionsButtonsBordersGrow=True,
                 optionsBorderGrowColor=Colors.BLACK, optionsBoxBackgroundColor=None, optionsButtonsDarken=True,
                 optionsFont=pygame.font.SysFont("arial", 20), titleFont=pygame.font.SysFont("arial", 45),
                 titleColor=Colors.BLACK, addExitButton=True, visible=True):

        textSize = titleFont.size(title)
        extraGaps = 3  # 2 for the up-down, 1 for title
        if addExitButton:
            if len(listOfWordsForOptions) % optionsXCellNum == 0:
                optionsYCellNum += 1
                listOfWordsForOptions.append("Exit")
                extraGaps += 1

        gapY = (overallMenuRect.height - textSize[1]) // (optionsYCellNum + extraGaps)
        titleRect = pygame.Rect(overallMenuRect.left, overallMenuRect.top, overallMenuRect.width,
                                overallMenuRect.top + textSize[1] + 2 * gapY)

        optionsRect = pygame.Rect(overallMenuRect.left, titleRect.bottom, overallMenuRect.width,
                                  overallMenuRect.height - titleRect.height)
        self.visible = visible

        self.menuGrid = MenuGrid(optionsRect, optionsXCellNum, optionsYCellNum,
                                 optionsCellWidth, optionsCellHeight, listOfFunctions=listOfFunctionsForOptions,
                                 listOfWords=listOfWordsForOptions,
                                 borderColor=optionsBorderColor, borderGrowColor=optionsBorderGrowColor,
                                 font=optionsFont,
                                 drawBoxesAroundWords=drawOptionsButtonsBorder,
                                 buttonsDarkenOnHover=optionsButtonsDarken,
                                 boxBackgroundColor=optionsBoxBackgroundColor,
                                 buttonsGrowOnHover=optionsButtonsBordersGrow,
                                 drawGridBorder=False)

        self.titleBox = WordBox(titleRect, text=title, font=titleFont, textColor=titleColor, drawBorder=False)

    def hoverOver(self, mp):
        self.menuGrid.hoverOver(mp)

    def clickedOn(self, mp):
        self.menuGrid.clickedOn(mp)

    def returnTextOfClickedButton(self, mp):
        return self.menuGrid.returnTextOfClickedButton(mp)

    def draw(self, win):
        if self.visible:
            self.titleBox.draw(win)
            self.menuGrid.draw(win)
