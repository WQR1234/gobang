import time

from PySide6.QtCore import QPoint, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QPushButton

from GUI.ui_gobangMainWidget import Ui_gobangMainWidget
from agent import Human

from gbboard import GameState, Move
from gbtypes import Player


class GobangMainWidget(QWidget, Ui_gobangMainWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.setFixedSize(600, 400)
        self.clearBtn.clicked.connect(self._clear)
        self.startBtn.clicked.connect(self._start)

    @Slot()
    def _clear(self):
        self.boardWidget.game = None
        self.boardWidget.loop.quit()
        self.boardWidget.m_pixmap = QPixmap()
        self.boardWidget.row, self.boardWidget.col = 100, 100
        self.boardWidget.m_rect_vertex = QPoint(100, 100)
        self.boardWidget.m_circle_radius = 0
        self.boardWidget.update()

        self.textEdit.clear()

    @Slot()
    def _start(self):
        if self.boardWidget.game is None:
            self.boardWidget.game = GameState.new_game()
            while not self.boardWidget.game.is_over():
                if isinstance(self.boardWidget.players[self.boardWidget.game.next_player], Human):
                    self.boardWidget.next_is_human = True
                    s = time.time()
                    self.boardWidget.loop.exec()

                    if self.boardWidget.game is None:
                        break
                    e = time.time()
                    self.textEdit.setText("spend %.2f s" % (e-s))
                    self.boardWidget.game = self.boardWidget.game.apply_move(
                        Move.play((self.boardWidget.row, self.boardWidget.col))
                    )
                else:
                    pass
            self.boardWidget.next_is_human = False
            if self.boardWidget.game is not None:
                if self.boardWidget.game.winner == Player.black:
                    self.textEdit.setText("black win")
                elif self.boardWidget.game.winner == Player.white:
                    self.textEdit.setText("white win")


