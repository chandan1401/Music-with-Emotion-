"""Face detection module using MediaPipe."""
import cv2
import mediapipe as mp

# Initialize MediaPipe Face Detection
mp_face = mp.solutions.face_detection.FaceDetection(
    model_selection=1, 
    min_detection_confidence=0.5
)


def detect_face(frame):
    """
    Detect face in the given frame using MediaPipe.
    
    Args:
        frame: Input image frame (BGR format from OpenCV)
        
    Returns:
        Cropped face region or None if no face detected
    """
    if frame is None or frame.size == 0:
        return None
        
    try:
        results = mp_face.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        if not results.detections:
            return None
            
        # Get first detected face
        detection = results.detections[0]
        h, w, _ = frame.shape
        box = detection.location_data.relative_bounding_box
        
        # Calculate bounding box coordinates
        x = int(box.xmin * w)
        y = int(box.ymin * h)
        w_box = int(box.width * w)
        h_box = int(box.height * h)
        
        # Ensure coordinates are within frame bounds
        x = max(0, x)
        y = max(0, y)
        w_box = min(w_box, w - x)
        h_box = min(h_box, h - y)
        
        return frame[y:y+h_box, x:x+w_box]
        
    except Exception as e:
        print(f"Error in face detection: {e}")
        return None
