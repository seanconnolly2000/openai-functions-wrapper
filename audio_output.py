"""
This module provides functionality related to audio playback.
"""
import os
from typing import Union
from io import BytesIO
import pygame
import pyttsx3


def initialize_audio():
    """
    Initialize the pyttsx3 engine.
    """
    engine = pyttsx3.init()

    # Get the settings from the .env file
    voice_id = os.environ.get("PYTTSX3_VOICE_ID")
    speed = os.environ.get("PYTTSX3_SPEED")

    # Set the voice
    voices = engine.getProperty('voices')
    for v in voices:
        if voice_id in v.id:
            engine.setProperty('voice', v.id)
            break

    # Set the speed
    if speed is not None:
        engine.setProperty('rate', int(speed))

    return engine


def play_audio(audio: Union[bytes, BytesIO]):
    """
    Play audio data using pygame.mixer.

    Args:
        audio (Union[bytes, BytesIO]): The audio data played.
    """

    if not isinstance(audio, (bytes, BytesIO)):
        return
    if isinstance(audio, bytes):
        audio = BytesIO(audio)

    pygame.mixer.music.load(audio)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(10)


def tts_output(engine, text):
    """
    Convert text to speech using pyttsx3.

    Args:
        engine: The pyttsx3 engine.
        text (str): The text to be converted to speech.
    """
    engine.say(text)
    engine.runAndWait()
