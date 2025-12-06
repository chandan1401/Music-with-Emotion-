# EMOTION-BASED MUSIC PLAYER - COMPLETE CODE

This file contains all the source code for the Emotion-Based Music Player project.

---

## FILE 1: src/emotion_detector.py

```python
"""
Emotion Detection Module using DeepFace
Detects dominant emotion from webcam frames in real-time
"""

from deepface import DeepFace
import cv2


class EmotionDetector:
    """
    Detects emotion from face images using DeepFace.
    
    Attributes:
        emotions (list): List of all supported emotions
        frame_count (int): Counter for frame processing
        skip_frames (int): Skip frames for performance optimization
    """
    
    def __init__(self, skip_frames=5):
        """
        Initialize the EmotionDetector.
        
        Args:
            skip_frames (int): Process every nth frame for performance
        """
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        self.frame_count = 0
        self.skip_frames = skip_frames
        self.last_emotion = None
        
    def detect_emotion(self, frame):
        """
        Detect dominant emotion from a frame.
        
        Args:
            frame (np.ndarray): Video frame from OpenCV (BGR format)
            
        Returns:
            tuple: (emotion_name, confidence_score) or (None, 0.0) if detection fails
        """
        self.frame_count += 1
        
        # Skip frames for performance
        if self.frame_count % self.skip_frames != 0:
            return self.last_emotion, 0.0
        
        if frame is None or frame.size == 0:
            return None, 0.0
        
        try:
            # Detect emotion using DeepFace
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            
            if not result:
                return None, 0.0
            
            # Get emotion with highest confidence
            emotion_dict = result[0]['emotion']
            dominant_emotion = max(emotion_dict, key=emotion_dict.get)
            confidence = emotion_dict[dominant_emotion] / 100  # Convert to 0-1 scale
            
            self.last_emotion = (dominant_emotion, confidence)
            return dominant_emotion, confidence
            
        except Exception as e:
            print(f"Error detecting emotion: {e}")
            return None, 0.0
    
    def get_supported_emotions(self):
        """
        Get list of supported emotions.
        
        Returns:
            list: List of emotion names
        """
        return self.emotions
```

---

## FILE 2: src/music_player.py

```python
"""
Music Player Module
Handles reading track CSV, selecting songs by emotion, and playing audio using pygame
"""

import pandas as pd
import pygame
import os
from pathlib import Path


class MusicPlayer:
    """
    Manages music playback based on detected emotions.
    
    Attributes:
        tracks_df (DataFrame): DataFrame containing track information
        current_song (str): Currently playing song name
        last_played (str): Last played song to avoid repeats
    """
    
    def __init__(self, csv_path='track.csv'):
        """
        Initialize the MusicPlayer.
        
        Args:
            csv_path (str): Path to track.csv file
        """
        self.tracks_df = None
        self.current_song = None
        self.last_played = None
        self.is_playing = False
        
        # Initialize pygame mixer
        try:
            pygame.mixer.init()
            print("✓ Pygame mixer initialized successfully")
        except Exception as e:
            print(f"✗ Error initializing pygame mixer: {e}")
        
        # Load tracks from CSV
        self.load_tracks(csv_path)
    
    def load_tracks(self, csv_path):
        """
        Load tracks from CSV file.
        
        Args:
            csv_path (str): Path to track.csv file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not os.path.exists(csv_path):
                print(f"✗ Error: {csv_path} not found!")
                print(f"  Please create {csv_path} with columns: song_name, emotion, path")
                return False
            
            self.tracks_df = pd.read_csv(csv_path)
            
            # Validate required columns
            required_cols = ['song_name', 'emotion', 'path']
            if not all(col in self.tracks_df.columns for col in required_cols):
                print(f"✗ Error: CSV must contain columns: {required_cols}")
                return False
            
            print(f"✓ Loaded {len(self.tracks_df)} tracks from {csv_path}")
            
            # Validate that track paths exist
            missing_tracks = []
            for idx, row in self.tracks_df.iterrows():
                if not os.path.exists(row['path']):
                    missing_tracks.append(row['song_name'])
            
            if missing_tracks:
                print(f"✗ Warning: {len(missing_tracks)} tracks not found:")
                for song in missing_tracks:
                    print(f"  - {song}")
            
            return True
            
        except pd.errors.ParserError as e:
            print(f"✗ Error parsing CSV: {e}")
            return False
        except Exception as e:
            print(f"✗ Error loading tracks: {e}")
            return False
    
    def get_song_by_emotion(self, emotion):
        """
        Get a random song matching the detected emotion.
        Avoids playing the same song twice in a row.
        
        Args:
            emotion (str): Detected emotion
            
        Returns:
            dict: Song information (song_name, emotion, path) or None if not found
        """
        if self.tracks_df is None or self.tracks_df.empty:
            print(f"✗ Error: No tracks loaded")
            return None
        
        # Filter tracks by emotion
        matching_tracks = self.tracks_df[self.tracks_df['emotion'].str.lower() == emotion.lower()]
        
        if matching_tracks.empty:
            print(f"✗ No tracks found for emotion: {emotion}")
            return None
        
        # Try to avoid repeating the same song
        available_tracks = matching_tracks[matching_tracks['song_name'] != self.last_played]
        
        # If all songs have been played, reset and use all songs
        if available_tracks.empty:
            available_tracks = matching_tracks
        
        # Select random song
        song = available_tracks.sample(1).iloc[0]
        return {
            'song_name': song['song_name'],
            'emotion': song['emotion'],
            'path': song['path']
        }
    
    def play_song(self, song_info):
        """
        Play a song from the given song info.
        
        Args:
            song_info (dict): Dictionary with song details (song_name, emotion, path)
            
        Returns:
            bool: True if playback started, False otherwise
        """
        if song_info is None:
            return False
        
        try:
            song_path = song_info['path']
            song_name = song_info['song_name']
            
            if not os.path.exists(song_path):
                print(f"✗ Error: Track file not found: {song_path}")
                return False
            
            # Stop current song if playing
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            
            # Load and play new song
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play(-1)  # -1 means loop
            
            self.current_song = song_name
            self.last_played = song_name
            self.is_playing = True
            
            print(f"♫ Now playing: {song_name}")
            return True
            
        except pygame.error as e:
            print(f"✗ Error playing song: {e}")
            return False
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            return False
    
    def stop_song(self):
        """Stop current song playback."""
        try:
            pygame.mixer.music.stop()
            self.is_playing = False
            print("⏹ Music stopped")
        except Exception as e:
            print(f"✗ Error stopping music: {e}")
    
    def pause_song(self):
        """Pause current song playback."""
        try:
            pygame.mixer.music.pause()
            print("⏸ Music paused")
        except Exception as e:
            print(f"✗ Error pausing music: {e}")
    
    def resume_song(self):
        """Resume paused song."""
        try:
            pygame.mixer.music.unpause()
            print("▶ Music resumed")
        except Exception as e:
            print(f"✗ Error resuming music: {e}")
    
    def get_playing_song(self):
        """
        Get currently playing song name.
        
        Returns:
            str: Song name or None
        """
        return self.current_song
```

---

## FILE 3: src/main.py

```python
"""
================================================================================
    EMOTION-BASED MUSIC PLAYER
    Real-time emotion detection and music playback system
================================================================================

HOW TO RUN THIS PROJECT:
1. Install dependencies:
   pip install -r requirements.txt

2. Create a track.csv file in the project root with columns:
   song_name,emotion,path
   (See example below)

3. Place your MP3/WAV files in the /tracks directory

4. Run the application:
   python main.py

5. Controls:
   - Q: Quit application
   - Space: Pause/Resume music
   - S: Stop music
   - ESC: Skip to next emotion detection

EXAMPLE track.csv format:
song_name,emotion,path
Happy Song 1,happy,tracks/happy1.mp3
Happy Song 2,happy,tracks/happy2.mp3
Sad Song 1,sad,tracks/sad1.mp3
Sad Song 2,sad,tracks/sad2.mp3
Angry Song 1,angry,tracks/angry1.mp3
Neutral Song 1,neutral,tracks/neutral1.mp3

================================================================================
"""

import cv2
import sys
from emotion_detector import EmotionDetector
from music_player import MusicPlayer


class EmotionMusicPlayer:
    """
    Main application class that combines emotion detection and music playback.
    """
    
    def __init__(self, camera_id=0, csv_path='track.csv'):
        """
        Initialize the Emotion Music Player.
        
        Args:
            camera_id (int): Camera device ID (usually 0 for default camera)
            csv_path (str): Path to track.csv file
        """
        self.camera_id = camera_id
        self.emotion_detector = EmotionDetector(skip_frames=5)
        self.music_player = MusicPlayer(csv_path)
        self.cap = None
        self.last_played_emotion = None
        self.confidence_threshold = 0.7
        self.window_name = "Emotion-Based Music Player"
        
    def initialize_camera(self):
        """
        Initialize webcam capture.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            
            if not self.cap.isOpened():
                print(f"✗ Error: Cannot access camera {self.camera_id}")
                return False
            
            # Set camera resolution for better performance
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            print(f"✓ Camera initialized successfully")
            return True
            
        except Exception as e:
            print(f"✗ Error initializing camera: {e}")
            return False
    
    def run(self):
        """
        Main application loop - runs emotion detection and music playback.
        """
        if not self.initialize_camera():
            return
        
        print("\n" + "="*60)
        print("EMOTION-BASED MUSIC PLAYER STARTED")
        print("="*60)
        print("Controls:")
        print("  Q      : Quit")
        print("  SPACE  : Pause/Resume")
        print("  S      : Stop")
        print("  ESC    : Skip")
        print("="*60 + "\n")
        
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        
        try:
            while True:
                ret, frame = self.cap.read()
                
                if not ret:
                    print("✗ Error: Failed to read frame from camera")
                    break
                
                # Flip frame for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Detect emotion
                emotion, confidence = self.emotion_detector.detect_emotion(frame)
                
                # Display emotion on frame
                self._display_emotion(frame, emotion, confidence)
                
                # Play music if emotion changed and confidence is high enough
                if emotion and emotion != self.last_played_emotion and confidence >= self.confidence_threshold:
                    print(f"\n🎭 Emotion detected: {emotion.upper()} (Confidence: {confidence:.2%})")
                    song_info = self.music_player.get_song_by_emotion(emotion)
                    if song_info:
                        self.music_player.play_song(song_info)
                        self.last_played_emotion = emotion
                
                # Display the frame
                cv2.imshow(self.window_name, frame)
                
                # Handle key press
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == ord('Q'):
                    print("\n✓ Exiting application...")
                    break
                elif key == ord(' '):
                    if self.music_player.is_playing:
                        self.music_player.pause_song()
                    else:
                        self.music_player.resume_song()
                elif key == ord('s') or key == ord('S'):
                    self.music_player.stop_song()
                elif key == 27:  # ESC key
                    self.last_played_emotion = None
                    print("Skipping to next emotion detection...")
        
        except KeyboardInterrupt:
            print("\n✓ Application interrupted by user")
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
        finally:
            self.cleanup()
    
    def _display_emotion(self, frame, emotion, confidence):
        """
        Display emotion and confidence on the video frame.
        
        Args:
            frame (np.ndarray): Video frame
            emotion (str): Detected emotion
            confidence (float): Confidence score
        """
        height, width = frame.shape[:2]
        
        if emotion:
            # Determine color based on emotion
            color_map = {
                'happy': (0, 255, 0),    # Green
                'sad': (255, 0, 0),      # Blue
                'angry': (0, 0, 255),    # Red
                'surprise': (0, 255, 255),  # Yellow
                'fear': (255, 0, 255),   # Magenta
                'disgust': (255, 165, 0),  # Orange
                'neutral': (128, 128, 128)  # Gray
            }
            color = color_map.get(emotion, (255, 255, 255))
            
            # Display emotion text
            text = f"{emotion.upper()} ({confidence:.2%})"
            cv2.putText(frame, text, (20, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)
            
            # Display current song
            if self.music_player.get_playing_song():
                song_text = f"Now Playing: {self.music_player.get_playing_song()}"
                cv2.putText(frame, song_text, (20, 100),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        else:
            cv2.putText(frame, "No face detected", (20, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    def cleanup(self):
        """Clean up resources before exiting."""
        if self.cap:
            self.cap.release()
        self.music_player.stop_song()
        cv2.destroyAllWindows()
        print("✓ Resources cleaned up")
        print("="*60)
        print("Thank you for using Emotion-Based Music Player!")
        print("="*60 + "\n")


def main():
    """Entry point of the application."""
    player = EmotionMusicPlayer()
    player.run()


if __name__ == "__main__":
    main()
```

---

## FILE 4: track.csv (Example)

```csv
song_name,emotion,path
Happy Day,happy,tracks/happy_day.mp3
Joy Bells,happy,tracks/joy_bells.mp3
Smile Wide,happy,tracks/smile_wide.mp3
Rainy Day,sad,tracks/rainy_day.mp3
Broken Heart,sad,tracks/broken_heart.mp3
Loneliness,sad,tracks/loneliness.mp3
Rage Storm,angry,tracks/rage_storm.mp3
Furious Beat,angry,tracks/furious_beat.mp3
Inner Conflict,angry,tracks/inner_conflict.mp3
Peaceful Mind,neutral,tracks/peaceful_mind.mp3
Still Moment,neutral,tracks/still_moment.mp3
Silent Night,neutral,tracks/silent_night.mp3
Surprised Joy,surprise,tracks/surprised_joy.mp3
Shock Wave,surprise,tracks/shock_wave.mp3
Unexpected Turn,surprise,tracks/unexpected_turn.mp3
Fear in Dark,fear,tracks/fear_in_dark.mp3
Tension Build,fear,tracks/tension_build.mp3
Creeping Dread,fear,tracks/creeping_dread.mp3
Disgusted Feeling,disgust,tracks/disgusted_feeling.mp3
Repulsive Sound,disgust,tracks/repulsive_sound.mp3
Bitter Taste,disgust,tracks/bitter_taste.mp3
```

---

## FINAL INSTRUCTIONS FOR RUNNING

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create Tracks Folder
```bash
mkdir tracks
```

### Step 3: Add Music Files
Place your MP3 or WAV files in the `tracks/` folder

### Step 4: Update track.csv
Edit `track.csv` with your song information:
- Column 1: song_name (display name)
- Column 2: emotion (happy, sad, angry, surprise, fear, disgust, neutral)
- Column 3: path (relative path to file)

### Step 5: Run the Application
```bash
python src/main.py
```

### Controls While Running
- **Q**: Quit
- **SPACE**: Pause/Resume
- **S**: Stop  
- **ESC**: Skip emotion detection

---

## Project Structure
```
emotion-music-generator2/
├── src/
│   ├── emotion_detector.py
│   ├── music_player.py
│   └── main.py
├── tracks/              (Create this folder)
├── track.csv
├── requirements.txt
└── README.md
```

---

**That's it! You now have a complete, working Emotion-Based Music Player!** 🎵😊
