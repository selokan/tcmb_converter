import sys
import requests
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from decimal import Decimal
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Form(QDialog):    
    def __init__(self, parent=None):
        super().__init__(parent)
        date = self.getdata()
        self.currencies=sorted(self.isim_kod)
        dateLabel = QLabel(date)
        self.fromComboBox = QComboBox()
        self.fromComboBox.addItems(self.currencies)
        self.fromSpinBox = QDoubleSpinBox()
        self.fromSpinBox.setRange(0.01, 10000000.00)
        self.fromSpinBox.setValue(1.00)
        self.toComboBox = QComboBox()
        self.toComboBox.addItems(self.currencies)
        self.toLabel = QLabel("1.00")

        grid = QGridLayout()
        grid.addWidget(dateLabel,0,0)
        grid.addWidget(self.fromComboBox,1,0)
        grid.addWidget(self.fromSpinBox, 1, 1)
        grid.addWidget(self.toComboBox, 2, 0)
        grid.addWidget(self.toLabel, 2, 1)
        self.setLayout(grid)

        self.fromComboBox.currentTextChanged.connect(self.updateUi)
        self.toComboBox.currentIndexChanged.connect(self.updateUi)
        self.fromSpinBox.valueChanged.connect(self.updateUi)
        
        self.setWindowTitle("Currency")

    
    def updateUi(self,to=""):
        try:
            to=self.toComboBox.currentText()
            frm=self.fromComboBox.currentText()
            to_code= (self.isim_kod[to])  
            frm_code= (self.isim_kod[frm])
            to_amt=Decimal(self.kod_buying[to_code])
            frm_amt=Decimal(self.kod_buying[frm_code])
            amt=Decimal(self.fromSpinBox.value())

            amount=(frm_amt/to_amt)*amt
            self.toLabel.setText("%0.2f" % amount)
        except Exception as e:
            print(e)


    def getdata(self,isim_kod={},kod_birim={},kod_buying={},kod_selling={}):
        self.isim_kod=isim_kod
        self.kod_birim=kod_birim
        self.kod_buying=kod_buying
        self.kod_selling=kod_selling
        try:
            date = "Unknown"
            file = urlopen("http://tcmb.gov.tr/kurlar/today.xml")
            # file_handler=[]
            cur_code={}
            tree=ET.parse(file)
            root=tree.getroot()
            kod=[]
            birim=[]
            isim=[]
            f_buying=[]
            f_selling=[]

            for row in root.findall('Currency'):
                code = row.get('Kod')
                unit = row.find('Unit').text
                name = row.find('Isim').text
                currency_name = row.find('CurrencyName').text
                forex_buying = row.find('ForexBuying').text
                forex_selling = row.find('ForexSelling').text
                # banknote_buying = row.find('BanknoteBuying').text
                # banknote_selling = row.find('BanknoteSelling').text
                # cross_rate = row.find('CrossRateOther').text #    <CrossRateUSD>1</CrossRateUSD>
                kod.append(code)
                birim.append(unit)
                isim.append(name)
                f_buying.append(forex_buying)
                f_selling.append(forex_selling)
        # b_buying.append(banknote_buying)
        # b_selling.append(banknote_selling)
            kod.pop()
            birim.pop()
            isim.pop()
            f_buying.pop()
            f_selling.pop()
        # birim=[int(i) for i in birim]
            # f_buying=[int(i) for i in f_buying]
            # f_selling=[int(i) for i in f_selling]
        # kod_birim = dict(zip(kod,birim))
            isim_kod=dict(zip(isim,kod))
            kod_buying=dict(zip(kod,f_buying))
            kod_selling=dict(zip(kod,f_selling))
            kod
        # print(kod_birim)
            print(isim_kod)
            print(kod_buying)
            print(kod_selling)
        except Exception as e:
            return "Failed to download"
            print(e)
        finally:
            file.close()


app = QApplication(sys.argv)
form = Form()
form.show()
sys.exit(app.exec_())

# f_buying=[float(i) for i in f_buying]
# f_selling=[float(i) for i in f_selling]
# b_buying=[float(i) for i in b_buying]
# b_selling=[float(i) for i in b_selling]


 
# Create a dictionary from zip object
# kod_birim = dict(kod_birim)

# print(birim)
# print(isim)
# print(f_buying)
# print(f_selling)



# for row in file:
#     file_handler.append(row.decode())
# print(file_handler)
# print(len(file_handler))

# for row in file_handler:
#     if row.startswith("\t<Currency CrossOrder="):
#         line=row.split(",")
#         cur=line[0].split("\t\t\t<Unit>")[0]
#         cur_code[cur.title()]=line[0]
#     else:
#         continue
# print(cur_code)