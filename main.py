# -*- coding: utf-8 -*-
from PyQt4.QtGui import QWidget,QDialog
from PyQt4.QtGui import QComboBox, QVBoxLayout
from PyQt4.QtGui import QHBoxLayout, QPushButton

from PyQt4.QtGui import QAction,QMessageBox

from qgis.core import QgsMapLayerRegistry



class main:
    
    def __init__(self,iface):
        self.iface = iface
        self.dlg_config = slideConfig(self.iface)
        
        
    def initGui(self):
        self.action = QAction(u"レイヤスライドショー",self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu(u"&レイヤスライドショー",self.action)

    def unload(self):        
        self.iface.removePluginMenu(u"&レイヤスライドショー", self.action)
    
    def run(self):   
        myLegendInterface = self.iface.legendInterface()              
        myGroupList = myLegendInterface.groups()
        
        if len(myGroupList) > 0:
            self.dlg_config.initGui(myGroupList)
            self.dlg_config.show()
        else:
            QMessageBox.warning(self.iface.mainWindow(),u"警告",u"グループがありません")

                
    
class slideConfig(QDialog):
    
    def __init__(self,iface):
        QDialog.__init__(self)
        self.iface = iface
        
        self.slideButonDia = slideButtonDia(self.iface) 
        self.myLayerTreeView = self.iface.layerTreeView()
        self.myLegendInterface = self.iface.legendInterface()
        
    def initGui(self,groupList):
        
        self.VBL_main = QVBoxLayout()
        
        self.CoB_group = QComboBox()
        self.CoB_group.addItems(groupList)
        
        self.VBL_main.addWidget(self.CoB_group)
        
        self.PuB_setGroup = QPushButton()
        self.PuB_setGroup.setText(u"SET")
        
        self.PuB_cancel = QPushButton()
        self.PuB_cancel.setText(u"Cancel")
        
        self.HBL= QHBoxLayout()
        self.HBL.addWidget(self.PuB_setGroup)
        self.HBL.addWidget(self.PuB_cancel)
        
        self.VBL_main.addLayout(self.HBL)
        
        self.setLayout(self.VBL_main)
        
        self.PuB_setGroup.clicked.connect(self.setButtonAction)
        self.PuB_cancel.clicked.connect(self.close)
        
    def setButtonAction(self):
        groupName = self.CoB_group.currentText()
        layerNameList = [list[1] for list in self.myLegendInterface.groupLayerRelationship() if list[0] == groupName][0]
        
        if len(layerNameList) > 1:
            self.myLayerTreeView.setCurrentLayer(QgsMapLayerRegistry.instance().mapLayer(layerNameList[0]))
            self.myLayerTreeView.currentGroupNode().setIsMutuallyExclusive(True)
                        
            self.slideButonDia.setLayerList(layerNameList)
            self.slideButonDia.moveTop()
            self.slideButonDia.initGui()
            self.slideButonDia.show()
            self.close()
        else:
            QMessageBox.warning(self,u"警告",u"そのグループにはレイヤが２つ以上ありません")
            self.close()
                
        
        
        
class slideButtonDia(QDialog):
    
    def __init__(self,iface):
        QDialog.__init__(self)
        
        self.iface = iface
        self.layerNameList = []
        
        self.myLegendInterface = self.iface.legendInterface()
        self.layerId = 0
        
        
    def initGui(self):
        self.VBL_main = QVBoxLayout()
        
        self.PuB_top = QPushButton()
        self.PuB_top.setText(u"Top")
        
        self.PuB_up = QPushButton()
        self.PuB_up.setText(u"Up")
        
        self.PuB_down = QPushButton()
        self.PuB_down.setText(u"Down")
        
        self.PuB_Bottom = QPushButton()
        self.PuB_Bottom.setText(u"Bottom")
        
        self.PuB_close = QPushButton()
        self.PuB_close.setText(u"Close")
        
        self.VBL_main.addWidget(self.PuB_top)
        self.VBL_main.addWidget(self.PuB_up)
        self.VBL_main.addWidget(self.PuB_down)
        self.VBL_main.addWidget(self.PuB_Bottom)
        self.VBL_main.addWidget(self.PuB_close)
        
        self.setLayout(self.VBL_main)
        
        self.PuB_top.clicked.connect(self.moveTop)
        self.PuB_up.clicked.connect(self.moveUp)
        self.PuB_down.clicked.connect(self.moveDown)
        self.PuB_Bottom.clicked.connect(self.moveBottom)
        self.PuB_close.clicked.connect(self.close)
        
        
        
    def setLayerList(self,layerNameList):
        self.layerNaameList = layerNameList


    def moveTop(self):
        self.myLegendInterface.setLayerVisible(QgsMapLayerRegistry.instance().mapLayer(self.layerNaameList[0]),True)
        self.layerId = 0
        
    def moveBottom(self):
        self.myLegendInterface.setLayerVisible(QgsMapLayerRegistry.instance().mapLayer(self.layerNaameList[-1]),True)
        self.layerId = len(self.layerNaameList)
        
    def moveDown(self):
        if self.layerId < len(self.layerNaameList)-1:
            self.layerId += 1
            self.myLegendInterface.setLayerVisible(QgsMapLayerRegistry.instance().mapLayer(self.layerNaameList[self.layerId]),True)
            
    def moveUp(self):
        if self.layerId > 0:
            self.layerId -= 1
            self.myLegendInterface.setLayerVisible(QgsMapLayerRegistry.instance().mapLayer(self.layerNaameList[self.layerId]),True)             
    
        
        
        
        
        
        
        
        
        
        
        
        