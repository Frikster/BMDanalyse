import sys, os
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import filter_jeff as fj
import displacement_jeff as dj
from matplotlib.pylab import *
from PIL import Image
from PIL.ImageQt import ISPmageQt
import qimage2ndarray
import numpy as np

#todo: make size variable
width = 256
height = 256

## Define main window class from template
path = os.path.dirname(os.path.abspath(__file__))
uiFile = os.path.join(path, 'ui/brainImageAnalyserGui.ui')
WindowTemplate, TemplateBaseClass = pg.Qt.loadUiType(uiFile)

class QMainWindow(TemplateBaseClass):

    def __init__(self):
        #super(QtGui.QMainWindow, self).__init__(parent)
        TemplateBaseClass.__init__(self)

        self.ui = WindowTemplate()
        self.ui.setupUi(self)
        self.ui.pushButton_LoadData.clicked.connect(self.open_raw_set)
        self.ui.pushButton.clicked.connect(self.do_alignment)


    def open_raw_set(self):
        #Todo: amend once done
        #raw_file_folder = str(QFileDialog.getExistingDirectory(self, "Select Directory where Raws are stored"))
        raw_file_folder = '/media/cornelis/DataCDH/Data/Raw-data/Test Data/0731/Videos/Green only'
        print(raw_file_folder)

        self.lof=[]
        for root, dirs, files in os.walk(raw_file_folder):
            for file in files:
                if ((file.endswith(".raw") or file.endswith(".g")) and (os.path.join(root, file)) not in self.lof):
                    self.lof.append((os.path.join(root, file)))

        self.ui.comboBox.addItems(self.lof)
        self.ui.comboBox.currentIndexChanged.connect(self.set_reference_frames)
        self.output_ref_frame()
        self.lp = None


    def do_alignment(self):
        print("Go!")

        if(self.comboBox.currentText()!=None):
            raw_file_to_align_ind = self.comboBox.currentIndex()
            frame_ref = self.spinBox_frameRef.value()
            frame_rate = self.spinBox_FrameRate.value()
            f_high = self.doubleSpinBox_fHigh.value()
            f_low = self.doubleSpinBox_fLow.value()

            # First element in aligned_frames_list is all frames aligned to user selected raw

            # Todo: Uncomment once needed

            # if len(self.lof) > 1:
            #     print("Doing alignments...")
            #     #self.aligned_frames_list = []
            #     if (self.lp == None):
            #         self.lp=dj.get_distance_var(self.lof,width,height,frame_ref)
            #     print('Working on this file: ')+str(self.lof[raw_file_to_align_ind])
            #     frames = dj.get_frames(str(self.lof[raw_file_to_align_ind]), width, height)
            #     frames = dj.shift_frames(frames, self.lp[raw_file_to_align_ind])
            #     # self.aligned_frames_list.append(frames_aligned)
            # else:
            frames = dj.get_green_frames(str(self.lof[raw_file_to_align_ind]),width,height)

            avg_frames=fj.calculate_avg(frames)
            frames=fj.cheby_filter(frames, f_low, f_high, frame_rate)
            frames+=avg_frames

            frames=fj.calculate_df_f0(frames)

            # Todo: incorporate gsr
            frames=fj.masked_gsr(frames,width,height)

            self.preprocessed_frames = frames



            frames.astype('float32').tofile('/home/cornelis/Downloads/dfoverf0_avg_framesIncl.raw')

            #todo: remove tests
            test1 = [i*3 for i in [71,43]]
            test2 = [i*3 for i in [63,39]]
            test3 = [i*3 for i in [59,31]]
            test4 = [i*3 for i in [38,28]]
            test5 = [i*3 for i in [33, 41]]
            test6 = [i*3 for i in [24, 46]]
            test7 = [i*3 for i in [30, 64]]
            test8 = [i*3 for i in [71, 60]]
            test9 = [i*3 for i in [54, 52]]
            test10 = [i*3 for i in [42, 51]]
            test11 = [i*3 for i in [44, 31]]
            test12 = [i*3 for i in [52, 31]]



            self.compute_spc_map(test1[0],test1[1])
            #self.compute_spc_map(test2[0],test2[1])
            #self.compute_spc_map(test3[0],test3[1])
            #self.compute_spc_map(test4[0],test4[1])
            #self.compute_spc_map(test5[0],test5[1])
            #self.compute_spc_map(test6[0],test6[1])
            #self.compute_spc_map(test7[0],test7[1])
            #self.compute_spc_map(test8[0],test8[1])
            #self.compute_spc_map(test9[0],test9[1])
            #self.compute_spc_map(test10[0],test10[1])
            #self.compute_spc_map(test11[0],test11[1])
            #self.compute_spc_map(test12[0],test12[1])

            #self.output_preprocessed_ref_frame()

            # preprocessed_frames_list = []
            # for f in self.aligned_frames_list:
            #     avg_frames=fj.calculate_avg(frames)
            #     frames=fj.cheby_filter(frames, f_low, f_high, frame_rate)
            #     frames+=avg_frames
            #
            #     frames=fj.calculate_df_f0(frames)
            #     preprocessed_frames_list.append(frames)
            #
            # preprocessed_frames = preprocessed_frames_list[0]
        else:
            print("No align reference")


    def set_reference_frames(self):
        print("referenced")
        self.reference_frames = self.comboBox.currentText()
        self.output_ref_frame()


    def output_ref_frame(self):
        if(self.ui.comboBox.currentText()!=None):
            frames=fj.get_green_frames(str(self.ui.comboBox.currentText()), width, height)
            frame = frames[self.ui.spinBox_frameRef.value()]
            img = pg.ImageItem(frame)

            self.ui.graphicsView.addItem(img)

            # scene = QGraphicsScene(self)
            # scene.addPixmap(QPixmap.fromImage(qimage2ndarray.array2qimage(frame)))
            #self.ui.graphicsView.setScene(scene)


    def output_spc(self):
        print("Print out that preprocessed thang")
        scene = self.QScene(self)

        #scaled_image = Image.fromarray(np.uint8(self.image*255))
        scaled_image = Image.fromarray(255-np.uint8(self.image*255))
        plt.imshow(scaled_image, interpolation = "nearest")
        #plt.axis("off")
        #scaled_image.set_size_inches(width,height)
        #scaled_image.set_cmap(scaled_image.cmap.name+"_r")

        plt.savefig("/home/cornelis/Downloads/doesntworkavg_framesIncl.png")



        gcf().canvas.draw() # IMPORTANT!
        stringBuffer = gcf().canvas.buffer_rgba() # IMPORTANT!
        l, b, w, h = gcf().bbox.bounds

        qImage = QtGui.QImage(stringBuffer,
                      w,
                      h,
                      QtGui.QImage.Format_ARGB32)


        pixmap = QtGui.QPixmap.fromImage(qImage)
        pixmapItem = QtGui.QGraphicsPixmapItem(pixmap)

        scene.addItem(pixmapItem)
        self.graphicsView.setScene(scene)


        ## Before SO EDIT2 ##

        # pixMap = QPixmap("/home/cornelis/Downloads/itworks.png")
        #
        #
        # #pixMap = QtGui.QPixmap.fromImage(imgQ)
        #
        # #pixMapItem = QtGui.QGraphicsPixmapItem(pixMap)
        #
        # scene.addPixmap(pixMap)
        # self.graphicsView.setScene(scene)

        ## Old ##
        # scaled_image = (im + 1) * (255 / 2)
        # QGraphicsPixmapItem item( QPixmap::fromImage(image))
        #
        #
        # scene.addPixmap(QPixmap.fromImage(qimage2ndarray.array2qimage(scaled_image)))
        # self.graphicsView.setScene(scene)

        # Todo: Make scene clickable
        #self.graphicsView.mouseDoubleClickEvent(QMouseEvent)

    def compute_spc_map(self, x, y):
        #CorrelationMapDisplayer = fj.CorrelationMapDisplayer(self.preprocessed_frames)
        self.image = fj.get_correlation_map(y, x, self.preprocessed_frames)

        self.output_spc()

    class QScene(QtGui.QGraphicsScene):
        def __init__(self, *args, **kwds):
            QtGui.QGraphicsScene.__init__(self, *args, **kwds)

        def mousePressEvent(self, event):
            self.startX = event.scenePos().x()
            self.startY = event.scenePos().y()
            if event.button() == QtCore.Qt.LeftButton\
                    and 0 <= self.startX <= width and 0 <= self.startY <= height:
                item = QtGui.QGraphicsTextItem("CLICK")
                item.setPos(event.scenePos())
                self.addItem(item)
            #e = QPointF(self.mapToScene(event.pos()))
            #self.tools(e)
            self.startX = event.scenePos().x()
            self.startY = event.scenePos().y()
            print(self.startX)
            print(self.startY)
            print("------")

            self.compute_spc_map(self.startX, self.startY)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = QMainWindow()
    form.show()
    app.exec_()