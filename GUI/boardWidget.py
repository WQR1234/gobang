import numpy as np
from PySide6.QtCore import QSize, QRect, QPoint, Qt
from PySide6.QtGui import QPixmap, QPalette, QBrush, QPaintEvent, QPainter, QMouseEvent, QPen
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QStyleOption, QStyle


class BoardWidget(QLabel):
    X_SCALE = np.array([28, 67, 105, 145, 185, 225, 264, 304, 344, 384, 423, 463, 502, 542, 581])
    Y_SCALE = np.array([11, 52, 93, 137, 179, 221, 263, 305, 347, 388, 431, 473, 513, 558, 597])

    def __init__(self, parent):
        super().__init__(parent)

        self.m_pixmap = QPixmap()
        self.m_circle_center = QPoint(0, 0)
        self.m_circle_radius = 0

        self.setMouseTracking(True)
        self.m_rect_vertex = QPoint(0, 0)
        self.m_rect_size = QSize()

        self.flag = True

    # def paintEvent(self, event: QPaintEvent) -> None:
    #     opt = QStyleOption()
    #     opt.initFrom(self)
    #     p = QPainter(self)
    #     self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        # painter.setRenderHint(QPainter.RenderHint)

        # if self.m_pixmap is not None:
        painter.drawPixmap(0, 0, self.m_pixmap)

        painter.setPen(Qt.red)
        painter.drawRect(QRect(self.m_rect_vertex, self.m_rect_size))

        painter.setPen(QPen(Qt.black, 2))
        if self.flag:
            painter.setBrush(Qt.white)
        else:
            painter.setBrush(Qt.black)
        painter.drawEllipse(self.m_circle_center, self.m_circle_radius, self.m_circle_radius+1)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:

            self.m_pixmap = self.grab()

            mouse_x, mouse_y = event.pos().x(), event.pos().y()
            index_x = np.argmin(np.abs(BoardWidget.X_SCALE-mouse_x))
            x = BoardWidget.X_SCALE[index_x]
            index_y = np.argmin(np.abs(BoardWidget.Y_SCALE-mouse_y))
            y = BoardWidget.Y_SCALE[index_y]
            self.m_circle_center = QPoint(x, y)
            self.m_circle_radius = 16

            self.update()

            self.flag = not self.flag

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        mouse_x, mouse_y = ev.pos().x(), ev.pos().y()
        index_x = np.argmin(np.abs(BoardWidget.X_SCALE - mouse_x))
        x = BoardWidget.X_SCALE[index_x]
        index_y = np.argmin(np.abs(BoardWidget.Y_SCALE - mouse_y))
        y = BoardWidget.Y_SCALE[index_y]
        self.m_rect_vertex = QPoint(x-10, y-10)
        self.m_rect_size = QSize(20, 20)

        self.update()
