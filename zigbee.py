import asyncio
import threading
import time

from bellows.zigbee.application import ControllerApplication
from PySide6.QtCore import (
    QObject,
    Signal,
)
from zigpy.config import (
    CONF_DEVICE,
    CONF_DEVICE_PATH,
)
from zigpy.types import EUI64

from DEBUG import DEBUG


class zigbee(QObject):
    CONFIG:dict
    
    def __init__(self):
        self.CONFIG = {
            CONF_DEVICE: {
                CONF_DEVICE_PATH: "COM6",
            },
            "database_path": "G:/zigpy_db/zigbee.db",
        }
    
        self.loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        
        asyncio.set_event_loop(self.loop)
        
        self.loop.create_task(self.main())
        
        threading.Thread(
            target=self.run_loop,
            args=(self.loop,),
            daemon=True
        ).start()
        self.lastSolvedTime = 0
        self.seconds = 0
        
    def run_loop(self,loop):
        loop.run_forever()
            
    requestChangeLabelStatusFirstPuzzle = Signal(str)
    requestChangePageSignal = Signal()
    requestSetCorrectValues = Signal()
    
    
    ieees = "a4:c1:38:06:f7:07:ff:ff"
    endpoints = {}  # global
    
    
    async def main(self):
        if not DEBUG:  # change later
            app = ControllerApplication(self.CONFIG)
            await app.startup(auto_form=True)
            await app.permit(30)
            
            print("Put your Sonoff plugs into pairing mode now...")
            await asyncio.sleep(30)
            
            for ieee, dev in app.devices.items():
                print(ieee, dev.manufacturer, dev.model)
                if "SONOFF" == dev.manufacturer:
                    self.endpoints[ieee] = dev.endpoints[1]
                    
            print("All endpoints ready:")
            print("Found Smart Plugs : " + str(len(self.endpoints)))
            print(len(self.endpoints))
            print(self.endpoints)
            print(self.endpoints.items())
            
    
    # a4:c1:38:07:73:b9:ff:ff
    def sumForListValues(self,list: list):
        result = 0
        for i in list:
            result += i
        return result
            
    
    
    
    async def checkEffects(self,listOfValues,solved):
        
        for ieee, ep in self.endpoints.items():
            print(f"light lastsolvedTime {self.lastSolvedTime} seconds {time.time()} ")
            if (
                ieee == EUI64.convert("a4:c1:38:07:73:b9:ff:ff")
                and int(time.time()- self.lastSolvedTime) > 5
            ):
                if (
                    listOfValues[0] == 27
                    and listOfValues[1] == 38
                    and listOfValues[2] == 24
                    and listOfValues[3] == 11
                ):
                    if solved[0] == False:
                        self.lastSolvedTime = time.time()
                        solved[0] = True
                        asyncio.get_event_loop().call_later(
                            3, lambda: self.requestSetCorrectValues.emit()
                        )
                        
                        self.requestChangeLabelStatusFirstPuzzle.emit("")
                        self.requestChangePageSignal.emit()
                        
                    await ep.on_off.on()
                    
                elif listOfValues[0] > 26 and self.sumForListValues(list=listOfValues) <= 100:
                    await ep.on_off.on()
                    self.requestChangeLabelStatusFirstPuzzle.emit("Invalid Input")
                elif self.sumForListValues(list=listOfValues) > 100:
                    await ep.on_off.off()
                    self.requestChangeLabelStatusFirstPuzzle.emit("Impossible Input")
                else:
                    await ep.on_off.off()
                    self.requestChangeLabelStatusFirstPuzzle.emit("Invalid Input")
                    return
            self.lastSolvedTime = time.time()               
    
    
    async def changeValue(self,listOfValues,value, i,solved):
        listOfValues[i] = value
        await self.checkEffects(listOfValues,solved)
        
    
    async def activateAlarm(self):
        for ieee, ep in self.endpoints.items():
            if ieee != EUI64.convert("a4:c1:38:07:73:b9:ff:ff"):
                await ep.on_off.on()
                
    
    async def stopAlarm(self):
        for ieee, ep in self.endpoints.items():
            if ieee != EUI64.convert("a4:c1:38:07:73:b9:ff:ff"):
                await ep.on_off.off()
                
    
    async def turnOffLight(self):
        for ieee, ep in self.endpoints.items():
            if ieee == EUI64.convert("a4:c1:38:07:73:b9:ff:ff"):
                await ep.on_off.off()
                
       
    
    