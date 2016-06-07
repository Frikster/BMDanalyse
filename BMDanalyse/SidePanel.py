# -*- coding: utf-8 -*-

# Copyright (C) 2013 Michael Hogg

# This file is part of BMDanalyse - See LICENSE.txt for information on usage and redistribution

from pyqtgraph.Qt import QtCore,QtGui
        
class SidePanel(QtGui.QWidget):

    def __init__(self, parent=None):
    
        QtGui.QWidget.__init__(self,parent)
        
        self.setMinimumWidth(250)
        self.buttMinimumSize = QtCore.QSize(36,36)
        self.iconSize        = QtCore.QSize(24,24)         
        self.icons           = self.parent().icons

        self.setupImageToolbox()
        self.setupRoiToolbox()

        sidePanelLayout = QtGui.QVBoxLayout()
        sidePanelLayout.addWidget(self.imageToolbox)
        sidePanelLayout.addWidget(self.roiToolbox)        
        sidePanelLayout.setContentsMargins(0,0,0,0)
        self.setLayout(sidePanelLayout)

        self.setMaximumWidth(300)
        
    def setupImageToolbox(self):
    
        # Image filelist
        imageFileListLabel = QtGui.QLabel("Loaded images")
        self.dtypeLabel = QtGui.QLabel("data type to be loaded")
        self.dtypeValue = QtGui.QLineEdit("uint8")
        self.frameRefNameLabel  = QtGui.QLabel("Frame reference for alignment")
        self.frameRefNameValue  = QtGui.QLineEdit("400")
        self.vidWidthLabel   = QtGui.QLabel("Width")
        self.vidWidthValue   = QtGui.QLineEdit("256")
        self.vidHeightLabel  = QtGui.QLabel("Height")
        self.vidHeightValue  = QtGui.QLineEdit("256")
        self.imageFileList = QtGui.QListWidget()
        self.alignButton = QtGui.QPushButton('Align All to top')
        self.concatButton = QtGui.QPushButton('Concatenate All')
        self.temporalFilterButton = QtGui.QPushButton('Temporal filter')
        self.gsrButton = QtGui.QPushButton('Global Signal Regression')
        self.stdevButton = QtGui.QPushButton('Standard Deviation Map')

        # Image buttons
        self.buttImageAdd  = QtGui.QPushButton(self.icons['imageAddIcon'], "")
        self.buttImageRem  = QtGui.QPushButton(self.icons['imageRemIcon'], "")
        self.buttImageUp   = QtGui.QPushButton(self.icons['imageUpIcon'], "")
        self.buttImageDown = QtGui.QPushButton(self.icons['imageDownIcon'], "")
        imageButtons       = [self.buttImageAdd, self.buttImageRem, self.buttImageUp, self.buttImageDown]
        imageToolTips      = ['Add image(s)', 'Remove selected image', 'Move image down', 'Move image up']
        for i in xrange(len(imageButtons)): 
            image = imageButtons[i]
            #image.setMinimumSize(self.buttMinimumSize)
            image.setIconSize(self.iconSize)
            image.setToolTip(imageToolTips[i])  

        self.imageFileTools  = QtGui.QFrame()
        imageFileToolsLayout = QtGui.QVBoxLayout() 
        imageFileToolsLayout.setContentsMargins(0,0,0,0)
        self.imageFileTools.setLayout(imageFileToolsLayout) 
        self.imageFileTools.setLineWidth(1)
        self.imageFileTools.setFrameStyle(QtGui.QFrame.StyledPanel)            
        imageFileToolsLayout.addWidget(self.buttImageAdd)
        imageFileToolsLayout.addWidget(self.buttImageRem)        
        imageFileToolsLayout.addWidget(self.buttImageDown)
        imageFileToolsLayout.addWidget(self.buttImageUp)
        imageFileToolsLayout.addSpacerItem(QtGui.QSpacerItem(0, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))

        # Image Toolbox (containing imageFileList + imageFileList buttons)
        self.imageToolbox = QtGui.QFrame()
        self.imageToolbox.setLineWidth(2)
        self.imageToolbox.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        imageToolboxLayout = QtGui.QVBoxLayout()
        self.imageToolbox.setLayout(imageToolboxLayout)       

        grid = QtGui.QGridLayout()
        imageToolboxLayout.addLayout(grid)
        grid.addWidget(self.dtypeLabel, 0, 0)
        grid.addWidget(self.dtypeValue, 0, 1)
        grid.addWidget(self.frameRefNameLabel, 1, 0)
        grid.addWidget(self.frameRefNameValue, 1, 1)

        hbox = QtGui.QHBoxLayout()
        imageToolboxLayout.addLayout(hbox)
        hbox.addWidget(self.vidWidthLabel)
        hbox.addWidget(self.vidWidthValue)
        hbox.addWidget(self.vidHeightLabel)
        hbox.addWidget(self.vidHeightValue)

        imageToolboxLayout.addWidget(imageFileListLabel)

        hbox = QtGui.QHBoxLayout()
        imageToolboxLayout.addLayout(hbox)
        hbox.addWidget(self.imageFileTools)
        hbox.addWidget(self.imageFileList)         

        grid = QtGui.QGridLayout()
        imageToolboxLayout.addLayout(grid)
        grid.addWidget(self.alignButton, 0, 0)
        grid.addWidget(self.concatButton, 0, 1)
        grid.addWidget(self.temporalFilterButton, 1, 0)
        grid.addWidget(self.gsrButton, 1, 1)
        grid.addWidget(self.stdevButton, 2, 0)

    def createRoiMenu(self):
        self.roiMenu = popupMenu(self, self.buttRoiAdd)        

    def showRoiMenu(self):
        if self.roiMenu==None:
            self.createRoiMenu()
        self.roiMenu.update()
        self.roiMenu.show()        

    def setupRoiToolbox(self):   

        # ROI buttons
        self.buttRoiAdd  = QtGui.QPushButton(self.icons['roiAddIcon'],"")
        self.buttRoiRem  = QtGui.QPushButton(self.icons['roiRemIcon'],"")
        self.buttRoiSave = QtGui.QPushButton(self.icons['roiSaveIcon'],"")
        self.buttRoiCopy = QtGui.QPushButton(self.icons['roiCopyIcon'],"")        
        self.buttRoiLoad = QtGui.QPushButton(self.icons['roiLoadIcon'],"")
        roiButtons       = [self.buttRoiAdd, self.buttRoiRem,self.buttRoiSave,self.buttRoiCopy,self.buttRoiLoad]
        roiToolTips      = ['Add ROI','Delete ROI','Save ROI','Copy ROI','Load ROI']
        for i in xrange(len(roiButtons)): 
            button = roiButtons[i]
            #button.setMinimumSize(self.buttMinimumSize)
            button.setIconSize(self.iconSize)
            button.setToolTip(roiToolTips[i])

        # Connect buttRoiAdd button to a popup menu to select roi type
        self.createRoiMenu()        
        self.buttRoiAdd.clicked.connect(self.showRoiMenu)      

        # ROI Buttons Frame       
        self.roiButtonsFrame = QtGui.QFrame()
        roiButtonsLayout     = QtGui.QGridLayout()
        roiButtonsLayout.setContentsMargins(0,0,0,0)
        self.roiButtonsFrame.setLayout(roiButtonsLayout)
        self.roiButtonsFrame.setLineWidth(1)
        self.roiButtonsFrame.setFrameStyle(QtGui.QFrame.StyledPanel)
        roiButtonsLayout.addWidget(self.buttRoiAdd, 0, 0)
        roiButtonsLayout.addWidget(self.buttRoiLoad, 1, 0) 
        roiButtonsLayout.addWidget(self.buttRoiCopy, 2, 0)
        roiButtonsLayout.addWidget(self.buttRoiSave, 0, 1)
        roiButtonsLayout.addWidget(self.buttRoiRem, 0, 1)
        
        # ROI Info Box
        self.roiInfoBox  = QtGui.QWidget()
        roiInfoBoxLayout = QtGui.QGridLayout()
        self.roiInfoBox.setLayout(roiInfoBoxLayout)
        self.frameRateLabel   = QtGui.QLabel("Frame Rate (Hz)")
        self.frameRateValue   = QtGui.QLineEdit("30")
        self.f_lowLabel  = QtGui.QLabel("f_low")
        self.f_lowValue  = QtGui.QLineEdit("0.3")
        self.f_highLabel = QtGui.QLabel("f_high")
        self.f_highValue = QtGui.QLineEdit("3")
        self.SPC_map_mode_label = QtGui.QLabel("Click to set seed")
        self.SPC_map_mode_value = QtGui.QCheckBox()

        roiInfoBoxLayout.addWidget(self.frameRateLabel, 1, 0)
        roiInfoBoxLayout.addWidget(self.frameRateValue, 1, 1)
        roiInfoBoxLayout.addWidget(self.f_lowLabel, 2, 0)
        roiInfoBoxLayout.addWidget(self.f_lowValue, 2, 1)
        roiInfoBoxLayout.addWidget(self.f_highLabel, 3, 0)
        roiInfoBoxLayout.addWidget(self.f_highValue, 3, 1)
        roiInfoBoxLayout.addWidget(self.SPC_map_mode_label, 4, 0)
        roiInfoBoxLayout.addWidget(self.SPC_map_mode_value, 4, 1)
        
        # ROI Toolbox
        self.roiToolbox  = QtGui.QFrame()
        roiToolboxLayout = QtGui.QHBoxLayout()
        roiToolboxLayout.setContentsMargins(0,0,0,0)
        self.roiToolbox.setLayout(roiToolboxLayout)
        self.roiToolbox.setLineWidth(2)
        self.roiToolbox.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)   
        roiToolboxLayout.addWidget(self.roiInfoBox) 
        roiToolboxLayout.addWidget(self.roiButtonsFrame)
      
    def addImageToList(self,filename):
        self.imageFileList.addItem(filename) 

    def moveImageUp(self):
        """ Move current item up the list """
        # Get current row
        currentRow = self.imageFileList.currentRow()
        # If no row is current, set first row as current
        if currentRow==-1: 
            self.imageFileList.setCurrentRow(0)
            currentRow = self.imageFileList.currentRow()
        # Do not move up list if already at the end
        if (currentRow+1) <= self.imageFileList.count()-1: 
            item = self.imageFileList.currentItem()
            self.imageFileList.takeItem(currentRow)
            self.imageFileList.insertItem(currentRow+1,item.text())
            self.imageFileList.setCurrentRow(currentRow+1)
        # Show current item as selected
        #self.imageFileList.setItemSelected(self.imageFileList.currentItem(),True)
        currentItem = self.imageFileList.currentItem()  
        if not currentItem is None: 
            currentItem.setSelected(True)
        
    def moveImageDown(self):
        """ Move current item down the list """ 
        # Get current row
        currentRow = self.imageFileList.currentRow()
        # If no row is current, set first row as current        
        if currentRow==-1: 
            self.imageFileList.setCurrentRow(0)  
            currentRow = self.imageFileList.currentRow()  
        # Do not move down list if already at the beginning    
        if (currentRow-1) >= 0:
            item = self.imageFileList.currentItem()
            self.imageFileList.takeItem(currentRow)
            self.imageFileList.insertItem(currentRow-1,item.text())
            self.imageFileList.setCurrentRow(currentRow-1)
        # Show current item as selected            
        #self.imageFileList.setItemSelected(self.imageFileList.currentItem(),True)
        currentItem = self.imageFileList.currentItem() 
        if not currentItem is None: 
            currentItem.setSelected(True)

    def getListOfImages(self):
        """ Create a list of all items in the listWidget """
        items = []
        for index in xrange(self.imageFileList.count()):
            items.append(self.imageFileList.item(index))        
        return items
        
    # def updateRoiInfoBox(self,name="",pos="",size="",angle=""):
    #     print("Obsolete function")
    #     self.gsrNameValue.setText(name)
    #     self.frameRateValue.setText(pos)
    #     self.f_lowValue.setText(size)
    #     self.f_highValue.setText(angle)
        
class popupMenu(QtGui.QWidget):

    def __init__(self, parent = None, widget=None): 
   
        QtGui.QWidget.__init__(self, parent)

        self.buttMinimumSize = QtCore.QSize(36,36)
        self.iconSize        = QtCore.QSize(28,28)
        icon1 = parent.icons['roiRectIcon']
        icon2 = parent.icons['roiPolyIcon']           
        self.button1 = QtGui.QPushButton(icon1,"")
        self.button2 = QtGui.QPushButton(icon2,"")
        self.button1.setIconSize(self.iconSize)
        self.button2.setIconSize(self.iconSize)
        self.button1.setMinimumSize(self.buttMinimumSize)
        self.button2.setMinimumSize(self.buttMinimumSize)
        self.button1.setToolTip('Add rectangular ROI')            
        self.button2.setToolTip('Add polyline ROI')       

        # Set the layout
        layout = QtGui.QHBoxLayout(self)            
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)                 
        self.setLayout(layout)
        self.adjustSize()
        widget.setContentsMargins(0,0,0,0)

        # Tag this widget as a popup
        self.setWindowFlags(QtCore.Qt.Popup)

        # Handle to widget (Pushbutton in sidepanel)
        self.widget = widget
            
        # Close popup if one of the buttons are pressed
        self.button1.clicked.connect(self.hide)
        self.button2.clicked.connect(self.hide)

    def update(self):       
        # Move to top right of pushbutton
        point = self.widget.rect().topRight()
        global_point = self.widget.mapToGlobal(point)
        self.move(global_point)      
            
    def leaveEvent(self,ev):
        self.hide()            
