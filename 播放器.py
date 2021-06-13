# coding:utf-8

# from PyQt5 import QtCore,QtGui,QtWidgets
import sys
import pygame

from mutagen import File
import time
import os
from PIL import Image, ImageDraw, ImageFilter
# import requests
# import jsonpath
# from mutagen.mp3 import MP3
# from mutagen import File
# from urllib.request import urlretrieve
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QListWidget, QLabel, QListWidgetItem, QApplication, QWidget
from PyQt5.QtCore import QTimer, QDateTime, Qt
from PyQt5.QtGui import QIcon, QPixmap, QColor, QPainter, QPixmap
from PyQt5 import QtMultimedia, QtWidgets, QtCore
from PyQt5.QtGui import QFont, QCursor
import qtawesome
import threading
import random
import requests

play = 'shun'
stop = False
SongPath = []
filew = 1
num = 0
voice = 0.5
pause = False
asas = 1
big = False


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        #self.start()

        try:
            icon_path = os.path.join(os.path.dirname(__file__), './logo.ico')

            icon = QIcon()
            icon.addPixmap(QPixmap(icon_path))  # 这是对的。
            self.setWindowIcon(icon)
        except:
            pass
        t1 = threading.Thread(target=self.action)
        t1.setDaemon(True)
        t1.start()

    def init_ui(self):
        self.setFixedSize(960, 700)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.close_widget = QtWidgets.QWidget()  # 创建关闭侧部件
        self.close_widget.setObjectName('close_widget')
        self.close_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.close_widget.setLayout(self.close_layout)  # 设置左侧部件布局为网格

        self.left_widget = QtWidgets.QWidget()  # 创建左边侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格

        self.down_widget = QtWidgets.QWidget()  # 创建下面部件
        self.down_widget.setObjectName('down_widget')
        self.down_layout = QtWidgets.QGridLayout()
        self.down_widget.setLayout(self.down_layout)  # 设置下侧部件布局为网格

        self.label = QLabel(self)
        self.label.setText("first line")
        self.label.setStyleSheet("color:white")
        self.label.setMaximumSize(310, 20)

        self.main_layout.addWidget(self.right_widget, 0, 20, 90, 90)  # 22右侧部件在第0行第3列，占8行9列
        self.down_layout.addWidget(self.label, 1, 0, 1, 1)
        self.main_layout.addWidget(self.left_widget, 0, 0, 90, 20)
        self.main_layout.addWidget(self.down_widget, 100, 0, 10, 110)
        self.main_layout.addWidget(self.close_widget, 0, 107, 1, 3)  # 左侧部件在第0行第0列，占1行3列
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件


        self.listwidget = QListWidget(self)
        self.listwidget.doubleClicked.connect(lambda: self.change_func(self.listwidget))
        self.right_layout.addWidget(self.listwidget, 3, 0, 100, 90)
        self.listwidget.setStyleSheet('''background-color:transparent''')

        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_close.clicked.connect(self.close)
        self.left_visit = QtWidgets.QPushButton("")  # 空白按钮
        self.left_visit.clicked.connect(self.big)
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮
        self.left_mini.clicked.connect(self.mini)
        self.close_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.close_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.close_layout.addWidget(self.left_visit, 0, 1, 1, 1)
        self.left_close.setFixedSize(15, 15)  # 设置关闭按钮的大小
        self.left_visit.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15)  # 设置最小化按钮大小
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        self.left_add = QtWidgets.QPushButton("添加")  # 添加按钮
        self.left_layout.addWidget(self.left_add, 0, 0, 2, 2)
        self.left_add.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_add.clicked.connect(self.add)



        self.label2 = QLabel(self)
        self.label2.setText("当前为顺序播放")
        self.label2.setStyleSheet("color:#6DDF6D")
        self.left_layout.addWidget(self.label2, 4, 0, 2, 2)

        self.label3 = QLabel(self)
        self.label3.setText("")
        self.label3.setStyleSheet("color:white")
        self.down_layout.addWidget(self.label3, 1, 3, 1, 1)

        self.label7 = QLabel(self)
        self.label7.setText("")
        self.label7.setStyleSheet("color:white")


        '''
        self.label1 = QLabel(self)
        self.label1.setText("first line")
        self.label1.setStyleSheet("color:white")
        '''

        self.label5 = QLabel(self)
        #self.label5.setScaledContents(True)
        pix_img = QtGui.QPixmap('./2.png')
        pix = pix_img.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
        self.label5.setPixmap(pix)
        #self.label5.setMaximumSize(1,1)
        self.left_layout.addWidget(self.label5,2,0,2,2)

        self.label6 = QLabel(self)
        self.label6.setText("")
        self.label6.setStyleSheet("color:#6DDF6D")
        self.left_layout.addWidget(self.label6, 2, 0, 2, 2)



        self.right_process_bar = QtWidgets.QProgressBar()  # 播放进度部件
        self.right_process_bar.setValue(49)
        self.right_process_bar.setFixedHeight(3)  # 设置进度条高度
        self.right_process_bar.setTextVisible(False)  # 不显示进度条文字

        self.right_playconsole_widget = QtWidgets.QWidget()  # 播放控制部件
        self.right_playconsole_layout = QtWidgets.QGridLayout()  # 播放控制部件网格布局层
        self.right_playconsole_widget.setLayout(self.right_playconsole_layout)

        self.console_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.backward', color='#3FC89C'), "")
        self.console_button_1.clicked.connect(self.last)
        self.console_button_1.setStyleSheet(
            '''QPushButton{background:#172940;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.forward', color='#3FC89C'), "")
        self.console_button_2.clicked.connect(self.nextion)
        self.console_button_2.setStyleSheet(
            '''QPushButton{background:#172940;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.pause', color='#3FC89C', font=18), "")
        self.console_button_3.clicked.connect(self.pause)
        self.console_button_3.setStyleSheet(
            '''QPushButton{background:#172940;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.volume-down', color='#3FC89C', font=18), "")
        self.console_button_4.clicked.connect(self.voicedown)
        self.console_button_4.setStyleSheet(
            '''QPushButton{background:#172940;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_5 = QtWidgets.QPushButton(qtawesome.icon('fa.volume-up', color='#3FC89C', font=18), "")
        self.console_button_5.clicked.connect(self.voiceup)
        self.console_button_5.setStyleSheet(
            '''QPushButton{background:#172940;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.align-center', color='#3FC89C', font=18), "")
        self.console_button_6.clicked.connect(self.playmode)
        self.console_button_6.setStyleSheet(
            '''QPushButton{background:#172940;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_3.setIconSize(QtCore.QSize(30, 30))

        self.right_playconsole_layout.addWidget(self.console_button_1, 0, 1)
        self.right_playconsole_layout.addWidget(self.console_button_2, 0, 3)
        self.right_playconsole_layout.addWidget(self.console_button_3, 0, 2)
        self.right_playconsole_layout.addWidget(self.console_button_4, 0, 0)
        self.right_playconsole_layout.addWidget(self.console_button_5, 0, 4)
        self.right_playconsole_layout.addWidget(self.console_button_6, 0, 5)
        self.right_playconsole_layout.setAlignment(QtCore.Qt.AlignCenter)  # 设置布局内部件居中显示

        self.down_layout.addWidget(self.right_process_bar, 0, 0, 1, 4)  # 第0行第0列，占8行3列
        # 第0行第0列，占8行3列

        self.down_layout.addWidget(self.label7, 1, 2, 1, 1)

        #self.down_layout.addWidget(self.label1, 1, 0, 1, 2)
        self.down_layout.addWidget(self.right_playconsole_widget, 1, 0, 1, 4)
        self.right_process_bar.setStyleSheet('''
            QProgressBar::chunk {
                background-color: #F76677;
            }
        ''')

        self.right_playconsole_widget.setStyleSheet('''
            QPushButton{
                border:none;
            }
        ''')

        self.left_widget.setStyleSheet('''
             QPushButton{border:none;color:white;}
             QPushButton#left_label{
             border:none;
             border-bottom:1px solid white;
             font-size:18px;
             font-weight:700;
             font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
             }
             QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
             QWidget#left_widget{
             background:#2B2B2B;
             border-top:1px solid white;
             border-bottom:1px solid white;
             border-left:1px solid white;
             border-top-left-radius:10px;
             border-bottom-left-radius:10px;
             }
             ''')

        self.close_widget.setStyleSheet('''
             QPushButton{border:none;color:white;}
             QPushButton#close_label{
             border:none;
             border-bottom:1px solid white;
             font-size:18px;
             font-weight:700;
             font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
             }
             QPushButton#close_button:hover{border-left:4px solid red;font-weight:700;}
             QWidget#close_widget{
             background:#232C51;
             border-top:1px solid white;
             border-bottom:1px solid white;
             border-left:1px solid white;
             border-top-left-radius:10px;
             border-bottom-left-radius:10px;
             border-top-right-radius:10px;
             border-bottom-right-radius:10px;
             }
             ''')
        self.right_widget.setStyleSheet('''
        QWidget#right_widget{
        color:#232C51;
        background:#191618;
        border-top:1px solid darkGray;
        border-bottom:1px solid darkGray;
        border-right:1px solid darkGray;
        border-top-right-radius:10px;
        border-bottom-right-radius:10px;
        }
        QLabel#right_lable{
        border:none;
        font-size:16px;
        font-weight:700;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        ''')

        self.down_widget.setStyleSheet('''
        QWidget#down_widget{
        color:#172940;
        background:#172940;
        border-top:1px solid darkGray;
        border-bottom:1px solid darkGray;
        border-right:1px solid darkGray;
        border-top-right-radius:10px;
        border-bottom-right-radius:10px;
        border-top-left-radius:10px;
        border-bottom-left-radius:10px;
        }
        QLabel#down_lable{
        border:none;
        font-size:16px;
        font-weight:700;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        ''')
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)

    # 以下为窗口控制代码



    def big(self):
        global big
        print (big)
        if not big:
            self.setWindowState(Qt.WindowMaximized)
            big = True
        elif big:
            self.setWindowState(Qt.WindowNoState)
            big = False
        # print (windowState())

    def close(self):
        reply = QtWidgets.QMessageBox.question(self, u'警告', u'确定退出?', QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            close = True
            try:
                pygame.mixer.music.stop()
            except:
                pass

            sys.exit()

        else:
            pass

    def mini(self):

        self.showMinimized()

    def mousePressEvent(self, event):
        global big
        big = False
        self.setWindowState(Qt.WindowNoState)
        # if event.button()==QtWidgets.QPushButton:
        self.m_flag = True
        self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
        event.accept()


    def mouseMoveEvent(self, QMouseEvent):
        global big
        big = False
        self.setWindowState(Qt.WindowNoState)
        # if QtWidgets.QPushButton and self.m_flag:
        self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
        QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        global big
        big = False
        self.setWindowState(Qt.WindowNoState)
        self.m_flag = False

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, u'警告', u'是否退出?', QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            sys.exit()


        else:
            event.ignore()

    # 以下为功能代码

    def dis(self):
        pass



    def photo(self,num):
        try:
            audio = File(SongPath[num])
            mArtwork = audio.tags['APIC:'].data
            with open('ls.png', 'wb') as img:
                img.write(mArtwork)
            try:
                lsfile = './ls.png'
                safile = './1.png'
                draw(lsfile,safile)

                pix_img = QtGui.QPixmap('./1.png')
                pix = pix_img.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
                self.label5.setPixmap(pix)
            except:
                print ('do error')
                pix_img = QtGui.QPixmap('./ls.png')
                pix = pix_img.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
                self.label5.setPixmap(pix)
        except:
            print('no picture')
            if  os.path.exists("2.png"):
                pix_img = QtGui.QPixmap('./2.png')
                pix = pix_img.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
                self.label5.setPixmap(pix)
            else:
                try:
                    req = requests.get('https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fy.gtimg.cn%2Fmusic%2Fphoto_new%2FT001R300x300M000002ztBMe06cOx0.jpg%3Fmax_age%3D2592000&refer=http%3A%2F%2Fy.gtimg.cn&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1625464213&t=a30c07bda8c2ab7d8001a59353e936e0')

                    checkfile  = open('ls2.png','w+b')
                    for i in req.iter_content(100000):
                        checkfile.write(i)

                    checkfile.close()
                    lsfile = './ls2.png'
                    safile = './2.png'
                    draw(lsfile,safile)
                except:
                    print ('download error')
                    pix_img = QtGui.QPixmap('./2.png')
                    pix = pix_img.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
                    self.label5.setPixmap(pix)
                    pass
                pass


    def bofang(self, num):
        try:
            global pause
            self.photo(num)
            self.console_button_3.setIcon(qtawesome.icon('fa.pause', color='#F76677', font=18))
            pause = False
            # QMessageBox.information(self, "ListWidget", "你选择了: "+item.text())# 显示出消息提示框
            fill = SongPath[num]
            print(fill)
            try:
                pygame.mixer.stop()
            except:
                pass
            pygame.mixer.init()
            try:
                self.Timer = QTimer()
                self.Timer.start(500)
            except:
                pass
            pygame.mixer.music.load(SongPath[num])  # 载入音乐
            pygame.mixer.music.play()  # 播放音乐


        except:
            time.sleep(0.1)
            print ('system error')
            self.next()
            pass

    def playmode(self):
        global play
        try:
            if play == 'shun':
                play = 'shui'
                print('随机播放')
                self.label2.setText("当前为随机播放")
                try:
                    self.console_button_6.setIcon(qtawesome.icon('fa.random', color='#3FC89C', font=18))
                    print('done')
                except:
                    print('none')
                    pass

                # self.left_shui.setText('切换为单曲循环')
            elif play == 'shui':
                play = 'always'
                print('单曲循环')
                self.label2.setText("当前为单曲循环")
                try:
                    self.console_button_6.setIcon(qtawesome.icon('fa.retweet', color='#3FC89C', font=18))
                    print('done')
                except:
                    print('none')


                # self.left_shui.setText('切换为顺序播放')
            elif play == 'always':
                play = 'shun'
                print('顺序播放')
                self.label2.setText("当前为顺序播放")
                try:
                    self.console_button_6.setIcon(qtawesome.icon('fa.align-center', color='#3FC89C', font=18))
                    print('done')
                except:
                    print('none')

                # self.left_shui.setText('切换为随机播放')
        except:
            print('error')
            pass

    def action(self):
        a = 1
        global num
        while a < 2:
            # print ('checking')
            try:
                time.sleep(1)
                if not pygame.mixer.music.get_busy() and pause == False:
                    if play == 'shun':
                        print('shuning')
                        self.next()
                    elif play == 'shui':
                        print('shuiing')
                        self.shui()
                    elif play == 'always':
                        print('alwaysing')
                        self.always()

            except:
                print('no')
                pass
        else:
            pygame.mixer.music.stop()

    def nextion(self):

            try:
                    if play == 'shun':
                        print('shuning')
                        self.next()
                    elif play == 'shui':
                        print('shuiing')
                        self.shui()
                    elif play == 'always':
                        print('alwaysing')
                        self.next()

            except:
                print('no')
                pass
    def add(self):
        try:

            global SongPath
            global num
            global filew
            global asas
            num = 0
            fileN = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "")
            self.listwidget.clear()
            filew = fileN + '/'
            asas = filew
            l1 = [name for name in os.listdir(fileN) if name.endswith('.mp3')]
            l2 = [name for name in os.listdir(fileN) if name.endswith('.flac')]
            l3 = [name for name in os.listdir(fileN) if name.endswith('wma')]
            SongName = l1 + l2 + l3
            SongPath = [filew + i for i in SongName]
            print(SongPath)
            # self.Timer.timeout.connect(self.timercontorl)#时间函数，与下面的进度条和时间显示有关
            # self.label = os.path.splitext(SongName[num])#分割文件名和扩展名
            # self.label.setText(wenjianming)#设置标签的文本为音乐的名字
            print(SongPath[num])
            r = 0
            for i in SongName:
                # self.listwidget.addItem(i)#将文件名添加到listWidget

                self.listwidget.addItem(i)
                self.listwidget.item(r).setForeground(QtCore.Qt.white)
                r = r + 1
            # self.next(self)
        except:
            filew = asas

    def start(self):
        try:
            global SongPath
            global num
            global filew
            global asas
            if not os.path.exists("2.png"):
                try:
                    req = requests.get('https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fy.gtimg.cn%2Fmusic%2Fphoto_new%2FT001R300x300M000002ztBMe06cOx0.jpg%3Fmax_age%3D2592000&refer=http%3A%2F%2Fy.gtimg.cn&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1625464213&t=a30c07bda8c2ab7d8001a59353e936e0')

                    checkfile  = open('ls2.png','w+b')
                    for i in req.iter_content(100000):
                        checkfile.write(i)

                    checkfile.close()
                    lsfile = './ls2.png'
                    safile = './2.png'
                    draw(lsfile,safile)
                except:
                    print ('download error')
                    pass
            fileN = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "")

            filew = fileN + '/'
            asas = filew
            l1 = [name for name in os.listdir(fileN) if name.endswith('.mp3')]
            l2 = [name for name in os.listdir(fileN) if name.endswith('.flac')]
            l3 = [name for name in os.listdir(fileN) if name.endswith('wma')]
            SongName = l1 + l2 + l3
            SongPath = [filew + i for i in SongName]
            print(SongPath)
            pygame.mixer.init()
            self.Timer = QTimer()
            self.Timer.start(500)
            # self.Timer.timeout.connect(self.timercontorl)#时间函数，与下面的进度条和时间显示有关
            # self.label = os.path.splitext(SongName[num])#分割文件名和扩展名
            # self.label.setText(wenjianming)#设置标签的文本为音乐的名字
            print(SongPath[num])
            self.photo(num)
            a, f = os.path.split(SongPath[num])  # 分割文件名
            f, ex = os.path.splitext(f)
            # self.label.setText(wenjianming)#设置标签的文本为音乐的名字
            self.label.setText(f)
            pygame.mixer.music.load(SongPath[num])  # 载入音乐
            pygame.mixer.music.play()  # 播放音乐2
            self.label3.setText(str(pygame.mixer.music.get_volume()))
            r = 0
            for i in SongName:
                # self.listwidget.addItem(i)#将文件名添加到listWidget

                self.listwidget.addItem(i)
                self.listwidget.item(r).setForeground(QtCore.Qt.white)
                r = r + 1
            # self.next(self)
        except:
            return

    def change_func(self, listwidget):
        global num
        item = QListWidgetItem(self.listwidget.currentItem())
        print(item.text())
        # print (item.flags())
        num = int(listwidget.currentRow())
        a, f = os.path.split(SongPath[num])  # 分割文件名
        f, ex = os.path.splitext(f)
        # self.label.setText(wenjianming)#设置标签的文本为音乐的名字
        self.label.setText(f)
        print(listwidget.currentRow())
        self.bofang(num)

    def pause(self):
        global pause
        if pause:
            try:
                pygame.mixer.music.unpause()
            except:
                pass
            self.console_button_3.setIcon(qtawesome.icon('fa.pause', color='#3FC89C', font=18))
            pause = False
        else:
            try:
                pygame.mixer.music.pause()
            except:
                pass
            self.console_button_3.setIcon(qtawesome.icon('fa.play', color='#F76677', font=18))
            pause = True




    def voiceup(self):
        print('up')
        global voice
        voice += 0.1
        if voice > 1:
            voice = 1
        pygame.mixer.music.set_volume(voice)
        self.label3.setText(str(pygame.mixer.music.get_volume()))

    def voicedown(self):
        print('down')
        global voice
        voice -= 0.1
        if voice < 0:
            voice = 0
        pygame.mixer.music.set_volume(voice)
        self.label3.setText(str(pygame.mixer.music.get_volume()))

    def shui(self):
        global num
        global SongPath
        q = int(len(SongPath) - 1)
        num = int(random.randint(1, q))
        try:
            print('shui')
            pygame.mixer.init()
            self.Timer = QTimer()
            self.Timer.start(500)
            # self.Timer.timeout.connect(self.timercontorl)#时间函数，与下面的进度条和时间显示有关
            a, f = os.path.split(SongPath[num])  # 分割文件名
            f, ex = os.path.splitext(f)
            # self.label.setText(wenjianming)#设置标签的文本为音乐的名字
            self.label.setText(f)
            pygame.mixer.music.load(SongPath[num])  # 载入音乐
            pygame.mixer.music.play()  # 播放音乐

        except:
            pass

    def next(self):
        global num
        global SongPath
        if num == len(SongPath) - 1:
            print('冇')
            num = 0
        else:
            num = num + 1
        try:
            self.photo(num)
            print('next')
            pygame.mixer.init()
            self.Timer = QTimer()
            self.Timer.start(500)
            # self.Timer.timeout.connect(self.timercontorl)#时间函数，与下面的进度条和时间显示有关
            a, f = os.path.split(SongPath[num])  # 分割文件名
            f, ex = os.path.splitext(f)
            # self.label.setText(wenjianming)#设置标签的文本为音乐的名字
            self.label.setText(f)
            pygame.mixer.music.load(SongPath[num])  # 载入音乐
            pygame.mixer.music.play()  # 播放音乐

        except:
            pass

    def always(self):
        try:
            self.photo(num)
            print('always')
            pygame.mixer.init()
            self.Timer = QTimer()
            self.Timer.start(500)
            # self.Timer.timeout.connect(self.timercontorl)#时间函数，与下面的进度条和时间显示有关
            a, f = os.path.split(SongPath[num])  # 分割文件名
            f, ex = os.path.splitext(f)
            # self.label.setText(wenjianming)#设置标签的文本为音乐的名字
            self.label.setText(f)
            pygame.mixer.music.load(SongPath[num])  # 载入音乐
            pygame.mixer.music.play()  # 播放音乐

        except:
            pass

    def last(self):
        global num
        global SongPath
        if num == 0:
            print('冇')
            num = len(SongPath) - 1
        else:
            num = num - 1
        try:
            self.photo(num)
            pygame.mixer.init()
            self.Timer = QTimer()
            self.Timer.start(500)
            a, f = os.path.split(SongPath[num])  # 分割文件名
            f, ex = os.path.splitext(f)
            # self.label.setText(wenjianming)#设置标签的文本为音乐的名字
            self.label.setText(f)
            pygame.mixer.music.load(SongPath[num])  # 载入音乐
            pygame.mixer.music.play()  # 播放音乐
        except:
            pass

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.modifiers() == Qt.ControlModifier and QKeyEvent.key() == Qt.Key_A:  # 键盘某个键被按下时调用
            print('surpise')

def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def mask_circle_transparent(pil_img, blur_radius, offset=0):
    offset = blur_radius * 2 + offset
    mask = Image.new("L", pil_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

    result = pil_img.copy()
    result.putalpha(mask)
    return result

def draw(lsfile,safile):
    markImg = Image.open(lsfile)
    thumb_width = 600

    im_square = crop_max_square(markImg).resize((thumb_width, thumb_width), Image.LANCZOS)
    im_thumb = mask_circle_transparent(im_square, 0)
    im_thumb.save(safile)
    os.remove(lsfile)

def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

#啦啦啦啦啦啦啦啦啦，今天2021/6/1,儿童节快乐鸭[]~(￣▽￣)~*