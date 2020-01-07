# File name: BoxComponents.py
# Programmer: Sebastien Marleau
# Contains:
#       class WordBox: contains a rect and text that can center in the rect. Many attribute changes
#       class Button: extends WordBox and adds features such as clicking and hovering
# Date: April 9th, 2019


import pygame
from Colors import *


class WordBox:
    # a class containing both a drawable box and text optionally centered in the box
    # the border color, width, background color are all changeable
    # has a drawList for improved efficiency and flexibility
    # coded with robustness in mind
    def __init__(self, rect, text='', font=pygame.font.SysFont("arial", 12), centerTextInBox=True,
                 textColor=Colors.BLACK, drawText=True, borderColor=Colors.BLACK, drawBorder=True,
                 borderWidth=1, boxBackgroundColor=None, fillBoxWithColor=False, visible=True):

        self._visible = visible
        self.rect = rect

        # border
        self._drawBorder = drawBorder
        self._borderColor = borderColor
        self._borderWidth = borderWidth

        # background color
        self._fillBoxWithColor = fillBoxWithColor
        self._boxBackgroundColor = boxBackgroundColor

        # text related
        self._drawText = drawText
        self._centerTextInBox = centerTextInBox
        self._textColor = textColor
        self._text = text
        self._font = font
        self.textPosition = 0  # initialized in _updateTextPosition()
        self.textBlit = None  # initialized in _updateTextBlit()
        self._updateTextBlit()
        self._updateTextPosition()

        self.drawList = []  # a list of the in-use draw functions
        self.updateDrawList()

    def getText(self):
        return self._text

    def getBackgroundColor(self):
        return self._boxBackgroundColor

    def _getCenteredTextPosition(self):
        pos = self._font.size(self._text)
        x = self.rect.left + self.rect.width / 2 - pos[0] / 2
        y = self.rect.top + self.rect.height / 2 - pos[1] / 2
        return x, y

    # draw functions

    def drawTheBorder(self, win):
        pygame.draw.rect(win, self._borderColor, self.rect, self._borderWidth)

    def drawTheBoxBackground(self, win):
        win.fill(self._boxBackgroundColor, rect=self.rect)

    def drawTheText(self, win):
        win.blit(self.textBlit, self.textPosition)

    # updating functions, also updating related things

    def updateBackgroundColor(self, color):
        self._boxBackgroundColor = color

    def updateText(self, text):
        self._text = text
        self._updateTextBlit()
        self._updateTextPosition()

    def updateTextColor(self, color):
        self._textColor = color
        self._updateTextBlit()

    def updateTextFont(self, font):
        self._font = font
        self._updateTextBlit()
        self._updateTextPosition()

    def updateBorderColor(self, color):
        self._borderColor = color

    def updateBorderWidth(self, width):
        self._borderWidth = width

    def _updateTextBlit(self):
        self.textBlit = self._font.render(self._text, True, self._textColor)

    def _updateTextPosition(self):
        if self._centerTextInBox:
            self.textPosition = self._getCenteredTextPosition()
        else:
            self.textPosition = (self.rect.left, self.rect.top)

    # attribute updates

    def startDrawingBoxBackground(self):
        self._fillBoxWithColor = True
        self.updateDrawList()
    def stopDrawingBoxBackground(self):
        self._fillBoxWithColor = False
        self.drawList.remove(self.drawTheBoxBackground)

    def startDrawingText(self):
        self._drawText = True
        self.updateDrawList()
    def stopDrawingText(self):
        self._drawText = False
        self.drawList.remove(self.drawTheText)

    def startCenteringText(self):
        self._centerTextInBox = True
        self._updateTextPosition()
    def stopCenteringText(self):
        self._centerTextInBox = False
        self._updateTextPosition()

    def startDrawingBorder(self):
        self._drawBorder = True
        self.updateDrawList()
    def stopDrawingBorder(self):
        self._drawBorder = False
        self.drawList.remove(self.drawTheBorder)

    def makeVisible(self):
        self._visible = True
        self.updateDrawList()
    def makeInvisible(self):
        self._visible = False
        self.updateDrawList()

    # updates drawList functions based on attributes
    def updateDrawList(self):
        self.drawList = []
        if not self._visible:
            return
        if self._fillBoxWithColor:
            self.drawList.append(self.drawTheBoxBackground)  # the function
        if self._drawBorder:
            self.drawList.append(self.drawTheBorder)  # the function
        if self._drawText:
            self.drawList.append(self.drawTheText)  # the function

    def draw(self, win):
        for drawFunction in self.drawList:
            drawFunction(win)


########################################################################################################################
########################################################################################################################


class Button(WordBox):
    # class containing a word box with different features on hover
    # can also executes a function when clicked
    def __init__(self, rect, functionIfClicked=lambda: None, text='', font=pygame.font.SysFont("arial", 12),
                 textColor=Colors.BLACK, drawText=True, borderColor=Colors.BLACK, drawBorder=True,
                 borderWidth=1, centerTextInBox=True, borderGrowOnHover=True, growColor=Colors.BLACK,
                 growWidth=3, darkenOnHover=True, boxBackgroundColor=None, fillBoxWithColor=False,
                 textColorChangesOnHover=False, textColorChangeColor=Colors.BLACK, visible=True):

        #  border grow
        self._drawBorderGrow = borderGrowOnHover
        self.borderGrowColor = growColor
        self._nonGrowColor = borderColor
        self._borderChangesColor = self._nonGrowColor != self.borderGrowColor  # behavior attribute
        self._nonGrowWidth = borderWidth
        self.growWidth = growWidth

        #  background changes
        self._darkenOnHover = darkenOnHover
        self._darkenedBackgroundColor = None  # initialized in function
        self._nonDarkenedBackground = boxBackgroundColor

        #  text color changes
        self._textColorChangeOnHover = textColorChangesOnHover
        self._nonChangedTextColor = textColor
        self._textColorChangeColor = textColorChangeColor

        self.__hovers = False
        self.hoverCheckList = list()

        self.functionIfClicked = functionIfClicked

        super().__init__(rect=rect, text=text, font=font, centerTextInBox=centerTextInBox, textColor=textColor,
                         drawText=drawText, borderColor=borderColor, drawBorder=drawBorder, borderWidth=borderWidth,
                         boxBackgroundColor=boxBackgroundColor, fillBoxWithColor=fillBoxWithColor, visible=visible)
        self.updateHoverCheckList()

    # hovering check functions

    def _hoverForBorderGrow(self):
        if self.__hovers:
            self.updateBorderWidth(self.growWidth)
        else:
            self.updateBorderWidth(self._nonGrowWidth)

    def _hoverForBorderColorChange(self):
        if self.__hovers:
            self.updateBorderColor(self.borderGrowColor)
        else:
            self.updateBorderColor(self._nonGrowColor)

    def _hoverForBackgroundDarken(self):
        if self.__hovers:
            super().updateBackgroundColor(self._darkenedBackgroundColor)
        else:
            super().updateBackgroundColor(self._nonDarkenedBackground)

    def _hoverForTextColorChange(self):
        if self.__hovers:
            super().updateTextColor(self._textColorChangeColor)
        else:
            super().updateTextColor(self._nonChangedTextColor)

    # updating functions

    def updateBackgroundColor(self, color):
        super().updateBackgroundColor(color)
        self._nonDarkenedBackground = color
        self._updateDarkenedColor()

    def _updateDarkenedColor(self):
        self._darkenedBackgroundColor = Colors.darkenColor(self._nonDarkenedBackground, amount=0.9)

    def updateBorderGrowColor(self, color):
        self.borderGrowColor = color
        update = self.borderGrowColor != self._nonGrowColor
        if update != self._borderChangesColor:
            self._borderChangesColor = update
            self.updateHoverCheckList()

    # updates hover functions list based on attributes
    def updateHoverCheckList(self):
        self.hoverCheckList = []
        if self._darkenOnHover:
            self._updateDarkenedColor()
            self.hoverCheckList.append(self._hoverForBackgroundDarken)
        if self._drawBorderGrow:
            self.hoverCheckList.append(self._hoverForBorderGrow)  # the function
        if self._textColorChangeOnHover:
            self.hoverCheckList.append(self._hoverForTextColorChange)
        if self._borderChangesColor:
            self.hoverCheckList.append(self._hoverForBorderColorChange)


    def draw(self, win):
        for check in self.hoverCheckList:
            check()
        super().draw(win)

    # attribute updates

    def startDarkeningOnHover(self):
        self._darkenOnHover = True
        self.updateHoverCheckList()
    def stopDarkeningOnHover(self):
        self._darkenOnHover = False
        self.hoverCheckList.remove(self._hoverForBackgroundDarken)

    def startBorderGrowOnHover(self):
        self._drawBorderGrow = True
        self.updateHoverCheckList()
    def stopBorderGrowOnHover(self):
        self._drawBorderGrow = True
        self.hoverCheckList.remove(self._hoverForBorderGrow)

    def startChangingTextColorOnHover(self):
        self._textColorChangeOnHover = True
        self.updateHoverCheckList()
    def startChangingTextColorOnHover(self):
        self._textColorChangeOnHover = False
        self.hoverCheckList.remove(self._hoverForTextColorChange)


    def clickedOn(self, mp):
        if not self._visible:
            return False
        if self.rect.collidepoint(mp):
            self.functionIfClicked()
            return True
        return False

    def hoverOver(self, mp):
        if not self._visible:
            return False
        self.__hovers = self.rect.collidepoint(mp)
        return self.__hovers
