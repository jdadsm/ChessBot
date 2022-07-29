import pygame 
from .constants import BLACK, GREY,ROWS, SQUARE_SIZE,WHITE,COLUMNS,pieces_initial_pos
from .pieces import Pieces

class Board:
    def __init__(self):
        self.board = []
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
            pass
        elif type == "knight":
            pass
        elif type == "bishop":
            pass
        elif type == "queen":
            pass
        elif type == "king":
            pass
        else:
            print("Error:get_valid_moves")
            
        print("Valid moves:")
        print(moves)
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
                    
    def draw(self,win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLUMNS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)