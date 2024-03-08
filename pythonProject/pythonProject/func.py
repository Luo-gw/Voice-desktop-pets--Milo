from PyQt5 import QtGui
from PyQt5.QtGui import QTextBlockFormat, QTextCursor
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys
import random
import requests

class Eat(QWidget):
    # 初始化界面
    def __init__(self, parent=None, **kwargs):
        # QWidget.__init__(self)
        super(Eat, self).__init__(parent)
        # 设置窗口的大小和位置
        self.setGeometry(600, 300, 600, 351)
        # 设置标题
        self.setWindowTitle("餐厅推荐")
        # 添加背景
        palette = QtGui.QPalette()
        bg = QtGui.QPixmap("./background/bgi2.png")
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(bg))
        self.setPalette(palette)
        self.dialog = []
        # 读取目录下dialog文件
        with open("dialog.txt", "r") as f:
            text = f.read()
            # 以\n 即换行符为分隔符，分割放进dialog中
            self.dialog = text.split("\n")
        self.add_ui()

    # 设置界面当中的组件
    def add_ui(self):
        # 多行文本显示，显示所有信息
        self.title = QTextBrowser(self)
        self.title.setGeometry(30, 10, 550, 40)
        font = self.title.font()  # 获取当前字体
        font.setPointSize(15)  # 设置字体大小为15点
        self.title.setFont(font)  # 应用新的字体到部件
        cursor = self.title.textCursor()  # 获取文本光标
        cursor.movePosition(QTextCursor.End)  # 将光标移动到文本末尾
        block_format = QTextBlockFormat()
        block_format.setAlignment(Qt.AlignCenter)  # 设置对齐方式为居中
        cursor.setBlockFormat(block_format)  # 应用文本块格式到光标位置
        self.title.setTextCursor(cursor)  # 将更新后的光标应用到部件
        self.title.append('今天吃什么呢')

        self.content = QTextBrowser(self)
        self.content.setGeometry(30, 80, 550, 250)
        font = self.content.font()  # 获取当前字体
        font.setPointSize(12)  # 设置字体大小为12点
        self.content.setFont(font)  # 应用新的字体到部件

        tmp = self.dialog
        for i in range(1, 6):
            choice = random.choice(tmp)
            tmp.remove(choice)
            self.content.append(str(i) + ' : ' + choice)
            self.content.append(' ')

    # 退出销毁对话窗口
    def closeEvent(self, event):
        self.destroy()


class Weather(QWidget):
    # 初始化界面
    def __init__(self, parent=None, **kwargs):
        # QWidget.__init__(self)
        super(Weather, self).__init__(parent)
        # 设置窗口的大小和位置
        self.setGeometry(600, 300, 340, 192)
        # 设置标题
        self.setWindowTitle("天气查询")
        # 添加背景
        palette = QtGui.QPalette()
        bg = QtGui.QPixmap("./background/bgi3.png")
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(bg))
        self.setPalette(palette)
        self.add_ui()

    # 设置界面当中的组件
    def add_ui(self):
        # 多行文本显示，显示所有信息
        self.title = QTextBrowser(self)
        self.title.setGeometry(20, 10, 300, 35)
        font = self.title.font()  # 获取当前字体
        font.setPointSize(13)  # 设置字体大小为15点
        self.title.setFont(font)  # 应用新的字体到部件
        cursor = self.title.textCursor()  # 获取文本光标
        cursor.movePosition(QTextCursor.End)  # 将光标移动到文本末尾
        block_format = QTextBlockFormat()
        block_format.setAlignment(Qt.AlignCenter)  # 设置对齐方式为居中
        cursor.setBlockFormat(block_format)  # 应用文本块格式到光标位置
        self.title.setTextCursor(cursor)  # 将更新后的光标应用到部件
        self.title.append('今天天气怎么样')

        self.content = QTextBrowser(self)
        self.content.setGeometry(20, 60, 300, 110)
        font = self.content.font()  # 获取当前字体
        font.setPointSize(12)  # 设置字体大小为12点
        self.content.setFont(font)  # 应用新的字体到部件

        api_key = 'e2c6294e0ac3959d4ece3d90d30fcccf'  # API 密钥
        base_url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'q': 'Shanghai',
            'appid': api_key,
            'units': 'metric',  # 摄氏度
            'lang': 'zh_cn'
        }

        try:
            response = requests.get(base_url, params=params)
            data = response.json()

            if data['cod'] == 200:
                weather = data['weather'][0]['description']
                temperature = data['main']['temp']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']

                self.content.append(f"上海的天气情况：{weather}")
                self.content.append(f"温度：{temperature}°C")
                self.content.append(f"湿度：{humidity}%")
                self.content.append(f"风速：{wind_speed} m/s")
            else:
                self.content.append(f"错误：{data['message']}")
        except requests.exceptions.RequestException as e:
            self.content.append(f"发生错误：{e}")

    # 退出销毁对话窗口
    def closeEvent(self, event):
        self.destroy()


class Translation(QWidget):
    # 初始化界面
    def __init__(self, chinese_text, parent=None, **kwargs):
        # QWidget.__init__(self)
        super(Translation, self).__init__(parent)
        # 设置窗口的大小和位置
        self.setGeometry(600, 300, 600, 334)
        # 设置标题
        self.setWindowTitle("汉英翻译")
        # 添加背景
        palette = QtGui.QPalette()
        bg = QtGui.QPixmap("./background/bgi1.png")
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(bg))
        self.setPalette(palette)
        self.add_ui(chinese_text)

    # 设置界面当中的组件
    def add_ui(self, text):
        # 多行文本显示，显示所有信息
        self.title = QTextBrowser(self)
        self.title.setGeometry(30, 10, 550, 150)
        font = self.title.font()  # 获取当前字体
        font.setPointSize(12)  # 设置字体大小为15点
        self.title.setFont(font)  # 应用新的字体到部件
        self.title.append('要翻译的内容：' + text)

        self.content = QTextBrowser(self)
        self.content.setGeometry(30, 175, 550, 150)
        font = self.content.font()  # 获取当前字体
        font.setPointSize(12)  # 设置字体大小为12点
        self.content.setFont(font)  # 应用新的字体到部件

        try:
            # 存储有道翻译的URL
            url = 'http://fanyi.youdao.com/translate'
            # 定义下载回来的翻译形式是以字典呈现
            data = {'i': text, 'doctype': 'json'}
            # headers可以防止爬虫被有道识别出来
            header = {'User-Agent': 'Mozilla/5.0'}
            # 使用post请求，把get到的东西封装在response里
            response = requests.post(url, data=data, headers=header)
            # 解析json
            reply = response.json()['translateResult'][0][0]['tgt']
            # 添加翻译的内容
            self.content.append('翻译：' + reply)

        except Exception:
            self.content.append('网络错误，请检查网络配置\n')

    # 退出销毁对话窗口
    def closeEvent(self, event):
        self.destroy()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    translation = Eat()
    translation.show()
    sys.exit(app.exec_())
