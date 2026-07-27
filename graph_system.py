from PySide6.QtCore import Signal, QPoint,QRectF
from PySide6.QtGui import QFontDatabase, QPainter, QPen, Qt, QColor, QPainterPath, QTextOption, QPainterPath
from PySide6.QtWidgets import QWidget


class graph_system(QWidget):
    mouse_pressed = Signal(float, float)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.route_params = None


    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True);
        path = QPainterPath()

        path.addRoundedRect(QRectF(0, 0, 1600, 700), 150, 150);


        painter.setPen(QPen(QColor(46, 53, 81), 10));
        painter.fillPath(path, QColor(46, 53, 81));
        painter.drawPath(path);


        w, h = self.width(), self.height() #1600,700
        painter.setPen(QPen(QColor(108, 128, 193), 3))
        painter.drawLine(0, 550, w, 550)
        painter.drawLine(w//2, 0, w//2, h)

        for n in range(50,700,100):
            painter.drawLine(w//2+25, n, w//2-25, n)

        for n in range(100,1600,100):
            painter.drawLine(n, 550+25, n,550-25)
        painter.setPen(QPen(Qt.white, 10))
        i = -7
        for n in range(100,1600,100):
            painter.drawText(QPoint(n - 5, 590), str(i))
            i+=1
        i =25
        for n in range(50,800,100):
            if i != 0:
                painter.drawText(QPoint(w//2-55, n+5), str(i))
            i-=5

        painter.setPen(QPen(Qt.white, 2))
        for n in range(50,700,50):
            painter.drawLine(w//2+15, n, w//2-15, n)

        for n in range(50,1600,50):
            painter.drawLine(n, 550+15, n,550-15)
        if self.route_params:
            self.drawRoute(*self.route_params, painter)
    



    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            self.mouse_pressed.emit(pos.x(), pos.y())#

    def setRoute(self, a, b, c, x, y,color:QColor):
        """Call this whenever you want to trigger a new route draw"""
        self.route_params = (a, b, c, x, y,color)
        self.update()  # triggers paintEvent

    def drawRoute(self, a: float, b: float, c: float, x: int, y: int, color: QColor, painter):
        painter.setPen(QPen(color, 2))
        origin_px, origin_py = 900, 700
        b =b* 100 +100
        c = (c/5) * 100 +150 #/5
        
        x = origin_px - b  
        y = origin_py + c
        globeX = 330
        steps = origin_px - globeX + 30 + 200
        
        path = QPainterPath()
    
        first_point = True

        for i in range(int(b), steps + 1):
            i *= -1
            y_val = a * (((i + b)/100))**2 + c /100 *5
            px = origin_px - i*-1 
            py = origin_py - y_val  * 100 /5
            
            if first_point:
                path.moveTo(px, py)
                first_point = False
            else:
                path.lineTo(px, py)
            path.lineTo(px, py)
       
        painter.drawPath(path)
  
