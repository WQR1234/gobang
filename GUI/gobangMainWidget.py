import time

from PySide6.QtCore import QPoint, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QPushButton

from GUI.ui_gobangMainWidget import Ui_gobangMainWidget
from agent import *
from evaluation2 import evaluation_fn

from gbboard2 import GameState, Move
from gbtypes import Player


class GobangMainWidget(QWidget, Ui_gobangMainWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.setFixedSize(600, 400)
        self.clearBtn.clicked.connect(self._clear)
        self.startBtn.clicked.connect(self._start)
        self.comboBox.currentIndexChanged.connect(self._changePlayer1)
        self.comboBox_2.currentIndexChanged.connect(self._changePlayer2)

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
                print(type(self.boardWidget.players[self.boardWidget.game.next_player]))
                if isinstance(self.boardWidget.players[self.boardWidget.game.next_player], Human):
                    self.boardWidget.next_is_human = True
                    s = time.time()
                    self.boardWidget.loop.exec()

                    if self.boardWidget.game is None:
                        break
                    e = time.time()
                    move = Move.play((self.boardWidget.row, self.boardWidget.col))
                    self.textEdit.setText(str(move)+" spend %.2f s" % (e-s))
                    self.boardWidget.game = self.boardWidget.game.apply_move(move)
                    self.boardWidget.repaint()

                else:
                    self.boardWidget.next_is_human = False
                    s = time.time()
                    if self.boardWidget.game is None:
                        break

                    move = self.boardWidget.players[self.boardWidget.game.next_player].select_move(self.boardWidget.game)
                    self.boardWidget.m_circle_radius = 16
                    self.boardWidget.m_pixmap = self.boardWidget.grab()
                    self.boardWidget.row, self.boardWidget.col = move.point
                    e = time.time()
                    self.textEdit.setText(str(move)+" spend %.2f s" % (e - s))
                    self.boardWidget.game = self.boardWidget.game.apply_move(move)
                    self.boardWidget.repaint()

            self.boardWidget.next_is_human = False
            if self.boardWidget.game is not None:
                if self.boardWidget.game.winner == Player.black:
                    self.textEdit.setText("black win")
                elif self.boardWidget.game.winner == Player.white:
                    self.textEdit.setText("white win")

    @Slot(int)
    def _changePlayer1(self, index):
        if index == 0:
            self.boardWidget.players[Player.black] = Human()

        elif index == 1:
            self.boardWidget.players[Player.black] = AlphaBetaAgent(3, evaluation_fn)

        elif index == 2:
            self.boardWidget.players[Player.black] = MCTSAgent(10000, 1.3)

    @Slot(int)
    def _changePlayer2(self, index):
        if index == 0:
            self.boardWidget.players[Player.white] = Human()

        elif index == 1:
            self.boardWidget.players[Player.white] = AlphaBetaAgent(3, evaluation_fn)

        elif index == 2:
            self.boardWidget.players[Player.white] = MCTSAgent(10000, 1.3)


