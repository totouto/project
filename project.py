# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import sys, os
import cv2
import qimage2ndarray
from KernelGAN.KernelGAN_main import *
from PIL import Image

form_class = uic.loadUiType("project.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self, fixed_hparams) :
        super().__init__()
        self.setupUi(self)
        self.progressBar.setValue(0)
        self.Button_Input.clicked.connect(self.showFiles)
        self.Button_Output.clicked.connect(self.showFiles_2)
        self.Button_Original.clicked.connect(self.showOrignal)
        self.Button_Bicubic.clicked.connect(self.showBicubic)
        self.Button_Test.clicked.connect(self.showKernelGAN(fixed_hparams=fixed_hparams))

    def showFiles(self):
        url = QFileDialog.getOpenFileName()[0]
        self.label_Input.setText(url)
        return url
    
    def showFiles_2(self):
        url = QFileDialog.getExistingDirectory()[:]
        self.label_Output.setText(url)
        return url
    
    def showOrignal(self):
        url = self.label_Input.text()
        qPixmapVar = QPixmap()
        qPixmapVar.load(url)
        qPixmapVar = qPixmapVar.scaledToWidth(300)
        self.label_Original.setPixmap(qPixmapVar)

    def showBicubic(self):
        url = self.label_Input.text()
        img_name = url[url.rfind("/")+1:-4]
        url_2 = self.label_Output.text()
        save_name = url_2 + "/" + img_name + "/Bicubic_" +img_name + ".png"

        out_folder = os.path.join(url_2, img_name)
        os.makedirs(out_folder)


        im = Image.open(url)
        width, height = im.size

        bicubic_upscaled = im.resize((width*2, height*2), Image.BICUBIC) #.save("resized.jpg")

        if bicubic_upscaled.mode == "RGB":
            r, g, b = bicubic_upscaled.split()
            bicubic = Image.merge("RGB", (b, g, r))
        elif bicubic_upscaled.mode == "RGBA":
            r, g, b, a = bicubic_upscaled.split()
            bicubic = Image.merge("RGBA", (b, g, r, a))
        elif bicubic_upscaled.mode == "L":
            bicubic = bicubic_upscaled.convert("RGBA")

        im2 = bicubic.convert("RGBA")
        data = im2.tobytes("raw", "RGBA")
        qim = QtGui.QImage(data, bicubic.size[0], bicubic.size[1], QtGui.QImage.Format_ARGB32)
        self.pixmap = QtGui.QPixmap.fromImage(qim)
        self.pixmap.save(save_name)
        self.scaledPixmap = self.pixmap.scaledToWidth(300)
        self.label_Bicubic.setPixmap(self.scaledPixmap)

        

    def showKernelGAN(self, fixed_hparams):
        url = self.label_Input.text()
        img_name = url[url.rfind("/")+1:-4]
        url_2 = self.label_Output.text()
        out_url = url_2 + "/" + img_name + "/ZSSR_" +img_name + ".png"
        params = ['--input_image_path', os.path.join(url),
              '--output_dir_path', os.path.abspath(url_2),
              '--noise_scale', "1",
              '--g_lr', str(fixed_hparams['lr']),
              '--d_lr', str(fixed_hparams['lr']),
              '--gpu_id', str(fixed_hparams['CUDA_VISIBLE_DEVICES'])[-3],
              '--max_iters', str(fixed_hparams['epochs']*10)]
        params.append('--do_ZSSR')
        params.append('--real_image')
        conf = Config().parse(params)
        train(conf, self)
        self.label_status.setText("Complete KernelGAN")
        self.progressBar.setValue(0)
        qPixmapVar = QPixmap()
        qPixmapVar.load(out_url)
        qPixmapVar = qPixmapVar.scaledToWidth(300)
        self.label_Test.setPixmap(qPixmapVar)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()