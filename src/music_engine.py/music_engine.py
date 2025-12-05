"""Music playback engine based on emotion."""
import pandas as pd
import os
try:
    import vlc
    HAS_VLC = True
except ImportError:
    HAS_VLC = False
    print("Warning: VLC not available. Install python-vlc to enable music playback.")

# Paths
TRACKS_CSV_PATH = "tracks.csv"

# Load tracks data
tracks = None
if os.path.exists(TRACKS_CSV_PATH):
    try:
        tracks = pd.read_csv(TRACKS_CSV_PATH)
    except Exception as e:
        print(f"Error loading tracks CSV: {e}")
else:
    print(f"Warning: Tracks CSV not found at {TRACKS_CSV_PATH}")

# Initialize VLC player
player = vlc.MediaPlayer() if HAS_VLC else None

# Emotion to characteristics mapping
emotion_map = {
    "happy": ("high", "high"),
    "sad": ("low", "low"),
    "angry": ("medium", "high"),
    "disgust": ("low", "medium"),
    "fear": ("medium", "high"),
    "surprise": ("high", "medium"),
    "neutral": ("mid", "mid"),
}


def play_music(emotion):
    """
    Play music matching the given emotion.
    
    Args:
        emotion: Detected emotion label
        
    Returns:
        True if music played successfully, False otherwise
    """
    if not HAS_VLC:
        print("VLC not available. Please install python-vlc.")
        return False
        
    if player is None:
        print("Music player not initialized.")
        return False
        
    if tracks is None or tracks.empty:
        print("No tracks available.")
        return False
        
    try:
        # Filter tracks by emotion
        matching_tracks = tracks[tracks["emotion"].str.lower() == emotion.lower()]
        
        # Fall back to all tracks if no matches
        if matching_tracks.empty:
            print(f"No tracks found for emotion: {emotion}. Playing random track.")
            matching_tracks = tracks
            
        # Select random track
        track_row = matching_tracks.sample(1).iloc[0]
        track_path = track_row.get("path") or track_row.get("track_path")
        
        if not track_path or not os.path.exists(track_path):
            print(f"Track path invalid or not found: {track_path}")
            return False
            
        # Play music
        media = vlc.Media(track_path)
        player.set_media(media)
        player.play()
        
        print(f"Playing: {track_row.get('name', 'Unknown')} (Emotion: {emotion})")
        return True
        
    except Exception as e:
        print(f"Error playing music: {e}")
        return False


def stop_music():
    """Stop currently playing music."""
    if player and HAS_VLC:
        player.stop()


def get_emotions():
    """
    Get available emotions.
    
    Returns:
        List of emotion labels
    """
    return list(emotion_map.keys())
