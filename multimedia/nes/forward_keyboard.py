import serial
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QDesktopWidget, QLabel, QVBoxLayout
import time, sys
import threading



class MainWindow(QMainWindow):
    
    def __init__(self, com):
        super().__init__()
        self.interval = 0.050   # s
        self.game=b'"mario.nes"'
        self.com = com
        self.send_flag = False
        self.key = []
        self.keyControlPressed = False
        t = threading.Thread(target=self.send_thread)
        t.setDaemon(True)
        t.start()
        self.init_window()
    
    def init_window(self):
        self.key_label = QLabel("")
        frameWidget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.key_label)
        frameWidget.setLayout(layout)
        self.setCentralWidget(frameWidget)
        self.resize(300, 200)
        self.MoveToCenter()
        self.setWindowTitle("nes controller")
        self.show()
    
    def MoveToCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def send_thread(self):
        tim = time.time()
        while True:
            if self.send_flag:
                if len(self.key) != 0:
                    if time.time() -tim >= self.interval:
                        for i in self.key:
                            self.com.write(i)
                        tim = time.time()
            time.sleep(0.01)
            # ret = self.com.read()
            # print(ret.decode(), end = "")
    
    def start(self):
        self.com.write(b'\r\n\r\n')
        time.sleep(0.01)
        self.com.write(b"\x03")
        time.sleep(0.5)
        self.com.write(b'\r\n\r\n')
        time.sleep(0.5)
        self.com.write(b'import nes\r\n')
        self.com.write(b'nes.init(nes.KEYBOARD, repeat=10)\r\n')
        self.com.write(b'nes.run('+self.game+b')\r\n')
        

    def keyPressEvent(self, event):
        print(event.key())
        if event.key() == Qt.Key_M:
            self.send_flag = False
            self.com.write(b"m")
            self.send_flag = False
        elif event.key() == Qt.Key_Return or event.key()==Qt.Key_Enter:
            self.send_flag = False
            self.com.write(b"m")
            self.send_flag = False
        elif event.key() == Qt.Key_N or event.key() == 92:
            self.send_flag = False
            self.com.write(b"n")
            self.send_flag = False
        elif event.key() == Qt.Key_Minus:
            self.send_flag = False
            self.com.write(b"-")
            self.send_flag = False
        elif event.key() == Qt.Key_Equal:
            self.send_flag = False
            self.com.write(b"=")
            self.send_flag = False
        elif event.key() == Qt.Key_W or event.key() == Qt.Key_Up:
            self.send_flag = True
            self.key.append(b"w")
        elif event.key() == Qt.Key_A or event.key() == Qt.Key_Left:
            self.send_flag = True
            self.key.append(b"a")
        elif event.key() == Qt.Key_S or event.key() == Qt.Key_Down:
            self.send_flag = True
            self.key.append(b"s")
        elif event.key() == Qt.Key_D or event.key() == Qt.Key_Right:
            self.send_flag = True
            self.key.append(b"d")
        elif event.key() == Qt.Key_J:
            self.send_flag = True
            self.key.append(b"j")
        elif event.key() == Qt.Key_K:
            self.send_flag = True
            self.key.append(b"k")
        elif event.key() == Qt.Key_Escape:
            self.send_flag = False
            self.com.write(b"\x03")
        elif event.key() == Qt.Key_Control:
            self.keyControlPressed = True
        elif event.key() == Qt.Key_C:
            if self.keyControlPressed:
                self.send_flag = False
                self.com.write(b"\x03")
        # self.key_label.setText(self.key.decode())
            

    def keyReleaseEvent(self,event):
        if event.key() == Qt.Key_Control:
            self.keyControlPressed = False
        if len(self.key):
            self.key.pop()
        
        # self.key_label.setText("")
    
    def closeEvent(self, event):
        self.com.write(b'\x03')
        time.sleep(0.5)
        self.com.close()
        event.accept()


com = serial.Serial()
com.baudrate = 115200
com.port = "/dev/ttyUSB1"
com.bytesize = 8
com.stopbits = 1
com.parity = "N"
com.timeout = 1
# com.rts = True
# com.dtr = True
com.open()


app = QApplication(sys.argv)
window = MainWindow(com)
window.start()
sys.exit(app.exec_())

