from typing import Optional

import numpy as np
from PySide6.QtCore import QSize, QRect, QPoint, Qt, QEventLoop
from PySide6.QtGui import QPixmap, QPalette, QBrush, QPaintEvent, QPainter, QMouseEvent, QPen
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QStyleOption, QStyle

from agent import Human
from gbboard import GameState, Move
from gbtypes import Player


class BoardWidget(QLabel):
    X_SCALE = np.array([28, 67, 105, 145, 185, 225, 264, 304, 344, 384, 423, 463, 502, 542, 581])
    Y_SCALE = np.array([11, 52, 93, 137, 179, 221, 263, 305, 347, 388, 431, 473, 513, 558, 597])

    def __init__(self, parent):
        super().__init__(parent)

        self.m_pixmap = QPixmap()
        # self.m_circle_center = QPoint(0, 0)
        self.m_circle_radius = 0

        self.setMouseTracking(True)
        self.m_rect_vertex = QPoint(-1, -1)
        self.m_rect_size = QSize()

        self.game:Optional[GameState] = None
        self.players = {
            Player.black: Human(),
            Player.white: Human()
        }
        self.row, self.col = 100, 100
        self.next_is_human = False

        self.loop = QEventLoop()

    # def paintEvent(self, event: QPaintEvent) -> None:
    #     opt = QStyleOption()
    #     opt.initFrom(self)
    #     p = QPainter(self)
    #     self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        # painter.setRenderHint(QPainter.RenderHint)

        # if self.m_pixmap is not None:
        if self.game is not None:
            painter.drawPixmap(0, 0, self.m_pixmap)
            painter.setPen(Qt.red)
            painter.drawRect(QRect(self.m_rect_vertex, self.m_rect_size))

            painter.setPen(QPen(Qt.black, 2))
            if self.game.next_player == Player.black:
                painter.setBrush(Qt.white)
            else:
                painter.setBrush(Qt.black)
            if self.row*self.col <= 196:
                circle_center = QPoint(BoardWidget.X_SCALE[self.col], BoardWidget.Y_SCALE[self.row])
                painter.drawEllipse(circle_center, self.m_circle_radius, self.m_circle_radius+1)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton and self.game is not None and self.next_is_human:

            mouse_x, mouse_y = event.pos().x(), event.pos().y()
            # index_x = np.argmin(np.abs(BoardWidget.X_SCALE-mouse_x))
            col = np.argmin(np.abs(BoardWidget.X_SCALE-mouse_x))
            # x = BoardWidget.X_SCALE[index_x]
            # index_y = np.argmin(np.abs(BoardWidget.Y_SCALE-mouse_y))
            row = np.argmin(np.abs(BoardWidget.Y_SCALE-mouse_y))
            # y = BoardWidget.Y_SCALE[index_y]
            # self.m_circle_center = QPoint(BoardWidget.X_SCALE[self.col], BoardWidget.Y_SCALE[self.row])
            self.m_circle_radius = 16

            if self.game.is_valid_move(Move.play((row, col))):
                self.m_pixmap = self.grab()
                self.row, self.col = row, col
                self.update()
                self.loop.quit()

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        if self.game is not None:
            if self.next_is_human:
                mouse_x, mouse_y = ev.pos().x(), ev.pos().y()
                index_x = np.argmin(np.abs(BoardWidget.X_SCALE - mouse_x))
                x = BoardWidget.X_SCALE[index_x]
                index_y = np.argmin(np.abs(BoardWidget.Y_SCALE - mouse_y))
                y = BoardWidget.Y_SCALE[index_y]
                self.m_rect_vertex = QPoint(x-10, y-10)
                self.m_rect_size = QSize(20, 20)

                self.update()

    def start_new_game(self):
        self.game = GameState.new_game()
        while not self.game.is_over():
            if isinstance(self.players[self.game.next_player], Human):
                self.loop.exec()
                if self.game is None:
                    break
                self.game = self.game.apply_move(Move.play((self.row, self.col)))
            else:
                pass


