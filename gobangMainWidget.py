from PySide6.QtCore import QPoint, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QPushButton

from ui_gobangMainWidget import Ui_GobangMainWidget
from agent import *
from gbboard2 import Board
from gbtypes import Player
from boardScene import BoardScene


class GobangMainWidget(QWidget, Ui_GobangMainWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.board_scene = BoardScene(0, 0, self.boardView.width(), self.boardView.height())
        self.boardView.setScene(self.board_scene)
        self.boardView.setMouseTracking(True)

        # 链接按钮对应的function
        self.startBtn.clicked.connect(self._on_startBtn_clicked)
        self.retractBtn.clicked.connect(self._on_retractBtn_clicked)
        self.clearBtn.clicked.connect(self._on_clearBtn_clicked)
        self.resignBtn.clicked.connect(self._on_resignBtn_clicked)

        # 下拉选择框的function
        self.comboBox.currentIndexChanged.connect(self._on_comboBox_changed)
        self.comboBox_2.currentIndexChanged.connect(self._on_comboBox2_changed)

        # 每落子，显示落子信息
        self.board_scene.has_moved.connect(self._show_move_info)
        # 终局，显示结果
        self.board_scene.game_over.connect(self._show_result)


    @Slot()
    def _on_startBtn_clicked(self):  # 点击开始按钮, 开始新的一局
        if self.board_scene.gobang_game is None:  # 若当前无正在进行的棋局（若有，可以先点击清空）
            self.board_scene.gobang_game = Board()
            if self.board_scene.are_players_robot[0] or self.board_scene.are_players_robot[1]:  # 若黑白有一方为人机，则为Agent的成员game赋值
                self.board_scene.robot.game = self.board_scene.gobang_game
            if self.board_scene.are_players_robot[0]:  # 若黑方为人机，则第一手默认走中心
                self.board_scene.gobang_game.place_stone(112, Player.Black)
                self.board_scene.set_cell_pix(112, Player.Black)
                self.textEdit.append("黑： 8行， 8列。")
                self.board_scene.call_robot_move.emit()

    @Slot()
    def _on_retractBtn_clicked(self):  # 点击悔棋按钮，回退一步
        if self.board_scene.gobang_game is not None and self.board_scene.gobang_game.step_num > 0:
            last_point = self.board_scene.gobang_game.retract()
            self.board_scene.set_cell_pix(last_point, Player.Empty)
            self.textEdit.append("悔棋")

    @Slot()
    def _on_clearBtn_clicked(self):  # 清空棋盘,重置所有控件状态
        if self.board_scene.gobang_game is not None:
            for i in range(225):
                self.board_scene.set_cell_pix(i, Player.Empty)

            self.board_scene.gobang_game = None
            self.textEdit.clear()
            self.comboBox.setCurrentIndex(0)
            self.comboBox_2.setCurrentIndex(0)
            self.board_scene.are_players_robot = [False, False]

    @Slot()
    def _on_resignBtn_clicked(self):  # 认输
        if self.board_scene.gobang_game is not None:
            if self.board_scene.gobang_game.step_num % 2:
                self.board_scene.gobang_game.winner = Player.Black
                self.textEdit.append("白方认输，黑胜")
            else:
                self.board_scene.gobang_game.winner = Player.White
                self.textEdit.append("黑方认输，白胜")

    @Slot(int)
    def _on_comboBox_changed(self, i):  # 修改黑方下拉框
        self.board_scene.are_players_robot[0] = bool(i)

    @Slot(int)
    def _on_comboBox2_changed(self, i):  # 修改白方下拉框
        self.board_scene.are_players_robot[1] = bool(i)

    @Slot(int)
    def _show_move_info(self, point):
        r, c = point // 15, point % 15
        info = "黑：" if self.board_scene.gobang_game.step_num % 2 else "白："
        info += f"{r+1}行，{c+1}列。"
        self.textEdit.append(info)

    @Slot(str)
    def _show_result(self, res):
        self.textEdit.append(res)

