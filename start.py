import sys

from PySide6.QtWidgets import QApplication, QStackedWidget

from puzzle.wattarium import Wattarium

listOfValues = [0, 0, 0, 0]




if __name__ == "__main__":

    

    app = QApplication(sys.argv)

    
    solved = [False,False,False]
    w = Wattarium()
    stack = QStackedWidget()
    widget = w.createWattarium(
        listOfValues,
        solved
    )
    def changed():
        print("change Page")
    w.changePageSignal.connect(
        changed
    )

    
    stack.addWidget(widget)

    w.setCentralWidget(stack)
    w.resize(1920, 1080)
    w.show()

    

    sys.exit(app.exec())