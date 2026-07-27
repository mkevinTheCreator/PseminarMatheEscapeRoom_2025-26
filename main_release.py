import math
import threading
import asyncio
from bellows.zigbee.application import ControllerApplication
from zigpy.config import (
    CONF_DEVICE,
    CONF_DEVICE_PATH,

)

import random
from circleButton import PaintedCircleButton
#
#
#
from endVideo import AutoplayVideoWidget

from pathlib import Path
from rocket_release import Rocket
from graph_system import graph_system
from PySide6.QtGui import Qt, QColor, QFontDatabase, QFont, QIcon
from movie_release import movie

import sys
from PySide6.QtCore import QUrl, Qt, QTimer, Signal, QPoint, QSize, QPointF,QObject, QThread
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QWidget,
    QGridLayout, QDial, QProgressBar, QVBoxLayout, QStackedWidget, QPushButton, QSizePolicy, QLineEdit,QHBoxLayout)
from customDial import CustomDial
from fontGlowEffect import FontGlowEffect

from zigpy.types import EUI64


from speech import SpeechWorker
user_input = " "
speechActive = False
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path,relative_path)
def run_loop(loop):
    loop.run_forever()

seconds =  -4
CONFIG = {
    CONF_DEVICE: {
        CONF_DEVICE_PATH: "COM6",  # adjust if needed 6 == school 3 == home
    },
    "database_path": "G:/zigpy_db/zigbee.db",

}
## usage
#with open(resource_path("config.json")) as f:

ieees = "a4:c1:38:06:f7:07:ff:ff"
endpoints = {}  # global
testing = True   

async def main():
    global endpoints
    if not testing: # change later 
     
        app = ControllerApplication(CONFIG)
        await app.startup(auto_form=True)
        await app.permit(20)

        print("Put your Sonoff plugs into pairing mode now...")
        await asyncio.sleep(30)

        for ieee, dev in app.devices.items():
            print(ieee, dev.manufacturer, dev.model)
            if "SONOFF" == dev.manufacturer:
                endpoints[ieee] = dev.endpoints[1]

        print("All endpoints ready:")
        changeSetuMessage("Found Smart Plugs : " + str(len(endpoints)))
        print(len(endpoints))
        print(endpoints)
        print(endpoints.items())

listOfValues = [0, 0, 0, 0]
variableA = 0.0
variableB = 0
variableC = 0
rocket = None
movieLabel = None

#a4:c1:38:07:73:b9:ff:ff
def sumForListValues(list: list):
    result = 0
    for i in list:
        result += i
    return result

lastSolvedTime = 0
async def checkEffects():

    global solved
    global seconds
    global lastSolvedTime
    for ieee, ep in endpoints.items():
        print(f"light lastsolvedTime {lastSolvedTime} seconds {seconds} ")
        if ieee == EUI64.convert("a4:c1:38:07:73:b9:ff:ff") and seconds - lastSolvedTime > 5:
            if listOfValues[0] == 27 and listOfValues[1] == 38 and listOfValues[2] == 24 and listOfValues[3] == 11:
                if solved[0] == False:
                    lastSolvedTime = seconds
                    solved[0] = True
                    asyncio.get_event_loop().call_later(3,lambda :  window.setCorrectValues.emit())
                    
                    window.changeLabelStatusFirstPuzzle.emit("")
                    window.changePageSignal.emit()
                    
                await ep.on_off.on()

            elif listOfValues[0] > 26 and sumForListValues(list=listOfValues) <= 100:
                await ep.on_off.on()
                window.changeLabelStatusFirstPuzzle.emit("Invalid Input")
            elif sumForListValues(list=listOfValues) >100:     
                await ep.on_off.off()
                window.changeLabelStatusFirstPuzzle.emit("Impossible Input")
            else:
                await ep.on_off.off()
                window.changeLabelStatusFirstPuzzle.emit("Invalid Input")    
                return
    if testing:    
        if listOfValues[0] == 27 and listOfValues[1] == 38 and listOfValues[2] == 24 and listOfValues[3] == 11:
            if solved[0] == False:
                print("kjyfybvxhjvahvkjajkjkjhh")
                window.changeLabelStatusFirstPuzzle.emit("")
                print("on")
                solved[0] = True
                window.changePageSignal.emit()
        elif listOfValues[0] > 26 and sumForListValues(list=listOfValues) <= 100:
            print("on")
            window.changeLabelStatusFirstPuzzle.emit("Invalid Input")
        elif sumForListValues(list=listOfValues) >100:     
            print("off")
            window.changeLabelStatusFirstPuzzle.emit("Impossible Input")
        else:
            print("off")
            window.changeLabelStatusFirstPuzzle.emit("Invalid Input")    
            return

    #else:
     #   window.changeLabelStatusFirstPuzzle.emit()

dials = []

asteroidOnce = True
async def changeValue(value, i):
    listOfValues[i] = value

    await checkEffects()

async def activateAlarm():
    for ieee, ep in endpoints.items():
        if ieee != EUI64.convert("a4:c1:38:07:73:b9:ff:ff"):
            await ep.on_off.on()

async def stopAlarm():
    for ieee, ep in endpoints.items():
        if ieee != EUI64.convert("a4:c1:38:07:73:b9:ff:ff"):
            await ep.on_off.off()
async def turnOffLight():
    for ieee, ep in endpoints.items():
        if ieee == EUI64.convert("a4:c1:38:07:73:b9:ff:ff"):
            await ep.on_off.off()
def changeSetuMessage(text: str):
    labelSetupScreen.setText(text)

solved = [False,False,False]
labelCheckingInput: QLabel = None
labelSetupScreen: QLabel = None
stack = None

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.create_task(main())
threading.Thread(target=run_loop,args=(loop,),daemon=True).start()

base_dir = Path(__file__).resolve().parent
font_path = base_dir / "fonts" / "Geostar-Regular.ttf"

app = QApplication(sys.argv)

font_id = QFontDatabase.addApplicationFont(str(font_path))
if font_id == -1:
    print("Font failed to load")
solvedOnce = True


class MainWindow(QMainWindow):
    changePageSignal = Signal()
    changeLabelStatusFirstPuzzle = Signal(str)
    setCorrectValues = Signal()
    
    def timerTick(self):
        self.effectAmbiance.play()
    def _dispatch_finished(self, text):
        self._on_speech_finished_impl(text)

    def _dispatch_failed(self):
        self._on_speech_failed_impl()
    def __init__(self):
        global dials
        global solved
        global rocket
        global stack
        global labelCheckingInput
        global labelSetupScreen
        global movieLabel
        global asteroidOnce
        def onSolved():
            print("solved")
            global rocket
            global solvedOnce
            global movieLabel
            
            
            self.effectWattariumsolved.play()
            #self.music1.play()
            rocket = Rocket(stack)
            movieLabel = movie(stack)
            self.resize(1920,1080)
            movieLabel.show()
            addButtons(3)
            movieLabel.raise_()
            
            if (solvedOnce):
                solvedOnce = False
                QTimer.singleShot(5000, lambda: onMessage())
                QTimer.singleShot(480000, lambda: self.music1.play())
                QTimer.singleShot(1680000,lambda: self.music2.play())
            

            checkIfEverythingIsSolved()
    
        def changeToInvalidInput(text):
            labelCheckingInput.setText(text)
        labelCheckingInput = QLabel("Invalid Input")
        stack = QStackedWidget()
        super().__init__()
        def setCorrectValuesFirstPuzzle():
            dials[0].setValue(27)
            dials[1].setValue(38)
            dials[2].setValue(24)
            dials[3].setValue(11)
        self.changePageSignal.connect(onSolved)
        self.setCorrectValues.connect(setCorrectValuesFirstPuzzle)
        self.changeLabelStatusFirstPuzzle.connect(changeToInvalidInput)


        self.setWindowTitle("EscapeRoomPSeminarMathe")
        layout = QGridLayout()
        self.showFullScreen()
        
        # --- 1. ADD THE HEADLINE ---
        headline = QLabel("Wattarium")
        FontGlowEffect(headline, glow_color=QColor(2, 170, 50), steps=25, intensity=15)






        headline.setFont(QFont("Geostar", 62, QFont.Weight.Bold))
        headline.setStyleSheet("""
                                                QLabel{
                                                    color: #E5791B;
                                                }
                                            """)

        headline.setAlignment(Qt.AlignCenter)



        # Parameters: (widget, row, column, rowSpan, colSpan)
        # We put it in row 0, starting at column 0, spanning 1 row and 4 columns
        layout.addWidget(headline, 0, 1, 1, 8)
        # ---------------------------

        self.effect = QSoundEffect()
        self.effect.setSource(QUrl.fromLocalFile(resource_path("media\\sounds\\dial2.wav")))#release
        self.effect.setVolume(0.6)

        self.music1 = QSoundEffect()
        self.music1.setSource(QUrl.fromLocalFile(resource_path("media/sounds/music/space_room_beat_1.wav")))
        self.music1.setVolume(0.2)

        self.music2 = QSoundEffect()
        self.music2.setSource(QUrl.fromLocalFile(resource_path("media/sounds/music/louder_atmosphere2.wav")))
        self.music2.setVolume(0.5)

        self.engineSound = QSoundEffect()
        self.engineSound.setSource(QUrl.fromLocalFile(resource_path("media/sounds/engineSound.wav")))
        self.engineSound.setVolume(0.8)

        self.effectWattariumsolved = QSoundEffect()
        self.effectWattariumsolved.setSource(QUrl.fromLocalFile(resource_path("media/sounds/wattarium.wav")))
        self.effectWattariumsolved.setVolume(0.9)
        self.effectNavigationSolved = QSoundEffect()
        self.effectNavigationSolved.setSource(QUrl.fromLocalFile(resource_path("media/sounds/navigation.wav")))
        self.effectNavigationSolved.setVolume(0.9)
        self.effectAsteroid = QSoundEffect()
        self.effectAsteroid.setSource(QUrl.fromLocalFile(resource_path("media/sounds/asteroid.wav")))
        self.effectAsteroid.setVolume(3)
        self.effectCommunication = QSoundEffect()
        self.effectCommunication.setSource(QUrl.fromLocalFile(resource_path("media/sounds/communication.wav")))
        self.effectCommunication.setVolume(0.9)

        self.effectAmbiance = QSoundEffect()
        self.effectAmbiance.setSource(QUrl.fromLocalFile(resource_path("media/sounds/ambiance.wav")))
        self.effectAmbiance.setVolume(0.05)
        self.speak = QSoundEffect()
        self.speak.setSource(QUrl.fromLocalFile(resource_path("media/sounds/solved.wav")))
        self.speak.setVolume(0.3)

        labels = ["Licht", "Antrieb", "Hitzeschild", "Klimaanlage"]
      
        for i in range(1, 5, 1):
            # --- 1. CONTAINER BOX ---
            title = QLabel(labels[i - 1])
            title.setAlignment(Qt.AlignLeft)

            titleFont = QFont("Geostar", 18)
            titleFont.setBold(True)
            title.setFont(titleFont)
            title.setFixedHeight(30)
            title.setStyleSheet("""
                QLabel {border: none;
                        color:#6C80C1;
                        background: transparent;
                        padding-bottom: 0px; 
                        padding-left: 24px;
                        height: 20px;




            }""")

            # BOX
            box = QWidget()
            box.setMinimumWidth(350)
            boxLayout = QVBoxLayout(box)
            boxLayout.setSpacing(-4)

            boxLayout.setContentsMargins(0, 0, 0, 0)  # zero top margin

            box.setStyleSheet("""
                QWidget {
                    border-right: 3px solid #6C80C1;
                    border-left: 3px solid #6C80C1;
                    border-radius: 18px;
                }
            """)

            # --- ADD TO GRID ---

            # --- 2. LABEL (NO BOX) ---
            label = QLabel("0%")
            label.setAlignment(Qt.AlignCenter)
            font = QFont("Geostar", 36)

            font.setBold(True)

            label.setFont(font)
            label.setFixedHeight(36)
            label.setContentsMargins(0, 0, 0, 0)

            label.setStyleSheet("""
            QLabel { 
                    color: #E5791B;

                    padding: 0px;
                    border: none; 
                    margin: 0px;
            }""")
            FontGlowEffect(label, glow_color=QColor(229, 121, 27), steps=15, intensity=40)
            # --- 3. PROGRESS BAR (UNCHANGED SIZE) ---
            # --- PROGRESS BAR: FIX SIZE + CORNERS ---
            progressBar = QProgressBar()
            progressBar.setOrientation(Qt.Orientation.Vertical)
            progressBar.setFixedSize(int(box.width() / 3.5), int(box.height() / 1.1))  # restore height
            progressBar.setTextVisible(False)

            progressBar.setStyleSheet("""
            QProgressBar:vertical {
                border: 2px solid transparent;
                background-color: #2E3551;
                border-radius: 0px;



            }

            QProgressBar::chunk:vertical {
                background:
                    qlineargradient(
                        x1:0, y1:1, x2:0, y2:0,
                        stop:0 #ECA376,
                        stop:1 #F3B2B3);
                margin-bottom: 20px; 
                margin-left: 10px; 
                margin-right: 10px;
                border-radius: 20px; 

            }
            """)

            #

            # --- 4. DIAL ---
            dial2 = QDial()
            dial = CustomDial(dial2)
            dials.append(dial)
            dial.setRange(0, 100)
            dial.setSingleStep(1)
            dial.setFixedSize((int)(box.width() / 2), (int)(box.width() / 2))

            dial.valueChanged.connect(lambda v, l=label: l.setText(f"{v}%"))
            dial.valueChanged.connect(progressBar.setValue)
            dial.valueChanged.connect(lambda _, l=labelCheckingInput: l.setText("Checking Input"))

            dial.valueChanged.connect(
                lambda value, i=i - 1: asyncio.run_coroutine_threadsafe(
                    changeValue(value, i),
                    loop)
            )
            dial.valueChanged.connect(self.effect.play)

            # --- 5. PACK INTO BOX ---
            boxLayout.addWidget(label, 0, alignment=Qt.AlignCenter)
            boxLayout.addWidget(progressBar, 0, alignment=Qt.AlignCenter)
            boxLayout.addWidget(dial, 0, alignment=Qt.AlignCenter)
            layout.setHorizontalSpacing(60)
            layout.setVerticalSpacing(0)
            layout.setContentsMargins(0, 0, 0, 100)
            layout.addWidget(title, 1, i +2)  # row above
            # --- 6. ADD TO GRID ---
            layout.addWidget(box, 2, i + 2, 3, 1)

        # Row 3

        labelCheckingInput.setFont(QFont("Geostar", 25, QFont.Weight.Bold))
        labelCheckingInput.setStyleSheet("color: #FFFFFF")
        labelCheckingInput.setAlignment(Qt.AlignCenter)
        layout.addWidget(labelCheckingInput, 5, 1, 1, 8)

        firstPuzzle = QWidget()
        firstPuzzle.setObjectName("MainContainer")  # Give it a unique ID
        firstPuzzle.setLayout(layout)

        firstPuzzle.setStyleSheet("""
            #MainContainer {
                background-color: #1B2024;
            }
            QLabel {
                background-color: rgba(0, 0, 0, 0); /* Keep labels transparent */
                color: white;
            }
        """)


        self.timerAmbiance = QTimer()
        self.timerAmbiance.setInterval(2 * 60 * 1000 + 49 * 1000)  # 2 minutes in milliseconds
        self.timerAmbiance.timeout.connect(self.timerTick)





        setupScreen = QWidget()
        setupScreen.setStyleSheet("""
            background-color: #000000;
        """)
        labelSetupScreen = QLabel("Put Sonoff Smart Plug into Pairing Mode")
        labelSetupScreen.setFont(QFont("Geostar", 50, QFont.Weight.Bold))
        labelSetupScreen.setStyleSheet("color: #FFFFFF")
        labelSetupScreen.setAlignment(Qt.AlignCenter)
        FontGlowEffect(labelSetupScreen, QColor(255, 255, 255), 15, 20)
        buttonSetupScreen = QPushButton("Start Escape Room?")
        buttonSetupScreen.setFixedSize(700, 300)
        buttonSetupScreen.setFont(QFont("Geostar", 30, QFont.Weight.Bold))
        buttonSetupScreen.setStyleSheet("color: #FFFFFF; border: 2px solid white; border-radius: 5px;")
        global seconds

        def takeTime():
            global seconds
            seconds += 1
            minutes, secs = divmod(seconds, 60)

            #print(seconds)
            #print(f"{minutes:02d}:{secs:02d}")

        self.timerCount = QTimer()
        self.timerCount.setInterval(1000)

        self.timerCount.timeout.connect(takeTime)
        buttonSetupScreen.clicked.connect(lambda _: (
            self.effectAmbiance.play(),
            self.timerAmbiance.start(),
            asyncio.run_coroutine_threadsafe(activateAlarm(), loop),
            stack.setCurrentIndex(1),
            self.timerCount.start(),
            QTimer.singleShot(5800, lambda: (
                stack.setCurrentIndex(2),
                asyncio.run_coroutine_threadsafe(stopAlarm(), loop),
                headline.setStyleSheet("""
                    QLabel{
                        color: #E5791B;
                        margin:50px;
                }
                """)
            ))
        ))




        layoutSetupScreen = QVBoxLayout()
        layoutSetupScreen.setContentsMargins(0, 0, 0, 0)
        layoutSetupScreen.setSpacing(30)

        labelSetupScreen.setFixedHeight(120)
        labelSetupScreen.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )
        layoutSetupScreen.addStretch(4)

        layoutSetupScreen.addWidget(labelSetupScreen, alignment=Qt.AlignHCenter)
        layoutSetupScreen.addStretch(1)
        layoutSetupScreen.addWidget(buttonSetupScreen, alignment=Qt.AlignHCenter)
        layoutSetupScreen.addStretch(3)
        setupScreen.setLayout(layoutSetupScreen)
        stack.addWidget(setupScreen)

        # optional — hook into incoming messages


        def onMessage():
            global variableA, variableB, variableC
            global user_input
            global lastSolvedTime
            with open("asteroidInformation.txt", "r+") as f:
                line = f.readline()
                if line == "w": # killmode/ failed
                    for i in range(4):
                        rand = random.randint(0, 100)
                        dials[i].setValue(rand)
                        numberA.setText(str(random.randint(0, 99)))
                        numberB.setText(str(random.randint(0, 999)))
                        numberC.setText(str(random.randint(0, 999)))
                        variableA = float(numberA.text())
                        variableB = int(numberB.text())
                        variableC = int(numberC.text())
                        thirdPuzzleNumbers[i].setText(str(random.randint(0, 10)))
                        if i <= 2:
                            solved[i] = False
                        inputThirdPuzzle[i] = str(random.randint(0, 9))
                        asyncio.run_coroutine_threadsafe(changeValue(rand, i), loop)
                    user_input = ""
                    
                    asyncio.run_coroutine_threadsafe(activateAlarm(), loop)
                    stack.setCurrentIndex(1),
                    QTimer.singleShot(4000, lambda: (
                            stack.setCurrentIndex(2),
                            asyncio.run_coroutine_threadsafe(stopAlarm(), loop)))
                    f.seek(0)
                    f.truncate()
                    f.write("g")
                    self.timerRocket.stop()
                    lastSolvedTime = 0
                    boxSecondPuzzle.setRoute(variableA,variableB,variableC,0,0,Qt.red)
                
                elif line == "n": #new
                    self.effectAsteroid.play()
                    f.seek(0)
                    f.truncate()
                    f.write("g")
            QTimer.singleShot(5000, lambda: onMessage())







        errorMessage = QWidget()
        errorMessage.setStyleSheet("""
            background-color: #000000;
        """)
        labelErrorMessage = QLabel("ERROR | RESTART WATTARIUM")
        labelErrorMessage.setFont(QFont("Geostar", 50, QFont.Weight.Bold))

        labelErrorMessage.setStyleSheet("color: #FD450A; border: 2px solid red;")
        labelErrorMessage.setAlignment(Qt.AlignCenter)
        FontGlowEffect(labelErrorMessage, QColor(253, 69, 10), 15, 20)
        layoutErrorMessage = QGridLayout()
        layoutErrorMessage.addWidget(labelErrorMessage)
        errorMessage.setLayout(layoutErrorMessage)
        stack.addWidget(errorMessage)

        stack.addWidget(firstPuzzle)







        if True:
            secondPuzzle = QWidget()

            secondPuzzle.setStyleSheet("""
                        background-color: #1B2024;
                    """)
            labelSecondPuzzle = QLabel("Navigation")
            labelSecondPuzzle.setFont(QFont("Geostar", 70, QFont.Weight.Bold))
            labelSecondPuzzle.setStyleSheet("""
                                QLabel{
                                    color: #E5791B;
                                }
                            """)
            FontGlowEffect(labelSecondPuzzle, glow_color=QColor(2, 170, 50), steps=25, intensity=15)
            labelSecondPuzzle.setAlignment(Qt.AlignCenter)

            layoutSecondPuzzle = QGridLayout()
            layoutSecondPuzzle.addWidget(labelSecondPuzzle, 1, 0, 1, 9)
            local_pos = QPointF(0, 0)

            def on_press(x, y): #importantlater
                global local_pos, variableC, variableB
                #print(variableB)
                print(f"x: {x}, y: {y}")
                if stack.currentIndex() == 3 and solved[1] == False:
                    rocket.show()
                    global_pos = boxSecondPuzzle.mapToGlobal(QPoint(round(x / 50) * 50 - 27, round(y / 50) * 50 - 35))
                    local_pos = self.centralWidget().mapFromGlobal(global_pos)
                    variableC = round((y-550)/-20)
                    variableB = round((x-800)/-100)
                    if variableB < 0:
                        numberB.setText(str(variableB))
                    else:
                        numberB.setText("+"+str(variableB))
                    if variableC < 0:
                        numberC.setText(str(variableC))
                    else:
                        numberC.setText("+"+str(variableC))

                    rocket.move(local_pos)
                    rocket.raise_()
                    on_change("", "test")

            boxSecondPuzzle = graph_system()
            boxSecondPuzzle.mouse_pressed.connect(on_press)
            boxSecondPuzzle.setStyleSheet("")
            boxSecondPuzzle.setFixedSize(1600, 700)

            layoutSecondPuzzle.addWidget(boxSecondPuzzle, 2, 1, 6, 7)
            self.timerRocket = QTimer()
            
            def on_change(text, type):
                global variableA
                global variableB
                global variableC
                global local_pos
                global solved
                if stack.currentIndex() == 3:
                    #print(text)
                    if not solved[1]:
                        if len(text) == 1 and text[0] == "+" or len(text) == 1 and text[0] == "-":
                            return
                        if len(text) >= 1:
                            #print(f"text after checks :  {text}")
                            if type == "a":
                                if text[0] == "+":
                                    variableA = float(text[1:len(text)].replace(",","."))
                                elif text[0] == "-":
                                    variableA = -float(text[1:len(text)].replace(",","."))
                                else:
                                    variableA = float(text.replace(",","."))
                                on_change("", "test")
                            if type == "b":
                                if text[0] == "+":
                                    variableB = int(text[1:len(text)])
                                elif text[0] == "-":
                                    variableB = -int(text[1:len(text)])
                                else:
                                    variableB = int(text)
                            #print(f"variableB:  {variableB} variable c: {variableC}")
                            #print(f"variableB:  {variableB} variable c: {variableC}")
                                on_press(-100*variableB+800,-20*variableC+550)
                                on_change("", "test")
                            if type == "c":
                                print(text)
                                if text[0] == "+":
                                    variableC = int(text[1:len(text)])
                                elif text[0] == "-":
                                    variableC = -int(text[1:len(text)])
                                else:
                                    variableC = int(text)
                            #print(f"variableB:  {variableB} variable c: {variableC}")
                                on_press(-100 * variableB + 800, -20 * variableC + 550)
                            #print(f"variableB:  {variableB} variable c: {variableC}")
                                on_change("", "test")#                                                              437
                    else: 
                        numberA.setText("0,46875")
                        numberB.setText("-2")
                        numberC.setText("-5")
                        rocket.raise_()
                        movieLabel.raise_()
                    if variableA == 0.46875 and variableB == -2 and variableC == -5 and solved[1] == False:
                        # rocket must be 200 -100
                        solved[1] = True
                        checkIfEverythingIsSolved()
                        rocket.solved = True
                        self.start_pos = local_pos  # snapshot position at launch time
                        self.anim_i = -200
                        
                        self.timerRocket.setInterval(16)  # 16ms ≈ 60fps, 1000ms is very slow
                        
                        self.timerRocket.start()
                        self.effectNavigationSolved.play()
                    boxSecondPuzzle.setRoute(variableA, variableB, variableC, local_pos.x(), local_pos.y(),Qt.red)

                    # print(str(variableA) + str(variableB) + str(variableC) + " " + str(local_pos.x()) + " " + str(local_pos.y()))

            self.anim_i = -200  # persistent counter

            def animateRocket():
                #xStart = self.start_pos.x() - 180  # fixed starting point, set once before timer starts
                #yStart = self.start_pos.y() -60
                xStart = 1000 -180
                yStart = 650
                bTrans = -2 * 100 
                cTrans = -5/5 * 100 
                x_val = -self.anim_i

                #y_val = yStart - (9.2  * (x_val / 100) ** 2)
                y_val = 0.465 * (((self.anim_i*-1 + bTrans)/100))**2 + cTrans / 100*5
                
                px = 775 -self.anim_i
                py = (510 - y_val * 100/5)
                
                #print(str(px) + " i " + str(self.anim_i) + " " + str(y_val) + " py " + str(py))
                if stack.currentIndex() == 3:
                    rocket.show()
                    global_pos = boxSecondPuzzle.mapToGlobal(QPoint(int(px), int(py)))
                    local_pos = self.centralWidget().mapFromGlobal(global_pos)
                    rocket.move(local_pos)

                self.anim_i += 1
                # tan
                # gegenkathete
                # ankathete
                rocket.setAngle(math.degrees(math.atan((py + 20) / (px - 138))))
                # stop when reached destination
                if px <= 200:
                    self.anim_i = -200
            self.timerRocket.timeout.connect(animateRocket)
            layoutSecondPuzzleFunction = QHBoxLayout()

            SFormF = QLabel()
            SFormF.setText("r(x)= ")
            SFormF.setFont(QFont("Arial", 32))
            SFormF.setStyleSheet("""padding-bottom: 8px;""")
            SFormF.resize(10, 60)
            SFormF.setMaximumSize(140, 60)
            SFormF.setStyleSheet("color:white;")



            numberA = QLineEdit()
            numberA.setPlaceholderText("a")
            numberA.setFont(QFont("Arial", 32))
            numberA.resize(490, 60)
            numberA.setMaxLength(7)
            numberA.setMaximumSize(490, 60)
            numberA.setAlignment(Qt.AlignCenter)
            numberA.setStyleSheet("color:white;")
            numberA.textEdited.connect(lambda text: on_change(text, "a"))

            SFormAnfang = QLabel()
            SFormAnfang.setText("* (x")
            SFormAnfang.setFont(QFont("Arial", 32))
            SFormAnfang.setStyleSheet("""padding-bottom: 8px;""")
            SFormAnfang.resize(10, 60)
            SFormAnfang.setMaximumSize(80, 60)
            SFormAnfang.setStyleSheet("color:white;")



            numberB = QLineEdit()
            numberB.setPlaceholderText("b")
            numberB.setFont(QFont("Arial", 32))
            numberB.resize(90, 60)
            numberB.setMaxLength(3)
            numberB.setMaximumSize(90, 60)
            numberB.setStyleSheet("color:white;")
            numberB.setAlignment(Qt.AlignCenter)
            numberB.textEdited.connect(lambda text: on_change(text, "b"))

            SFormMitte = QLabel()
            SFormMitte.setText(")\u00b2 ")
            SFormMitte.setFont(QFont("Arial", 32))
            SFormMitte.setStyleSheet("""padding-bottom: 8px;""")
            SFormMitte.resize(60, 60)
            SFormMitte.setMaximumSize(60, 60)
            SFormMitte.setStyleSheet("color:white;")





            numberC = QLineEdit()
            numberC.setPlaceholderText("c")
            numberC.setFont(QFont("Arial", 32))
            numberC.resize(90, 60)
            numberC.setMaxLength(3)
            numberC.setMaximumSize(90, 60)
            numberC.setStyleSheet("color:white;")
            numberC.setAlignment(Qt.AlignCenter)
            numberC.textEdited.connect(lambda text: on_change(text, "c"))

            layoutSecondPuzzleFunction.addWidget(SFormF)
            layoutSecondPuzzleFunction.addWidget(numberA)
            layoutSecondPuzzleFunction.addWidget(SFormAnfang)
            layoutSecondPuzzleFunction.addWidget(numberB)
            layoutSecondPuzzleFunction.addWidget(SFormMitte)
            layoutSecondPuzzleFunction.addWidget(numberC)


            layoutSecondPuzzle.addLayout(layoutSecondPuzzleFunction,7,0,3,9,alignment=Qt.AlignmentFlag.AlignCenter)

            secondPuzzle.setLayout(layoutSecondPuzzle)
            stack.addWidget(secondPuzzle)

        thirdPuzzle = QWidget()
        thirdPuzzle.setStyleSheet("""
                                background-color: #1B2024;
                            """)
        thirdPuzzleLabel = QLabel()

        thirdPuzzleLabel.setText("Kommunikation")
        thirdPuzzleLabel.setFont(QFont("Geostar", 62, QFont.Weight.Bold))
        thirdPuzzleLabel.setStyleSheet("""
                                        QLabel{
                                            color: #E5791B;
                                        }
                                    """)
        FontGlowEffect(thirdPuzzleLabel, glow_color=QColor(2, 170, 50), steps=25, intensity=15)
        thirdPuzzleLabel.setAlignment(Qt.AlignCenter)

        thirdPuzzleNumbers = []
        thirdPuzzleLayout = QGridLayout()
        thirdPuzzleLayout.addWidget(thirdPuzzleLabel, 0, 1, 1, 20)
        thirdPuzzle.setLayout(thirdPuzzleLayout)
        for i in range(1,5,1):
            thirdPuzzleNumber = QLineEdit()
            thirdPuzzleNumbers.append(thirdPuzzleNumber)
            thirdPuzzleNumber.setPlaceholderText("-")
            thirdPuzzleNumber.setFont(QFont("Arial", 112))
            thirdPuzzleNumber.resize(140, 300)
            thirdPuzzleNumber.setMaxLength(1)
            thirdPuzzleNumber.setMaximumSize(140, 300)
            thirdPuzzleNumber.setAlignment(Qt.AlignCenter)
            thirdPuzzleNumber.setStyleSheet("color:white;")
            thirdPuzzleNumber.textEdited.connect(lambda text, n=i-1: on_inputThirdPuzzle(text, n))
            thirdPuzzleLayout.addWidget(thirdPuzzleNumber, 1, i*4+3,5, 4)

        voiceCommandButton = PaintedCircleButton(icon=QIcon(resource_path("media\\textures\\microphone.png")), icon_size=QSize(28, 28))

        voiceCommandButton.setFixedSize(240, 240)
        voiceCommandButton.clicked.connect(lambda _: onTalk())
        voiceCommandButton.setStyleSheet("""margin-bottom: 100px;
                                        """)
        thirdPuzzleLayout.addWidget(voiceCommandButton,5,13 ,3,2)

        def onTalk():
            global speechActive
            if speechActive:
                return

            speechActive = True
            voiceCommandButton.setActive(False)     # now this WILL actually paint,
            voiceCommandButton.setEnabled(False)    # since the main thread isn't blocked
            self.effect.play()

            self.thread = QThread()
            self.worker = SpeechWorker()
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self._dispatch_finished)
            self.worker.failed.connect(self._dispatch_failed)
            self.thread.start()

        def on_speech_finished(text):
            global user_input, speechActive
            user_input = text
            voiceCommandButton.setActive(True)
            voiceCommandButton.setEnabled(True)
            speechActive = False
            self.thread.quit()
            on_inputThirdPuzzle(user_input, 4)
        

        def on_speech_failed():
            global speechActive
            self.effect.play()
            voiceCommandButton.setActive(True)
            voiceCommandButton.setEnabled(True)
            speechActive = False    
            self.thread.quit() 
        self._on_speech_finished_impl = on_speech_finished
        self._on_speech_failed_impl = on_speech_failed   

        inputThirdPuzzle= [0,0,0,0]
        def on_inputThirdPuzzle(text:str , type:int):
            user_input = ""
            if type != 4:
                inputThirdPuzzle[type] = int(text)
            else:
                user_input = text
                print(user_input)
            if inputThirdPuzzle[0] == 2 and inputThirdPuzzle[1] == 0 and inputThirdPuzzle[2] == 8 and inputThirdPuzzle[3] == 0 and correctSpeech(user_input) or inputThirdPuzzle[0] == 4 and inputThirdPuzzle[1] == 6 and inputThirdPuzzle[2] == 8 and inputThirdPuzzle[3] == 7 :
                self.effectCommunication.play()
                solved[2] = True
           
                checkIfEverythingIsSolved()

        stack.addWidget(thirdPuzzle)
        def correctSpeech(user_input:str):
            print("testing")
            possible = ["Landratsamt bitte bestätigen","London Street bitte", "wann kannst du bitte bestätigen","Landeanflug bitte", "Landeanflug bitte bestätigen","Londonflug bitte bestätigen","anderen Flug bitte bestätigen","Lampe Anzug bitte bestellen","Lampe bitte bestätigen","Lampe","Landeanflug bitte bestellen","London Flug bitte bestätigen","bitte bestätigen","London Stellplätze bitte bestätigen","London bitte"] 
            for x in range(len(possible)):
                if possible[x] == user_input:
                    return True
            return False


        buttonForFirstPuzzle = QPushButton("Wattarium")
        buttonForFirstPuzzle.setFixedSize(130, 70)
        buttonForFirstPuzzle.setFont(QFont("Geostar", 11, QFont.Weight.Bold))
        buttonForFirstPuzzle.setStyleSheet("color: #FFFFFF; border: 2px solid orange; border-radius: 5px;")
        buttonForFirstPuzzle.clicked.connect(lambda _: (addButtons(2)))
        
        buttonForNavigation = QPushButton("Navigation")
        buttonForNavigation.setFixedSize(130, 70)
        buttonForNavigation.setFont(QFont("Geostar", 11, QFont.Weight.Bold))
        buttonForNavigation.setStyleSheet("color: #FFFFFF; border: 2px solid orange; border-radius: 5px;")
        buttonForNavigation.clicked.connect(lambda _: (addButtons(3)))

        buttonForCommunication = QPushButton("Kommunikation")
        buttonForCommunication.setFixedSize(180, 70)
        buttonForCommunication.setFont(QFont("Geostar", 11, QFont.Weight.Bold))
        buttonForCommunication.setStyleSheet("color: #FFFFFF; border: 2px solid orange; border-radius: 5px;")
        buttonForCommunication.clicked.connect(lambda _: (addButtons(4)))

        buttonForAsteroid = QPushButton("Schutzschild")
        buttonForAsteroid.setFixedSize(150, 70)
        buttonForAsteroid.setFont(QFont("Geostar", 11, QFont.Weight.Bold))
        buttonForAsteroid.setStyleSheet("color: #FFFFFF; border: 2px solid orange; border-radius: 5px;")
        buttonForAsteroid.clicked.connect(lambda _: (addButtons(7)))

        layoutButtonsBoxLayout = QHBoxLayout()



        #layoutSecondPuzzle.addWidget(buttonForFirstPuzzle, 1, 7, 1, 1, Qt.AlignmentFlag.AlignCenter)
        #layoutSecondPuzzle.addWidget(buttonForThirdPuzzle, 1, 7, 1, 1, Qt.AlignmentFlag.AlignRight)
        #layoutSecondPuzzle.addWidget(buttonForSecondPuzzle, 1, 8, 1, 1, Qt.AlignmentFlag.AlignCenter)
        def addButtons(puzzle: int):
            for grid in (layoutSecondPuzzle, layout, thirdPuzzleLayout, asteroidLayout):
                grid.removeItem(layoutButtonsBoxLayout)

            for btn in (buttonForFirstPuzzle, buttonForNavigation,
                        buttonForCommunication, buttonForAsteroid):
                layoutButtonsBoxLayout.removeWidget(btn)
                btn.setParent(None)

            if puzzle == 2:
                for btn in (buttonForAsteroid, buttonForNavigation, buttonForCommunication):
                    layoutButtonsBoxLayout.addWidget(btn)
                    btn.updateGeometry()  # reset size hint
                layout.addLayout(layoutButtonsBoxLayout, 0, 6, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
                layout.activate()

            elif puzzle == 3:
                for btn in (buttonForFirstPuzzle, buttonForAsteroid, buttonForCommunication):
                    layoutButtonsBoxLayout.addWidget(btn)
                    btn.updateGeometry()  # reset size hint
                layoutSecondPuzzle.addLayout(layoutButtonsBoxLayout, 1, 6, 1, 2,
                                             alignment=Qt.AlignmentFlag.AlignHCenter)
                layoutSecondPuzzle.activate()
                

            elif puzzle == 4:
                for btn in (buttonForFirstPuzzle, buttonForNavigation, buttonForAsteroid):
                    layoutButtonsBoxLayout.addWidget(btn)
                    btn.updateGeometry()  # reset size hint
                thirdPuzzleLayout.addLayout(layoutButtonsBoxLayout, 0, 19, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
                thirdPuzzleLayout.activate()

            elif puzzle == 7:
                for btn in (buttonForFirstPuzzle, buttonForNavigation, buttonForCommunication):
                    layoutButtonsBoxLayout.addWidget(btn)
                    btn.updateGeometry()  # reset size hint
                asteroidLayout.addLayout(layoutButtonsBoxLayout, 0, 7, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
                asteroidLayout.activate()
            stack.setCurrentIndex(puzzle)
            if puzzle == 3:
                movieLabel.show()
                movieLabel.raise_()
                rocket.show()
                rocket.raise_()
            

            

        def checkIfEverythingIsSolved():
            global seconds
            global asteroidOnce
            print(f"1 {solved[0]} 2 {solved[1]} 3 {solved[2]}")
            if solved[1] and asteroidOnce:
                asteroidOnce = False
                with open("asteroidInformation.txt", "r+") as f:
                    f.write("s")
            if solved[1] and solved[2] and solved[0]:
                self.timerCount.stop()
                minutes, secs = divmod(seconds, 60)
                print("solve detected ")

                with open("scoreboard.txt", "a+") as f:
                    minutes, secs = divmod(seconds, 60)
                    f.write(f"{minutes:02d}:{secs:02d}\n")
                    f.seek(0)
                    lines = f.readlines()
                    sorted_lines = sorted(lines)
                    place = sorted_lines.index(f'{minutes:02d}:{secs:02d}\n') + 1
                    print(f"lpace : {place}")
                labelEndScreen.setText(f"time : {minutes:02d}:{secs:02d} #{place}")
                print("done")
                QTimer.singleShot(9000,lambda :stack.setCurrentIndex(6))
                QTimer.singleShot(7500,lambda: self.engineSound.play())
                QTimer.singleShot(32800,lambda :stack.setCurrentIndex(5))


        endScreen = QWidget()
        endScreen.setStyleSheet("""
                    background-color: #000000;
                """)
        labelEndScreen = QLabel(f"TY FOR PLAYING \n time : ")
        labelEndScreen.setFont(QFont("Geostar", 100, QFont.Weight.Bold))
        labelEndScreen.setStyleSheet("color: #E5791B")
        labelEndScreen.setAlignment(Qt.AlignCenter)
        FontGlowEffect(labelEndScreen, QColor(255, 255, 255), 15, 20)
        buttonEndScreen = QPushButton("ReStart Escape Room?")
        buttonEndScreen.setFixedSize(700, 300)
        buttonEndScreen.setFont(QFont("Geostar", 30, QFont.Weight.Bold))
        buttonEndScreen.setStyleSheet("color: #FFFFFF; border: 2px solid white; border-radius: 5px;")
        buttonEndScreen.clicked.connect(lambda _: (
            reset()
        ))
        def reset():
            global variableA
            global variableB
            global variableC
            global solved
            global seconds
            global solvedOnce
            global asteroidOnce
            global lastSolvedTime
            stack.setCurrentIndex(0)
            dials[0].setValue(0)
            dials[1].setValue(0)
            dials[2].setValue(0)
            dials[3].setValue(0)
            numberA.setText("")
            numberB.setText("")
            numberC.setText("")
            variableA = 0
            variableB = 0
            variableC = 0
            solved[0] = False
            solved[1] = False
            solved[2] = False
            solvedOnce = True
            asteroidOnce = True
            inputThirdPuzzle[0] = ""
            inputThirdPuzzle[1] = ""
            inputThirdPuzzle[2] = ""
            inputThirdPuzzle[3] = ""
            thirdPuzzleNumbers[0].setText(" ")
            thirdPuzzleNumbers[1].setText(" ")
            thirdPuzzleNumbers[2].setText(" ")
            thirdPuzzleNumbers[3].setText(" ")
            boxSecondPuzzle.setRoute(1, 0, 0, 0, 0,QColor(0,0,0,0))
            seconds = 0
            lastSolvedTime = 0
            asyncio.run_coroutine_threadsafe(turnOffLight(), loop)
            self.timerRocket.stop()

            
            
            with open("asteroidInputText.txt", "w") as f: 
                f.seek(0)
                f.write('{}{}'.format("0\n", "0"))
                f.truncate()
            with open("asteroidInformation.txt", "w") as f: 
                f.write("p")
            

        layoutEndScreen = QVBoxLayout()
        layoutEndScreen.setContentsMargins(0, 0, 0, 0)
        layoutEndScreen.setSpacing(30)

        labelEndScreen.setFixedHeight(120)
        labelEndScreen.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )
        layoutEndScreen.addStretch(4)

        layoutEndScreen.addWidget(labelEndScreen, alignment=Qt.AlignHCenter)
        layoutEndScreen.addStretch(1)
        layoutEndScreen.addWidget(buttonEndScreen, alignment=Qt.AlignHCenter)
        layoutEndScreen.addStretch(3)
        endScreen.setLayout(layoutEndScreen)
        stack.addWidget(endScreen)

        video_widget = AutoplayVideoWidget(resource_path("media\\textures\\0619.mp4"))
        stack.addWidget(video_widget)

        #QFontDatabase.addApplicationFont("fonts/BrunoAceSC-Regular.ttf")
        #font_id = QFontDatabase.addApplicationFont("fonts/BrunoAceSC-Regular.ttf")
        #families = QFontDatabase.applicationFontFamilies(font_id)

        asteroidLayout = QGridLayout()
        # self.showFullScreen()
        # --- 1. ADD THE HEADLINE ---
        asteroidHeadline = QLabel("Schutzschild")
        FontGlowEffect(asteroidHeadline, glow_color=QColor(2, 170, 50), steps=25, intensity=15)

        asteroidHeadline.setFont(QFont("Geostar", 62, QFont.Weight.Bold))
        asteroidHeadline.setStyleSheet("""
                                                       QLabel{
                                                           color: #E5791B;
                                                       }
                                                   """)

        asteroidHeadline.setAlignment(Qt.AlignCenter)

        # Parameters: (widget, row, column, rowSpan, colSpan)
        # We put it in row 0, starting at column 0, spanning 1 row and 4 columns

        m = random.randint(1, 9)
        t = random.randint(1, 40)

        xLabel = QLabel("x=")
        xLabel.setStyleSheet("""
                    QLabel{
                        color: #a600b5;

                    }
                """)
        FontGlowEffect(xLabel, glow_color=QColor(96, 0, 14), steps=25, intensity=15)
        asteroidHeadline_font = QFont("Bruno Ace SC", 270)

        asteroidHeadline_font.setBold(True)
        xLabel.setFont(asteroidHeadline_font)
        xLabel.setAlignment(Qt.AlignCenter)

        yLabel = QLabel("y=")
        yLabel.setStyleSheet("""
                            QLabel{
                                color: #a600b5;
                            }
                        """)
        FontGlowEffect(yLabel, glow_color=QColor(96, 0, 14), steps=25, intensity=15)
        asteroidHeadline_font = QFont("Bruno Ace SC", 270)

        asteroidHeadline_font.setBold(True)
        yLabel.setFont(asteroidHeadline_font)
        yLabel.setAlignment(Qt.AlignCenter)

        # Parameters: (widget, row, column, rowSpan, colSpan)
        # We put it in row 0, starting at column 0, spanning 1 row and 4 columns

        asteroidFirstNumber = QLineEdit()
        asteroidFirstNumber.setPlaceholderText("-")

        asteroidFirstNumber.resize(800, 800)
        asteroidFirstNumber.setMaxLength(3)
        asteroidFirstNumber.setMaximumSize(800, 800)
        asteroidFirstNumber.setAlignment(Qt.AlignCenter)

        asteroidFirstNumber.setStyleSheet("color:#a600b5;background-color:black; border-color:black;")
        asteroidFirstNumber.textEdited.connect(lambda text: (writeToFile(text, 1)))

        def writeToFile(text: str, line: int):
            with open("asteroidInputText.txt", "r+") as f:
                print(text)
                if text == "":
                    text = "0"
                lines = f.readlines()
                savedText = lines[line]
                f.seek(0)
                if line == 0:
                    f.write('{}{}'.format(savedText, text))
                else:
                    f.write('{}\n{}'.format(text, savedText))
                f.truncate()

        asteroidSecondNumber = QLineEdit()
        asteroidSecondNumber.setPlaceholderText("-")

        asteroidSecondNumber.resize(800, 800)
        asteroidSecondNumber.setMaxLength(3)
        asteroidSecondNumber.setMaximumSize(800, 800)
        asteroidSecondNumber.setAlignment(Qt.AlignCenter)
        asteroidSecondNumber.setStyleSheet("color:#a600b5;background-color:black; border-color:black;")
        asteroidSecondNumber.textEdited.connect(lambda text: (writeToFile(text, 0)))
        asteroidLayout.addWidget(asteroidHeadline,0,0,1,10)
        asteroidLayout.addWidget(xLabel,1,1,7,2)
        asteroidLayout.addWidget(asteroidFirstNumber,1,3,7,2)
        asteroidLayout.addWidget(yLabel,1,5,7,2)
        asteroidLayout.addWidget(asteroidSecondNumber,1,7,7,2)
        # --------------------------

        asteriod_input = QWidget()
        asteriod_input.setObjectName("MainContainer")  # Give it a unique ID
        asteriod_input.setLayout(asteroidLayout)

        asteriod_input.setStyleSheet("""
                    #MainContainer {
                        background-color: black;
                    }
                    QLabel {
                        background-color: rgba(0, 0, 0, 0); /* Keep labels transparent */
                        color: white;
                    }
                    QLineEdit {
                        color: #a600b5;
                        background-color: black;
                        border-color: black;
                        font-size: 200px;
                        font-weight: bold;
                    }
                """)
        stack.addWidget(asteriod_input)



        self.setCentralWidget(stack)

        stack.setCurrentIndex(0)  #  7total
        # set affter second puzle aopoears

    # QTimer.singleShot(5000,lambda v = 1: stack.setCurrentIndex(v)) # change to 28000 for production




font_path = resource_path("fonts/BrunoAceSC-Regular.ttf")
font_id = QFontDatabase.addApplicationFont(font_path)
families = QFontDatabase.applicationFontFamilies(font_id)
app.setStyleSheet(f"* {{ font-family: '{families[0]}';}}")
window = MainWindow()
window.show()
app.exec()



#   + add starting trvel voiceline              redo all voicelines 

#   wait for introduction before alarm          reevaluate

#   change timers                               testing should work 

#   testing/testing/testing