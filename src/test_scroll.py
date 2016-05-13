from PyQt4.QtGui import * 
from PyQt4.QtCore import * 
import sys

#_________MyMainWindow Class Definition______________
class MyMainWindow(QMainWindow):  
  @pyqtSlot()
  def slotAbout(self):
    QMessageBox.about(self,"About","This is an about box \n shown with QAction of QMenu.")
#_________End of MyMainWindow Class Definition_______


#_________Main Method________________________________
def main():  
    app 	  = QApplication(sys.argv)
    mainWindow	  = MyMainWindow()
    centralWidget = QWidget()
    menu  	  = QMenuBar(centralWidget)
    menu1 	  = QMenu("About Menu")
    action 	  = menu1.addAction("About")
    
    action.setShortcut(QKeySequence("Shift+P"))
    
    menu.addMenu(menu1)
    
    mainWindow.setCentralWidget(centralWidget)
    mainWindow.setWindowTitle("QMenu Add Action")
    mainWindow.setFixedSize(400,400)
    mainWindow.show()
    
    QObject.connect(action,SIGNAL("triggered()"),mainWindow,SLOT("slotAbout()"))
    return app.exec_()    
#____________________________________________________


if __name__ == '__main__':
  main()
