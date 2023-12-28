import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                             QWidget, QSpinBox, QSplitter, QHBoxLayout, QLabel)
from PyQt5.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class DynamicMplCanvas(FigureCanvas):
    """一個展示動態三維散點圖的類。"""

    def __init__(self, *args, interval=1000, **kwargs):
        fig = Figure(figsize=(10, 6), dpi=100)
        super().__init__(fig)
        self.axes = fig.add_subplot(111, projection='3d')
        self.timer_event = fig.canvas.new_timer(interval=interval)
        self.timer_event.add_callback(self._update_canvas)
        self.timer_event.start()

    def _update_canvas(self):
        self.axes.clear()
        # 生成隨機數據
        x = np.random.rand(100)
        y = np.random.rand(100)
        z = np.random.rand(100)
        self.axes.scatter(x, y, z)
        self.axes.set_xlabel('X 軸')
        self.axes.set_ylabel('Y 軸')
        self.axes.set_zlabel('Z 軸')
        self.axes.figure.canvas.draw()


class PieChartCanvas(FigureCanvas):
    """用於展示圓餅圖的類。"""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(fig)
        self.axes = fig.add_subplot(111)
        self.draw_pie_chart()

    def draw_pie_chart(self):
        labels = 'A', 'B', 'C', 'D'
        sizes = [15, 30, 45, 10]
        self.axes.clear()
        self.axes.pie(sizes, labels=labels, autopct='%1.1f%%')
        # Equal aspect ratio ensures that pie is drawn as a circle.
        self.axes.axis('equal')
        self.draw()


class MainWindow(QMainWindow):
    """主視窗類別。"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("雙動態三維圖表與圓餅圖")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 使用QSplitter進行布局
        self.main_splitter = QSplitter(Qt.Vertical)
        self.top_splitter = QSplitter(Qt.Horizontal)

        # 創建動態圖表並添加到分隔器
        self.dynamic_canvas1 = DynamicMplCanvas(
            self.central_widget, interval=1000)
        self.dynamic_canvas2 = DynamicMplCanvas(
            self.central_widget, interval=1500)
        self.top_splitter.addWidget(self.dynamic_canvas1)
        self.top_splitter.addWidget(self.dynamic_canvas2)

        # 創建圓餅圖和數值框的布局
        bottom_layout = QVBoxLayout()
        self.pie_chart_canvas = PieChartCanvas(self.central_widget)
        bottom_layout.addWidget(self.pie_chart_canvas)

        self.spin_box1 = QSpinBox(self.central_widget)
        self.spin_box2 = QSpinBox(self.central_widget)
        spin_layout = QHBoxLayout()
        spin_layout.addWidget(self.spin_box1)
        spin_layout.addWidget(self.spin_box2)
        bottom_layout.addLayout(spin_layout)

        # 添加溫度顯示框
        self.temperature_label = QLabel("溫度: --°C", self.central_widget)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.temperature_label.setStyleSheet("""
            QLabel {
                border: 2px solid #aaaaaa;
                border-radius: 5px;
                padding: 5px;
                background-color: #222222;
                font-size: 14pt;
                color: #eeeeee;
            }
        """)
        bottom_layout.addWidget(self.temperature_label)

        # 設置定時器以定期更新溫度
        self.temperature_timer = QTimer(self)
        self.temperature_timer.timeout.connect(self.update_temperature)
        self.temperature_timer.start(1000)  # 每秒更新一次

        # 將布局放入另一個widget並添加到分隔器
        bottom_widget = QWidget()
        bottom_widget.setLayout(bottom_layout)
        self.main_splitter.addWidget(self.top_splitter)
        self.main_splitter.addWidget(bottom_widget)

        # 設置中央widget的布局
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.addWidget(self.main_splitter)
        self.central_widget.setLayout(main_layout)

        # 添加QSS樣式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #333333;
            }
            QWidget {
                color: #ffffff;
                font-size: 12pt;
                background-color: #444444;
            }
            QSpinBox {
                background-color: #555555;
                border: 1px solid #666666;
                border-radius: 5px;
                padding: 5px;
            }
        """)

    def update_temperature(self):
        # 生成一個隨機溫度值
        temperature = random.uniform(20, 30)
        self.temperature_label.setText(f"溫度: {temperature:.2f}°C")


app = QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())