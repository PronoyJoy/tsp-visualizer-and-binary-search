import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QLabel
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtCore import Qt, QPropertyAnimation, QRectF

class BinarySearchVisualization(QWidget):
    def __init__(self, array):
        super().__init__()
        self.array = sorted(array)
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Binary Search Simulation')

        layout = QVBoxLayout()

        self.graphicsView = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)

        self.inputField = QLineEdit(self)
        self.searchButton = QPushButton('Search', self)
        self.searchButton.clicked.connect(self.perform_search)

        layout.addWidget(self.graphicsView)
        layout.addWidget(self.inputField)
        layout.addWidget(self.searchButton)

        self.setLayout(layout)
        self.draw_array()

    def draw_array(self):
        self.scene.clear()
        self.bars = []
        bar_width = self.graphicsView.width() / len(self.array)

        for i, value in enumerate(self.array):
            x = i * bar_width
            y = self.graphicsView.height() - value * 5
            rect = QGraphicsRectItem(x, y, bar_width, value * 5)
            rect.setBrush(QColor(0, 0, 255))
            self.bars.append(rect)
            self.scene.addItem(rect)

    def perform_search(self):
        target = self.inputField.text()
        if not target.isdigit():
            return

        target = int(target)
        left, right = 0, len(self.array) - 1
        bar_width = self.graphicsView.width() / len(self.array)

        while left <= right:
            mid = (left + right) // 2
            rect = self.bars[mid]
            rect.setBrush(QColor(255, 255, 0))
            QApplication.processEvents()

            if self.array[mid] == target:
                rect.setBrush(QColor(0, 255, 0))
                self.animate_rect(rect)
                return
            elif self.array[mid] < target:
                left = mid + 1
                rect.setBrush(QColor(255, 0, 0))
            else:
                right = mid - 1
                rect.setBrush(QColor(255, 0, 0))

            QApplication.processEvents()

    def animate_rect(self, rect):
        animation = QPropertyAnimation(rect, b"rect")
        animation.setDuration(1000)
        start_rect = rect.rect()
        end_rect = QRectF(start_rect.x(), start_rect.y() - 20, start_rect.width(), start_rect.height())
        animation.setStartValue(start_rect)
        animation.setEndValue(end_rect)
        animation.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BinarySearchVisualization([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    window.show()
    sys.exit(app.exec_())
