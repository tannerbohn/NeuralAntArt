# NeuralAntArt
Evolve ants that observe surrounding colours to determine new colour to deposit and where to move.

## How it Works
... 

## Usage
Run with:
```
python3.5 main.py
```

You will see a grid of tiles. Select the best ones, press Enter, wait, repeat.

You can change parameters by either editing `EG = EvolutionGrid(pop_grid_size=(4, 4), num_steps=500, window_size=(800, 800))` in `main.py` or by using key commands during run time. 

- **Up/Down**: increase/decrease timesteps by 250
- **Right/Left**: increase/decrease tile resolutions by 25

(parameter changes will be applied when a new generation is started)

If you have a nice grid of tiles, save the image in the `/output` folder with **Crtl+s**
