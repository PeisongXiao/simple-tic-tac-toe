#!/usr/bin/python
############################################################
### Project: simple-tictactoe
### File: main.py
### Description: the main file for the tic-tac-toe game
### Version: 1.0
############################################################
import PyQt6
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6 import QtCore, QtGui, QtWidgets
from UI import *
import sys

CHAR = ['-', 'X', 'O']
PLAY = 0
WON  = 1
TIE  = 2

class tictactoe_gui(QtWidgets.QMainWindow):
    def __init__(self):
        print("Initializing GUI...")

        QtWidgets.QMainWindow.__init__(self)
        # self.ui = uic.loadUi("UI.ui", self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.resetButton.clicked.connect(self.newGame)

        self.boardUI = QStandardItemModel(3, 3)
        self.ui.board.setModel(self.boardUI)

        self.populateBoard()
        print("Initialized new board!")

        self.newGame()

    # declareWinner(winner): Declares the winner of the game
    def declareWinner(self, winner):
        self.ui.prompt.setText("Player " + str(winner) + " won!")
        msg_box = QMessageBox()
        msg_box.setWindowTitle("We have a winner!")
        msg_box.setText("The winner is Player " + str(winner) + "!")
        msg_box.exec()

    # checkWinner(): check if there's a winner or a tie
    def checkWinner(self):
        state = PLAY

        for i in range(3):
            if self.boardData[i][2] == 0:
                continue
            flag = True
            for j in range(2):
                if self.boardData[i][j] != self.boardData[i][2]:
                    flag = False
                    break
            if flag:
                self.declareWinner(self.boardData[i][0])
                state = WON
                break

        if state == PLAY:
            for i in range(3):
                if self.boardData[2][i] == 0:
                    continue
                flag = True
                for j in range(2):
                    if self.boardData[j][i] != self.boardData[2][i]:
                        flag = False
                        break
                if flag:
                    self.declareWinner(self.boardData[j][i])
                    state = WON
                    break

        if state == PLAY:
            if (self.boardData[1][1] and
                ((self.boardData[0][0] == self.boardData[1][1] and
                  self.boardData[1][1] == self.boardData[2][2]) or
                 (self.boardData[0][2] == self.boardData[1][1] and
                  self.boardData[1][1] == self.boardData[2][0]))):
                self.declareWinner(self.boardData[1][1])
                state = WON

        if state == PLAY:
            flag = True
            for i in range(3):
                for j in range(3):
                    if self.boardData[i][j] == 0:
                        flag = False
            if flag:
                state = TIE
                msg_box = QMessageBox()
                msg_box.setWindowTitle("We have a tie!")
                msg_box.setText("We have a tie!")
                msg_box.exec()                

        if state != PLAY:
            self.newGame()

    # updateBoard(): Updates the board on the GUI
    def updateBoard(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].setText(CHAR[self.boardData[i][j]])

    # populateBoard(): Populates the board with buttons before the
    #  first game
    def populateBoard(self):
        self.buttons = []
        
        for i in range(3):
            self.buttons.append([])
            for j in range(3):
                self.buttons[i].append(QPushButton("X"))
                font = self.buttons[i][j].font()
                font.setPointSize(20)
                self.buttons[i][j].setFont(font)
                self.buttons[i][j].setObjectName(str(i) + str(j))
                self.ui.board.setIndexWidget(
                    self.boardUI.index(i,j),
                    self.buttons[i][j])
                self.buttons[i][j].clicked.connect(self.place)

        for i in range(3):
            self.ui.board.setColumnWidth(i, 146)
            self.ui.board.setRowHeight(i, 152)

    # place(): Place a marker if there isn't a marker on the button
    #  pressed
    def place(self):
        button = self.sender()
        pos = [int(button.objectName()[0]),
               int(button.objectName()[1])]

        if self.boardData[pos[0]][pos[1]] != 0:
            return
        
        prompt = ("Player " + str(self.turn) +
                  " landed at (" + str(pos[0]) + ", " +
                  str(pos[1]) + ")")
        self.ui.statusbar.showMessage(prompt)

        self.boardData[pos[0]][pos[1]] = self.turn
        self.turn = self.turn % 2 + 1
        self.ui.prompt.setText("Player " + str(self.turn) + "'s turn!")
        
        self.updateBoard()

        self.checkWinner()

    # newGame(): Starts a new game of tic-tac-toe
    def newGame(self):
        self.boardData = [[0, 0, 0],
                          [0, 0, 0],
                          [0, 0, 0]]
        self.turn = 1
        
        self.ui.statusbar.showMessage("Initialized new game!")
        self.ui.prompt.setText("Player " + str(self.turn) + "'s turn!")

        self.updateBoard()

def main():
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    main_window = tictactoe_gui()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
