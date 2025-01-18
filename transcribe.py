#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import logging
import os
import ssl
import sys
import ffmpeg

import whisper
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# SSL verification bypass (if needed)
ssl._create_default_https_context = ssl._create_unverified_context

# Supported audio formats
SUPPORTED_FORMATS = {".mp3", ".wav", ".m4a", ".ogg", ".wma"}

def convert_audio(input_path: str):
    """Convert audio file to WAV format if needed."""
    try:
        input_path = Path(input_path)
        
        # Check file extension
        if input_path.suffix.lower() in SUPPORTED_FORMATS:
            return str(input_path), False
            
        # Convert to WAV
        output_path = input_path.with_suffix('.wav')
        logger.info(f"Converting audio file: {input_path} -> {output_path}")
        
        stream = ffmpeg.input(str(input_path))
        stream = ffmpeg.output(stream, str(output_path))
        ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
        
        return str(output_path), True
        
    except Exception as e:
        logger.error(f"Conversion error: {str(e)}")
        return None

def transcribe_audio(audio_path: str):
    """Transcribe audio file to text using Whisper."""
    try:
        # Check if file exists
        if not os.path.exists(audio_path):
            logger.error(f"File not found: {audio_path}")
            return None

        # Convert audio format if needed
        conversion_result = convert_audio(audio_path)
        if conversion_result is None:
            logger.error("Audio conversion failed")
            return None
            
        audio_path, was_converted = conversion_result
        audio_path = Path(audio_path)
        
        # Load model
        logger.info("Loading Whisper model (small)...")
        model = whisper.load_model("small")
        
        # Transcribe
        logger.info(f"Transcribing file in Turkish: {audio_path}")
        with tqdm(total=100, desc="Transcribing") as pbar:
            result = model.transcribe(
                str(audio_path),
                language="turkish",
                task="transcribe"
            )
            pbar.update(100)
        
        # Create output file
        output_path = audio_path.parent / f"{audio_path.stem}_transcript_TR.txt"
        
        # Save transcript
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result["text"].strip())
        
        logger.info(f"\nTranscript saved successfully: {output_path}")
        logger.info("\nTranscript content:")
        logger.info("-" * 50)
        logger.info(result["text"].strip())
        logger.info("-" * 50)
        
        # Clean up temporary converted file
        if was_converted and os.path.exists(audio_path):
            os.remove(audio_path)
            logger.info(f"Temporary converted file deleted: {audio_path}")
        
        return str(output_path)
        
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        return None

def main():
    """Main program."""
    if len(sys.argv) != 3:
        logger.error("Invalid number of arguments")
        print("Usage: python transcribe.py <audio_file_path> TR")
        sys.exit(1)
    
    try:
        audio_path = sys.argv[1]
        
        if not os.path.exists(audio_path):
            logger.error(f"File not found: {audio_path}")
            sys.exit(1)
            
        result = transcribe_audio(audio_path)
        if result is None:
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Program error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
