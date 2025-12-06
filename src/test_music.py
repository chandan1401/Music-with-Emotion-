"""
Quick test script to verify music playing works
"""

import pygame
import os
import time

# Initialize pygame mixer
pygame.mixer.init()
print("✓ Pygame mixer initialized")

# Test songs
songs = [
    '../tracks/happy-background-music-442792 (1).mp3',
    '../tracks/sad-dramatic-piano-sad-alone-drama-262415.mp3',
    '../tracks/must-be-angry-259502.mp3',
    '../tracks/pondering-weak-and-weary-193890.mp3',
]

for song_path in songs:
    if os.path.exists(song_path):
        abs_path = os.path.abspath(song_path)
        print(f"\n✓ File exists: {song_path}")
        print(f"  Absolute path: {abs_path}")
        
        try:
            pygame.mixer.music.load(abs_path)
            pygame.mixer.music.play()
            print(f"  ▶ Playing... ({os.path.getsize(abs_path) / 1024 / 1024:.2f} MB)")
            
            # Play for 3 seconds
            time.sleep(3)
            pygame.mixer.music.stop()
            print(f"  ⏹ Stopped")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    else:
        print(f"\n✗ File not found: {song_path}")

pygame.mixer.quit()
print("\n✓ Test complete")
