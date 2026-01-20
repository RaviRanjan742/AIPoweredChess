# ♟️ AICheck

A UCI-compatible chess game built from scratch in Python, featuring drag-and-drop gameplay and the option to play against an AI powered by the Stockfish chess engine.

🎥 **YouTube Demo:**  
https://www.youtube.com/watch?v=YOUR_VIDEO_ID

---

## 🎥 Demo (YouTube)

[![AICheck Chess Game Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)]([https://www.youtube.com/watch?v=YOUR_VIDEO_ID](https://youtu.be/7lTeOBloHqg))

---

## ✨ Features

- **Two Modes of Play**
  - **Play with Human**  
    Traditional two-player chess with drag-and-drop piece movement and sound effects.
  - **Play with AI**  
    Challenge the Stockfish chess engine with adjustable difficulty levels.

- **UCI-Compatible**
  - Integrated with Stockfish using the UCI (Universal Chess Interface) protocol.

- **Real Chess Rules**
  - Castling  
  - En passant  
  - Pawn promotion  

- **Interactive UI**
  - Drag-and-drop movement
  - Sound effects for piece actions

---

## 🛠️ How We Built It

The project follows **Object-Oriented Programming (OOP)** principles, with clearly separated responsibilities across classes:

- **Main Class**
  - Controls the overall game loop and event handling.

- **Game Class**
  - Manages game state and AI interaction.

- **Board Class**
  - Initializes and maintains the chessboard.
  - Handles piece movement and rule enforcement.

- **Square Class**
  - Represents individual squares on the chessboard.

- **Move Class**
  - Validates legal chess moves.

- **Dragger Class**
  - Implements drag-and-drop functionality for chess pieces.

- **Sound Class**
  - Manages sound effects for gameplay actions.

- **Const Class**
  - Stores constants such as screen resolution and board dimensions.

---

## 🚧 Challenges We Faced

- Implementing **special chess rules** like castling, en passant, and pawn promotion.
- Integrating Stockfish smoothly while keeping the UI responsive.
- Designing a modular OOP architecture for maintainability and scalability.

---

## 🏆 What We’re Proud Of

- The AI-powered chess engine has defeated **all team members and friends**.
- Successfully built a **fully functional chess game from scratch**.
- Clean separation of concerns using OOP principles.

---

## 🔮 Future Work

- Integrate **neural networks** so the AI can learn from its own games.
- Add a **learning mode** that explains:
  - Why a move is incorrect
  - The potentia
