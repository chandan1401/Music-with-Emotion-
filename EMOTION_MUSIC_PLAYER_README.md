# 🎵 Emotion-Based Music Player

A real-time emotion detection system that automatically plays music matching your current emotion using webcam input.

## Features

✨ **Real-time Emotion Detection**
- Uses DeepFace for accurate facial emotion recognition
- Detects 7 emotions: Happy, Sad, Angry, Surprise, Fear, Disgust, Neutral

🎵 **Intelligent Music Playback**
- Automatically plays songs matching detected emotions
- Reads songs from a simple CSV database
- Avoids playing the same song twice in a row
- Smooth music transitions

🎥 **Live Video Display**
- Real-time webcam feed with emotion overlay
- Displays current emotion and confidence score
- Shows currently playing song name
- Color-coded emotion display

⚡ **Easy to Use**
- Simple configuration via CSV file
- One-command execution
- Intuitive keyboard controls

## Project Structure

```
emotion-music-generator2/
├── src/
│   ├── emotion_detector.py      # Emotion detection module
│   ├── music_player.py           # Music playback module
│   └── main.py                   # Main application
├── tracks/                       # Add your MP3/WAV files here
├── track.csv                     # Song database
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Installation

### Step 1: Install Python Packages
```bash
pip install -r requirements.txt
```

### Step 2: Prepare Music Files
1. Create a `tracks/` folder in the project directory
2. Add your MP3 or WAV files to the `tracks/` folder
3. Note the exact file names

### Step 3: Create track.csv
Create or edit `track.csv` with your songs:

```csv
song_name,emotion,path
Happy Day,happy,tracks/happy_day.mp3
Joy Bells,happy,tracks/joy_bells.mp3
Rainy Day,sad,tracks/rainy_day.mp3
Broken Heart,sad,tracks/broken_heart.mp3
Rage Storm,angry,tracks/rage_storm.mp3
Peaceful Mind,neutral,tracks/peaceful_mind.mp3
```

**Column Explanation:**
- `song_name`: Display name of the song
- `emotion`: One of: happy, sad, angry, surprise, fear, disgust, neutral
- `path`: Relative path to the audio file from project root

## How to Run

```bash
python src/main.py
```

Or simply:
```bash
cd src
python main.py
```

## Keyboard Controls

| Key | Action |
|-----|--------|
| **Q** | Quit application |
| **SPACE** | Pause/Resume music |
| **S** | Stop music |
| **ESC** | Skip to next emotion detection |

## How It Works

1. **Initialization**
   - Loads songs from `track.csv`
   - Initializes webcam and emotion detector
   - Initializes pygame audio player

2. **Main Loop**
   - Captures frames from webcam
   - Analyzes frames for facial expressions
   - Detects dominant emotion
   - Displays emotion with confidence score

3. **Music Selection**
   - When emotion changes and confidence > 70%
   - Finds all songs matching that emotion
   - Randomly selects a song (avoids repeats)
   - Plays the song

4. **Display**
   - Shows live video with emotion overlay
   - Displays emotion name and confidence
   - Shows currently playing song

## Error Handling

The application handles:
- ✓ Camera not detected
- ✓ Face not found in frame
- ✓ Emotion detection fails
- ✓ Missing song files
- ✓ No songs for detected emotion
- ✓ Audio file format issues

## Module Documentation

### EmotionDetector (emotion_detector.py)
```python
detector = EmotionDetector(skip_frames=5)
emotion, confidence = detector.detect_emotion(frame)
emotions = detector.get_supported_emotions()
```

**Methods:**
- `detect_emotion(frame)` - Returns (emotion, confidence)
- `get_supported_emotions()` - Returns list of 7 emotions

### MusicPlayer (music_player.py)
```python
player = MusicPlayer('track.csv')
song_info = player.get_song_by_emotion('happy')
player.play_song(song_info)
player.pause_song()
player.resume_song()
player.stop_song()
```

**Methods:**
- `load_tracks(csv_path)` - Load songs from CSV
- `get_song_by_emotion(emotion)` - Get random song for emotion
- `play_song(song_info)` - Play the selected song
- `pause_song()` - Pause playback
- `resume_song()` - Resume paused song
- `stop_song()` - Stop playback

## Requirements

| Package | Version | Purpose |
|---------|---------|---------|
| opencv-python | 4.10.0.84 | Webcam capture |
| deepface | 0.0.93 | Emotion detection |
| tensorflow | 2.17.0 | Deep learning |
| pandas | 2.2.2 | CSV reading |
| pygame | 2.6.0 | Audio playback |
| numpy | 1.26.4 | Array operations |

## Customization

### Change Confidence Threshold
Edit `src/main.py`:
```python
self.confidence_threshold = 0.7  # Change to 0.5-0.9
```

### Change Skip Frames (Performance)
Edit `src/main.py`:
```python
EmotionDetector(skip_frames=10)  # Process every 10th frame
```

### Add More Emotions
Edit `track.csv` with new emotion types (currently supports: happy, sad, angry, surprise, fear, disgust, neutral)

## Troubleshooting

### "No camera found"
- Check camera is connected
- Try `camera_id=1` or higher if multiple cameras

### "No tracks found for emotion"
- Check `track.csv` format
- Ensure emotion column matches one of: happy, sad, angry, surprise, fear, disgust, neutral

### "Track file not found"
- Verify file paths in `track.csv`
- Check files exist in `tracks/` folder
- Use relative paths from project root

### "No face detected"
- Ensure good lighting
- Face should be clearly visible
- Get closer to camera

### "Emotion detection is slow"
- Increase `skip_frames` value
- Lower camera resolution
- Close other applications

## Performance Tips

1. **Faster Emotion Detection**
   - Increase `skip_frames` (e.g., 10 instead of 5)
   - Reduces CPU usage but less responsive

2. **Better Detection**
   - Ensure good lighting
   - Clear face visibility
   - Lower skip_frames value

3. **Audio Quality**
   - Use MP3 format for better compatibility
   - 128+ kbps bitrate recommended

## Limitations

- Single face detection (uses first detected face)
- Emotion model works best with clear facial expressions
- Requires good lighting for accurate detection
- Audio files must be MP3 or WAV format

## Future Enhancements

- [ ] Multi-face emotion detection
- [ ] Spotify integration
- [ ] Emotion history tracking
- [ ] Web-based UI
- [ ] Real-time visualizer
- [ ] Emotion-based playlist generation
- [ ] Cloud music streaming

## License

MIT License - Feel free to use and modify!

## Support

For issues or suggestions, please check:
1. That all files are in correct paths
2. That `track.csv` is properly formatted
3. That music files exist and are readable
4. That dependencies are installed

---

**Enjoy your emotion-based music experience!** 🎵😊
