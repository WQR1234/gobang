from PySide6.QtCore import Qt, Signal, QEvent, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsSceneMouseEvent

from typing import List, Optional

from agent import Agent
from gbtypes import Player
from gbboard2 import Board

CELL_SIZE = 60  # 每个格子的大小


class BoardScene(QGraphicsScene):
    call_robot_move = Signal()  # 每次落子，触发该信号，调用_robot_move函数
    has_moved = Signal(int)  # 每次落子，触发该信号，文本框输出落子信息
    game_over = Signal(str)  # 终局，触发该信号，文本框输出胜负结果

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

        # 黑棋子图片
        self._black_pix = QPixmap()
        self._black_pix.load(":/imgs/shell_stb1.png")
        self._black_pix = self._black_pix.scaled(CELL_SIZE, CELL_SIZE)

        # 白棋子图片
        self._white_pix = QPixmap()
        self._white_pix.load(":/imgs/shell_stw1.png")
        self._white_pix = self._white_pix.scaled(CELL_SIZE, CELL_SIZE)

        # 透明图片
        self._empty_pix = QPixmap(CELL_SIZE, CELL_SIZE)
        self._empty_pix.fill(Qt.transparent)

        # 半透明黑棋子图片
        self._translucent_black_pix = QPixmap()
        self._translucent_black_pix.load(":/imgs/translucent_b.png")
        self._translucent_black_pix = self._translucent_black_pix.scaled(CELL_SIZE, CELL_SIZE)

        # 半透明白棋子图片
        self._translucent_white_pix = QPixmap()
        self._translucent_white_pix.load(":/imgs/translucent_w.png")
        self._translucent_white_pix = self._translucent_white_pix.scaled(CELL_SIZE, CELL_SIZE)

        # 为225个交叉点设置225个图元
        self._cell_pixmaps: List[QGraphicsPixmapItem] = []
        for i in range(225):
            cell_pix = QGraphicsPixmapItem(self._empty_pix)
            cell_pix.setPos(i % 15 * CELL_SIZE, i // 15 * CELL_SIZE)
            self.addItem(cell_pix)
            self._cell_pixmaps.append(cell_pix)

        self.gobang_game: Optional[Board] = None
        self.robot: Optional[Agent] = None
        self.are_players_robot = [False, False]  # 记录黑白是否为人机

        self._prev_mouse_pos = 0

        self.call_robot_move.connect(self._robot_move)

    def set_cell_pix(self, point, player):
        # 修改指定位置图元的图片
        if player == Player.Black:
            self._cell_pixmaps[point].setPixmap(self._black_pix)
        elif player == Player.White:
            self._cell_pixmaps[point].setPixmap(self._white_pix)
        else:
            self._cell_pixmaps[point].setPixmap(self._empty_pix)

    def _player_move(self, player_idx, point):
        """
        输入落子方与落子点，修改Board对象，修改界面显示。
        :param player_idx:  落子方，0表示黑，1表示白
        :param point:  落子点
        :return:
        """
        if player_idx == 0:
            self.gobang_game.place_stone(point, Player.Black)
            self._cell_pixmaps[point].setPixmap(self._black_pix)
        else:
            self.gobang_game.place_stone(point, Player.White)
            self._cell_pixmaps[point].setPixmap(self._white_pix)

        self.has_moved.emit(point)

        if self.gobang_game.winner == Player.Empty:
            self.call_robot_move.emit()
        else:
            res = "黑胜" if self.gobang_game.winner == Player.Black else "白胜"
            self.game_over.emit(res)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        # 鼠标点击落子
        if (self.gobang_game is not None) and (self.gobang_game.winner==Player.Empty):
            player_idx = self.gobang_game.step_num % 2
            if self.are_players_robot[player_idx]:  # 若当前为人机落子，则鼠标点击无效
                return

            # 根据鼠标位置计算棋盘位置，进而得到图元列表的索引
            mouse_x, mouse_y = int(event.scenePos().x()), int(event.scenePos().y())
            row, col = mouse_y // CELL_SIZE, mouse_x // CELL_SIZE
            point = 15 * row + col
            if not self.gobang_game.is_valid_move(point):
                return

            self._player_move(player_idx, point)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        # 鼠标移动时，将在其当前位置的图元填充对应的半透明色棋子图片。
        if (self.gobang_game is not None) and (self.gobang_game.winner==Player.Empty):
            if self.gobang_game.is_valid_move(self._prev_mouse_pos):
                self._cell_pixmaps[self._prev_mouse_pos].setPixmap(self._empty_pix)  # 将前一位置的图元设一个空图

            # 根据鼠标位置计算棋盘位置，进而得到图元列表的索引
            mouse_x, mouse_y = int(event.scenePos().x()), int(event.scenePos().y())
            row, col = mouse_y // CELL_SIZE, mouse_x // CELL_SIZE

            point = 15*row+col
            self._prev_mouse_pos = point
            if self.gobang_game.is_valid_move(point):
                if self.gobang_game.step_num % 2:
                    self._cell_pixmaps[point].setPixmap(self._translucent_white_pix)
                else:
                    self._cell_pixmaps[point].setPixmap(self._translucent_black_pix)

    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.Type.GraphicsSceneLeave:  # 鼠标离开scene后，将上一位置的图元设个空图
            if (self.gobang_game is not None) and (self.gobang_game.winner==Player.Empty):
                self._cell_pixmaps[self._prev_mouse_pos].setPixmap(self._empty_pix)

        return super().event(event)

    @Slot()
    def _robot_move(self):  # 人机落子
        if (self.gobang_game is None) or (self.gobang_game.winner!=Player.Empty):
            return

        robot_idx = self.gobang_game.step_num % 2
        if self.are_players_robot[robot_idx]:
            move = self.robot.choice_move()  # 耗时的计算，可考虑放入子线程中
            self._player_move(robot_idx, move)

