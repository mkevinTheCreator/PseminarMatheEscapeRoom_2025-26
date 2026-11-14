from asyncio.events import AbstractEventLoop

from PySide6.QtCore import QObject, Signal


class zigbee(QObject):
    
    requestChangeLabelStatusFirstPuzzle = Signal(str)
    requestChangePageSignal = Signal()
    requestSetCorrectValues = Signal()
    loop:AbstractEventLoop
    def sumForListValues(self,list: list):
        result = 0
        for i in list:
            result += i
        return result
    
    
    
    
    def checkEffects(self,listOfValues,solved):
        if (
            listOfValues[0] == 27
            and listOfValues[1] == 38
            and listOfValues[2] == 24
            and listOfValues[3] == 11
        ):
            if solved[0] == False:
                print("kjyfybvxhjvahvkjajkjkjhh")
                self.requestChangeLabelStatusFirstPuzzle.emit("")
                print("on")
                solved[0] = True
                self.requestChangePageSignal.emit()
        elif listOfValues[0] > 26 and self.sumForListValues(list=listOfValues) <= 100:
            print("on")
            self.requestChangeLabelStatusFirstPuzzle.emit("Invalid Input")
        elif self.sumForListValues(list=listOfValues) > 100:
            print("off")
            self.requestChangeLabelStatusFirstPuzzle.emit("Impossible Input")
        else:
            print("off")
            self.requestChangeLabelStatusFirstPuzzle.emit("Invalid Input")
            return

    
    
    
    def changeValue(self,listOfValues,value, i,solved):
        listOfValues[i] = value
        self.checkEffects(listOfValues,solved)
        print(listOfValues)
    
    
    def activateAlarm(self):
               print("Alarm on")
    
    
    def stopAlarm(self):
                print("Alarm off")
    
    
    def turnOffLight(self):
                print("Light Off")
    
