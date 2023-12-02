import random

from gbboard2 import Board
from gbtypes import Player

black_scores = {"011110": 9000, "01111": 1000, "11110": 1000, "01110": 900, "0110": 90, "010": 9}
white_scores = {"022220": 9000, "02222": 1000, "22220": 1000, "02220": 900, "0220": 90, "020": 9}
# COL_NAMES = 'ABCDEFGHJKLMNOP'

__all__ = ['Agent']

class Agent:
    directions = [-16, -15, -14, -1, 1, 14, 15, 16]

    def __init__(self):
        self.game: Board = None
        self.max_depth = 4

    def move(self, point: int, player: Player):
        self.game.place_stone(point, player)

    def choice_move(self):
        next_player = Player.White if self.game.step_num % 2 else Player.Black

        best_moves = []
        best_score = best_black = best_white = -999999

        # 遍历所有可能的落子点，并对于该处落子后的局面继续评估。
        possible_moves = self.get_possible_moves()
        for p in possible_moves:
            # 对于该处落子
            self.game.place_stone(p, next_player)
            # 注意： 此时的评分是对手的分数，我方的分数应为其相反数。
            opponent_best_res = self.alpha_beta_result(self.max_depth, best_black, best_white)
            my_res = -opponent_best_res
            # 回退到上一步，为搜索下一个可能点做准备。
            self.game.retract()
            # print((p, my_res), end=' ')
            # 以上与alphaBetaResult函数相同

            # 若当前点的评分高于已搜索到的最高评分，则更新最高评分，将bestMoves清空并将该点放入；
            # 若当前点的评分等于已搜索到的最高评分，则直接将该点放入bestMoves。
            if not best_moves or my_res > best_score:
                best_moves.clear()
                best_moves.append(p)
                best_score = my_res
                if next_player == Player.Black:
                    best_black = best_score
                else:
                    best_white = best_score
            elif my_res == best_score:
                best_moves.append(p)

        # print(list(map(lambda x: (COL_NAMES[x%15], x//15+1), best_moves)))
        # print(best_moves)
        # print()
        return random.choice(best_moves)

    def alpha_beta_result(self, depth, best_black, best_white):
        # 使用α - β剪枝评估当前局面的分数（是针对当前局面的下一手方的分数）
        # 参数depth：搜索深度

        next_player = Player.White if self.game.step_num % 2 else Player.Black
        # 若胜负已分，则返回一个极大（小）分
        if self.game.winner!=Player.Empty:
            return 999999 if self.game.winner==next_player else -999999
        # 当搜索到指定的深度时，直接用evaluate函数对局面评分。
        if depth==0:
            return self._evaluate()

        best_so_far = -999999
        # 遍历所有可能的落子点，并对于该处落子后的局面继续评估。
        possible_moves = self.get_possible_moves()
        for p in possible_moves:
            # 对于该处落子
            self.game.place_stone(p, next_player)
            # 注意： 此时的评分是对手的分数，我方的分数应为其相反数。
            opponent_best_res = self.alpha_beta_result(depth - 1, best_black, best_white)
            my_res = -opponent_best_res
            # 回退到上一步，为搜索下一个可能点做准备。
            self.game.retract()

            # 更新评分
            best_so_far = max(best_so_far, my_res)
            # 宽度剪枝
            if next_player == Player.Black:
                best_black = max(best_black, best_so_far)
                if best_white > -best_so_far:
                    return best_so_far
            else:
                best_white = max(best_white, best_so_far)
                if best_black > -best_so_far:
                    return best_so_far

        return best_so_far

    def get_possible_moves(self):
        # 先获取所有已有棋子的位置的相邻8个点位，放入points_evaluation中
        points_evaluation = {}
        possible_moves = []
        for m in self.game.manual:
            for d in self.directions:
                vm = m + d
                # 只有棋盘内的空位才会被加入
                if 0 <= vm < 225 and self.game.is_valid_move(vm):
                    if vm not in points_evaluation:
                        points_evaluation[vm] = 0
        # 用evaluate_one_point函数给points_evaluation中的点打分
        for p in points_evaluation:
            points_evaluation[p] = self._evaluate_one_point(p)
            possible_moves.append(p)

        # 根据评分大到小将点位排序
        possible_moves.sort(key=lambda x: points_evaluation[x], reverse=True)
        # 截取评分前8名的点
        if len(possible_moves) > 8:
            possible_moves = possible_moves[:8]
        return possible_moves

    def _evaluate(self):
        next_player = Player.Black if self.game.step_num%2==0 else Player.White
        total_score = 0

        for i in range(0, 225, 15):
            line = self.game.get_one_line(i, 0)
            total_score += self._evaluate_one_line(line, next_player)

        for i in range(15):
            line = self.game.get_one_line(i, 1)
            total_score += self._evaluate_one_line(line, next_player)

        for i in range(0, 151, 15):
            line = self.game.get_one_line(i, 2)
            total_score += self._evaluate_one_line(line, next_player)

        for i in range(10):
            line = self.game.get_one_line(i, 2)
            total_score += self._evaluate_one_line(line, next_player)

        for i in range(4, 15):
            line = self.game.get_one_line(i, 3)
            total_score += self._evaluate_one_line(line, next_player)

        for i in range(14, 165, 15):
            line = self.game.get_one_line(i, 3)
            total_score += self._evaluate_one_line(line, next_player)

        return total_score

    @staticmethod
    def _evaluate_one_line(line: str, next_player: Player):
        if len(line) < 5:
            return 0
        black_score = 0
        for p in black_scores:
            if p in line:
                black_score = black_scores[p]
                break

        white_score = 0
        for p in white_scores:
            if p in line:
                white_score = white_scores[p]
                break

        if next_player == Player.Black:
            return black_score - white_score
        else:
            return white_score - black_score

    def _evaluate_one_point(self, point):
        score = 0

        self.game.grid[point] = 1
        for i in range(4):
            line = self.game.get_one_line(point, i)
            if "11111" in line:
                self.game.grid[point] = 0
                return 100000
            for p in black_scores:
                if p in line:
                    score += black_scores[p]
                    break

        self.game.grid[point] = 2
        for i in range(4):
            line = self.game.get_one_line(point, i)
            if "22222" in line:
                self.game.grid[point] = 0
                return 100000
            for p in white_scores:
                if p in line:
                    score += white_scores[p]
                    break
        self.game.grid[point] = 0

        return score


if __name__ == '__main__':
    game = Board()
    game.grid[112] = 1
    game.grid[111] = 2
    game.grid[127] = 1
    game.grid[128] = 2
    a = Agent()
    a.game = game
    print(a._evaluate())


