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
    
    def __init__(self, camera_id=0, csv_path='../track.csv'):
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
        Shows camera for 10 seconds, captures emotion after 6 seconds, then plays song.
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
            frame_count = 0
            emotion_capture_frame = int(6 * 30)  # Capture emotion at 6 seconds (180 frames at 30fps)
            max_frames = int(10 * 30)  # 10 seconds (300 frames at 30fps)
            detected_emotion = None
            detected_confidence = None
            
            while True:
                ret, frame = self.cap.read()
                
                if not ret:
                    print("✗ Error: Failed to read frame from camera")
                    break
                
                # Flip frame for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Detect emotion every frame
                emotion, confidence = self.emotion_detector.detect_emotion(frame)
                
                # Display countdown timer
                self._display_countdown(frame, frame_count, max_frames)
                
                # If we're past the 6-second mark and haven't captured yet
                if frame_count == emotion_capture_frame and emotion:
                    detected_emotion = emotion
                    detected_confidence = confidence
                    print(f"\n🎭 Emotion captured at 6 seconds: {emotion.upper()} (Confidence: {confidence:.2%})")
                    self._display_emotion(frame, emotion, confidence)
                elif frame_count > emotion_capture_frame:
                    # Show the captured emotion
                    if detected_emotion:
                        self._display_emotion(frame, detected_emotion, detected_confidence)
                else:
                    # Show current detection before capture
                    self._display_emotion(frame, emotion, confidence)
                
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
                    detected_emotion = None
                    frame_count = 0
                    print("Restarting emotion detection...")
                
                frame_count += 1
                
                # After 10 seconds, play the song if emotion was detected
                if frame_count >= max_frames:
                    if detected_emotion and detected_confidence >= self.confidence_threshold:
                        print(f"\n🎵 Playing song for emotion: {detected_emotion.upper()}")
                        song_info = self.music_player.get_song_by_emotion(detected_emotion)
                        if song_info:
                            print(f"   Song info: {song_info}")
                            success = self.music_player.play_song(song_info)
                            if success:
                                print("✓ Music playback started successfully")
                                self.last_played_emotion = detected_emotion
                            else:
                                print("✗ Failed to play music")
                        else:
                            print(f"✗ No song found for emotion: {detected_emotion}")
                    else:
                        print(f"✗ Emotion not detected or confidence too low ({detected_confidence:.2%})")
                    
                    # Reset for next cycle
                    frame_count = 0
                    detected_emotion = None
                    detected_confidence = None
        
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
    
    def _display_countdown(self, frame, frame_count, max_frames):
        """
        Display countdown timer on the video frame.
        
        Args:
            frame (np.ndarray): Video frame
            frame_count (int): Current frame number
            max_frames (int): Total frames for 10 seconds
        """
        height, width = frame.shape[:2]
        
        # Calculate elapsed time
        elapsed_time = frame_count / 30  # Assuming 30 fps
        remaining_time = max(0, (max_frames - frame_count) / 30)
        
        # Display countdown
        countdown_text = f"Time: {elapsed_time:.1f}s / {max_frames/30:.1f}s"
        cv2.putText(frame, countdown_text, (width - 300, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        # Display capture status
        if elapsed_time < 6:
            status_text = f"Waiting... ({6 - elapsed_time:.1f}s until capture)"
            cv2.putText(frame, status_text, (20, height - 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
        elif elapsed_time < 10:
            status_text = "📸 Emotion captured! Preparing music..."
            cv2.putText(frame, status_text, (20, height - 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        else:
            status_text = "🎵 Playing song..."
            cv2.putText(frame, status_text, (20, height - 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
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
