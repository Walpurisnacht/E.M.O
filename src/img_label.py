import sys
import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MainActivity(QWidget):

    label = []
    iterator = 0
    
    # Constructor
    def __init__(self):
        super(MainActivity, self).__init__()

        QMessageBox.about(self,'README',
                          'Z = -1\nX = 0\nC = 1\nBackspace = Back')
        
        # File fetch
        self.flist = str(QFileDialog.getExistingDirectory(
            self,'Select img folder')) + '/'
        self.fname = QDir(self.flist)

        self.limg = self.fname.entryList(['*.jpg','*.png'],
                                         QDir.Files, QDir.Name)
        MainActivity.label = [None] * len(self.limg)
        
        self.initUI()
        
    # Init GUI
    def initUI(self):
        
        # Main panel
        self.center()
        self.setWindowTitle('Label')

        # Shortcut set
        self.set_neu = QShortcut(self)
        self.set_neu.setKey(Qt.Key_X)
        self.set_neu.activated.connect(self.neu_lbl)

        self.set_pos = QShortcut(self)
        self.set_pos.setKey(Qt.Key_C)
        self.set_pos.activated.connect(self.pos_lbl)

        self.set_neg = QShortcut(self)
        self.set_neg.setKey(Qt.Key_Z)
        self.set_neg.activated.connect(self.neg_lbl)

        self.set_fix = QShortcut(self)
        self.set_fix.setKey(Qt.Key_Backspace)
        self.set_fix.activated.connect(self.fix_lbl)

        # Layout
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.label = QLabel(self)
        self.pixmap = QPixmap(self.flist+self.limg[MainActivity.iterator])
        self.label.setPixmap(self.pixmap)
        self.grid.addWidget(self.label,0,0)
        
        self.show()

    # Labeling
    def fix_lbl(self):
        if (MainActivity.iterator <= 0):
            QMessageBox.about(self,'Warming!','Out of index')
            pass
        else:
            MainActivity.iterator -= 1
            self.pixmap = QPixmap(self.flist+self.limg[MainActivity.iterator])
            self.label.setPixmap(self.pixmap)
    
    def neu_lbl(self):
        MainActivity.label[MainActivity.iterator] = 0
        MainActivity.iterator += 1
        if (MainActivity.iterator == len(self.limg)):
            self.close()
        else:
            self.pixmap = QPixmap(self.flist+self.limg[MainActivity.iterator])
            self.label.setPixmap(self.pixmap)

    def neg_lbl(self):
        MainActivity.label[MainActivity.iterator] = -1
        MainActivity.iterator += 1
        if (MainActivity.iterator == len(self.limg)):
            self.close()
        else:
            self.pixmap = QPixmap(self.flist+self.limg[MainActivity.iterator])
            self.label.setPixmap(self.pixmap)

    def pos_lbl(self):
        MainActivity.label[MainActivity.iterator] = 1
        MainActivity.iterator += 1
        if (MainActivity.iterator == len(self.limg)):
            self.close()
        else:
            self.pixmap = QPixmap(self.flist+self.limg[MainActivity.iterator])
            self.label.setPixmap(self.pixmap)
        
    # Set window at enter
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Close event handler
    def closeEvent(self, event):

        rep = QMessageBox.question(self, 'Confirmation',
                                   'Quit and save?', QMessageBox.Yes |
                                   QMessageBox.No)

        if rep == QMessageBox.Yes:
            if (os.path.exists(self.flist+'label.txt')):
                print('Deleted label.txt')
                os.remove(self.flist+'label.txt')
                
            with open(self.flist+'label.txt','w') as fopen:
                data = ""
                for x in range(len(self.limg)):
                    data += str(self.limg[x]) + ' '
                    data += str(MainActivity.label[x]) + '\n'
                fopen.write(data)
                fopen.close()
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    pk = MainActivity()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
