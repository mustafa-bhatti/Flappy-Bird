# Flappy Bird (PyGame)

A clone of the classic Flappy Bird game built using Python and PyGame.

## Features

- Classic Flappy Bird gameplay with smooth animation  
- Pixel-perfect collision detection  
- Animated bird and moving pipes  
- Score tracking and persistent leaderboard  
- Sound effects and background music  
- Custom fonts and graphics  

## Folder Structure

```
Final Game/
  board.json              # Leaderboard data (auto-generated)
  flappyV2.py             # Main game script
  pipes.py                # Pipe obstacle logic
  player.py               # Player (bird) logic
  audio/                  # Sound effects and music
    bg.wav
    die.wav
    hit.wav
    point.wav
    swoosh.wav
    wing.wav
  font/                   # Game fonts
    flappyfont.TTF
    Pixeltype.ttf
  sprites/                # Game graphics
    background.png
    base.png
    bird.png
    bird1.png
    bird2.png
    pipe.png
    play.png
    podium.png
    title.png
```

## Requirements

- Python 3.x  
- [PyGame](https://www.pygame.org/) (`pip install pygame`)

## How to Play

1. Install the requirements.
2. Run the main game script:
   ```sh
   python "Final Game/flappyV2.py"
   ```
3. On the welcome screen, click the play button or press `Space` to start.
4. Press `Space` to make the bird jump and avoid the pipes.
5. Try to get the highest score! After a game over, enter your 4-letter name to save your score to the leaderboard.

## Leaderboard

- The top scores are saved in `board.json`.
- The leaderboard can be viewed from the main menu.

## Screenshots

![Home](Final%20Game/screenshots/main.png)
![gameplay](Final%20Game/screenshots/game.png)
![Leaderboard](Final%20Game/screenshots/leaderboard1.png)

## Credits

- Developed using PyGame.
- All assets (sprites, fonts, sounds) are included in the repository.