# Quick Start Guide - Emotion-Based Music Player

## 5-Minute Setup

### 1. Install Dependencies (2 minutes)
```bash
pip install -r requirements.txt
```

### 2. Create Tracks Folder
```bash
mkdir tracks
```

### 3. Add Your Music Files
Place MP3 or WAV files in the `tracks/` folder:
```
tracks/
  ├── happy_day.mp3
  ├── rainy_day.mp3
  ├── rage_storm.mp3
  └── peaceful_mind.mp3
```

### 4. Update track.csv
Edit the `track.csv` file to match your music files:

```csv
song_name,emotion,path
Happy Day,happy,tracks/happy_day.mp3
Rainy Day,sad,tracks/rainy_day.mp3
Rage Storm,angry,tracks/rage_storm.mp3
Peaceful Mind,neutral,tracks/peaceful_mind.mp3
```

### 5. Run the Application
```bash
python src/main.py
```

## Tested with Example Songs

If you want to test without your own music:

1. Download free MP3s from:
   - [Free Music Archive](https://freemusicarchive.org/)
   - [Incompetech](https://incompetech.com/)
   - [YouTube Audio Library](https://www.youtube.com/audiolibrary)

2. Place them in `tracks/` folder

3. Update `track.csv` with correct paths

4. Run!

## Common Issues & Fixes

### Issue: "ModuleNotFoundError: No module named 'cv2'"
**Fix:** Run `pip install -r requirements.txt`

### Issue: "track.csv not found"
**Fix:** Make sure `track.csv` is in project root (same folder as `src/`)

### Issue: "No face detected"
**Fix:** 
- Ensure good lighting
- Face should be visible in camera
- Get closer to camera

### Issue: "Track file not found"
**Fix:**
- Check file paths in `track.csv`
- Use format: `tracks/filename.mp3`
- Verify files exist in `tracks/` folder

### Issue: Application runs but no music plays
**Fix:**
- Check `track.csv` for correct emotions
- Ensure emotion column matches: happy, sad, angry, surprise, fear, disgust, neutral
- Check volume settings on computer

## File Structure Check

Your project should look like:
```
emotion-music-generator2/
├── src/
│   ├── emotion_detector.py
│   ├── music_player.py
│   └── main.py
├── tracks/                  # Your music files here
│   ├── happy_day.mp3
│   ├── rainy_day.mp3
│   └── ...
├── track.csv               # Your song database
└── requirements.txt
```

## Usage Example

### Example track.csv
```csv
song_name,emotion,path
Morning Joy,happy,tracks/morning_joy.mp3
Happy Vibes,happy,tracks/happy_vibes.mp3
Melancholy Mood,sad,tracks/melancholy_mood.mp3
Sad Piano,sad,tracks/sad_piano.mp3
Angry Rock,angry,tracks/angry_rock.mp3
Calm Meditation,neutral,tracks/calm_meditation.mp3
Surprise Music,surprise,tracks/surprise_music.mp3
Scary Sounds,fear,tracks/scary_sounds.mp3
Disgusting Noise,disgust,tracks/disgusting_noise.mp3
```

### Running the App
```bash
$ python src/main.py

============================================================
EMOTION-BASED MUSIC PLAYER STARTED
============================================================
Controls:
  Q      : Quit
  SPACE  : Pause/Resume
  S      : Stop
  ESC    : Skip
============================================================

✓ Camera initialized successfully
🎭 Emotion detected: HAPPY (Confidence: 85.23%)
♫ Now playing: Morning Joy
```

## Keyboard Controls While Running

| Key | Function |
|-----|----------|
| **Q** | Quit app |
| **SPACE** | Play/Pause |
| **S** | Stop |
| **ESC** | Skip emotion |

## What Happens When You Run It

1. **Initialization** (2-3 seconds)
   - Loads songs from `track.csv`
   - Initializes camera
   - Initializes audio system

2. **Emotion Detection** (Real-time)
   - Analyzes your face
   - Detects emotion
   - Displays emotion name & confidence

3. **Music Playback**
   - When emotion changes (70%+ confidence)
   - Selects matching song
   - Plays automatically

4. **Display**
   - Shows live video
   - Shows current emotion
   - Shows now playing song

## Performance Notes

- First run may take 10-15 seconds (model loading)
- Emotion detection updates every 5 frames
- Music loads immediately when selected
- Works with 1-3 FPS minimum (slower = less responsive)

## Next Steps

1. ✅ Install dependencies
2. ✅ Create `tracks/` folder
3. ✅ Add music files
4. ✅ Update `track.csv`
5. ✅ Run `python src/main.py`
6. ✅ Enjoy!

## Support

See `EMOTION_MUSIC_PLAYER_README.md` for detailed documentation.

---

**That's it! You're ready to go!** 🎵😊
