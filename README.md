# AI Powered Chess

A UCI-compatible chess game built from scratch in Python, with drag-and-drop functionality and the option to play against an AI using the powerful Stockfish chess engine.

## Features

- **Two Modes of Play**:
  - **Play with Human**: Traditional two-player chess, complete with drag-and-drop piece movement and sound effects.
  - **Play with AI**: Challenge the Stockfish chess engine with adjustable difficulty levels. Test your skills against one of the strongest open-source chess engines.

## How We Built It

We designed the game using object-oriented programming (OOP) principles, organizing our code into distinct classes to handle different parts of the game:

- **Main Class**: Oversees the entire game flow, managing interactions between other components like the board, pieces, and players.
  
- **Dragger Class**: Manages the drag-and-drop functionality for moving chess pieces.
  
- **Square Class**: Represents individual squares on the chessboard.
  
- **Sound Class**: Handles sound effects for piece movements.
  
- **Board Class**: 
  - Initializes and maintains the chessboard structure.
  - Moves and updates pieces during the game.
  - Enforces special chess rules (castling, en passant, pawn promotion).

- **Game Class**: Manages the overall game flow and interaction with the AI.

- **Move Class**: Ensures that the  moves comply with chess rules.

- **Const Class**: Handles the screen resolution and board size settings.

## Challenges We Faced

Building this game required careful integration of various classes and functions using OOP concepts. We also faced challenges in ensuring the game logic conformed to chess rules, especially for special moves like castling and pawn promotion.

## What We’re Proud Of

- Our AI-powered chess game has defeated all of our team members and friends!
  
- We've built a fully functional chess game that not only allows for human vs. human play but also features a challenging AI opponent.

## Future Work

- We plan to implement neural networks to enable the AI to learn from its own games and improve over time. This would allow our chess engine to train itself based on real-world gameplay data.
  
- In the future, we also plan to add a learning mode that helps players analyze all their moves. During gameplay, the system will guide players by explaining why their move is incorrect and what the potential repercussions could be.

## How to Play

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-powered-chess.git
