import yt_dlp
import os
import json_manager

ffmpeg_path = json_manager.ffmpeg_path

def download_audio(link, save_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',  # Convert to WAV
                'preferredquality': '192',  # Adjust quality if needed
            }
        ],
        'ffmpeg_location': ffmpeg_path,  # Set FFmpeg location
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(link, download=True)  # Download and extract info
            title = info_dict.get('title', 'audio')  # Get title of the video

            downloaded_file_path = save_path + f"/{title}.wav"  # Final output file
            return True, None, downloaded_file_path

        except yt_dlp.utils.DownloadError as e:
            return False, str(e), None  # Return error message if download fails
