import os
import sys
import time
import re

try:
    import yt_dlp
    import requests
    from colorama import Fore, Style, init
except ImportError:
    print("Missing dependencies. Run: pip install colorama requests yt_dlp")
    sys.exit(1)

init(autoreset=True)

DOWNLOADS_PATH = "downloads"
MP3_DOWNLOADS_PATH = os.path.join(DOWNLOADS_PATH, "MP3")
MP4_DOWNLOADS_PATH = os.path.join(DOWNLOADS_PATH, "MP4")
os.makedirs(DOWNLOADS_PATH, exist_ok=True)
os.makedirs(MP3_DOWNLOADS_PATH, exist_ok=True)
os.makedirs(MP4_DOWNLOADS_PATH, exist_ok=True)
HISTORY_FILE = "history.txt"

banner = fr"""{Fore.BLUE + Style.BRIGHT}
    ____       ______      __        _  __
   / __ \__  _/_  __/_  __/ /_  ___ | |/ /
  / /_/ / / / // / / / / / __ \/ _ \|   / 
 / ____/ /_/ // / / /_/ / /_/ /  __/   |    Author: @JfrzxCode
/_/    \__, //_/  \__,_/_.___/\___/_/|_|    Version 1.1
      /____/{Fore.RESET + Style.RESET_ALL}                             
"""

def check_internet() -> bool:
    try:
        return requests.get("https://www.youtube.com", timeout=5).status_code == 200
    except requests.exceptions.RequestException:
        return False

def prefix(text: str) -> str:    
    return f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTBLUE_EX}{text}{Fore.LIGHTBLACK_EX}]{Fore.RESET}"

def validate_url(url: str) -> bool:
    """ Validate YouTube URL with regex. """
    pattern = r"^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]+"
    return bool(re.match(pattern, url))

def get_video_title(url: str) -> str:
    """ Get video title before downloading. """
    options = {'quiet': True, 'no_warnings': True, 'logger': None}
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get('title', 'Unknown Title')
    except:
        return None

def silent_download(url: str, options: dict):
    """ Run yt-dlp without showing logs. """
    try:
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

def save_history(url: str, filename: str):
    """ Save downloaded video details to a file. """
    with open(HISTORY_FILE, "a", encoding="utf-8") as file:
        file.write(f"{filename} - {url}\n")

def download_mp3(url: str, path: str) -> bool:
    title = get_video_title(url)
    if not title:
        print(f"\n{prefix('pytubex')} {Fore.LIGHTRED_EX}Failed to get video info.")
        return False

    options = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'}],
        'quiet': True, 'no_warnings': True, 'logger': None
    }

    try:
        print(f"\n{prefix('pytubex')} {Fore.LIGHTGREEN_EX}Downloading: {title} (MP3)...\n")
        silent_download(url, options)
        save_history(url, f"{title}.mp3")
        print(f"{prefix('pytubex')} {Fore.LIGHTGREEN_EX}MP3 Downloaded Successfully!")
        return True
    except Exception as e:
        print(f"\n{prefix('pytubex')} {Fore.LIGHTRED_EX}Download failed: {e}")
        return False

def download_mp4(url: str, path: str) -> bool:
    title = get_video_title(url)
    if not title:
        print(f"\n{prefix('pytubex')} {Fore.LIGHTRED_EX}Failed to get video info.")
        return False

    options = {
        'format': 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]',
        'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'quiet': True, 'no_warnings': True, 'logger': None
    }

    try:
        print(f"\n{prefix('pytubex')} {Fore.LIGHTGREEN_EX}Downloading: {title} (MP4)...\n")
        silent_download(url, options)
        save_history(url, f"{title}.mp4")
        print(f"{prefix('pytubex')} {Fore.LIGHTGREEN_EX}MP4 Downloaded Successfully!")
        return True
    except Exception as e:
        print(f"\n{prefix('pytubex')} {Fore.LIGHTRED_EX}Download failed: {e}")
        return False

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(banner)
        print(f"{prefix('1')}{Fore.GREEN} Download Video (MP4)")
        print(f"{prefix('2')}{Fore.GREEN} Download Audio (MP3)")
        print(f"{prefix('3')}{Fore.GREEN} View Download History")
        print(f"{prefix('4')}{Fore.GREEN} Exit\n")

        try:
            choice = input(f"{prefix('pytubex')} {Fore.LIGHTBLUE_EX}Option {Fore.LIGHTBLACK_EX}> ")

            if choice == '1':
                url = input(f"\n{prefix('pytubex')} {Fore.LIGHTBLUE_EX}Enter YouTube URL {Fore.LIGHTBLACK_EX}> ")
                if validate_url(url):
                    download_mp4(url, MP4_DOWNLOADS_PATH)
                else:
                    print(f"{prefix('pytubex')} {Fore.LIGHTRED_EX}Invalid URL!")
                time.sleep(1)

            elif choice == '2':
                url = input(f"\n{prefix('pytubex')} {Fore.LIGHTBLUE_EX}Enter YouTube URL {Fore.LIGHTBLACK_EX}> ")
                if validate_url(url):
                    download_mp3(url, MP3_DOWNLOADS_PATH)
                else:
                    print(f"{prefix('pytubex')} {Fore.LIGHTRED_EX}Invalid URL!")
                time.sleep(1)

            elif choice == '3':
                if os.path.exists(HISTORY_FILE):
                    print(f"\n{prefix('pytubex')} {Fore.YELLOW}Download History:\n")
                    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                        for line in file.readlines():
                            print(f"{Fore.LIGHTBLACK_EX}- {line.strip()}")
                else:
                    print(f"\n{prefix('pytubex')} {Fore.LIGHTRED_EX}No downloads yet.")
                input(f"\n{prefix('pytubex')} {Fore.LIGHTBLUE_EX}Press any key to continue..")

            elif choice == '4':
                print(f"\n{prefix('pytubex')} {Fore.GREEN}Goodbye!{Fore.RESET + Style.RESET_ALL}")
                sys.exit(0)

        except KeyboardInterrupt:
            print(f"\n\n{prefix('pytubex')} {Fore.LIGHTYELLOW_EX}Detected Ctrl+C. Exiting...")
            sys.exit(0)

if __name__ == "__main__":
    try:
        if check_internet():
            main()
        else:
            print(f"{prefix('error')} {Fore.LIGHTRED_EX}No internet connection!\n")
            sys.exit(0)
    except KeyboardInterrupt:
        print(f"\n{prefix('pytubex')} {Fore.LIGHTYELLOW_EX}Program interrupted. Exiting...{Fore.RESET}")
        sys.exit(0)
