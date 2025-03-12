# PyTubeX - YouTube Video & Audio Downloader

![ZeroRAT](https://img.shields.io/badge/version-1.0-blue.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg)

## Overview
PyTubeX is a command-line tool for downloading YouTube videos and audio files with high quality. It uses `yt-dlp` for efficient downloading and supports MP3 and MP4 formats.

![image](https://github.com/user-attachments/assets/cb86b5b9-a6d3-4970-b70c-f02c5dd6731e)

## Features
- Download YouTube videos in MP4 format.
- Extract audio in high-quality MP3 format.
- Automatic folder organization.
- Simple and intuitive CLI interface.
- Saves download history.

## Installation

Clone the repository:
```sh
git clone https://github.com/jfrzz/PyTubeX.git
```
Navigate into the folder:
```sh
cd PyTubeX
```

Ensure you have Python installed, then run:
```sh
pip install colorama requests yt_dlp
```

## Usage
Run the script:
```sh
python PyTubeX.py
```
### Options:
1. **Download Video (MP4)** - Enter a YouTube URL to download as MP4.
2. **Download Audio (MP3)** - Enter a YouTube URL to download as MP3.
3. **View Download History** - Displays previously downloaded files.
4. **Exit** - Closes the program.

## Folder Structure
```
PyTubeX/
│── downloads/
│   ├── MP3/
│   ├── MP4/
│── PyTubeX.py
│── history.txt
│── README.md
```

## Dependencies
- Python 3.6+
- `yt-dlp`
- `requests`
- `colorama`

## License
This project is licensed under the MIT License.

## Author
Developed by @JfrzxCode.

