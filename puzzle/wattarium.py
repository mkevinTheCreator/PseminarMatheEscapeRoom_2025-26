import asyncio
from pathlib import Path
from typing import Any, Coroutine, cast

from PySide6.QtCore import (
    Qt,
    QUrl,
    Signal,
)
from PySide6.QtGui import QColor, QFont, QFontDatabase
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import (
    QDial,
    QGridLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)

from DEBUG import DEBUG

if DEBUG:
    from zigbeeEmulation import zigbee
else:
    from zigbee import zigbee

from customDial import CustomDial
from fontGlowEffect import FontGlowEffect


class Wattarium(QMainWindow):
   
    
    changePageSignal = Signal()
    setCorrectValues = Signal()
    zigbeeProt:zigbee = zigbee()
    dials = []
    
    def createWattarium(self,listOfValues,solved):
        labelCheckingInput = QLabel()
        self.zigbeeProt.requestChangeLabelStatusFirstPuzzle.connect(
            labelCheckingInput.setText
        )
        self.zigbeeProt.requestChangePageSignal.connect(
            self.changePageSignal.emit
        )
        self.zigbeeProt.requestSetCorrectValues.connect(
            lambda _ : (
                self.dials[0].setValue(27),
                self.dials[1].setValue(38),
                self.dials[2].setValue(24),
                self.dials[3].setValue(11)
            )

            
        )
        base_dir = Path(__file__).resolve().parent.parent
        font_path = base_dir / "fonts" / "Geostar-Regular.ttf"
        sound_path = base_dir/ "media" / "sounds" / "dial2.wav"
        QFontDatabase.addApplicationFont(str(font_path))
        headline = QLabel("Wattarium")
        FontGlowEffect(headline, glow_color=QColor(2, 170, 50), steps=25, intensity=15)
        self.effect = QSoundEffect()
        self.effect.setSource(QUrl.fromLocalFile(str(sound_path)))
        self.effect.setVolume(0.6)
        
    
    
    
    
        headline.setFont(QFont("Geostar", 62, QFont.Weight.Bold))
        headline.setStyleSheet("""
                                                QLabel{
                                                    color: #E5791B;
                                                }
                                            """)
        
        headline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
    
    
        # Parameters: (widget, row, column, rowSpan, colSpan)
        # We put it in row 0, starting at column 0, spanning 1 row and 4 columns
        layout = QGridLayout()
        layout.addWidget(headline, 0, 1, 1, 8)
        # ---------------------------
        
    
        labels = ["Licht", "Antrieb", "Hitzeschild", "Klimaanlage"]
        
        for i in range(1, 5, 1):
            # --- 1. CONTAINER BOX ---
            title = QLabel(labels[i - 1])
            title.setAlignment(Qt.AlignmentFlag.AlignLeft)
            
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
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
            
    
            # --- 4. DIAL ---
            dial2 = QDial()
            dial = CustomDial(dial2)
            self.dials.append(dial)
            dial.setRange(0, 100)
            dial.setSingleStep(1)
            dial.setFixedSize((int)(box.width() / 2), (int)(box.width() / 2))
            dial.valueChanged.connect(self.effect.play)
            dial.valueChanged.connect(lambda v, l=label: l.setText(f"{v}%"))
            dial.valueChanged.connect(progressBar.setValue)
            dial.valueChanged.connect(lambda _, l=labelCheckingInput: l.setText("Checking Input"))
            if DEBUG:
                dial.valueChanged.connect(
                    lambda value, i=i - 1: 
                        self.zigbeeProt.changeValue(listOfValues,value, i,solved)
                )
            else:
                dial.valueChanged.connect(
                        lambda value, i=i - 1:
                            asyncio.run_coroutine_threadsafe(
                                cast(
                                    Coroutine[Any, Any, None],
                                    self.zigbeeProt.changeValue(
                                        listOfValues, value, i, solved
                                    )
                                ),
                                self.zigbeeProt.loop
                            )
                    )
            
            
            # --- 5. PACK INTO BOX ---
            boxLayout.addWidget(label, 0, alignment=Qt.AlignmentFlag.AlignCenter)
            boxLayout.addWidget(progressBar, 0, alignment=Qt.AlignmentFlag.AlignCenter)
            boxLayout.addWidget(dial, 0, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.setHorizontalSpacing(60)
            layout.setVerticalSpacing(0)
            layout.setContentsMargins(0, 0, 0, 100)
            layout.addWidget(title, 1, i +2)  # row above
            # --- 6. ADD TO GRID ---
            layout.addWidget(box, 2, i + 2, 3, 1)
            
        # Row 3
        
        labelCheckingInput.setFont(QFont("Geostar", 25, QFont.Weight.Bold))
        labelCheckingInput.setStyleSheet("color: #FFFFFF")
        labelCheckingInput.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        return firstPuzzle
