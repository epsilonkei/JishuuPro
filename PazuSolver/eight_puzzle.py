# -*- coding: utf-8 -*
"""
8-puzzle path search by A* algorithim
"""
from heapq import heappush, heappop
from random import shuffle


class sBoard():

    def __init__(self, board_list, distance, parent):
        self._array = board_list
        self.heuristic = calc_heuristic(self._array)
        self.distance = distance
        self.cost = self.distance + self.heuristic
        self.parent = parent
        self.hashvalue = hash(tuple(self._array))

    def _getsBoard(self):
        return self._array

    def __hash__(self):
        return self.hashvalue

    def __eq__(self,other):
        return self._array == other._array

def astar():
    queue = []          # 待ち行列
    dist_dic = {}       # 初期盤面からの手数
    visited = {}        # 訪問済みnode；過去の盤面
    # インスタンス化
    start = sBoard(init_board, 0, None)
    end = sBoard(goal_board, 99, None)
    # open-listのstart-node（コストとインスタンスを登録）
    heappush(queue, (start.cost, start))
    No = 0                                              # debug
    # ゴールに到達するまで新しい盤面を探索する
    while len(queue) > 0:
        No += 1                                         # debug
        # open-listからコスト最小の探索済みnode（盤面）を取り出す
        now_tuple = heappop(queue)
        now_board = now_tuple[1]
        if now_board._array == goal_board or now_board._array == goal_board2:

            # ゴールを発見
            end = now_board
            break
        """debug
        if No > 100000:
            end = now_board
            break
        """
        # ピースのない位置へ入ることのできる隣接座標
        index = now_board._array.index(0)
        x, y = XY_coord(index)
        coord_next_OK = coord_next(x, y)
        # 次のnodeを探索；ピースのない位置へスライドを試行
        for coord in coord_next_OK:
            next_board = now_board._array[:]
            next_index = coord[0] * No_XY + coord[1]
            next_board[index],next_board[next_index] = \
                    next_board[next_index],next_board[index]
            # インスタンス化
            new_sboard = sBoard(next_board, now_board.distance+1, now_board)
            new_distance = new_sboard.cost
            if tuple(new_sboard._array) not in visited or \
                    new_distance < dist_dic[new_sboard]:
                # 未訪問ならばor訪問済みで今回のコストのほうが小さいならば
                # start nodeからの距離（コスト）を登録
                dist_dic[new_sboard] = new_distance
                # 訪問済みリストに登録
                visited[tuple(new_sboard._array)] = new_sboard
                # 親nodeを登録
                new_sboard.parent = now_board
                # 待ち行列に登録
                heappush(queue, (new_sboard.cost, new_sboard))
    var = end
    sol = []
    while var != start:
        sol = sol + [var._getsBoard()]
        var = var.parent
    sol = sol + [var._getsBoard()]
    sol.reverse()
    #print sol
    # print len(sol), No
    return sol, No

def calc_heuristic(array):
    """現局面からゴールまでのコスト予測値
    """
    board_list = array
    same = 0
    manhattan = 0
    for var in board_list:
        """ゴール盤面と一致しないピースの数"""
        x, y = XY_coord(var)
        if goal_board.index(var) != board_list.index(var):
            same += 1
        """ゴール盤面へ移動するときのマンハッタン距離"""
        pos = goal_board.index(var)
        goal_board_x, goal_board_y = XY_coord(pos)
        x, y = XY_coord(board_list.index(var))
        manhattan += abs(x-goal_board_x) + abs(y-goal_board_y)
    # print same, manhattan                   # debug
    # heuristic = same + manhattan            # debug
    heuristic = manhattan                   # debug
    # heuristic = same                        # debug
    return 1.0 * heuristic

def coord_next(x, y):
    """ピースのない位置へスライドできる隣接マスのXY座標のリストを返す
    """
    coord_next_OK = [[x, y]]
    # right
    if(x+1 < No_XY):
        coord_next_OK.append([x+1, y])
    # left
    if(x-1 >= 0):
        coord_next_OK.append([x-1, y])
    # down
    if(y-1 >= 0):
        coord_next_OK.append([x, y-1])
    # up
    if(y+1 < No_XY):
        coord_next_OK.append([x, y+1])

    return coord_next_OK


def XY_coord(index):
    """盤面配列のインデックスからXY座標を返す
    """
    x = index / No_XY
    y = index % No_XY
    return x, y

def main():
    global init_board, goal_board, goal_board2, No_XY

    No_XY = 3
    goal_board = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    goal_board2 = [1, 2, 3, 4, 5, 6, 8, 7, 0]
    init_board = [8, 6, 7, 2, 5, 4, 3, 0, 1]
    # shuffle(init_board)     # init_boardをシャッフルする
    sol, visit = astar()
    return sol, visit

if __name__ == '__main__':
    sol, visit = main()
    print sol
    print len(sol), visit

