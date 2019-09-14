class GameState:
    def __init__(self, orig=None):
        if orig is None:
            self.board = [
                [2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 0, 1, 2, 2, 2],
                [2, 2, 2, 1, 0, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2],
            ]
            self.turn = 1
            self.choices = [
                [2, 2], [2, 3], [2, 4], [2, 5],
                [3, 2], [3, 5],
                [4, 2], [4, 5],
                [5, 2], [5, 3], [5, 4], [5, 5]
            ]
            self.moves = [
                [
                    [2, 4], [3, 5], [4, 2], [5, 3]
                ],
                [
                    [2, 3], [3, 2], [4, 5], [5, 4]
                ]
            ]
            self.pieces = [2, 2]
        else:
            self.board = orig.board
            self.turn = orig.turn
            self.choices = orig.choices
            self.moves = orig.moves
            self.pieces = orig.pieces

    def putpiece(self, row, col):
        self.choices.remove([row, col])
        self.board[row][col] = self.turn
        self.pieces[self.turn] += 1
        self.capture(row, col)
        self.updatelegalmoves(row, col)

    def capture(self, row, col):
        # Mengiterasi 8 arah yang perlu dicari
        for y in range(-1,2):
            for x in range(-1,2):
                distance = 1
                while (0 <= row + y*distance < 8) & (0 <= col + x*distance < 8):
                    if self.board[row+y*distance][col+x*distance] == self.turn:
                        # Kembali ke keping yang baru sambil mengganti warna keping diantaranya
                        while distance != 0:
                            if self.board[row+y*distance][col+x*distance] == 1 - self.turn:
                                self.pieces[self.turn] += 1
                                self.pieces[1 - self.turn] -= 1
                            self.board[row+y*distance][col+x*distance] = self.turn
                            distance -= 1
                        break
                    elif self.board[row+y*distance][col+x*distance] == (1 - self.turn):
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
                if self.islegal(choice[0], choice[1], turn):
                    self.moves[turn].append(choice)

    def count(self, color):
        colorcount = 0

        for row in self.board:
            for square in row:
                if (square == int(color)):
                    colorcount += 1
        
        return colorcount