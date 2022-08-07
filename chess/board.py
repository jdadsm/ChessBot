import pygame 
from .constants import BLACK, GREY,ROWS, SQUARE_SIZE,WHITE,COLUMNS,pieces_initial_pos
from .pieces import Pieces
from copy import deepcopy

class Board:
    def __init__(self):
        self.board = []
        self.white_threat_board = []
        self.black_threat_board = []
        self.en_passant_piece = [] # piece that can be en passanted this turn
        self.previous_en_passant_piece = [] # piece that was able to be en passanted in the previous turn
        self.white_king = self.black_king = 1
        self.white_queen = self.black_queen = 1
        self.white_rook = self.black_rook = 2
        self.white_knight = self.black_knight = 2
        self.white_bishop_white = self.black_bishop_white = 1
        self.white_bishop_black = self.black_bishop_black = 1
        self.white_pawns = self.black_pawns = 8
        self.create_board()
        self.create_threat_board()
        
    def create_threat_board(self):
        for row in range(ROWS):
            self.black_threat_board.append([])
            self.white_threat_board.append([])
            for col in range(COLUMNS):
                self.white_threat_board[row].append(0)
                self.black_threat_board[row].append(0)
        self.update_threat_board()
    
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLUMNS):
                if(row==0):
                    self.board[row].append(Pieces(row,col,BLACK,pieces_initial_pos[col]))
                elif(row==7):
                    self.board[row].append(Pieces(row,col,WHITE,pieces_initial_pos[col]))
                elif(row==1):
                    self.board[row].append(Pieces(row,col,BLACK,"pawn"))
                elif(row==6):
                    self.board[row].append(Pieces(row,col,WHITE,"pawn"))
                else:
                    self.board[row].append(0)
                    
    def draw_squares(self, win):
        win.fill(GREY)
        for row in range(ROWS):
            for col in range(row % 2, COLUMNS, 2):
                pygame.draw.rect(win, WHITE, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
    def move(self, piece, row, col):
        if(piece != 0):
            if(piece.type == "pawn"):
                self.check_en_passant(piece,row,col)
            self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
            piece.move(row, col)
            
    def update_threat_board(self):
        for x in range(8):
            for y in range(8):
                self.black_threat_board[x][y] = 0
                self.white_threat_board[x][y] = 0
        for r in range(8):
            for l in range(8):
                piece = self.get_piece(r,l)
                if(piece == 0):
                    continue 
                color = piece.color   
                moves = self.get_threat_moves(piece)
                if(color == WHITE):
                    for (row,col) in moves:
                        self.white_threat_board[row][col] += 1
                else:
                    for (row,col) in moves:
                        self.black_threat_board[row][col] += 1
        print("\nWhite Threat Board")
        for x in range(8):
            s = ""
            for y in range(8):
                s+=(str(self.white_threat_board[x][y])+" ")
            print(s)
        print("\nBlack Threat Board")
        for x in range(8):
            s = ""
            for y in range(8):
                s+=(str(self.black_threat_board[x][y])+" ")
            print(s)
        
    def get_threat_moves(self, piece):
        moves = []
        type = piece.type
        if type == "pawn":
            moves = self.threat_moves_pawn(piece)
        elif type == "rook":
            moves = self.threat_moves_rook(piece)
        elif type == "knight":
            moves = self.threat_moves_knight(piece)
        elif type == "bishop":
            moves = self.threat_moves_bishop(piece)
        elif type == "queen":
            moves = self.threat_moves_queen(piece)
        elif type == "king":
            moves = self.threat_moves_king(piece)
        else:
            print("Error:get_threat_moves")
        return moves
    
    def threat_moves_king(self,piece):
        moves = []
        row = piece.row
        col = piece.col
        if row+1>=0 and row+1<=7 and col+1>=0 and col+1<=7:
            moves.append((row+1,col+1))
        if row+1>=0 and row+1<=7 and col-1>=0 and col-1<=7:
            moves.append((row+1,col-1))
        if row-1>=0 and row-1<=7 and col+1>=0 and col+1<=7:
            moves.append((row-1,col+1))
        if row-1>=0 and row-1<=7 and col-1>=0 and col-1<=7:
            moves.append((row-1,col-1))
        if col+1>=0 and col+1<=7:
            moves.append((row,col+1))
        if col-1>=0 and col-1<=7:
            moves.append((row,col-1))
        if row+1>=0 and row+1<=7:
            moves.append((row+1,col))
        if row-1>=0 and row-1<=7:
            moves.append((row-1,col))
        return moves
    
    def threat_moves_rook(self,piece):
        moves = []
        row = piece.row
        col = piece.col
        color = piece.color
        for i in range(1,8):
            if row+i>=0 and row+i<=7:
                if self.get_piece(row+i,col) == 0:
                    moves.append((row+i,col))
                else:
                    moves.append((row+i,col))
            else:
                break
            if self.get_piece(row+i,col) != 0:
                if not (self.get_piece(row+i,col).type == "king" and self.get_piece(row+i,col).color != color):
                    break
        for i in range(1,8):
            if row-i>=0 and row-i<=7:
                if self.get_piece(row-i,col) == 0:
                    moves.append((row-i,col))
                else:
                    moves.append((row-i,col))
            else:
                break
            if self.get_piece(row-i,col) != 0:
                if not (self.get_piece(row-i,col).type == "king" and self.get_piece(row-i,col).color != color):
                    break
        for i in range(1,8):
            if col+i>=0 and col+i<=7:
                if self.get_piece(row,col+i) == 0:
                    moves.append((row,col+i))
                else:
                    moves.append((row,col+i))
            else:
                break
            if self.get_piece(row,col+i) != 0:
                if not (self.get_piece(row,col+i).type == "king" and self.get_piece(row,col+i).color != color):
                    break
        for i in range(1,8):
            if col-i>=0 and col-i<=7:
                if self.get_piece(row,col-i) == 0:
                    moves.append((row,col-i))
                else:
                        moves.append((row,col-i))
            else:
                break
            if self.get_piece(row,col-i) != 0:
                if not (self.get_piece(row,col-i).type == "king" and self.get_piece(row,col-i).color != color):
                    break
        return moves
    
    def threat_moves_bishop(self,piece):
        moves = []
        row = piece.row
        col = piece.col
        color = piece.color
        for i in range(1,8):
            if row+i>=0 and row+i<=7 and col+i>=0 and col+i<=7:
                if self.get_piece(row+i,col+i) == 0:
                    moves.append((row+i,col+i))
                else:
                    moves.append((row+i,col+i))
            else:
                break
            if self.get_piece(row+i,col+i) != 0:
                if not (self.get_piece(row+i,col+i).type == "king" and self.get_piece(row+i,col+i).color != color):
                    break
        for i in range(1,8):
            if row+i>=0 and row+i<=7 and col-i>=0 and col-i<=7:
                if self.get_piece(row+i,col-i) == 0:
                    moves.append((row+i,col-i))
                else:
                    moves.append((row+i,col-i))
            else:
                break
            if self.get_piece(row+i,col-i) != 0:
                if not (self.get_piece(row+i,col-i).type == "king" and self.get_piece(row+i,col-i).color != color):
                    break
        for i in range(1,8):
            if row-i>=0 and row-i<=7 and col+i>=0 and col+i<=7:
                if self.get_piece(row-i,col+i) == 0:
                    moves.append((row-i,col+i))
                else:
                    moves.append((row-i,col+i))
            else:
                break
            if self.get_piece(row-i,col+i) != 0:
                if not (self.get_piece(row-i,col+i).type == "king" and self.get_piece(row-i,col+i).color != color):
                    break
        for i in range(1,8):
            if row-i>=0 and row-i<=7 and col-i>=0 and col-i<=7:
                if self.get_piece(row-i,col-i) == 0:
                    moves.append((row-i,col-i))
                else:
                    moves.append((row-i,col-i))
            else:
                break
            if self.get_piece(row-i,col-i) != 0:
                if not (self.get_piece(row-i,col-i).type == "king" and self.get_piece(row-i,col-i).color != color):
                    break
        return moves
    
    def threat_moves_knight(self,piece):
        moves = []
        row = piece.row
        col = piece.col
        if row-1>=0 and row-1<=7 and col-2>=0 and col-2<=7:
            moves.append((row-1,col-2))
        if row-1>=0 and row-1<=7 and col+2>=0 and col+2<=7:
            moves.append((row-1,col+2))
        if row+1>=0 and row+1<=7 and col-2>=0 and col-2<=7:
            moves.append((row+1,col-2))
        if row+1>=0 and row+1<=7 and col+2>=0 and col+2<=7:
            moves.append((row+1,col+2))
        if row-2>=0 and row-2<=7 and col-1>=0 and col-1<=7:
            moves.append((row-2,col-1))
        if row-2>=0 and row-2<=7 and col+1>=0 and col+1<=7:
            moves.append((row-2,col+1))
        if row+2>=0 and row+2<=7 and col-1>=0 and col-1<=7:
            moves.append((row+2,col-1))
        if row+2>=0 and row+2<=7 and col+1>=0 and col+1<=7:
            moves.append((row+2,col+1))
        return moves
    
    def threat_moves_queen(self,piece):
        return list(set(self.threat_moves_bishop(piece) + self.threat_moves_rook(piece)))
    
    def threat_moves_pawn(self,piece):
        moves = []
        row = piece.row
        col = piece.col
        color = piece.color
        if(color == WHITE):
            if(row == 0):
                return moves
            else:
                if(col == 0):
                    moves.append((row-1,col+1))
                elif(col == 7):
                    moves.append((row-1,col-1))
                else:
                    moves.append((row-1,col-1))
                    moves.append((row-1,col+1))
        else:
            if(row == 7):
                    return moves
            else:
                if(col == 0):
                    moves.append((row+1,col+1))
                elif(col == 7):
                    moves.append((row+1,col-1))
                else:
                    moves.append((row+1,col-1))
                    moves.append((row+1,col+1))
        
        return moves
            
    def check_en_passant(self,piece,row,col):
        if(piece.color == WHITE):
            if(piece.row == row+2 and piece.col == col):
                self.en_passant_piece = [(row,col)]
            elif((row+1,col) in self.previous_en_passant_piece):
                self.board[row+1][col] = 0
        else:
            if(piece.row == row-2 and piece.col == col):
                self.en_passant_piece = [(row,col)]
            elif((row-1,col) in self.previous_en_passant_piece):
                self.board[row-1][col] = 0
        
    def capture(self, piece, row, col):
        captured_piece = self.get_piece(row,col)
        if(captured_piece == 0):
            print("Error:capture()")
        if(piece != 0):
            self.board[captured_piece.row][captured_piece.col] = 0
            self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
            piece.move(row, col)
        else:
            pass
          
    def get_piece(self, row, col):
        return self.board[row][col]
    
    def get_valid_moves(self, piece):
        moves = []
        type = piece.type
        if type == "pawn":
            moves = self.moves_pawn(piece)
        elif type == "rook":
            moves = self.moves_rook(piece)
        elif type == "knight":
            moves = self.moves_knight(piece)
        elif type == "bishop":
            moves = self.moves_bishop(piece)
        elif type == "queen":
            moves = self.moves_queen(piece)
        elif type == "king":
            moves = self.moves_king(piece)
        else:
            print("Error:get_valid_moves")
            
        print("Valid moves:")
        print(moves)
        #print(self.board)
        return moves
    
    def moves_king(self,piece):
        moves = []
        row = piece.row
        col = piece.col
        color = piece.color
        if row+1>=0 and row+1<=7 and col+1>=0 and col+1<=7:
            if (color == WHITE and self.black_threat_board[row+1][col+1] == 0) or (color == BLACK and self.white_threat_board[row+1][col+1] == 0):
                if self.get_piece(row+1,col+1) == 0:
                    moves.append((row+1,col+1))
                elif self.get_piece(row+1,col+1).color != color:
                    moves.append((row+1,col+1))
        if row+1>=0 and row+1<=7 and col-1>=0 and col-1<=7:
            if (color == WHITE and self.black_threat_board[row+1][col-1] == 0) or (color == BLACK and self.white_threat_board[row+1][col-1] == 0):
                if self.get_piece(row+1,col-1) == 0:
                    moves.append((row+1,col-1))
                elif self.get_piece(row+1,col-1).color != color:
                    moves.append((row+1,col-1))
        if row-1>=0 and row-1<=7 and col+1>=0 and col+1<=7:
            if (color == WHITE and self.black_threat_board[row-1][col+1] == 0) or (color == BLACK and self.white_threat_board[row-1][col+1] == 0):
                if self.get_piece(row-1,col+1) == 0:
                    moves.append((row-1,col+1))
                elif self.get_piece(row-1,col+1).color != color:
                    moves.append((row-1,col+1))
        if row-1>=0 and row-1<=7 and col-1>=0 and col-1<=7:
            if (color == WHITE and self.black_threat_board[row-1][col-1] == 0) or (color == BLACK and self.white_threat_board[row-1][col-1] == 0):
                if self.get_piece(row-1,col-1) == 0:
                    moves.append((row-1,col-1))
                elif self.get_piece(row-1,col-1).color != color:
                    moves.append((row-1,col-1))
        if col+1>=0 and col+1<=7:
            if (color == WHITE and self.black_threat_board[row][col+1] == 0) or (color == BLACK and self.white_threat_board[row][col+1] == 0):
                if self.get_piece(row,col+1) == 0:
                    moves.append((row,col+1))
                elif self.get_piece(row,col+1).color != color:
                    moves.append((row,col+1))
        if col-1>=0 and col-1<=7:
            if (color == WHITE and self.black_threat_board[row][col-1] == 0) or (color == BLACK and self.white_threat_board[row][col-1] == 0):
                if self.get_piece(row,col-1) == 0:
                    moves.append((row,col-1))
                elif self.get_piece(row,col-1).color != color:
                    moves.append((row,col-1))
        if row+1>=0 and row+1<=7:
            if (color == WHITE and self.black_threat_board[row+1][col] == 0) or (color == BLACK and self.white_threat_board[row+1][col] == 0):
                if self.get_piece(row+1,col) == 0:
                    moves.append((row+1,col))
                elif self.get_piece(row+1,col).color != color:
                    moves.append((row+1,col))
        if row-1>=0 and row-1<=7:
            if (color == WHITE and self.black_threat_board[row-1][col] == 0) or (color == BLACK and self.white_threat_board[row-1][col] == 0):
                if self.get_piece(row-1,col) == 0:
                    moves.append((row-1,col))
                elif self.get_piece(row-1,col).color != color:
                    moves.append((row-1,col))
        return moves
    
    def moves_queen(self,piece):
        return self.moves_bishop(piece) + self.moves_rook(piece)
    
    def moves_rook(self,piece):
        moves = []
        row = piece.row
        col = piece.col
        color = piece.color
        for i in range(1,8):
            if row+i>=0 and row+i<=7:
                if self.get_piece(row+i,col) == 0:
                    moves.append((row+i,col))
                else:
                    if self.get_piece(row+i,col).color != color:
                        moves.append((row+i,col))
                    else:
                        break
            else:
                break
            if self.get_piece(row+i,col) != 0:
                break
        for i in range(1,8):
            if row-i>=0 and row-i<=7:
                if self.get_piece(row-i,col) == 0:
                    moves.append((row-i,col))
                else:
                    if self.get_piece(row-i,col).color != color:
                        moves.append((row-i,col))
                    else:
                        break
            else:
                break
            if self.get_piece(row-i,col) != 0:
                break
        for i in range(1,8):
            if col+i>=0 and col+i<=7:
                if self.get_piece(row,col+i) == 0:
                    moves.append((row,col+i))
                else:
                    if self.get_piece(row,col+i).color != color:
                        moves.append((row,col+i))
                    else:
                        break
            else:
                break
            if self.get_piece(row,col+i) != 0:
                break
        for i in range(1,8):
            if col-i>=0 and col-i<=7:
                if self.get_piece(row,col-i) == 0:
                    moves.append((row,col-i))
                else:
                    if self.get_piece(row,col-i).color != color:
                        moves.append((row,col-i))
                    else:
                        break
            else:
                break
            if self.get_piece(row,col-i) != 0:
                break
        return moves
    
    def moves_bishop(self,piece):
        moves = []
        row = piece.row
        col = piece.col
        color = piece.color
        for i in range(1,8):
            if row+i>=0 and row+i<=7 and col+i>=0 and col+i<=7:
                if self.get_piece(row+i,col+i) == 0:
                    moves.append((row+i,col+i))
                else:
                    if self.get_piece(row+i,col+i).color != color:
                        moves.append((row+i,col+i))
                    else:
                        break
            else:
                break
            if self.get_piece(row+i,col+i) != 0:
                break
        for i in range(1,8):
            if row+i>=0 and row+i<=7 and col-i>=0 and col-i<=7:
                if self.get_piece(row+i,col-i) == 0:
                    moves.append((row+i,col-i))
                else:
                    if self.get_piece(row+i,col-i).color != color:
                        moves.append((row+i,col-i))
                    else:
                        break
            else:
                break
            if self.get_piece(row+i,col-i) != 0:
                break
        for i in range(1,8):
            if row-i>=0 and row-i<=7 and col+i>=0 and col+i<=7:
                if self.get_piece(row-i,col+i) == 0:
                    moves.append((row-i,col+i))
                else:
                    if self.get_piece(row-i,col+i).color != color:
                        moves.append((row-i,col+i))
                    else:
                        break
            else:
                break
            if self.get_piece(row-i,col+i) != 0:
                break
        for i in range(1,8):
            if row-i>=0 and row-i<=7 and col-i>=0 and col-i<=7:
                if self.get_piece(row-i,col-i) == 0:
                    moves.append((row-i,col-i))
                else:
                    if self.get_piece(row-i,col-i).color != color:
                        moves.append((row-i,col-i))
                    else:
                        break
            else:
                break
            if self.get_piece(row-i,col-i) != 0:
                break
        return moves
    
    def moves_knight(self,piece):
        moves = []
        row = piece.row
        col = piece.col
        color = piece.color
        if row-1>=0 and row-1<=7 and col-2>=0 and col-2<=7:
            moves.append((row-1,col-2))
        if row-1>=0 and row-1<=7 and col+2>=0 and col+2<=7:
            moves.append((row-1,col+2))
        if row+1>=0 and row+1<=7 and col-2>=0 and col-2<=7:
            moves.append((row+1,col-2))
        if row+1>=0 and row+1<=7 and col+2>=0 and col+2<=7:
            moves.append((row+1,col+2))
        if row-2>=0 and row-2<=7 and col-1>=0 and col-1<=7:
            moves.append((row-2,col-1))
        if row-2>=0 and row-2<=7 and col+1>=0 and col+1<=7:
            moves.append((row-2,col+1))
        if row+2>=0 and row+2<=7 and col-1>=0 and col-1<=7:
            moves.append((row+2,col-1))
        if row+2>=0 and row+2<=7 and col+1>=0 and col+1<=7:
            moves.append((row+2,col+1))
        i = 0
        for (temp_row,temp_col) in moves:
            print((temp_row,temp_col))
            if (self.get_piece(temp_row,temp_col) != 0) and (self.get_piece(temp_row,temp_col).color == color):
                print((temp_row,temp_col))
                moves = moves[:i] + moves[i+1:]
            else:
                i = i + 1
        return moves
    
    def moves_pawn(self, piece):
        moves = []
        row = piece.row
        col = piece.col
        color = piece.color
        if(color == WHITE):
            if(self.get_piece(row-1,col) == 0):
                moves.append((row-1,col))
                if(self.get_piece(row-2,col) == 0):
                    if(row == 6):
                        moves.append((row-2,col))
            if col != 0 and col != 7:
                if(self.get_piece(row-1,col-1) != 0 and self.get_piece(row-1,col-1).color != color):
                    moves.append((row-1,col-1))
                if(self.get_piece(row-1,col+1) != 0 and self.get_piece(row-1,col+1).color != color):
                    moves.append((row-1,col+1))  
                if(self.get_piece(row,col-1) != 0 and self.get_piece(row,col-1).color != color):
                    if((row,col-1) in self.previous_en_passant_piece):
                        moves.append((row-1,col-1))
                if(self.get_piece(row,col+1) != 0 and self.get_piece(row,col+1).color != color):
                    if((row,col+1) in self.previous_en_passant_piece):
                        moves.append((row-1,col+1)) 
            if col == 0:
                if(self.get_piece(row-1,col+1) != 0 and self.get_piece(row-1,col+1).color != color):
                    moves.append((row-1,col+1))
                if(self.get_piece(row,col+1) != 0 and self.get_piece(row,col+1).color != color):
                    if((row,col+1) in self.previous_en_passant_piece):
                        moves.append((row-1,col+1))
            if col == 7:
                if(self.get_piece(row-1,col-1) != 0 and self.get_piece(row-1,col-1).color != color):
                    moves.append((row-1,col-1))
                if(self.get_piece(row,col-1) != 0 and self.get_piece(row,col-1).color != color):
                    if((row,col-1) in self.previous_en_passant_piece):
                        moves.append((row-1,col-1))
        else:
            if(self.get_piece(row+1,col) == 0):
                moves.append((row+1,col))
                if(self.get_piece(row+2,col) == 0):
                    if(row == 1):
                        moves.append((row+2,col))
            if col != 0 and col != 7:
                if(self.get_piece(row+1,col-1) != 0 and self.get_piece(row+1,col-1).color != color):
                    moves.append((row+1,col-1))
                if(self.get_piece(row+1,col+1) != 0 and self.get_piece(row+1,col+1).color != color):
                    moves.append((row+1,col+1)) 
                if(self.get_piece(row,col-1) != 0 and self.get_piece(row,col-1).color != color):
                    if((row,col-1) in self.previous_en_passant_piece):
                        moves.append((row+1,col-1))
                if(self.get_piece(row,col+1) != 0 and self.get_piece(row,col+1).color != color):
                    if((row,col+1) in self.previous_en_passant_piece):
                        moves.append((row+1,col+1)) 
            if col == 0:
                if(self.get_piece(row+1,col+1) != 0 and self.get_piece(row+1,col+1).color != color):
                    moves.append((row+1,col+1))
                if(self.get_piece(row,col+1) != 0 and self.get_piece(row,col+1).color != color):
                    if((row,col+1) in self.previous_en_passant_piece):
                        moves.append((row+1,col+1))
            if col == 7:
                if(self.get_piece(row+1,col-1) != 0 and self.get_piece(row+1,col-1).color != color):
                    moves.append((row+1,col-1))
                if(self.get_piece(row,col-1) != 0 and self.get_piece(row,col-1).color != color):
                    if((row,col-1) in self.previous_en_passant_piece):
                        moves.append((row+1,col-1))
        return moves
                    
    def draw(self,win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLUMNS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)