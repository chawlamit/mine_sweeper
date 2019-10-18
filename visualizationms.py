from environment import Environment
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *



import random
import time

IMG_BOMB = QImage("./images/bug.png")
IMG_FLAG = QImage("./images/flag.png")
IMG_START = QImage("./images/rocket.png")
IMG_CLOCK = QImage("./images/clock-select.png")

NUM_COLORS = {
    1: QColor('#f44336'),
    2: QColor('#9C27B0'),
    3: QColor('#3F51B5'),
    4: QColor('#03A9F4'),
    5: QColor('#00BCD4'),
    6: QColor('#4CAF50'),
    7: QColor('#E91E63'),
    8: QColor('#FF9800')
}

LEVELS = [
    (8, 10),
    (16, 40),
    (24, 99)
]

STATUS_READY = 0
STATUS_PLAYING = 1
STATUS_FAILED = 2
STATUS_SUCCESS = 3

STATUS_ICONS = {
    STATUS_READY: "./images/plus.png",
    STATUS_PLAYING: "./images/smiley.png",
    STATUS_FAILED: "./images/cross.png",
    STATUS_SUCCESS: "./images/smiley-lol.png",
}



class Pos(QWidget):
    expandable = pyqtSignal(int, int)
    clicked = pyqtSignal()
    ohno = pyqtSignal()

    def __init__(self, x, y, *args, **kwargs):
        super(Pos, self).__init__(*args, **kwargs)

        self.setFixedSize(QSize(20, 20))

        self.x = x
        self.y = y

    def reset(self):
        self.is_start = False
        self.is_mine = False
        self.adjacent_n = 0

        self.is_revealed = False
        self.is_flagged = False

        self.update()

    def set_mine(self) :
        self.is_mine = True
        
    def set_adjacent(self,adjacent_n:int):    
        self.adjacent_n = adjacent_n

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        r = event.rect()

        if self.is_revealed:
            color = self.palette().color(QPalette.Background)
            outer, inner = color, color
        else:
            outer, inner = Qt.gray, Qt.lightGray

        p.fillRect(r, QBrush(inner))
        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)

        if self.is_revealed:
            if self.is_start:
                p.drawPixmap(r, QPixmap(IMG_START))

            elif self.is_mine:
                p.drawPixmap(r, QPixmap(IMG_BOMB))

            elif self.adjacent_n > 0:
                pen = QPen(NUM_COLORS[self.adjacent_n])
                p.setPen(pen)
                f = p.font()
                f.setBold(True)
                p.setFont(f)
                p.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, str(self.adjacent_n))

        elif self.is_flagged:
            p.drawPixmap(r, QPixmap(IMG_FLAG))
    def flag(self):
        self.is_flagged = True
        self.update()

        self.clicked.emit()

    def reveal(self):
        self.is_revealed = True
        self.update()

    def click(self):
        print("clicked")
        if not self.is_revealed:
            self.reveal()
            if self.adjacent_n == 0:
                self.expandable.emit(self.x, self.y)

        self.clicked.emit()

    def mouseReleaseEvent(self, e):
        print("Mouse {}".format(e))
        if (e.button() == Qt.RightButton and not self.is_revealed):
            self.flag()

        elif (e.button() == Qt.LeftButton):
            self.click()

            if self.is_mine:
                self.ohno.emit()


class MainWindow(QMainWindow):
    
    def __init__(self,env:Environment, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.env = env
        self.b_size = 5
        self.w=QWidget()
        self.vb=QVBoxLayout()
        self.grid=QGridLayout()
        self.grid.setSpacing(5)
        
        self.vb.addLayout(self.grid)
        
        self.w.setLayout(self.vb)
        self.setCentralWidget(self.w)
        self.init_map()
        self.reset_map()
        self.show()
        
    def init_map(self):
        # Add positions to the map
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w = Pos(x, y)
                self.grid.addWidget(w, y, x)
                # Connect signal to handle expansion.
#                 w.clicked.connect(self.trigger_start)
#                 w.expandable.connect(self.expand_reveal)
#                 w.ohno.connect(self.game_over)
    def reset_map(self):
        # Clear all mine positions
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.reset()
                query_op = self.env.query(y,x)
                if query_op == Environment.MINE :
                    w.set_mine()
                else :
                    w.set_adjacent(query_op)

        # Add mines to the positions
        #TODO : Import env
        # for cell in mine_cells:
        #     x,y  = cell // dim,cell % dim
        #     w = self.grid.itemAtPosition(y, x).widget()
        #     w.is_mine = True
        
        
if __name__ == '__main__':
    app=QApplication([])
    window=MainWindow()
    app.exec_()