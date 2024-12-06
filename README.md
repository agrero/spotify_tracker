# A Song Tracker for Spotify

## Thing This does
1) collect previously played spotify data
    - authorization handled by spotify

2) track each time you skip
    - currently does this by calculating the times that the song should end vs when the next song started


## Things it will do

1) track the approximate % of song skipped
    - needs to be implemented
    
2) visualize your grooves
    - see patterns based on spotify analytics of your song 'streaks'
        - thinking box and whisker plots right now for each analytic 
    - take song 'streak's and compare based on spotify's song analytics

3) command line interface
    - current thoughts are to add this via curses but tbd


## Definitions

1) Streaks
    - currently this is just a set of uninterrupted songs


## Actions

Activate the poetry venv
```bash
poetry shell
```
Run program
```bash
poetry run python main.py
```
