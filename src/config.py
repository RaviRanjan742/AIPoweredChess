import pygame
import os

from sound import Sound
from theme import Theme

class Config:
    def __init__(self):
        self.themes=[]
        self._add_themes()
        self.idx=0
        self.theme=self.themes[self.idx]
        self.font=pygame.font.SysFont('monospace',18,bold=True)
        self.move_sound=Sound(
            os.path.join('assets/sounds/move.wav')
        )
        self.capture_sound=Sound(
            os.path.join('assets/sounds/capture.wav')
        )

        self.stockfish_path =r"E:\stockfish\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"  # Update this with your Stockfish path
        self.ai_mode = False  # False for PvP, True for PvAI
        self.ai_difficulty = 10  # Stockfish skill level (0-20)
        self.ai_depth = 15  # Search depth for Stockfish
        self.ai_time = 2.0  # Time limit for Stockfish to make a move (in seconds)
    def change_theme(self):
        self.idx +=1
        self.idx %=len(self.themes)
        self.theme=self.themes[self.idx]
    
    def _add_themes(self):
        green = Theme((234, 235, 200), (119, 154, 88), (244, 247, 116), (172, 195, 51), '#C86464', '#C84646')
        brown = Theme((235, 209, 166), (165, 117, 80), (245, 234, 100), (209, 185, 59), '#C86464', '#C84646')
        blue = Theme((229, 228, 200), (60, 95, 135), (123, 187, 227), (43, 119, 191), '#C86464', '#C84646')
        gray = Theme((120, 119, 118), (86, 85, 84), (99, 126, 143), (82, 102, 128), '#C86464', '#C84646')

        self.themes=[green,brown,blue,gray]
    
    def toggle_ai_mode(self):
        self.ai_mode = not self.ai_mode

    def set_ai_difficulty(self, level):
        if 0 <= level <= 20:
            self.ai_difficulty = level

    def set_ai_depth(self, depth):
        if depth > 0:
            self.ai_depth = depth

    def set_ai_time(self, time):
        if time > 0:
            self.ai_time = time

    def set_stockfish_path(self, path):
        if os.path.exists(path):
            self.stockfish_path = path
        else:
            raise FileNotFoundError(f"Stockfish executable not found at {path}")

    
