import os
import sys
import random
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *
import win32api

from func import Eat, Weather, Translation
import speech_recognition as sr


# 语音识别线程类
class SpeechRecognitionThread(QThread):
    def __init__(self):
        super().__init__()  # 调用父类 QThread 的构造函数

    # 创建一个字符串类型的信号，用于在语言识别对象与宠物类对象之间传递信息
    recognition_completed = pyqtSignal(str)

    def run(self):
        while 1:
            print("begin")
            r = sr.Recognizer()
            # 获取麦克风
            with sr.Microphone() as source:
                audio = r.listen(source)
                print("done")
                try:
                    # 将语音转换为文字
                    speech_text = r.recognize_google(audio, language='zh-CN')
                    # 输出信号
                    self.recognition_completed.emit(speech_text)
                    if "關閉" in speech_text or "关闭" in speech_text or "关" in speech_text:
                        print("quit")
                        break
                except sr.UnknownValueError:
                    self.recognition_completed.emit("Unable to recognize speech.")
                except sr.RequestError:
                    self.recognition_completed.emit("Speech recognition service unavailable.")


class PetAssistant(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(PetAssistant, self).__init__(parent)
        # 窗体初始化
        self.init()
        # 托盘初始化
        self.initPall()
        # 图片资源初始化
        self.initPetImage()
        # 宠物正常待机，实现随机切换动作
        self.petNormalAction()
        # 语音识别
        self.speech_thread = SpeechRecognitionThread()

    # 窗体初始化
    def init(self):
        # 设置窗口属性:窗口无标题栏且固定在最前面
        # FrameWindowHint:无边框窗口
        # WindowStaysOnTopHint: 窗口总显示在最上面
        # SubWindow: 新窗口部件是子窗口
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        # setAutoFillBackground(True)表示的是自动填充背景,False为透明背景
        self.setAutoFillBackground(False)
        # 窗口透明，窗体空间不透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 重绘组件、刷新
        self.repaint()

    # 托盘初始化
    def initPall(self):
        # 导入准备在托盘化显示上使用的图标
        icons = os.path.join('./icon/icon.png')
        # 设置右键显示最小化的菜单项
        # 菜单项退出，点击后调用quit函数
        quit_action = QAction('退出', self, triggered=self.quit)
        # 设置托盘图标
        quit_action.setIcon(QIcon(icons))
        # 菜单项显示，点击后调用showing函数
        showing = QAction(u'显示', self, triggered=self.showwin)
        # 新建一个菜单项控件
        self.tray_icon_menu = QMenu(self)
        # 添加菜单项‘退出’
        self.tray_icon_menu.addAction(quit_action)
        # 添加菜单项‘显示’
        self.tray_icon_menu.addAction(showing)
        # QSystemTrayIcon类为应用程序在系统托盘中提供一个图标
        self.tray_icon = QSystemTrayIcon(self)
        # 设置托盘化图标
        self.tray_icon.setIcon(QIcon(icons))
        # 设置托盘化菜单项
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        # 展示
        self.tray_icon.show()

    # 图片资源初始化
    def initPetImage(self):
        # 定义显示图片部分
        self.image = QLabel(self)
        # QMovie是一个可以存放动态视频的类，一般是配合QLabel使用的,可以用来存放GIF动态图
        self.movie = QMovie("wait/wait1.gif")
        # 设置标签大小
        self.movie.setScaledSize(QSize(150, 150))
        # 将Qmovie在定义的image中显示
        self.image.setMovie(self.movie)
        self.movie.start()
        self.resize(300, 300)

        # "休息一下"时间显示
        self.show_time_rest = QLabel(self)

        # 对话框样式设计
        self.show_time_rest.setStyleSheet("font:15pt '楷体';border-width: 1px;color:blue;")

        # 宠物随机出现
        self.randomPosition()

        # 垂直布局设置
        vbox = QVBoxLayout()
        vbox.addWidget(self.image)
        vbox.addWidget(self.show_time_rest)

        # 加载布局
        self.setLayout(vbox)

        # 展示
        self.show()

        # 将宠物正常待机状态的动图放入pet1中
        self.pet1 = []
        for i in os.listdir("wait"):
            self.pet1.append("wait/" + i)

    # 宠物正常待机动作
    def petNormalAction(self):
        # 每隔一段时间做个动作
        # 定时器设置
        self.timer = QTimer()
        self.timer.timeout.connect(self.randomAct)
        self.timer.start(5000)
        # 宠物状态设置为常规
        self.condition = 0
        self.dir = 0
        # 休息一下
        self.timer_rest = QTimer()
        self.timer_rest.timeout.connect(self.haveRest)
        self.rest_open = 1

    # 随机动作切换
    def randomAct(self):
        # condition记录宠物状态，宠物状态为0时，代表常规待机状态
        if not self.condition:
            # 随机选择装载在pet1里面的gif图进行展示，实现随机切换
            self.movie = QMovie(random.choice(self.pet1))
            # 宠物大小
            self.movie.setScaledSize(QSize(150, 150))
            # 将动画添加到label中
            self.image.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()

        elif self.condition == 1:
            # 点击
            self.movie = QMovie("./action/click.gif")
            # 宠物大小
            self.movie.setScaledSize(QSize(150, 150))
            # 将动画添加到label中
            self.image.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            # 宠物状态设置为正常待机
            self.condition = 0

        elif self.condition == 2:
            # 休息提示
            self.movie = QMovie("./action/remind.gif")
            # 宠物大小
            self.movie.setScaledSize(QSize(150, 150))
            # 将动画添加到label中
            self.image.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()

        elif self.condition == 3:
            # 移动
            self.movie.stop()
            if self.dir == 0:
                self.movie = QMovie("./action/run_left.gif")
            else:
                self.movie = QMovie("./action/run_right.gif")
            # 宠物大小
            self.movie.setScaledSize(QSize(150, 150))
            # 将动画添加到label中
            self.image.setMovie(self.movie)
            # 开始播放动画
            self.movie.started.connect(self.movieStarted)
            self.movie.start()
            # 宠物状态设置为正常待机
            self.condition = 0

        elif self.condition == 4:
            # 唱歌
            self.movie.stop()
            self.movie = QMovie("./action/music.gif")
            # 宠物大小
            self.movie.setScaledSize(QSize(150, 150))
            # 将动画添加到label中
            self.image.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            # 宠物状态设置为正常待机
            self.condition = 0

        elif self.condition == 5:
            # 餐厅推荐
            self.movie.stop()
            self.movie = QMovie("./action/eat.gif")
            # 宠物大小
            self.movie.setScaledSize(QSize(150, 150))
            # 将动画添加到label中
            self.image.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            # 宠物状态设置为正常待机
            self.condition = 0

        elif self.condition == 6:
            # 天气查询
            self.movie.stop()
            self.movie = QMovie("./action/weather.gif")
            # 宠物大小
            self.movie.setScaledSize(QSize(150, 150))
            # 将动画添加到label中
            self.image.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            # 宠物状态设置为正常待机
            self.condition = 0

        elif self.condition == 7:
            # 汉英翻译
            self.movie.stop()
            self.movie = QMovie("./action/translate.gif")
            # 宠物大小
            self.movie.setScaledSize(QSize(150, 150))
            # 将动画添加到label中
            self.image.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            # 宠物状态设置为正常待机
            self.condition = 0

    # 关闭程序
    def quit(self):
        self.close()
        sys.exit()

    # 显示宠物
    def showwin(self):
        # setWindowOpacity（）设置窗体的透明度，通过调整窗体透明度实现宠物的展示和隐藏
        self.setWindowOpacity(1)

    # 宠物随机位置
    def randomPosition(self):
        screen_geo = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        pet_geo = self.geometry()
        width = (screen_geo.width() - pet_geo.width()) * random.random()
        height = (screen_geo.height() - pet_geo.height()) * random.random()
        self.move(int(width), int(height))

    # 鼠标左键按下时, 宠物将和鼠标位置绑定
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            # 更改宠物状态为点击
            self.condition = 1
            self.randomAct()
        # globalPos() 事件触发点相对于桌面的位置
        # pos() 程序相对于桌面左上角的位置，实际是窗口的左上角坐标
        self.mouse_drag_pos = event.globalPos() - self.pos()
        event.accept()
        # 拖动时改变鼠标
        self.setCursor(QCursor(Qt.OpenHandCursor))
        # 取消休息状态
        self.show_time_rest.setText("")
        # 宠物状态设置为正常待机
        self.condition = 0

    # 鼠标移动时调用，实现宠物随鼠标移动
    def mouseMoveEvent(self, event):
        # 如果鼠标左键按下，且处于绑定状态
        if Qt.LeftButton and self.is_follow_mouse:
            # 宠物随鼠标进行移动
            self.move(event.globalPos() - self.mouse_drag_pos)
        event.accept()

    # 鼠标释放调用，取消绑定
    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        # 鼠标图形设置为箭头
        self.setCursor(QCursor(Qt.ArrowCursor))

    # 鼠标移进时调用
    def enterEvent(self, event):
        # 设置鼠标形状 Qt.ClosedHandCursor   非指向手
        self.setCursor(Qt.ClosedHandCursor)

    # 宠物右键点击交互
    def contextMenuEvent(self, event):
        # 定义菜单

        menu = QMenu(self)
        # '''
        # 定义菜单项
        hide = menu.addAction("隐藏")

        voice_control = menu.addAction("语音识别")

        if self.rest_open == 1:
            rest = menu.addAction("打开休息提醒")
        elif self.rest_open == 2:
            rest = menu.addAction("关闭休息提醒")
        move_left = menu.addAction("左移")
        move_right = menu.addAction("右移")
        play_music = menu.addAction("播放音乐")
        can_rec = menu.addAction("餐厅推荐")
        weather_rep = menu.addAction("天气查询")
        translation = menu.addAction("汉英翻译")
        menu.addSeparator()  # 分割线
        quitAction = menu.addAction("退出")
        action = menu.exec_(self.mapToGlobal(event.pos()))

        # 点击事件为退出
        if action == quitAction:
            qApp.quit()

        if action == voice_control:
            # 按下按键启动线程
            self.speech_thread.recognition_completed.connect(self.handle_speech_recognition_completed)
            self.speech_thread.start()
        # 点击事件为隐藏
        if action == hide:
            # 通过设置透明度方式隐藏宠物
            self.setWindowOpacity(0)
        # 打开休息提醒
        if action == rest:
            if self.rest_open == 1:
                self.timer_rest.start(5000)
                self.rest_open = 2
            elif self.rest_open == 2:
                self.timer_rest.stop()
                self.rest_open = 1
        # 左移
        if action == move_left:
            self.timer.stop()
            self.dir = 0
            self.changemoving()
            self.timer.start(5000)
        # 右移
        if action == move_right:
            self.timer.stop()
            self.dir = 1
            self.changemoving()
            self.timer.start(5000)
        # 播放音乐
        if action == play_music:
            self.timer.stop()
            self.playMusic('爱.mp3')
            self.timer.start(5000)
        # 餐厅推荐
        if action == can_rec:
            self.timer.stop()
            self.canteenRecommendation()
            self.timer.start(5000)
        # 天气查询
        if action == weather_rep:
            self.timer.stop()
            self.weatherReport()
            self.timer.start(5000)
        # 汉英翻译
        if action == translation:
            self.timer.stop()
            self.trans_Ch_to_En("老默，我想吃鱼了")
            self.timer.start(5000)

    # 根据语音识别的内容做出不同的行动，翻译的语句为"翻译+翻译的文本” 比如说“翻译我是谁” 翻译结果就是“who am I”
    # 音乐的语句为“播放音乐 + 音乐名称” 比如说“ 播放音乐但愿” 就会播放“但愿.MP3"
    # 其余都是识别关键词然后行动
    def handle_speech_recognition_completed(self, speech_text):
        print("Speech Recognition Result:", speech_text)
        # 处理语音命令
        if "左" in speech_text or "向左" in speech_text or "向左走" in speech_text:
            self.timer.stop()
            self.dir = 0
            self.changemoving()
            self.timer.start(5000)
        elif "右" in speech_text or "向右" in speech_text or "向右走" in speech_text:
            self.timer.stop()
            self.dir = 1
            self.changemoving()
            self.timer.start(5000)
        elif ("播放" in speech_text and "爱" in speech_text) or ("音乐" in speech_text and "爱" in speech_text):
            self.timer.stop()
            self.playMusic('爱.mp3')
            self.timer.start(5000)
        elif ("播放" in speech_text and "七里香" in speech_text) or ("音乐" in speech_text and "七里香" in speech_text):
            self.timer.stop()
            self.playMusic('七里香.mp3')
            self.timer.start(5000)
        elif ("播放" in speech_text and "但愿" in speech_text) or ("音乐" in speech_text and "但愿" in speech_text):
            self.timer.stop()
            self.playMusic('但愿.mp3')
            self.timer.start(5000)
        elif ("播放" in speech_text and "信念" in speech_text) or ("音乐" in speech_text and "信念" in speech_text):
            self.timer.stop()
            self.playMusic('信念.mp3')
            self.timer.start(5000)
        elif ("播放" in speech_text and "谎言" in speech_text) or ("音乐" in speech_text and "谎言" in speech_text):
            self.timer.stop()
            self.playMusic('谎言.mp3')
            self.timer.start(5000)
        elif "餐廳" in speech_text or "推薦" in speech_text or "餐" in speech_text or "餐厅" in speech_text or "推荐" in speech_text:
            self.timer.stop()
            self.canteenRecommendation()
            self.timer.start(5000)
        elif "天氣" in speech_text or "查詢" in speech_text or "天气" in speech_text or "查询" in speech_text:
            self.timer.stop()
            self.weatherReport()
            self.timer.start(5000)
        elif "翻譯" in speech_text or "翻译" in speech_text:
            self.timer.stop()
            text_to_translate = speech_text.split('翻译', 1)[1].strip()
            self.trans_Ch_to_En(text_to_translate)
            self.timer.start(5000)
        elif "退出" in speech_text or "退" in speech_text:
            qApp.quit()
        elif "隱藏" in speech_text or "藏" in speech_text or "隐藏" in speech_text:
            # 通过设置透明度方式隐藏宠物
            self.setWindowOpacity(0)

    def haveRest(self):
        self.show_time_rest.setText("休息一下")
        self.show_time_rest.setStyleSheet(
            "font: bold;"
            "font:25pt '楷体';"
            "color:white;"
            "background-color: white"
            "url(:/)"
        )
        self.condition = 2
        self.randomAct()

    def moveLeft(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        target_x = int(self.x() - screen_width / 3)
        if target_x < 0:
            target_x = 0
        for i in range(self.x(), target_x, -1):
            self.move(i, self.y())
        self.condition = 0
        self.randomAct()

    def moveRight(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        target_x = int(self.x() + screen_width / 3)
        if target_x > screen_width - 200:
            target_x = screen_width - 200
        for i in range(self.x(), target_x):
            self.move(i, self.y())
        self.condition = 0
        self.randomAct()

    def changemoving(self):
        self.condition = 3
        self.randomAct()

    def playMusic(self, filename):
        win32api.ShellExecute(0, 'open', filename, '', '', 1)
        self.condition = 4
        self.randomAct()

    def canteenRecommendation(self):
        self.eat = Eat()
        self.eat.show()
        self.condition = 5
        self.randomAct()

    def weatherReport(self):
        self.weather = Weather()
        self.weather.show()
        self.condition = 6
        self.randomAct()

    def trans_Ch_to_En(self, text):
        self.translation = Translation(text)
        self.translation.show()
        self.condition = 7
        self.randomAct()

    def movieStarted(self):
        if self.dir == 1:
            QTimer.singleShot(100, self.moveRight)
        else:
            QTimer.singleShot(100, self.moveLeft)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = PetAssistant()
    sys.exit(app.exec_())
