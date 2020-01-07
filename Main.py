# File name: Main.py
# Programmer: Sebastien Marleau
# Description: imports puzzle data and starts the game
# Date: April 9th, 2019


import pygame
pygame.init()
from Game import *

class PuzzleData:

    def __init__(self, title, rowCount, columnCount, letters, words):

        self.title = title
        self.rowCount = rowCount
        self.columnCount = columnCount
        self.letters = letters
        self.words = words



fi = open("puzzles.txt", 'r')

puzzleDataDict = dict()
amountOfPuzzles = int(fi.readline().strip())


for puzzle in range(amountOfPuzzles):
    title = fi.readline().strip()

    columnCount = int(fi.readline().strip())
    rowCount = int(fi.readline().strip())
    letters = []
    for row in range(rowCount):
        letters += fi.readline().strip().split(' ')
    words = []
    wordCount = int(fi.readline().strip())
    for word in range(wordCount):
        words.append(fi.readline().strip())
    puzzleDataDict[title]= PuzzleData(title=title, rowCount=rowCount, columnCount=columnCount, letters=letters, words=words)


game = Game(puzzleDataDict)
game.start()
