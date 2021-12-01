class Robot(object):
    '''An AI base on the basic rule of gomoku game'''

    def __init__(self, _board):
        self.board = _board

    def haveValuePoints(self, player, enemy, board):
        """calculate all points on the board which have value"""
        points = []

        for x in range(15):
            for y in range(15):
                list1 = []
                list2 = []
                list3 = []
                list4 = []
                if self.board[x][y] == -1:
                    for tmp in range(9):
                        i = x + tmp - 4
                        j = y + tmp - 4
                        # search range is the space around (x,y) of 8*8
                        if i < 0 or i > 14:
                            list1.append(-2)
                        else:
                            list1.append(board[i][y])
                        if j < 0 or j > 14:
                            list2.append(-2)
                        else:
                            list2.append(board[x][j])
                        if i < 0 or j < 0 or i > 14 or j > 14:
                            list3.append(-2)
                        else:
                            list3.append(board[i][j])
                        k = y - tmp + 4
                        if i < 0 or k < 0 or i > 14 or k > 14:
                            list4.append(-2)
                        else:
                            list4.append(board[i][k])

                    playerValue = self.value_point(player, enemy, list1, list2, list3, list4)
                    enemyValue = self.value_point(enemy, player, list1, list2, list3, list4)
                    if enemyValue >= 10000:
                        enemyValue -= 500
                    elif enemyValue >= 5000:
                        enemyValue -= 300
                    elif enemyValue >= 2000:
                        enemyValue -= 250
                    elif enemyValue >= 1500:
                        enemyValue -= 200
                    elif enemyValue >= 99:
                        enemyValue -= 10
                    elif enemyValue >= 5:
                        enemyValue -= 1
                    value = playerValue + enemyValue
                    if value > 0:
                        points.append([x, y, value])
        return points

    def MaxValue_po(self, player, enemy):
        """calculate the most valuable point，fetch all points have value，then check which is max"""
        points = self.haveValuePoints(player, enemy, self.board)
        flag = 0
        _point = []
        for p in points:
            if p[2] > flag:
                _point = p
                flag = p[2]
        return _point[0], _point[1], _point[2]  # return x,y value

    def value_point(self, player, enemy, list1, list2, list3, list4):
        """calculate value of points"""
        flag = 0
        flag += self.willbefive(player, list1)
        flag += self.willbefive(player, list2)
        flag += self.willbefive(player, list3)
        flag += self.willbefive(player, list4)
        flag += self.willbealive4(player, list1)
        flag += self.willbealive4(player, list2)
        flag += self.willbealive4(player, list3)
        flag += self.willbealive4(player, list4)
        flag += self.willbesleep4(player, enemy, list1)
        flag += self.willbesleep4(player, enemy, list2)
        flag += self.willbesleep4(player, enemy, list3)
        flag += self.willbesleep4(player, enemy, list4)
        flag += self.willbealive3(player, list1)
        flag += self.willbealive3(player, list2)
        flag += self.willbealive3(player, list3)
        flag += self.willbealive3(player, list4)
        flag += self.willbesleep3(player, enemy, list1)
        flag += self.willbesleep3(player, enemy, list2)
        flag += self.willbesleep3(player, enemy, list3)
        flag += self.willbesleep3(player, enemy, list4)
        flag += self.willbealive2(player, enemy, list1)
        flag += self.willbealive2(player, enemy, list2)
        flag += self.willbealive2(player, enemy, list3)
        flag += self.willbealive2(player, enemy, list4)
        flag += self.willbesleep2(player, enemy, list1)
        flag += self.willbesleep2(player, enemy, list2)
        flag += self.willbesleep2(player, enemy, list3)
        flag += self.willbesleep2(player, enemy, list4)
        return flag

    @staticmethod
    def willbefive(player, checklist):
        """move this step get five in a row /?ooooo?"""
        if checklist[0] == player and checklist[1] == player and \
                checklist[2] == player and checklist[3] == player:
            return 10000
        elif checklist[5] == player and checklist[6] == player and \
                checklist[7] == player and checklist[8] == player:
            return 10000
        elif checklist[2] == player and checklist[3] == player and \
                checklist[5] == player and checklist[6] == player:
            return 10000
        elif checklist[1] == player and checklist[2] == player and \
                checklist[3] == player and checklist[5] == player:
            return 10000
        elif checklist[3] == player and checklist[5] == player and \
                checklist[6] == player and checklist[7] == player:
            return 10000
        else:
            return 0

    @staticmethod
    def willbealive4(player, checklist):
        """move this step get alive 4 /_oooo_"""
        if checklist[0] == -1 and checklist[1] == player and \
                checklist[2] == player and checklist[3] == player \
                and checklist[5] == -1:
            return 5000
        elif checklist[3] == -1 and checklist[5] == player and \
                checklist[6] == player and checklist[7] == player \
                and checklist[8] == -1:
            return 5000
        elif checklist[1] == -1 and checklist[2] == player and \
                checklist[3] == player and checklist[5] == player \
                and checklist[6] == -1:
            return 5000
        elif checklist[2] == -1 and checklist[3] == player and \
                checklist[5] == player and checklist[6] == player \
                and checklist[7] == -1:
            return 5000
        else:
            return 0

    @staticmethod
    def willbesleep4(player, enemy, checklist):
        """move this step get sleep 4 /xoooo_"""
        if checklist[0] == enemy and checklist[1] == player and \
                checklist[2] == player and checklist[3] == player \
                and checklist[5] == -1:
            return 1700
        elif checklist[1] == enemy and checklist[2] == player and \
                checklist[3] == player and checklist[5] == player \
                and checklist[6] == -1:
            return 1700
        elif checklist[2] == enemy and checklist[3] == player and \
                checklist[5] == player and checklist[6] == player \
                and checklist[7] == -1:
            return 1700
        elif checklist[3] == enemy and checklist[5] == player and \
                checklist[6] == player and checklist[7] == player \
                and checklist[8] == -1:
            return 1700
        elif checklist[0] == -1 and checklist[1] == player and \
                checklist[2] == player and checklist[3] == player \
                and checklist[5] == enemy:
            return 1700
        elif checklist[1] == -1 and checklist[2] == player and \
                checklist[3] == player and checklist[5] == player \
                and checklist[6] == enemy:
            return 1700
        elif checklist[2] == -1 and checklist[3] == player and \
                checklist[5] == player and checklist[6] == player \
                and checklist[7] == enemy:
            return 1700
        elif checklist[3] == -1 and checklist[5] == player and \
                checklist[6] == player and checklist[7] == player \
                and checklist[8] == enemy:
            return 1700
        else:
            return 0

    @staticmethod
    def willbealive3(player, checklist):
        """move this step get alive 3 /_ooo_"""
        if checklist[0] == -1 and checklist[1] == -1 and \
                checklist[2] == player and checklist[3] == player \
                and checklist[5] == -1:
            return 1900
        elif checklist[1] == -1 and checklist[2] == -1 and \
                checklist[3] == player and checklist[5] == player \
                and checklist[6] == -1:
            return 1900
        elif checklist[2] == -1 and checklist[3] == -1 and \
                checklist[5] == player and checklist[6] == player \
                and checklist[7] == -1:
            return 1900
        elif checklist[1] == -1 and checklist[2] == player and \
                checklist[3] == player and checklist[5] == -1 \
                and checklist[6] == -1:
            return 1900
        elif checklist[2] == -1 and checklist[3] == player and \
                checklist[5] == player and checklist[6] == -1 \
                and checklist[7] == -1:
            return 1900
        elif checklist[3] == -1 and checklist[5] == player and \
                checklist[6] == player and checklist[7] == -1 \
                and checklist[8] == -1:
            return 1900
        elif checklist[0] == -1 and checklist[1] == player and \
                checklist[2] == player and checklist[3] == -1 \
                and checklist[5] == -1:
            return 1600
        elif checklist[2] == -1 and checklist[3] == player and \
                checklist[6] == player and checklist[5] == -1 \
                and checklist[7] == -1:
            return 1600
        elif checklist[3] == -1 and checklist[5] == player and \
                checklist[7] == player and checklist[6] == -1 \
                and checklist[8] == -1:
            return 1600
        elif checklist[3] == -1 and checklist[5] == -1 and \
                checklist[7] == player and checklist[6] == player \
                and checklist[8] == -1:
            return 1600
        elif checklist[0] == -1 and checklist[1] == player and \
                checklist[2] == player and checklist[3] == -1 \
                and checklist[6] == -1:
            return 1600
        elif checklist[0] == -1 and checklist[1] == player and \
                checklist[2] == player and checklist[3] == -1 \
                and checklist[6] == -1:
            return 1600
        else:
            return 0

    @staticmethod
    def willbesleep3(player, enemy, checklist):
        """move this step get sleep 3 /xooo_"""
        if checklist[1] == enemy and checklist[2] == player and \
                checklist[3] == player and checklist[5] == -1 \
                and checklist[6] == -1:
            return 350
        elif checklist[2] == enemy and checklist[3] == player and \
                checklist[5] == player and checklist[6] == -1 \
                and checklist[7] == -1:
            return 350
        elif checklist[3] == enemy and checklist[5] == player and \
                checklist[6] == player and checklist[7] == -1 \
                and checklist[8] == -1:
            return 350
        elif checklist[0] == -1 and checklist[1] == -1 and \
                checklist[2] == player and checklist[3] == player \
                and checklist[5] == enemy:
            return 350
        elif checklist[1] == -1 and checklist[2] == -1 and \
                checklist[3] == player and checklist[5] == player \
                and checklist[6] == enemy:
            return 350
        elif checklist[2] == -1 and checklist[3] == -1 and \
                checklist[5] == player and checklist[6] == player \
                and checklist[7] == enemy:
            return 350
        elif checklist[0] == enemy and checklist[1] == -1 and \
                checklist[2] == player and checklist[3] == player \
                and checklist[5] == -1 and checklist[6] == enemy:
            return 300
        elif checklist[1] == enemy and checklist[2] == -1 and \
                checklist[3] == player and checklist[5] == player \
                and checklist[6] == -1 and checklist[7] == enemy:
            return 300
        elif checklist[2] == enemy and checklist[3] == -1 and \
                checklist[5] == player and checklist[6] == player \
                and checklist[7] == -1 and checklist[8] == enemy:
            return 300
        elif checklist[0] == enemy and checklist[1] == player and \
                checklist[2] == -1 and checklist[3] == player \
                and checklist[5] == -1 and checklist[6] == enemy:
            return 300
        elif checklist[1] == enemy and checklist[2] == player and \
                checklist[3] == -1 and checklist[5] == player \
                and checklist[6] == -1 and checklist[7] == enemy:
            return 300
        elif checklist[2] == enemy and checklist[3] == player and \
                checklist[5] == -1 and checklist[6] == player \
                and checklist[7] == -1 and checklist[8] == enemy:
            return 300
        elif checklist[0] == enemy and checklist[1] == player and \
                checklist[2] == -1 and checklist[3] == player \
                and checklist[5] == -1 and checklist[6] == enemy:
            return 300
        elif checklist[1] == enemy and checklist[2] == player and \
                checklist[3] == -1 and checklist[5] == player \
                and checklist[6] == -1 and checklist[7] == enemy:
            return 300
        elif checklist[3] == enemy and checklist[5] == -1 and \
                checklist[6] == player and checklist[7] == player \
                and checklist[8] == -1:
            return 300
        elif checklist[0] == enemy and checklist[1] == player and \
                checklist[2] == player and checklist[3] == -1 \
                and checklist[5] == -1:
            return 300
        elif checklist[2] == enemy and checklist[3] == player and \
                checklist[5] == -1 and checklist[6] == player \
                and checklist[7] == -1:
            return 300
        elif checklist[3] == enemy and checklist[5] == player and \
                checklist[6] == -1 and checklist[7] == player \
                and checklist[8] == -1:
            return 300
        elif checklist[0] == player and checklist[1] == player and \
                checklist[2] == -1 and checklist[3] == -1 \
                and checklist[5] == enemy:
            return 300
        elif checklist[2] == enemy and checklist[3] == player and \
                checklist[5] == -1 and checklist[6] == -1 \
                and checklist[7] == player:
            return 300
        elif checklist[3] == enemy and checklist[5] == player and \
                checklist[6] == -1 and checklist[7] == -1 \
                and checklist[8] == player:
            return 300
        elif checklist[0] == player and checklist[1] == -1 and \
                checklist[2] == -1 and checklist[3] == player \
                and checklist[5] == enemy:
            return 300
        elif checklist[1] == player and checklist[2] == -1 and \
                checklist[3] == -1 and checklist[5] == player \
                and checklist[6] == enemy:
            return 300
        elif checklist[3] == enemy and checklist[5] == -1 and \
                checklist[6] == -1 and checklist[7] == player \
                and checklist[8] == player:
            return 300
        elif checklist[0] == -1 and checklist[1] == player and \
                checklist[2] == player and checklist[3] == -1 \
                and checklist[5] == enemy:
            return 30
        elif checklist[2] == -1 and checklist[3] == player and \
                checklist[5] == -1 and checklist[6] == player \
                and checklist[7] == enemy:
            return 300
        elif checklist[3] == -1 and checklist[5] == player and \
                checklist[6] == -1 and checklist[7] == player \
                and checklist[8] == enemy:
            return 300
        elif checklist[0] == -1 and checklist[1] == player and \
                checklist[2] == -1 and checklist[3] == player \
                and checklist[5] == enemy:
            return 300
        elif checklist[1] == -1 and checklist[2] == player and \
                checklist[3] == -1 and checklist[5] == player \
                and checklist[6] == enemy:
            return 300
        elif checklist[3] == -1 and checklist[5] == -1 and \
                checklist[6] == player and checklist[7] == player \
                and checklist[8] == enemy:
            return 300
        elif checklist[0] == player and checklist[1] == -1 and \
                checklist[2] == player and checklist[3] == -1 \
                and checklist[5] == enemy:
            return 300
        elif checklist[1] == enemy and checklist[2] == player and \
                checklist[3] == -1 and checklist[5] == -1 \
                and checklist[6] == player:
            return 300
        elif checklist[2] == player and checklist[3] == -1 and \
                checklist[5]== -1 and checklist[6] == player \
                and checklist[7] == enemy:
            return 300
        elif checklist[3] == enemy and checklist[5] == -1 and \
                checklist[6] == player and checklist[7] == -1 \
                and checklist[8] == player:
            return 300
        else:
            return 0

    @staticmethod
    def willbealive2(player, enemy, checklist):
        """move this step get alive 2 /_oo_"""
        if checklist[1] == -1 and checklist[2] == -1 and \
                checklist[3] == player and checklist[5] == -1 \
                and checklist[6] == -1:
            return 99
        elif checklist[2] == -1 and checklist[3] == -1 and \
                checklist[5] == player and checklist[6] == -1 \
                and checklist[7] == -1:
            return 99
        elif checklist[0] == -1 and checklist[1] == -1 and \
                checklist[2] == -1 and checklist[3] == player \
                and checklist[5] == -1 and checklist[6] == enemy:
            return 99
        elif checklist[1] == -1 and checklist[2] == -1 and \
                checklist[3] == -1 and checklist[5] == player \
                and checklist[6] == -1 and checklist[7] == enemy:
            return 99
        elif checklist[1] == enemy and checklist[2] == -1 and \
                checklist[3] == player and checklist[5] == -1 \
                and checklist[6] == -1 and checklist[7] == -1:
            return 99
        elif checklist[2] == enemy and checklist[3] == -1 and \
                checklist[5] == player and checklist[6] == -1 \
                and checklist[7] == -1 and checklist[8] == -1:
            return 99
        else:
            return 0

    @staticmethod
    def willbesleep2(player, enemy, checklist):
        """move this step get sleep 2 /_oox"""
        if checklist[2] == enemy and checklist[3] == player and \
                checklist[5] == -1 and checklist[6] == -1 \
                and checklist[7] == -1:
            return 5
        elif checklist[3] == enemy and checklist[5] == player and \
                checklist[6] == -1 and checklist[7] == -1 \
                and checklist[8] == -1:
            return 5
        elif checklist[0] == -1 and checklist[1] == -1 and \
                checklist[2] == -1 and checklist[3] == player \
                and checklist[5] == enemy:
            return 5
        elif checklist[1] == -1 and checklist[2] == -1 and \
                checklist[3] == -1 and checklist[5] == player \
                and checklist[6] == enemy:
            return 5
        elif checklist[1] == enemy and checklist[2] == -1 and \
                checklist[3] == player and checklist[5] == -1 \
                and checklist[6] == -1 and checklist[7] == enemy:
            return 5
        elif checklist[2] == enemy and checklist[3] == -1 and \
                checklist[5] == player and checklist[6] == -1 \
                and checklist[7] == -1 and checklist[8] == enemy:
            return 5
        elif checklist[0] == enemy and checklist[1] == -1 and \
                checklist[2] == player and checklist[3] == -1 \
                and checklist[5] == -1 and checklist[6] == enemy:
            return 5
        elif checklist[2] == enemy and checklist[3] == -1 and \
                checklist[5] == -1 and checklist[6] == player \
                and checklist[7] == -1 and checklist[8] == enemy:
            return 5
        elif checklist[0] == enemy and checklist[1] == -1 and \
                checklist[2] == -1 and checklist[3] == player \
                and checklist[5] == -1 and checklist[6] == enemy:
            return 5
        elif checklist[1] == enemy and checklist[2] == -1 and \
                checklist[3] == -1 and checklist[5] == player \
                and checklist[6] == -1 and checklist[7] == enemy:
            return 5
        elif checklist[0] == -1 and checklist[1] == player and \
                checklist[2] == -1 and checklist[3] == -1 \
                and checklist[5] == enemy:
            return 5
        elif checklist[3] == -1 and checklist[5] == -1 and \
                checklist[6] == -1 and checklist[7] == player \
                and checklist[8] == enemy:
            return 5
        elif checklist[0] == -1 and checklist[1] == -1 and \
                checklist[2] == player and checklist[3] == -1 \
                and checklist[5] == enemy:
            return 5
        elif checklist[2] == -1 and checklist[3] == -1 and \
                checklist[5] == -1 and checklist[6] == player \
                and checklist[7] == enemy:
            return 5
        elif checklist[1] == enemy and checklist[2] == player and \
                checklist[3] == -1 and checklist[5] == -1 \
                and checklist[6] == -1:
            return 5
        elif checklist[3] == enemy and checklist[5] == -1 and \
                checklist[6] == player and checklist[7] == -1 \
                and checklist[8] == -1:
            return 5
        elif checklist[0] == enemy and checklist[1] == player and \
                checklist[2] == -1 and checklist[3] == -1 \
                and checklist[5] == -1:
            return 5
        elif checklist[3] == enemy and checklist[5] == -1 and \
                checklist[6] == -1 and checklist[7] == player \
                and checklist[8] == -1:
            return 5
        else:
            return 0
