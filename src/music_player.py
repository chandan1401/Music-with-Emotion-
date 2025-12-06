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
            print("[OK] Pygame mixer initialized successfully")
        except Exception as e:
            print(f"[ERROR] Error initializing pygame mixer: {e}")
        
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
            # Try to find CSV in parent directory if not found in current directory
            if not os.path.exists(csv_path):
                parent_csv_path = os.path.join('..', csv_path)
                if os.path.exists(parent_csv_path):
                    csv_path = parent_csv_path
                else:
                    print(f"[ERROR] {csv_path} not found!")
                    print(f"  Please create {csv_path} with columns: song_name, emotion, path")
                    return False
            
            self.tracks_df = pd.read_csv(csv_path)
            
            # Validate required columns
            required_cols = ['song_name', 'emotion', 'path']
            if not all(col in self.tracks_df.columns for col in required_cols):
                print(f"[ERROR] CSV must contain columns: {required_cols}")
                return False
            
            print(f"[OK] Loaded {len(self.tracks_df)} tracks from {csv_path}")
            
            # Validate that track paths exist and convert to absolute paths
            missing_tracks = []
            for idx, row in self.tracks_df.iterrows():
                track_path = row['path']
                # If path doesn't exist, try parent directory
                if not os.path.exists(track_path):
                    parent_path = os.path.join('..', track_path)
                    if os.path.exists(parent_path):
                        self.tracks_df.at[idx, 'path'] = parent_path
                    else:
                        missing_tracks.append(row['song_name'])
            
            if missing_tracks:
                print(f"[ERROR] Warning: {len(missing_tracks)} tracks not found:")
                for song in missing_tracks:
                    print(f"  - {song}")
            
            return True
            
        except pd.errors.ParserError as e:
            print(f"[ERROR] Error parsing CSV: {e}")
            return False
        except Exception as e:
            print(f"[ERROR] Error loading tracks: {e}")
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
            
            # Try both relative paths
            if not os.path.exists(song_path):
                parent_path = os.path.join('..', song_path)
                if os.path.exists(parent_path):
                    song_path = parent_path
                else:
                    print(f"[ERROR] Track file not found: {song_path}")
                    return False
            
            # Convert to absolute path
            song_path = os.path.abspath(song_path)
            
            # Stop current song if playing
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            
            # Load and play new song
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play(-1)  # -1 means loop
            
            self.current_song = song_name
            self.last_played = song_name
            self.is_playing = True
            
            print(f"[MUSIC] Now playing: {song_name} (from: {song_path})")
            return True
            
        except pygame.error as e:
            print(f"[ERROR] Pygame Error playing song: {e}")
            return False
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            return False
    
    def stop_song(self):
        """Stop current song playback."""
        try:
            pygame.mixer.music.stop()
            self.is_playing = False
            print("[STOP] Music stopped")
        except Exception as e:
            print(f"[ERROR] Error stopping music: {e}")
    
    def pause_song(self):
        """Pause current song playback."""
        try:
            pygame.mixer.music.pause()
            print("[PAUSE] Music paused")
        except Exception as e:
            print(f"[ERROR] Error pausing music: {e}")
    
    def resume_song(self):
        """Resume paused song."""
        try:
            pygame.mixer.music.unpause()
            print("[PLAY] Music resumed")
        except Exception as e:
            print(f"[ERROR] Error resuming music: {e}")
    
    def get_playing_song(self):
        """
        Get currently playing song name.
        
        Returns:
            str: Song name or None
        """
        return self.current_song
