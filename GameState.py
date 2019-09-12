class GameState:
    board = [
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 0, 1, 2, 2, 2],
        [2, 2, 2, 1, 0, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2],
    ]
    turn = 1
    choices = [
        [2, 2], [2, 3], [2, 4], [2, 5],
        [3, 2], [3, 5],
        [4, 2], [4, 5],
        [5, 2], [5, 3], [5, 4], [5, 5]
    ]
    moves = [
        [
            [2, 4], [3, 5], [4, 2], [5, 3]
        ],
        [
            [2, 3], [3, 2], [4, 5], [5, 4]
        ]
    ]
    pieces = [2, 2]

    def putpiece(self, row, col, turn):
        self.choices.remove([row, col])
        self.board[row][col] = turn
        self.capture(self, row, col, turn)
        self.updatelegalmoves(self, row, col)

    def capture(self, row, col, turn):
        # Mengiterasi 8 arah yang perlu dicari
        for y in range(-1,2):
            for x in range(-1,2):
                distance = 1
                while (0 <= row + y*distance < 8) & (0 <= col + x*distance < 8):
                    if self.board[row+y*distance][col+x*distance] == turn:
                        # Kembali ke keping yang baru sambil mengganti warna keping diantaranya
                        while distance != 0:
                            self.board[row+y*distance][col+x*distance] = turn
                            distance -= 1
                        break
                    elif self.board[row+y*distance][col+x*distance] == (1 - turn):
                        distance += 1
                    else: break

    def islegal(self, row, col, turn):
        for y in range(-1,2):
            for x in range(-1,2):
                distance = 1
                while (0 <= row + y*distance < 8) & (0 <= col + x*distance < 8): #didalem papan
                    if (self.board[row + y * distance][col + x * distance] == turn) & ((x != 0) | (y != 0)):
                        #nemu keping yang warnanya sama
                        if distance > 1: #tidak tepat di sebelahnya, berarti legal
                            return True
                        else: # tepat sebelahnya, lanjut arah selanjutnya
                            break
                    elif self.board[row + y * distance][col + x * distance] == (1 - turn):
                        # nemu keping yang warnanya beda, ngelihat ke yang lebih jauh lagi
                        distance += 1
                    else:
                        # nemu petak kosong, lanjut arah selanjutnya
                        break
        return False

    def updatelegalmoves(self, row, col):
        # Menambahkan petak disekitar kotak yang baru diisi
        self.moves[0].clear()
        self.moves[1].clear()
        for y in range(-1,2):
            for x in range(-1,2):
                if (0 <= row + y < 8) & (0 <= col + x < 8):
                    if ([row+y, col+x] not in self.choices) & ((x != 0)|(y != 0)) & (self.board[row+y][col+x] == 2):
                        self.choices.append([row+y, col+x])
        # Menambahkan petak yang valid ke masing-masing list
        for choice in self.choices:
            for turn in range(0,2):
                if self.islegal(self, choice[0], choice[1], turn):
                    self.moves[turn].append(choice)