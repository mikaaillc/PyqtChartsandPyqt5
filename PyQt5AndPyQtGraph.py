
from PyQt5 import uic,QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget,QVBoxLayout
import sys
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QChartView, QPieSeries, QPieSlice
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import pandas as pd

datafreamraw = pd.read_csv('cleaned_generation.csv')
datafreamraw = datafreamraw.loc[datafreamraw['Region'].isin(['England', 'Northern Ireland','Scotland','Wales','Other Sites4'])]
datafreamraw.replace('-', 0, inplace=True)
datafreamraw.replace(',', '', regex=True)
datafreamraw = datafreamraw.replace({'Region' : {
    'England' : 1,
    'Northern Ireland' : 2,
    'Scotland' : 3,
    'Wales' : 4,
    'Other Sites4' : 5
}})
datafream = datafreamraw.apply(pd.to_numeric, errors="coerce")

forpie=datafream[['Region', 'Solar PV']] 
forpie = forpie.groupby([ 'Region']).sum()
pie_country=['England', 'Northern Ireland','Scotland','Wales','Other Sites4']
pie_PV_panel=forpie.values.tolist()

total_output = datafream[['Year', 'Total']] 
total_output = total_output.groupby('Year').sum() 
total_output_years=total_output.index.tolist()
total_output_data=total_output.values.tolist()

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("interfaceui.ui", self)
        self.setWindowFlag(Qt.FramelessWindowHint) 
        self.layout1=QVBoxLayout()
        self.layout2=QVBoxLayout()
        self.checkOne.stateChanged.connect(self.create_linechart)
        self.checkTwo.stateChanged.connect(self.create_piechart)
        

    def create_linechart(self,toggle):
        if toggle == QtCore.Qt.Checked:
            self.series = QLineSeries(self) 

            
            for i, j in zip(total_output_years, total_output_data):
                self.series.append(int(i),j[0])
            
            chart =  QChart()
            chart.addSeries(self.series)
            chart.createDefaultAxes()
            chart.setAnimationOptions(QChart.SeriesAnimations)
            chart.setTitle("UK Renewable Energy 2003-2015")
            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignBottom)
        
            chartview = QChartView(chart)
            chartview.setRenderHint(QPainter.Antialiasing)

            self.layout1.addWidget(chartview)
            self.widget.setLayout(self.layout1)
   

    def create_piechart(self,toggle):
        if toggle == QtCore.Qt.Checked:
            series = QPieSeries()
            for i, j in zip(pie_country, pie_PV_panel):
                series.append(i,j[0])

            slice = QPieSlice()
            slice = series.slices()[0]
            slice.setExploded(True)
            slice.setLabelVisible(True)
            slice.setPen(QPen(Qt.darkGreen, 2))
            slice.setBrush(Qt.green)
    
            chart = QChart()
            chart.addSeries(series)
            chart.createDefaultAxes()
            chart.setAnimationOptions(QChart.SeriesAnimations)
            chart.setTitle("UK SOLAR PV 2003-2015")
    
    
            chartview = QChartView(chart)
            chartview.setRenderHint(QPainter.Antialiasing)
    
            self.layout2.addWidget(chartview)
            self.widget_2.setLayout(self.layout2)

App = QApplication([])
window = Window()
window.show()
App.exec_()
