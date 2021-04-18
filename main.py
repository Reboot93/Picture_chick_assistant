import sys, time, _thread, os, shutil, cv2, numpy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from windows import Ui_Form

# 信号初始化
update_flag = 0  # 界面刷新信号
quit_flag = 0
choose_flag = 0
inf_flag = 0
now_number = 0
all_number = 0
chick_percent = 7
run_number = 0
percent = 0
work_dir = ''
p1 = 'python_none.png'
p1_inf = ''
p2 = 'python_none.png'
p2_inf = ''
file_list = []
pf = ['jpg', 'jpeg', 'png']


class MainWindow(QWidget, Ui_Form):
    # 定义点击信号
    chooseSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        global control_data, status_flag
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('图片对比助手 V1.0')
        # ==/ Icon设置 /===
        # self.setWindowIcon(QIcon('icon/256x256.ico'))
        # ==/ 按键信号设置 /================
        self.bt_save_1.clicked.connect(lambda: self.save(1))
        self.bt_save_2.clicked.connect(lambda: self.save(2))
        self.bt_save_all.clicked.connect(lambda: self.save(0))
        # self.bt_find_p.clicked.connect(lambda: self.find_p())
        self.bt_chick_p.clicked.connect(lambda: self.start())
        self.bt_set_percent.clicked.connect(lambda: self.set_percent())
        self.bt_workdir_set.clicked.connect(lambda: self.set_workdir())
        self.print_p1.setScaledContents(True)
        self.print_p2.setScaledContents(True)

        # ==/ 界面初始化 /==========
        self.print_p1.setPixmap(QPixmap('python_none.png'))
        self.print_p2.setPixmap(QPixmap('python_none.png'))
        # 界面更新
        _thread.start_new_thread(lambda: self.flash(), ())

    def flash(self):  # ==/ 页面刷新函数 /====
        global update_flag, p1, p2, percent, inf_flag
        while True:
            time.sleep(0.0005)
            while update_flag == 1:
                update_flag = 0
                # ===/ 更新控件 /=================================
                time.sleep(0.1)
                self.print_workdir.setText(work_dir)
                time.sleep(0.01)
                self.percent_number.setValue(chick_percent)
                self.print_p1.setPixmap(QPixmap(p1))
                self.print_p2.setPixmap(QPixmap(p2))
                percent = run_number * (100 / ((all_number * (all_number - 1)) / 2))
                print(int(percent))
                self.print_percent.display(int(percent))
                if inf_flag == 1:
                    inf_flag = 0
                    self.print_p1_inf.append('图片目录：' + p1 + '\n')
                    time.sleep(0.1)
                    self.print_p1_inf.moveCursor(self.print_p1_inf.textCursor().End)
                    self.print_p1_inf.append(p1_inf + '\n=======================================================')
                    self.print_p1_inf.moveCursor(self.print_p1_inf.textCursor().End)
                    time.sleep(0.1)
                    self.print_p2_inf.append('图片目录：' + p2 + '\n')
                    self.print_p2_inf.moveCursor(self.print_p2_inf.textCursor().End)
                    time.sleep(0.1)
                    self.print_p2_inf.append(p2_inf + '\n=======================================================')
                    self.print_p2_inf.moveCursor(self.print_p2_inf.textCursor().End)
            if p1 == 'duibizhon.jpg' and p2 == 'duibizhon.jpg':
                time.sleep(0.01)
                self.print_p1.setPixmap(QPixmap('python_none.png'))
                self.print_p2.setPixmap(QPixmap('python_none.png'))

    def start(self):
        _thread.start_new_thread(lambda: self.start_chick(), ())

    def start_chick(self):
        global update_flag, all_number, now_number, p1, p2, chick_percent, choose_flag, file_list, run_number, inf_flag
        run_number = 0
        while len(file_list) > 0:
            pic1 = file_list[0]
            p1_dhash = self.dhash(pic1, 'p1')
            now_number = now_number + 1
            i = 1
            while i < len(file_list):
                pic2 = file_list[i]
                p2_dhash = self.dhash(pic2, 'p2')
                outn = self.campHash(p1_dhash, p2_dhash)
                print(chick_percent)
                if outn <= chick_percent:
                    choose_flag = 1
                    inf_flag = 1
                    p1 = file_list[0]
                    p2 = pic2
                    update_flag = 1
                    while choose_flag == 1:
                        time.sleep(0.1)
                    else:
                        p1 = 'duibizhon.jpg'
                        p2 = 'duibizhon.jpg'
                else:
                    pass
                i = i + 1
                run_number = run_number + 1
                print('run:' + str(run_number))
                update_flag = 1
            file_list = file_list[1:]
            print(pic1 + ' :对比完成')
        p1 = 'python_end.png'
        p2 = 'python_end.png'
        update_flag = 1
        time.sleep(0.2)
        print('对比完成')

    def set_workdir(self):
        global work_dir, update_flag
        work_dir = QFileDialog.getExistingDirectory(self)
        self.find_p()
        update_flag = 1

    def set_percent(self):
        global chick_percent, update_flag
        chick_percent = int(self.percent_number.text())
        update_flag = 1
        print(chick_percent)

    def find_p(self):
        global work_dir, now_number, all_number, update_flag, file_list, run_number
        all_number = 0
        now_number = 0
        run_number = 0
        file_list = []
        for root, dirs, files in os.walk(work_dir):
            for name in files:
                filename = root + '/' + name
                if pf.count(str(filename[-4:])) != 0 or pf.count(str(filename[-3:])) != 0:
                    if filename[len(work_dir):].rfind('output') != -1:
                        pass
                    else:
                        file_list.append(filename)
                        all_number = all_number + 1
        update_flag = 1
        QMessageBox.warning(self, '遍历提示', '工作目录下的图片遍历完成\n=================\n共有:' + str(all_number) + '个指定格式的图片文件')

    def save(self, msg):
        global choose_flag
        if os.path.isdir(work_dir + '/output') != True:
            os.mkdir(work_dir + '/output')
        if msg == 1:  # 保存p1
            if p2 == '' or p2 == 'python_end.png' or p2 == 'python_none.png':
                return
            p2_name = p2[p2.rfind('/'):]
            shutil.move(p2, work_dir + '/output' + p2_name)
            QMessageBox.warning(self, '对比提示', '图片：\n' + p2 + '\n已移至' + work_dir + '/output' + p2_name + '下')
        if msg == 2:  # 保存p2
            if p1 == '' or p1 == 'python_end.png' or p1 == 'python_none.png':
                return
            p1_name = p1[p1.rfind('/'):]
            shutil.move(p1, work_dir + '/output' + p1_name)
            QMessageBox.warning(self, '对比提示', '图片：\n' + p1 + '\n已移至' + work_dir + '/output' + p2_name + '下')
        if msg == 3:
            pass
        choose_flag = 0

    def dhash(self, image, msg):  # https://zhuanlan.zhihu.com/p/68215900?from_voters_page=true
        global p1_inf, p2_inf
        # 将图片转化为8*8
        img_data = numpy.fromfile(image, numpy.uint8)
        image = cv2.imdecode(img_data, -1)
        if msg == 'p1':
            a = image.shape
            p1_inf = '图像大小： ' + str(a[1]) + 'x' + str(a[0]) + ' (宽x高)'
            print(p1_inf)
        if msg == 'p2':
            a = image.shape
            p2_inf = '图像大小： ' + str(a[1]) + 'x' + str(a[0]) + ' (宽x高)'
            print(p2_inf)
        image = cv2.resize(image, (9, 8), interpolation=cv2.INTER_CUBIC)
        # 将图片转化为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        dhash_str = ''
        for i in range(8):
            for j in range(8):
                if gray[i, j] > gray[i, j + 1]:
                    dhash_str = dhash_str + '1'
                else:
                    dhash_str = dhash_str + '0'
        result = ''
        for i in range(0, 64, 4):
            result += ''.join('%x' % int(dhash_str[i: i + 4], 2))
        print("dhash值", result)
        return result

    def campHash(self, hash1, hash2):  # https://zhuanlan.zhihu.com/p/68215900?from_voters_page=true
        n = 0
        # hash长度不同返回-1,此时不能比较
        if len(hash1) != len(hash2):
            return -1
        # 如果hash长度相同遍历长度
        for i in range(len(hash1)):
            if hash1[i] != hash2[i]:
                n = n + 1
        print('汉明值' + str(n))
        return n


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ma = MainWindow()
    ma.show()
    sys.exit(app.exec_())
