# Speech-to-Text Transcription Tool

A simple yet powerful tool to transcribe audio files to text using OpenAI's Whisper model. Currently optimized for Turkish language transcription, but can be easily modified for other languages.

## Features

- Supports multiple audio formats (mp3, wav, m4a, ogg, wma, etc.)
- Automatic audio format conversion using ffmpeg
- Clean and simple command-line interface
- Detailed logging for better debugging
- Saves transcriptions to text files

## Prerequisites

- Python 3.8 or higher
- ffmpeg (for audio conversion)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ooguza/speech-to-text.git
cd speech-to-text
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

3. Install ffmpeg:
- On macOS:
```bash
brew install ffmpeg
```
- On Ubuntu/Debian:
```bash
sudo apt-get install ffmpeg
```
- On Windows:
Download from [ffmpeg website](https://ffmpeg.org/download.html)

## Usage

1. Place your audio files in the `audio` directory
2. Run the transcription script:
```bash
./transcribe.sh
```

The script will:
1. Look for audio files in the `audio` directory
2. Convert them to a compatible format if needed
3. Transcribe them using Whisper
4. Save the transcriptions as text files in the same directory

## Changing Whisper Models

The script currently uses the "small" Whisper model. You can change it to other models for better accuracy:

- `tiny` (39M parameters) - Fastest, lowest quality
- `base` (74M) - Fast, basic quality
- `small` (244M) - Current default, good balance
- `medium` (769M) - Better quality, slower
- `large` (1.5GB) - Best quality, slowest

To change the model, edit `transcribe.py` and modify this line:
```python
model = whisper.load_model("small")  # Change "small" to your preferred model
```

Note: Larger models require more RAM and processing power, but generally provide better transcription quality.

## File Structure

```
speech-to-text/
├── README.md
├── requirements.txt
├── transcribe.py        # Main Python script
├── transcribe.sh        # Shell script wrapper
└── audio/              # Directory for audio files
```

## Contributing

Feel free to open issues or submit pull requests. Some ideas for contributions:
- Add support for more languages
- Implement batch processing
- Add a progress bar for long transcriptions
- Create a web interface

## License

MIT License - see LICENSE file for details
