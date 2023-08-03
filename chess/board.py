import pygame 
from .constants import BLACK, GREY,ROWS, SQUARE_SIZE,WHITE,COLUMNS,pieces_initial_pos
from .pieces import Pieces

class Board:
    def __init__(self):
        self.board = []
        self.white_threat_board = []
        self.black_threat_board = []
        self.white_king_coords = (7,4)
        self.black_king_coords = (0,4)
        self.en_passant_piece = [] # piece that can be en passanted this turn
        self.previous_en_passant_piece = [] # piece that was able to be en passanted in the previous turn
        self.simulation_captured_piece = None
        self.black_can_castle_qs = True # False if black king or queenside black rook has moved 
        self.black_can_castle_ks = True # False if black king or kingside black rook has moved
        self.white_can_castle_qs = True # False if white king or queenside white rook has moved
        self.white_can_castle_ks = True # False if white king or kingside white rook has moved
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
            if(piece.type == "king"):
                if(piece.color == WHITE):
                    self.white_king_coords = (row,col)
                    if self.white_can_castle_qs and row == 7 and col == 2:
                        qs_white_rook = self.get_piece(7,0)
                        self.move(qs_white_rook,7,3)
                    elif self.white_can_castle_ks and row == 7 and col == 6:
                        ks_white_rook = self.get_piece(7,7)
                        self.move(ks_white_rook,7,5)
                else:
                    self.black_king_coords = (row,col)
                    if self.black_can_castle_qs and row == 0 and col == 2:
                        qs_black_rook = self.get_piece(0,0)
                        self.move(qs_black_rook,0,3)
                    elif self.black_can_castle_ks and row == 0 and col == 6:
                        ks_black_rook = self.get_piece(0,7)
                        self.move(ks_black_rook,0,5)
            
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
        """
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
        print("\nBoard")
        for x in range(8):
            s = ""
            for y in range(8):
                s+=(str(self.board[x][y])+",")
            print(s)
        """   
        
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
            if(piece.type == "king"):
                if(piece.color == WHITE):
                    self.white_king_coords = (row,col)
                else:
                    self.black_king_coords = (row,col)
        else:
            pass
          
    def get_piece(self, row, col):
        return self.board[row][col]
    
    def get_valid_moves(self, piece:Pieces):
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
            moves.extend(self.get_castle_moves(piece.color))
        else:
            print("Error:get_valid_moves")
        
        pre_check_moves = list(moves)
        if piece.type != "king":
            #print("Moves:",pre_check_moves)
            for move in pre_check_moves:
                if self.verify_move_for_checks_and_pins(move,piece):
                    moves.remove(move)
                    
        #print("En passant:",self.en_passant_piece)
        #print("Previous en passant:",self.previous_en_passant_piece)
        
        print("Valid moves:",moves)
        #print(self.board)
        return moves
    
    def get_castle_moves(self,color):
        moves = []
        if color == WHITE:
            if self.board[7][1] == 0 and self.board[7][2] == 0 and self.board[7][3] == 0 and self.black_threat_board[7][2] == 0 and self.black_threat_board[7][3] == 0 and self.white_can_castle_qs:
                moves.append((7,2))
            if self.board[7][5] == 0 and self.board[7][6] == 0 and self.black_threat_board[7][5] == 0 and self.black_threat_board[7][6] == 0 and self.white_can_castle_ks:
                moves.append((7,6))
        else:
            if self.board[0][1] == 0 and self.board[0][2] == 0 and self.board[0][3] == 0 and self.white_threat_board[0][2] == 0 and self.white_threat_board[0][3] == 0 and self.black_can_castle_qs:
                moves.append((0,2))
            if self.board[0][5] == 0 and self.board[0][6] == 0 and self.white_threat_board[0][5] == 0 and self.white_threat_board[0][6] == 0 and self.black_can_castle_ks:
                moves.append((0,6))
        return moves
    
    # returns true if the move is not legal
    def verify_move_for_checks_and_pins(self,move,piece:Pieces): 
        illegal_move = False
        
        #print("Move:",move)
        #print("Moving "+ piece.type + " in " + str(piece.row) + "," + str(piece.col) +" to "+ str(move[0]) + "," + str(move[1]))
        
        original_pos = (piece.row,piece.col)
        self.simulate_move(piece,move[0],move[1])
        self.update_threat_board()
        if piece.color == WHITE:
            if self.black_threat_board[self.white_king_coords[0]][self.white_king_coords[1]] != 0:
                illegal_move = True
        else:
            if self.white_threat_board[self.black_king_coords[0]][self.black_king_coords[1]] != 0:
                illegal_move = True
        #print("Moving "+ piece.type + " in " + str(piece.row) + "," + str(piece.col) +" back to "+ str(original_pos[0]) + "," + str(original_pos[1]))
        self.undo_simulation_move(piece,original_pos[0],original_pos[1])
        self.update_threat_board()
        
        return illegal_move
    
    def simulate_move(self, piece, row, col):
        if(piece != 0):
                
            self.simulation_init_pos = (piece.row,piece.col)
            if self.board[row][col] != 0:
                self.simulation_captured_piece = self.board[row][col]
                self.board[row][col] = 0
                
            self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
            piece.move(row, col)
            if(piece.type == "king"):
                if(piece.color == WHITE):
                    self.white_king_coords = (row,col)
                else:
                    self.black_king_coords = (row,col)
        #print("Simulation - Captured piece: ",self.simulation_captured_piece)
        #print("Simulation - piece: ",piece)
        #print("Simulation - moved to: " + str(row) + "," + str(col))
    
    def undo_simulation_move(self, piece, row, col):
        if(piece != 0):
            
            self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
            if self.simulation_captured_piece:
                self.board[self.simulation_captured_piece.row][self.simulation_captured_piece.col] = self.simulation_captured_piece
                self.simulation_captured_piece = None
            piece.move(row, col)
            if(piece.type == "king"):
                if(piece.color == WHITE):
                    self.white_king_coords = (row,col)
                else:
                    self.black_king_coords = (row,col)
        #print("Undoing simulation - Captured piece: ",self.simulation_captured_piece)
        #print("Undoing simulation - piece: ",piece)
        #print("Undoing simulation - moved back to: " + str(row) + "," + str(col))
    
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
            if (self.get_piece(temp_row,temp_col) != 0) and (self.get_piece(temp_row,temp_col).color == color):
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