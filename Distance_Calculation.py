#Importing required modules
############################################################################
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog,QMainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import sys
import os 
from os import path
import utm
import math

FORM_CLASS,_ = loadUiType(path.join(path.dirname(__file__),"Distance_Calculation.ui"))
########################################################################
 #Initiate UI File
#####################################################################
class Distance_App(QMainWindow,FORM_CLASS):
    def __init__(self,parent=None):
        super(Distance_App,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
###############################    
        self.GUI_Settings()
        self.Generator()        
###############################
    
    def GUI_Settings(self):
        self.setWindowTitle ("Distance Calculator")
        self.setFixedSize (723,395)
    
    def Generator(self):
        self.pushButton.clicked.connect(self.Inputs)

    def Inputs(self):
        self.lis = [self.lineEdit.text(),self.lineEdit_2.text(),self.lineEdit_3.text(),self.lineEdit_4.text()]
        inputs = [float(i) for i in self.lis]
        self.lat1 = inputs[0]
        self.long1 = inputs[1]
        self.lat2 = inputs[2]
        self.long2 = inputs[3]
        self.Geo_To_Utm()
        self.Bearing()
       
    def Geo_To_Utm(self):
        self.point1 = utm.from_latlon(self.lat1,self.long1)
        self.point2 = utm.from_latlon(self.lat2,self.long2)
        self.N_1 = self.point1[0]
        self.E_1 = self.point1[1]
        self.N_2 = self.point2[0]
        self.E_2 = self.point2[1]

        Dist = (((self.N_1 - self.N_2 )**2) + ((self.E_1 - self.E_2 )**2))**0.5
        self.lineEdit_5.setText(str(round(Dist,3))) 
        
        
        
        
        
    def Bearing(self):
"""
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
        self.pointA = (self.N_1,self.E_1)
        self.pointB = (self.N_2,self.E_2)
         
        if (type(self.pointA) != tuple) or (type(self.pointB) != tuple):
            raise TypeError("Only tuples are supported as arguments")
    
        lat1 = math.radians(self.pointA[0])
        lat2 = math.radians(self.pointB[0])
    
        diffLong = math.radians(self.pointB[1] - self.pointA[1])
    
        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                * math.cos(lat2) * math.cos(diffLong))
    
        initial_bearing = math.atan2(x, y)
    
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360
    
        self.lineEdit_6.setText(str(round(compass_bearing,2)))
    
#######################################################################  
#Initiate UI File
#######################################################################      
def main ():
        app = QApplication(sys.argv)
        window = Distance_App()
        window.show()
        app.exec_()
    
if __name__ == '__main__':
                main()
#######################################################################  