from tkinter.constants import ROUND

from PySide6.QtGui import Qt, QColor, QFontDatabase, QFont
import sys
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QWidget,
    QGridLayout,  QStackedWidget,)
from fontGlowEffect import FontGlowEffect
import random
from sympy import symbols, solve
from sender import Sender
listOfSolutions = []
puzzleSolved = False
graceHigh = 900000
graceLow = 600000
solveHigh = 540000
solveLow = 360000
class MainWindow(QMainWindow):


    def __init__(self):
        global graceHigh
        global graceLow
        global  solveHigh
        global solveLow

        stack = QStackedWidget()
        super().__init__()

        self.setWindowTitle("My App")
        QFontDatabase.addApplicationFont("fonts/BrunoAceSC-Regular.ttf")
        self.showFullScreen()

        layout = QGridLayout()
        # --- 1. ADD THE HEADLINE ---



        headline = QLabel()
        headline.setStyleSheet("""
            QLabel{
                color: #a600b5;
                margin-bottom: 0px;
                padding: 0px;
            }
        """)
        label = QLabel()
        label.setStyleSheet("""
                                QLabel{
                                    color: #a600b5;
                                    
                                }
                            """)



        def updateScreen():

            global m, t, listOfSolutions
            m = random.randint(1, 9)
            t = random.randint(1, 40)
            headline.setText(f" !!FLUGBAHN!!")


            label.setText(f"y = {m}x+{t}")


            print(f"{m}x+{t}")
            listOfSolutions = expectedResult(self)
            print(listOfSolutions)
            self.graceTimer.stop()
            with open("asteroidInformation.txt", "r+") as f:
                f.write("n")#                           120000 180000
            self.solveTimer.setInterval(random.randint(solveLow, solveHigh))
            self.solveTimer.start()

        def checkForSolve(self):
            global puzzleSolved
            self.solveTimer.stop()
            headline.setText("")
            label.setText("")
            with open("asteroidInformation.txt", "r+") as f:
                f.write("w")
            puzzleSolved = False#                       180000 300000
            self.graceTimer.setInterval(random.randint(graceLow, graceHigh))
            self.graceTimer.start()
        self.graceTimer = QTimer()
        self.graceTimer.timeout.connect(updateScreen)
        self.graceTimer.setInterval(random.randint(graceLow, graceHigh))


        self.solveTimer = QTimer()
        self.solveTimer.timeout.connect(lambda : checkForSolve(self))


        def checkFileInput(self):
            global listOfSolutions , puzzleSolved
            with open ("asteroidInformation.txt", "r+") as f:
                line = f.readline()
                print(self.solveTimer.isActive())
                print(self.graceTimer.isActive())
                print(line)
                if line == "s":
                    self.graceTimer.setInterval(random.randint(2*60*1000, 3*60*1000))
                    self.graceTimer.start()
                    f.seek(0)
                    f.truncate()
                    f.write("g")

                elif line == "p":
                    self.graceTimer.stop()
                    self.solveTimer.stop()
                    headline.setText("")
                    label.setText("")

                elif line == "n":
                    with open("asteroidInputText.txt", "r") as f:
                        lines = f.readlines()
                        inputX = int(lines[0])
                        inputY = int(lines[1])
                        print(self.solveTimer.isActive())
                        if listOfSolutions[0][0] == inputX or listOfSolutions[1][0] == inputX and listOfSolutions[0][
                            1] == inputY or listOfSolutions[1][1] == inputY:
                            puzzleSolved = True#                            180000 300000
                            self.graceTimer.setInterval(random.randint(graceLow, graceHigh))
                            self.graceTimer.start()
                            self.solveTimer.stop()
                            headline.setText("")
                            label.setText("")
                            with open("asteroidInformation.txt", "r+") as f:
                                print("jhklafslkj sfajn hvhnjkö asnhhnsvnjhnjldjknlsajmlkndmjasjdmamdmjads")
                                f.seek(0)
                                f.truncate()
                                f.write("g")


        self.timerForChecking = QTimer()
        self.timerForChecking.timeout.connect(lambda *args :checkFileInput(self))
        self.timerForChecking.setInterval(1000)
        self.timerForChecking.start()
        def expectedResult(self):
            global m,t
            x = symbols('x')
            solutions = solve(0.46875 * (x-2) ** 2  -5 - (m * x + t), x)
            try :
                return [[round(solutions[0]),round(m * solutions[0] + t)], [round(solutions[1]), round(m * solutions[1] + t)]]
            except:
                updateScreen()
        FontGlowEffect(headline, glow_color=QColor(96, 0, 14), steps=25, intensity=15)
        headline_font = QFont("Bruno Ace SC", 160)

        headline_font.setBold(True)
        headline.setFont(headline_font)
        headline.setAlignment(Qt.AlignCenter)
        label_font = QFont("Bruno Ace SC", 242)
        label_font.setBold(True)
        label.setFont(headline_font)
        label.setAlignment(Qt.AlignCenter)

        # Parameters: (widget, row, column, rowSpan, colSpan)
        # We put it in row 0, starting at column 0, spanning 1 row and 4 columns
        layout.addWidget(headline, 0, 0, 1, 1)
        layout.addWidget(label, 1, 0, 1, 1)
        # --------------------------

        firstPuzzle = QWidget()
        firstPuzzle.setObjectName("MainContainer")  # Give it a unique ID
        firstPuzzle.setLayout(layout)

        firstPuzzle.setStyleSheet("""
            #MainContainer {
                background-color: black;
            }
            QLabel {
                background-color: rgba(0, 0, 0, 0); /* Keep labels transparent */
                color: white;
            }
        """)
        stack.addWidget(firstPuzzle)
        self.setCentralWidget(stack)

        stack.setCurrentIndex(0)  # actually 0


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
