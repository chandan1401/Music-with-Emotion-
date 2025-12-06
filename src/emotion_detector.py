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
            if self.last_emotion:
                return self.last_emotion
            return None, 0.0
        
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
            return None, 0.0
    
    def get_supported_emotions(self):
        """
        Get list of supported emotions.
        
        Returns:
            list: List of emotion names
        """
        return self.emotions
