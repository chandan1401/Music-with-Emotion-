# Emotion Music Generator 🎵😊

An intelligent real-time emotion detection and music recommendation system that analyzes facial expressions and plays music matching the detected emotion.

## Features

✨ **Real-time Facial Emotion Detection** - Uses deep learning to detect emotions from webcam feed  
🎵 **Intelligent Music Matching** - Automatically plays music based on detected emotions  
📊 **7 Emotion Categories** - Recognizes happy, sad, angry, disgust, fear, surprise, and neutral  
🚀 **Real-time Processing** - Optimized for live streaming and instant feedback  
🎯 **High Accuracy** - Deep learning model trained on emotional facial expressions  

## Emotions Supported

- 😊 Happy
- 😢 Sad
- 😠 Angry
- 🤢 Disgust
- 😨 Fear
- 😮 Surprise
- 😐 Neutral

## Tech Stack

- **Computer Vision**: OpenCV, MediaPipe
- **Deep Learning**: TensorFlow/Keras
- **Face Detection**: MediaPipe Face Detection
- **Data Processing**: NumPy, Pandas
- **Audio Playback**: VLC Media Player
- **UI**: Streamlit (optional)

## Installation

### Prerequisites
- Python 3.7 or higher
- Webcam
- VLC Media Player

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/emotion-music-generator.git
cd emotion-music-generator2
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download the emotion model**
```bash
# The model should be placed in the models/ directory
# File: models/emotion_model.h5
```

5. **Prepare your music dataset**
```bash
# Place your music tracks CSV file in the tracks/ directory
# File: tracks.csv with columns: path, emotion
```

## Project Structure

```
emotion-music-generator2/
├── src/
│   ├── app.py                 # Main application entry point
│   ├── emotion_model.py       # Emotion prediction model
│   ├── face_detector.py       # Face detection using MediaPipe
│   ├── music_engine.py        # Music playback engine
│   └── ui_streamlit.py        # Streamlit UI (optional)
├── models/
│   └── emotion_model.h5       # Pre-trained emotion detection model
├── tracks/
│   └── archive (3)/
│       ├── artists.csv        # Artist information
│       ├── dict_artists.json  # Artist dictionary
│       └── tracks.csv         # Music tracks database
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Usage

### Running the Main Application

```bash
cd src
python app.py
```

The application will:
1. Open your webcam feed in a window titled "Emotion Music Generator"
2. Detect faces in real-time
3. Predict emotions from detected faces
4. Automatically play music matching the detected emotion
5. Update music when emotion changes (with >60% confidence)

**Controls:**
- Press `Q` to quit the application

### Running with Streamlit UI (Optional)

```bash
cd src
streamlit run ui_streamlit.py
```

## How It Works

1. **Face Detection**: Uses MediaPipe to detect faces in each frame
2. **Preprocessing**: Converts detected face to grayscale and resizes to 48x48 pixels
3. **Emotion Prediction**: Feeds preprocessed face to TensorFlow model
4. **Music Matching**: Maps detected emotion to music tracks
5. **Playback**: Uses VLC to play selected music track

## Configuration

### Emotion Confidence Threshold
Edit the confidence threshold in `src/app.py`:
```python
if emotion != last_emotion and conf > 0.6:  # Adjust 0.6 threshold
```

### Music Mapping
Customize emotion-to-music mapping in `src/music_engine.py`:
```python
emotion_map = {
    "happy":  ("high", "high"),
    "sad":    ("low", "low"),
    "angry":  ("medium","high"),
    "neutral":("mid","mid"),
}
```

## Requirements

See `requirements.txt` for all dependencies:
- opencv-python==4.10.0.84
- deepface==0.0.93
- tensorflow==2.17.0
- numpy==1.26.4
- pandas==2.2.2
- pygame==2.6.0
- mediapipe==0.10.14

## Performance Optimization

- **GPU Support**: Install `tensorflow-gpu` for faster inference on NVIDIA GPUs
- **Model Selection**: MediaPipe uses model_selection=1 for faster detection
- **Detection Confidence**: Minimum detection confidence set to 0.5

## Known Limitations

- Requires a pre-trained emotion model file
- Music selection depends on CSV data quality
- Single face detection at a time
- VLC Media Player must be installed for audio playback

## Future Enhancements

- [ ] Multi-face emotion detection
- [ ] Web-based UI with Flask/FastAPI
- [ ] Spotify integration for music streaming
- [ ] Emotion statistics and history tracking
- [ ] Model fine-tuning capabilities
- [ ] Real-time video recording with emotion overlay

## Troubleshooting

### Issue: Model file not found
**Solution**: Ensure `models/emotion_model.h5` exists in the correct path

### Issue: No webcam detected
**Solution**: Verify webcam is connected and accessible; check camera permissions

### Issue: Audio not playing
**Solution**: Install VLC Media Player and ensure `python-vlc` is properly installed

### Issue: Memory errors with TensorFlow
**Solution**: Use GPU acceleration or reduce frame processing frequency

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Author

Created by [Your Name]

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Acknowledgments

- MediaPipe for face detection
- TensorFlow/Keras for deep learning
- OpenCV for computer vision processing
- VLC for media playback
