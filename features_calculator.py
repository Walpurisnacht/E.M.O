import numpy as np
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import math

class MainActivity(QWidget):

    #Constructor
    def __init__(self):
        
        super(MainActivity, self).__init__()

        QMessageBox.about(self, 'Notification',
                          'Combo box for choosing quantity of features')
        self.initUI()
    
    #init UI
    def initUI(self):

        self.center()
        self.resize(300,300)

        self.setWindowTitle('Features Calculator')

        grid = QGridLayout()

        #Text Result
        self.tRes = QTextEdit()
        self.tRes.setReadOnly(True)
        self.tRes.setLineWrapMode(QTextEdit.NoWrap)
        self.tRes.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        grid.addWidget(self.tRes,1,0,1,2)

        #Open button
        self.open = QPushButton('Open')
        self.open.resize(self.open.sizeHint())
        self.open.clicked.connect(self.openClick)
        grid.addWidget(self.open,0,0)

        #Combobox to select quantity of features calculate.
        self.cb = QComboBox()
        self.cb.addItems(["[Select one]", "13 features", "26 features", "all features"])
        #self.cb.currentIndexChanged.connect(self.selectionchange)
        grid.addWidget(self.cb,0,1)

        self.setLayout(grid)
        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def openClick(self):
        
        flist = str(QFileDialog.getExistingDirectory(None, "Select img folder")) + "/"
        fname = QDir(flist)

        res =""
        if self.cb.currentText() == '13 features':
            res += "um1,um2,lm1,lm2,ule,lle,ure,lre,le,re,l1,l2,l3,label,id\n"
        elif self.cb.currentText() == '26 features':
            res += "um1,um,lm1,lm2,ule,lle,ure,lre,le,re,l1,l2,l3," \
                   "dum1,dum2,dlm1,dlm2,dule,dlle,dure,dlre,dle,dre,dl1,dl2,dl3,label,id\n"
        elif self.cb.currentText() == 'all features':
            res += "om,ole,ore,d1_1,a1_1,d1_2,a1_2,d1_3,a1_3,d1_4,a1_4,d1_5,a1_5,d1_6,a1_6,d1_7,a1_7,d1_8,a1_8," \
                   "d1_9,a1_9,d2_9,a2_9,d2_10,a2_10,d2_11,a2_11,d2_12,a2_12,d2_13,a2_13,d2_14,a2_14,d2_15,a2_15," \
                   "d2_16,a2_16,d2_17,a2_17,dc_49,ac_49,dc_50,ac_50,dc_51,ac_51,dc_52,ac_52,dc_53,ac_53,dc_54,ac_54," \
                   "dc_55,ac_55,dc_56,ac_56,dc_57,ac_57,dc_58,ac_58,dc_59,ac_59,dc_60,ac_60,dc_61,ac_61,dc_62,ac_62," \
                   "dc_63,ac_63,dc_64,ac_64,dc_65,ac_65,dc_66,ac_66,dc_67,ac_67,dc_68,ac_68,um1,um,lm1,lm2,ule,lle," \
                   "ure,lre,le,re,l1,l2,l3,dum1,dum2,dlm1,dlm2,dule,dlle,dure,dlre,dle,dre,dl1,dl2,dl3,label,id\n"

        #take all annotation file.
        lanns = fname.entryList(["*.pts"], QDir.Files, QDir.Name)

        labels = open(flist+"label.txt").read().split("\n")

        for i in range(len(labels)):
            labels[i] = labels[i].replace('.',' ')

        la = []

        for label in labels:
            la.append(label.split(" "))

        ln = []
        
        for lann in lanns:
            ln.append(lann.split("."))
        
        for i in range(len(lanns)):
            lines = open(flist+lanns[i]).read().split("\n")
            lines = lines[3:71]
            
            raw = []
            
            for line in lines:
                if line != "":
                    raw.append(np.fromstring(line, sep=" ", dtype=np.float64))
                
            for l in la:
                if l[0] == ln[i][0]:
                    res += ",".join(str(e) for e in self.calculator(raw)) + "," + l[2] + "," + l[0] + "\n"
                    break

        name = flist.replace('\\', ' ').replace('/', ' ').replace(':', '')
        name = name.split(" ")

        file = open(flist + name[-2] + "(" + self.cb.currentText() + ")" + "-dataset.csv", "w")
        file.write(res)
        file.close()             

        self.tRes.setPlainText(name[-2] + " done")
             
        
    #def selectionchange(self):

        #self.tRes.setPlainText(self.cb.currentText())
        
    def calculator(self, data):

        def eccentricity_calc(a, b):
            return np.sqrt(abs(a*a - b*b))/a

        def eccentricities_calc(data):

            res =[]

            #upper mouth 1
            res.append(eccentricity_calc((data[54][0]-data[48][0])/2,
                              (data[54][1]+data[48][1])/2 - data[51][1]))
            
            #upper mouth 2
            res.append(eccentricity_calc((data[54][0]-data[48][0])/2,
                              (data[54][1]+data[48][1])/2 - data[62][1]))
            
            #lower mouth 1
            res.append(eccentricity_calc((data[54][0]-data[48][0])/2,
                              (data[54][1]+data[48][1])/2 - data[66][1]))
            

            #lower mouth 2
            res.append(eccentricity_calc((data[54][0]-data[48][0])/2,
                              (data[54][1]+data[48][1])/2 - data[57][1]))
            

            #upper left eye
            res.append(eccentricity_calc((data[39][0]-data[36][0])/2,
                              (data[39][1]+data[36][1])/2 - (data[38][1]+data[37][1])/2))
            

            #lower left eye
            res.append(eccentricity_calc((data[39][0]-data[36][0])/2,
                              (data[39][1]+data[36][1])/2 - (data[41][1]+data[40][1])/2))
            

            #upper right eye
            res.append(eccentricity_calc((data[45][0]-data[42][0])/2,
                              (data[45][1]+data[42][1])/2 - (data[44][1]+data[43][1])/2))
            

            #lower right eye
            res.append(eccentricity_calc((data[45][0]-data[42][0])/2,
                              (data[45][1]+data[42][1])/2 - (data[47][1]+data[46][1])/2))
            

            #left eyebrown
            res.append(eccentricity_calc((data[21][0]-data[17][0])/2,
                              (data[21][1]+data[17][1])/2 - data[19][1]))
            

            #right eyebrown
            res.append(eccentricity_calc((data[26][0]-data[22][0])/2,
                              (data[26][1]+data[22][1])/2 - data[24][1]))

            return res
            

        def features_calc_13(data):

            res = []
            res += eccentricities_calc(data)
            res += linear_calc_3(data)

            return res

        def features_calc_26(data):

            f_13 = eccentricities_calc(data) + linear_calc_3(data)
            res = []
            res += f_13

            line = open("/home/elmon/neutral.csv").read()
            ldata = np.fromstring(line, sep=",")

            for i in range(0, len(ldata)):
                res.append(f_13[i] - ldata[i])

            return res

        def features_calc(data):

            res = []
            #open mouth
            res.append((data[57][1] - data[51][1])/(data[54][0] - data[48][0]))
            #open left eye
            res.append((data[41][1] - data[37][1])/(data[39][0] - data[36][0]))
            #open right eye
            res.append((data[47][1] - data[43][1])/(data[45][0] - data[42][0]))
            #distances
            vecaa = np.array([data[54][0] - data[48][0], data[54][1] - data[48][1]])
            modulus_vecaa = np.sqrt(np.dot(vecaa, vecaa))
            vecbb = np.array([data[57][0] - data[51][0], data[57][1] - data[51][1]])
            modulus_vecbb = np.sqrt(np.dot(vecbb, vecbb))

            for i in range(0, 9):
                vec = np.array([data[48][0] - data[i][0], data[48][1] - data[i][1]]) / modulus_vecaa
                modulus_vec = np.sqrt(np.dot(vec, vec))
                dot = np.dot(vec, vecaa)
                cos_angle = dot / modulus_vec / modulus_vecaa
                res.append(modulus_vec)
                res.append(cos_angle)

            for i in range(8, 17):
                vec = np.array([data[54][0] - data[i][0], data[54][1] - data[i][1]]) / modulus_vecaa
                modulus_vec = np.sqrt(np.dot(vec, vec))
                dot = np.dot(vec, vecaa)
                cos_angle = dot / modulus_vec / modulus_vecaa
                res.append(modulus_vec)
                res.append(cos_angle)

            a = np.array(data[48])
            b = np.array(data[51])
            nvecaa = np.array([vecaa[1], -vecaa[0]])
            nvecbb = np.array([vecbb[1], -vecbb[0]])

            if nvecbb[0] == 0 and nvecbb[1] == 0:
                nvecbb = np.array((1, 0))

            c = np.dot(nvecaa, a)
            d = np.dot(nvecbb, b)
            matrix = np.matrix((nvecaa, nvecbb))
            free_col = np.matrix(([c], [d]))
            cross = np.linalg.inv(matrix)*free_col

            for i in range(48, 68):
                vec = np.array([cross.item(0) - data[i][0], cross.item(1) - data[i][1]]) / modulus_vecaa
                modulus_vec = np.sqrt(np.dot(vec, vec))
                if modulus_vec == 0:
                    modulus_vec = 1
                dot = np.dot(vec, vecaa)
                cos_angle = dot / modulus_vec / modulus_vecaa
                res.append(modulus_vec)
                res.append(cos_angle)

            for e in features_calc_26(data):
                res.append(e)

            le = len(res)
            return res

        def linear_calc_3(data):

            res = []
            res.append((data[37][1]-data[19][1])/(data[8][1]-data[27][1]))
            res.append((data[51][1]-data[33][1])/(data[8][1]-data[27][1]))
            res.append((data[57][1]-data[33][1])/(data[8][1]-data[27][1]))

            return res
        
        if self.cb.currentText() == '13 features':
            return features_calc_13(data)
        elif self.cb.currentText() == '26 features':
            return features_calc_26(data)
        elif self.cb.currentText() == 'all features':
            return features_calc(data)
        
            
def main():

    app = QApplication(sys.argv)
    pk = MainActivity()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
