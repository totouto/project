from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5 import uic
from project import WindowClass

main_form = uic.loadUiType("./main.ui")[0]

class WindowClass_main(QDialog, main_form):
    DEFAULT_MODEL_PATH = (Path(__file__).parent / 'esrgan/models').absolute()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('ESPRESOMEDIA SR Demos')

        # UI Components (n_workers, batch_size, epochs, img_size, lr, device)
        self.spinBox_nworkers.valueChanged.connect(self.run_train)
        self.spinBox_batchsize.valueChanged.connect(self.run_train)
        self.spinBox_epochs.valueChanged.connect(self.run_train)
        self.spinBox_imgsize.valueChanged.connect(self.run_train)
        self.doubleSpinBox_lr.valueChanged.connect(self.run_train)
        self.comboBox_device.addItem('CPU')
        self.comboBox_device.addItem('CUDA')

        # 'GPUs' checkboxes
        self.checked_chkBoxList = []
        self.checkBox_GPU0.stateChanged.connect(self.checkBoxState)
        self.checkBox_GPU1.stateChanged.connect(self.checkBoxState)
        self.checkBox_GPU2.stateChanged.connect(self.checkBoxState)
        self.checkBox_GPU3.stateChanged.connect(self.checkBoxState)
        self.checkBox_GPU4.stateChanged.connect(self.checkBoxState)
        self.checkBox_GPU5.stateChanged.connect(self.checkBoxState)
        self.checkBox_GPU6.stateChanged.connect(self.checkBoxState)
        self.checkBox_GPU7.stateChanged.connect(self.checkBoxState)

        # Set train & test set path
        self.pushButton_trainpath.clicked.connect(self.pushButton_selectTrainPath)
        self.pushButton_testpath.clicked.connect(self.pushButton_selectTestPath)

        # 'Train' and 'Test' Buttons
        self.pushButton_train.clicked.connect(self.run_train)
        self.pushButton_test.clicked.connect(self.onButtonCLocked_test)

    # TODO: Widget으로 훈련 진행상황 출력하는 코드 삽입예정
    def onButtonCLocked_train(self):
        win = WindowClass_test(self)

    # Parameter 넘겨서 test 위젯 켜기
    def onButtonCLocked_test(self):
        fixed_hparams = {}
        fixed_hparams['n_workers'] = self.spinBox_nworkers.value()
        fixed_hparams['batch_size'] = self.spinBox_batchsize.value()
        fixed_hparams['epochs'] = self.spinBox_epochs.value()
        fixed_hparams['img_size'] = self.spinBox_imgsize.value()
        fixed_hparams['lr'] = self.doubleSpinBox_lr.value()
        fixed_hparams['device'] = self.comboBox_device.currentText()
        fixed_hparams['CUDA_VISIBLE_DEVICES'] = self.checkBoxState()
#        fixed_hparams['trainset_path'] = self.pushButton_trainpath.text()
#        fixed_hparams['testset_path'] = self.pushButton_testpath.text()

        if fixed_hparams['device'] == 'CPU':
            fixed_hparams['CUDA_VISIBLE_DEVICES'] = None
        if fixed_hparams['device'] == 'CUDA' and fixed_hparams['CUDA_VISIBLE_DEVICES'] == None:
            print('Please specify GPU IDs.')
            raise NotImplementedError

        print(fixed_hparams)

        self.w = WindowClass(fixed_hparams)
        self.w.show()
        self.hide()

    def pushButton_selectTrainPath(self):
        self.dir = QFileDialog.getExistingDirectory(self, 'Set Train Directory...')
        self.pushButton_trainpath.setText(self.dir)

    def pushButton_selectTestPath(self):
        self.dir = QFileDialog.getExistingDirectory(self, 'Set Test Directory...')
        self.pushButton_testpath.setText(self.dir)

    def checkBoxState(self):
        if self.checkBox_GPU0.isChecked(): self.checked_chkBoxList.append(self.checkBox_GPU0.text())
        if self.checkBox_GPU1.isChecked(): self.checked_chkBoxList.append(self.checkBox_GPU1.text())
        if self.checkBox_GPU2.isChecked(): self.checked_chkBoxList.append(self.checkBox_GPU2.text())
        if self.checkBox_GPU3.isChecked(): self.checked_chkBoxList.append(self.checkBox_GPU3.text())
        if self.checkBox_GPU4.isChecked(): self.checked_chkBoxList.append(self.checkBox_GPU4.text())
        if self.checkBox_GPU5.isChecked(): self.checked_chkBoxList.append(self.checkBox_GPU5.text())
        if self.checkBox_GPU6.isChecked(): self.checked_chkBoxList.append(self.checkBox_GPU6.text())
        if self.checkBox_GPU7.isChecked(): self.checked_chkBoxList.append(self.checkBox_GPU7.text())

        return sorted(list(set(self.checked_chkBoxList)))

    def run_train(self):
        fixed_hparams = {}
        fixed_hparams['n_workers'] = self.spinBox_nworkers.value()
        fixed_hparams['batch_size'] = self.spinBox_batchsize.value()
        fixed_hparams['epochs'] = self.spinBox_epochs.value()
        fixed_hparams['img_size'] = self.spinBox_imgsize.value()
        fixed_hparams['lr'] = self.doubleSpinBox_lr.value()
        fixed_hparams['device'] = self.comboBox_device.currentText()
        fixed_hparams['CUDA_VISIBLE_DEVICES'] = self.checkBoxState()
        fixed_hparams['trainset_path'] = self.pushButton_trainpath.text()
        fixed_hparams['testset_path'] = self.pushButton_testpath.text()

        if fixed_hparams['device'] == 'CPU':
            fixed_hparams['CUDA_VISIBLE_DEVICES'] = None
        if fixed_hparams['device'] == 'CUDA' and fixed_hparams['CUDA_VISIBLE_DEVICES'] == None:
            print('Please specify GPU IDs.')
            raise NotImplementedError

        print(fixed_hparams)

        return fixed_hparams

if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName('ESPRESOMEDIA SR Demos')

    main = WindowClass_main()
    main.show()

    app.exec_()
