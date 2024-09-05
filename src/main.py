import pygame
import sys
import chess
import chess.engine
import os
import signal

from const import *
from game import Game
from square import Square
from move import Move
import threading
import queue
from piece import Pawn,Queen

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()
        
        
        # Initialize Stockfish engine
        self.engine = chess.engine.SimpleEngine.popen_uci(r"E:\stockfish\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe")
        self.board = chess.Board()
        self.depth = 10
        self.game_mode=None
        self.ai_color=None
        self.move_queue=queue.Queue()
        self.ai_thinking=False
        self.captured_sound=pygame.mixer.Sound("assets/sounds/capture.wav")
        self.running=True
        self.ai_thread=None
        self.exit_event=threading.Event()
    
    def ai_move_thread(self):
        while not self.exit_event.is_set() and self.ai_thinking:
            try:
                ai_move=self.ai_move()
                self.move_queue.put(ai_move)
                self.ai_thinking=False
            except Exception as e:
                break
    
    def select_game_mode(self):
        menu_font = pygame.font.Font(None, 32)
        modes = ["Human vs Human", "Human vs AI"]
        buttons = []
        background_image=pygame.image.load(r"D:\Downloads\view-dramatic-chess-pieces-with-stormy-weather.jpg").convert()
        background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        for i, mode in enumerate(modes):
            text = menu_font.render(mode, True, (255, 255, 255))
            button = text.get_rect(center=(WIDTH//2, HEIGHT//2 + i*50))
            buttons.append((text, button))
        
        while self.game_mode is None:
            self.screen.blit(background_image,(0,0))
            for text,button in buttons:
                self.screen.blit(text,button)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.engine.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(f"Mouse clicked at {event.pos}")
                    for i, (_, button) in enumerate(buttons):
                        if button.collidepoint(event.pos):
                            print(f"Button {i} clicked!")
                            if i == 0:                                
                                self.game_mode = "human_vs_human"
                                print("Human vs Human selected")
                            elif i == 1:
                                self.game_mode = "human_vs_ai"
                                self.ai_color = "white"
                                print("Human vs AI (white) selected")
                            break

            
        
        return self.game_mode,self.ai_color


    def ai_move(self):
        self.sync_board()
        # Get the best move from Stockfish
        self.board=chess.Board(self.game.board.get_fen())
        print("Before AI move:")
        print("Pygame board FEN:", self.game.board.get_fen())
        print("Chess engine board FEN:", self.board.fen())
        result = self.engine.play(self.board, chess.engine.Limit(depth=self.depth))
        ai_move=result.move
        self.board.push(ai_move)

        from_row, from_col = 7 - (ai_move.from_square // 8), ai_move.from_square % 8
        to_row, to_col = 7 - (ai_move.to_square // 8), ai_move.to_square % 8

        from_square=Square(from_row,from_col)
        to_square=Square(to_row,to_col)
        
        move = Move(from_square, to_square)

       
        
        print("After AI move:")
        print("Pygame board FEN:", self.game.board.get_fen())
        print("Chess engine board FEN:", self.board.fen())
        
        return move
    def sync_board(self):
        self.board=chess.Board(self.game.board.get_fen())

    def mainloop(self):
        self.game_mode,self.ai_color=self.select_game_mode()
        self.game.set_game_mode(self.game_mode,self.ai_color)

        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        clock=pygame.time.Clock()

        if self.game_mode == "human_vs_ai" and self.ai_color == "white":
            self.ai_thinking=True
            self.ai_thread=threading.Thread(target=self.ai_move_thread)
            self.ai_thread.start()
        
        try:
            while self.running:
             # show methods
                clock.tick(60)
            
                if not self.move_queue.empty():
                    ai_move=self.move_queue.get()
                    initial=ai_move.initial
                    final=ai_move.final
                    piece=board.squares[initial.row][initial.col].piece
                    if piece:
                        board.move(piece,ai_move)
                        game.next_turn()
                        self.sync_board()
                                
            
                game.show_bg(screen)
                game.show_last_move(screen)
                game.show_pieces(screen)
                game.show_hover(screen)         
            

                
                

               
               

                if dragger.dragging:
                    dragger.update_blit(screen)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running=False
                        self.exit_event.set()
                        break
 
                # click
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        dragger.update_mouse(event.pos)

                        clicked_row = dragger.mouseY // SQSIZE
                        clicked_col = dragger.mouseX // SQSIZE

                    # if clicked square has a piece ?
                        if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece (color) ?
                            if piece.color == game.next_player:
                                board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(piece)
                            # show methods 
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)

                # mouse motion
                    elif event.type == pygame.MOUSEMOTION:
                        motion_row = event.pos[1] // SQSIZE
                        motion_col = event.pos[0] // SQSIZE

                        game.set_hover(motion_row, motion_col)

                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                        # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                            game.show_hover(screen)
                            dragger.update_blit(screen)
                            pygame.display.update()

                # click release
                    elif event.type == pygame.MOUSEBUTTONUP:
                    
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)

                            released_row = dragger.mouseY // SQSIZE
                            released_col = dragger.mouseX // SQSIZE

                        # create possible move
                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final)

                        # valid move ?
                            if board.valid_move(dragger.piece, move):
                                board.move(dragger.piece,move)
                            # normal capture
                           

                                if isinstance(dragger.piece,Pawn):
                                    if(dragger.piece.color == 'white' and released_row==0)or(dragger.piece.color =='black' and released_row == 7):
                                        board.squares[released_row][released_col].piece = Queen(dragger.piece.color)

                            
                            
                            
                                board.set_true_en_passant(dragger.piece)                            

                            # sounds
                                self.captured_sound.play()
                            # show methods
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_pieces(screen)
                                pygame.display.update()
                            # next turn
                                game.next_turn()
                                self.sync_board()

                                if self.game_mode == "human_vs_ai" and game.next_player == self.ai_color and not self.ai_thinking:

                                    self.ai_thinking=True
                                    threading.Thread(target=self.ai_move_thread).start()
                            
                            
                        dragger.undrag_piece()

                # key press
                    elif event.type == pygame.KEYDOWN:
                    
                    # changing themes
                        if event.key == pygame.K_t:
                            game.change_theme()

                     # changing themes
                        if event.key == pygame.K_r:
                            game.reset()
                            game = self.game
                            board = self.game.board
                            dragger = self.game.dragger
                            self.board=chess.Board()
                            self.sync_board()

                            if self.game_mode == "human_vs_ai" and self.ai_color == "white":
                                ai_move = self.ai_move()
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_pieces(screen)
                                game.show_hover(screen)
                                game.next_turn()

                
            
                pygame.display.update()
        finally:
            self.cleanup()
    def cleanup(self):
        print("Cleaning up...")
        self.exit_event.set()
        if self.ai_thread and self.ai_thread.is_alive():
            print("Waiting for AI thread to finish..")
            if self.ai_thread.join(timeout=5):
                print("AI thread did not finish in time, forcefully exiting")
        print("Qitting pygame...")
        pygame.quit()
        print("Closing stockfish engine ...")
        self.engine.quit()
        print("Exiting program...")
        sys.exit()


main = Main()
main.mainloop()