import pygame
from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square
from move import Move
import chess 
import chess.engine
class Game:
    def __init__(self):

        self.hovered_sqr=None
        self.board=Board()
        self.dragger=Dragger()
        self.config=Config()
        self.game_mode=None
        self.ai_color=None
        self.ai_engine=None
        self.next_player='white'
        if self.config.ai_mode:
            self.init_ai_engine()

    def init_ai_engine(self):
        self.ai_engine = chess.engine.SimpleEngine.popen_uci(self.config.stockfish_path)
        self.ai_engine.configure({"Skill Level": self.config.ai_difficulty})

        if self.ai_color is None:
            self.ai_color='white'
    
    def set_game_mode(self, mode, ai_color=None):
        self.game_mode = mode
        if mode == "human_vs_ai":
            self.ai_color = ai_color
            self.init_ai_engine()
        else:
            self.ai_color = None
            if self.ai_engine:
                self.ai_engine.quit()
                self.ai_engine = None
    
    def show_bg(self,surface):
        theme=self.config.theme
        for row in range(ROWS):
            for col in range(COLS):
                
                color=theme.bg.light if (row+col)%2 ==0 else theme.bg.dark
                rect=(col*SQSIZE,row*SQSIZE,SQSIZE,SQSIZE) 

                pygame.draw.rect(surface,color,rect)

                if col == 0:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    lb1=self.config.font.render(str(ROWS-row),1,color)
                    lb1_pos=(5,5+row*SQSIZE)
                    
                    surface.blit(lb1,lb1_pos)
                
                if row == 7:
                    color=theme.bg.dark if (row+col) % 2 == 0 else theme.bg.light
                    lb1=self.config.font.render(Square.get_alphacol(col),1,color)
                    lb1_pos=(col*SQSIZE+SQSIZE-20,HEIGHT-20)
                    surface.blit(lb1,lb1_pos)


    def show_pieces(self,surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                   piece=self.board.squares[row][col].piece
                   if piece is not self.dragger.piece:
                       piece.set_texture(size=80)
                       img=pygame.image.load(piece.texture)
                       img_centre=col * SQSIZE+SQSIZE // 2,row*SQSIZE+SQSIZE //2
                       piece.texture_rect=img.get_rect(center=img_centre)
                       surface.blit(img,piece.texture_rect)

    def show_moves(self,surface):
        theme=self.config.theme
        if self.dragger.dragging:
            piece=self.dragger.piece

            for move in piece.moves:
                #color
                color=theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                #rect
                rect=(move.final.col * SQSIZE,move.final.row *SQSIZE,SQSIZE,SQSIZE)
                #blit
                pygame.draw.rect(surface,color,rect)
    
    def show_last_move(self,surface):
        theme=self.config.theme

        if self.board.last_move:
            initial=self.board.last_move.initial
            final=self.board.last_move.final

            for pos in [initial,final]:
                color=theme.trace.light if (pos.row+pos.col) % 2 == 0 else theme.trace.dark
                rect=(pos.col*SQSIZE,pos.row*SQSIZE,SQSIZE,SQSIZE)
                pygame.draw.rect(surface,color,rect)
    
    def show_hover(self,surface):
        if self.hovered_sqr:
            color=(180,180,180)
            rect=(self.hovered_sqr.col*SQSIZE,self.hovered_sqr.row*SQSIZE,SQSIZE,SQSIZE)
            pygame.draw.rect(surface,color,rect,width=3)

    def next_turn(self):
        self.next_player='white' if self.next_player == 'black' else 'black'
        if self.game_mode == "human_vs_ai" and self.next_player==self.ai_color:
            self.ai_move()

    def set_hover(self,row,col):
        self.hovered_sqr=self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()
    
    def play_sound(self,captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'
        if self.config.ai_mode and self.next_player == 'black':  # Assuming AI plays as black
            self.ai_move()
    
    def ai_move(self):
        if not self.ai_engine:
            self.init_ai_engine()
        
        fen = self.board.get_fen()  # You need to implement this method in your Board class
        chess_board = chess.Board(fen)
        
        result = self.ai_engine.play(chess_board, chess.engine.Limit(time=self.config.ai_time))
        ai_move = result.move
        
        # Convert chess.Move to your custom Move class
        initial = Square(ai_move.from_square % 8, ai_move.from_square // 8)
        final = Square(ai_move.to_square % 8, ai_move.to_square // 8)
        move = Move(initial, final)
        
        # Make the move
        piece = self.board.squares[initial.row][initial.col].piece
        self.board.move(piece, move)
        
        # Play sound
        captured = self.board.squares[final.row][final.col].has_piece()
        self.play_sound(captured)
        
        # Set last move
        self.board.last_move = move
        
        
    
    def reset(self):
        self.__init__()
        self.game_mode=None
        self.ai_color=None
        if self.ai_engine:
            self.ai_engine.quit()
            self.ai_engine = None
    
    def quit(self):
        if self.ai_engine:
            self.ai_engine.quit()
            self.ai_engine=None



