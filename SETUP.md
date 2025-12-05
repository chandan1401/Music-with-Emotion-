# Setup Instructions

## Prerequisites
- Python 3.7+
- VLC Media Player
- Webcam
- At least 2GB free disk space

## Step-by-Step Installation

### 1. Clone or Download the Repository
```bash
git clone https://github.com/yourusername/emotion-music-generator.git
cd emotion-music-generator2
```

### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Packages
```bash
pip install -r requirements.txt
```

### 4. Download Pre-trained Model
- Download the emotion detection model: `emotion_model.h5`
- Place it in the `models/` directory

### 5. Prepare Music Dataset
- Create a CSV file with your music tracks
- Place it in `tracks/` directory
- CSV should have columns: `path`, `emotion`, `name`

### 6. Run the Application
```bash
cd src
python app.py
```

## File Structure Setup

```
emotion-music-generator2/
├── src/
│   ├── app.py
│   ├── emotion_model.py
│   ├── face_detector.py
│   ├── music_engine.py
│   └── ui_streamlit.py
├── models/
│   └── emotion_model.h5          # <- Place pre-trained model here
├── tracks/
│   └── tracks.csv                # <- Place music dataset here
├── requirements.txt
├── README.md
├── SETUP.md
└── .gitignore
```

## Troubleshooting

### Import Errors
If you get import errors, ensure all packages are installed:
```bash
pip install --upgrade -r requirements.txt
```

### Webcam Not Detected
- Check if camera is connected
- Verify camera permissions (especially on macOS/Linux)
- Try: `python -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"`

### Model Not Found
- Download emotion_model.h5 from the releases
- Place in `models/` directory
- Ensure file path is correct in `emotion_model.py`

### No Audio Playing
- Install VLC Media Player
- Check audio device is connected
- Verify tracks.csv exists and has correct paths

### Out of Memory
- Reduce video resolution in app.py
- Enable GPU acceleration if available
- Process fewer frames per second

## Configuration

### Performance Tuning
Edit `src/app.py`:
```python
CONFIDENCE_THRESHOLD = 0.6  # Increase for stricter emotion matching
CAMERA_ID = 0               # Change if multiple cameras connected
```

### Custom Emotions
Edit `src/music_engine.py`:
```python
emotion_map = {
    "custom": ("characteristic1", "characteristic2"),
}
```

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.7 | 3.10+ |
| RAM | 4GB | 8GB+ |
| GPU | None | NVIDIA (optional) |
| Disk Space | 2GB | 5GB+ |

## Next Steps

1. Read the [README.md](README.md) for features and usage
2. Check [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
3. Review the code structure in the source files
4. Customize emotions and music mapping as needed

## Support

For detailed help, see the main [README.md](README.md) file.
