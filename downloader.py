# downloader.py

import os
import sys
import yt_dlp
from threading import Lock

# A lock to prevent multiple threads from writing to the console at the same time
print_lock = Lock()

def ytdlp_progress_hook(d, progress_callback=None):
    """
    Progress hook for yt-dlp that can optionally call a GUI callback.
    """
    if progress_callback:
        # Pass the entire dictionary to the GUI for rich updates.
        progress_callback(d)

    # We also keep the console print for debugging purposes, but protect it with a lock.
    with print_lock:
        if d['status'] == 'downloading':
            # Extract download information safely using .get()
            percent_str = d.get('_percent_str', '---%').strip()
            eta_str = d.get('_eta_str', '---s').strip()
            speed_str = d.get('_speed_str', '--- B/s').strip()
            
            # Get playlist info if available
            info = d.get('info_dict', {})
            playlist_info = ''
            if 'playlist_title' in info and 'playlist_index' in info and info.get('n_entries'):
                playlist_info = f" (Playlist: {info['playlist_index']}/{info['n_entries']})"

            # Robustness: Using sys.stdout for better control in threaded environments
            sys.stdout.write(f"\r[Downloader]{playlist_info} {percent_str} | Speed: {speed_str} | ETA: {eta_str}...")
            sys.stdout.flush()
        
        elif d['status'] == 'finished':
            # Avoid printing the finish message for intermediate post-processing steps
            if d.get("postprocessor") is None:
                sys.stdout.write('\n') # Move to the next line for a clean log
                print(f"[Downloader] Finished downloading: {os.path.basename(d.get('filename', 'Unknown File'))}")


def download_video(url: str, output_path: str, quality_choice: str, progress_callback=None, video_subdir="Video", audio_subdir="Audio"):
    """
    Downloads a single YouTube video or audio using yt-dlp, with selectable quality.
    Now includes robust error handling and configurable subdirectories.
    """
    hook = lambda d: ytdlp_progress_hook(d, progress_callback)
    
    # Base options for yt-dlp
    ydl_opts = {
        'progress_hooks': [hook],
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,  # This is key for robust playlist/batch downloads
        'nocheckcertificate': True, # Can help in some network environments
    }

    # --- Dynamically set format based on quality_choice ---
    if "Audio Only (MP3)" in quality_choice:
        ydl_opts['format'] = 'bestaudio/best'
        # Use provided audio subdirectory
        ydl_opts['outtmpl'] = os.path.join(output_path, audio_subdir, '%(title)s.%(ext)s')
        # Add post-processor to convert to MP3
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', # Standard MP3 quality
        }]
    else:
        # Video format selection logic
        if '1080p' in quality_choice:
            format_str = 'bv[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best'
        else:
            height = quality_choice.split('p')
            format_str = f'bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4][height<={height}]'
        
        ydl_opts['format'] = format_str
        # Use provided video subdirectory
        ydl_opts['outtmpl'] = os.path.join(output_path, video_subdir, '%(title)s.%(ext)s')

    # --- Execute Download with improved error handling ---
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(ydl_opts['outtmpl']), exist_ok=True)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download([url])
            if error_code != 0:
                with print_lock:
                    print(f"\n[Downloader] WARNING: yt-dlp returned a non-zero exit code ({error_code}) for {url}. It might have been skipped.")

    except yt_dlp.utils.DownloadError as e:
        # This handles network errors, video unavailability, etc.
        with print_lock:
            print(f"\n[Downloader] DOWNLOAD_ERROR: Could not download {url}. Reason: {e}")
    except Exception as e:
        # This handles unexpected errors in the downloader setup or execution
        with print_lock:
            print(f"\n[Downloader] UNEXPECTED_ERROR: An issue occurred with {url}. Reason: {e}")