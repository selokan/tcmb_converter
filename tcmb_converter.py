import sys
import requests
import xml.etree.ElementTree as ET
import datetime
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
        self.fromSpinBox.setRange(0.001, 10000000.00)
        self.fromSpinBox.setValue(1.000)
        self.toComboBox = QComboBox()
        self.toComboBox.addItems(self.currencies)
        self.toLabel = QLabel("1.000")

        grid = QGridLayout()
        grid.addWidget(dateLabel,0,0)
        grid.addWidget(self.fromComboBox,1,0)
        grid.addWidget(self.fromSpinBox, 1, 1)
        grid.addWidget(self.toComboBox, 2, 0)
        grid.addWidget(self.toLabel, 2, 1)
        self.setLayout(grid)

        self.fromComboBox.currentIndexChanged.connect(self.updateUi)
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
            frm_amt=Decimal(self.kod_selling[frm_code])
            amt=Decimal(self.fromSpinBox.value())

            amount=(frm_amt/to_amt)*amt
            self.toLabel.setText("%0.2f" % amount)

        except Exception as e:
            print(e)


    def getdata(self):       
        try:
            
            file = urlopen("http://tcmb.gov.tr/kurlar/today.xml")
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
                kod.append(code)
                birim.append(unit)
                isim.append(name)
                f_buying.append(forex_buying)
                f_selling.append(forex_selling)
            kod.pop()
            birim.pop()
            isim.pop()
            f_buying.pop()
            f_selling.pop()
            kod.append('TRY')
            birim.append('1')
            isim.append('TÜRK LİRASI')
            f_buying.append('1.00000')
            f_selling.append('1.00000')

            self.isim_kod=dict(zip(isim,kod))
            self.kod_buying=dict(zip(kod,f_buying))
            self.kod_selling=dict(zip(kod,f_selling))
            print(self.isim_kod)
            print(self.kod_buying)
            print(self.kod_selling)
            date=datetime.date.today()
            return "Türkiye Cumhuriyet Merkez Bankası Kurları: %s " % date
              
        except Exception as e:
            return "Failed to download"
            print(e)
        finally:
            file.close()


app = QApplication(sys.argv)
form = Form()
form.show()
sys.exit(app.exec_())