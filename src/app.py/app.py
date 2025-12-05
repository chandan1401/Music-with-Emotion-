"""Main application for Emotion Music Generator."""
import cv2
import sys
from face_detector import detect_face
from emotion_model import predict_emotion
from music_engine import play_music, stop_music

# Configuration
CAMERA_ID = 0
CONFIDENCE_THRESHOLD = 0.6
WINDOW_NAME = "Emotion Music Generator"
FPS_DISPLAY = True


def main():
    """
    Main application loop for real-time emotion detection and music playing.
    """
    # Initialize video capture
    cap = cv2.VideoCapture(CAMERA_ID)
    
    if not cap.isOpened():
        print(f"Error: Cannot open camera {CAMERA_ID}")
        print("Please ensure your webcam is connected and accessible.")
        sys.exit(1)
    
    # Set camera resolution for better performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    last_emotion = None
    frame_count = 0
    
    print("\n" + "="*50)
    print("Emotion Music Generator Started")
    print("="*50)
    print(f"Confidence Threshold: {CONFIDENCE_THRESHOLD}")
    print("Controls: Press 'Q' to quit")
    print("="*50 + "\n")
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("Error: Failed to read frame from camera")
                break
            
            # Flip frame for selfie-view
            frame = cv2.flip(frame, 1)
            frame_count += 1
            
            # Detect face
            face = detect_face(frame)
            
            if face is not None:
                # Predict emotion
                emotion, conf = predict_emotion(face)
                
                if emotion != 'unknown':
                    # Display emotion and confidence
                    color = (0, 255, 0) if conf > CONFIDENCE_THRESHOLD else (0, 165, 255)
                    cv2.putText(frame, f"{emotion.upper()} ({conf:.2f})",
                               (20, 30), cv2.FONT_HERSHEY_SIMPLEX,
                               1, color, 2)
                    
                    # Change music if emotion changed and confidence is high
                    if emotion != last_emotion and conf > CONFIDENCE_THRESHOLD:
                        print(f"\n-> Emotion changed: {last_emotion} → {emotion} (confidence: {conf:.2f})")
                        play_music(emotion)
                        last_emotion = emotion
            else:
                # Display no face detected message
                cv2.putText(frame, "No face detected",
                           (20, 30), cv2.FONT_HERSHEY_SIMPLEX,
                           1, (0, 0, 255), 2)
            
            # Display FPS if enabled
            if FPS_DISPLAY and frame_count % 10 == 0:
                cv2.putText(frame, f"FPS: {cap.get(cv2.CAP_PROP_FPS):.1f}",
                           (frame.shape[1] - 150, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            
            # Display frame
            cv2.imshow(WINDOW_NAME, frame)
            
            # Check for quit command
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q'):
                print("\nQuitting...")
                break
    
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"\nError in main loop: {e}")
    finally:
        # Cleanup
        stop_music()
        cap.release()
        cv2.destroyAllWindows()
        print("Application closed.\n")


if __name__ == "__main__":
    main()
