# 🌌 Zenith Downloader

A futuristic, sci-fi themed **YouTube Downloader** with professional features and a smooth, responsive user experience.  
Developed by: **WIA Digital**

---

## ✨ Introduction
Zenith Downloader is not just another YouTube downloader. It is a **powerful desktop tool** engineered for speed, stability, and control — all wrapped in a custom cyberpunk-inspired interface.  

Built with a **multi-threaded architecture**, it stays fully responsive even during heavy download sessions. The backend runs on the reliable [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) engine, ensuring fast and accurate downloads every time.

---

## 🚀 Features

- **Custom Sci-Fi GUI**  
  Unique cyberpunk design built with `CustomTkinter` for clarity and style.  

- **Detailed Progress Dashboard**  
  Real-time info:  
  - File Title + Playlist Progress  
  - Download Status & Live Speed  
  - Size (Downloaded vs Total)  
  - Estimated Time Remaining (ETA)  

- **Selectable Video/Audio Quality**  
  Choose formats:  
  - Video → 1080p, 720p, 480p, 360p  
  - Audio Only → MP3 high-quality extraction  

- **Bulk Downloading**  
  - Manual: Paste up to 5 URLs  
  - Bulk Mode: Load unlimited URLs from `links.txt`  

- **Robust Playlist Handling**  
  Full playlist support with intelligent skipping of unavailable videos.  

- **Persistent Download Location**  
  Your chosen folder is remembered across sessions.  

- **Cancellable Operations**  
  A dedicated STOP button lets you halt downloads gracefully.  

---

## 📖 How to Use

### Manual Downloads
1. Launch the application.  
2. Paste up to 5 YouTube video or playlist URLs.  
3. Select quality from the dropdown.  
4. Click **Initiate Download**.  

### Bulk Mode
1. Create a file named `links.txt` in the app folder.  
2. Add one YouTube URL per line.  
3. Toggle **Bulk Mode** in the app.  
4. Select quality and click **Initiate Download**.  

### Changing the Download Folder
- Click **Change Folder**, choose your destination, and it will be saved for future sessions.  

### Stopping Downloads
- Click the red **Halt Download** button.  
- The current file finishes, then the queue stops.  

---

## 🛠️ Technologies Used

- **Language**: Python 3  
- **Core Engine**: [YT-DLP](https://github.com/yt-dlp/yt-dlp)  
- **GUI**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter), Tkinter  
- **Concurrency**: Python `threading`  
- **Media Processing**: [FFmpeg](https://ffmpeg.org/)  
- **Standard Libraries**: `os`, etc.  

---

⭐ *Zenith Downloader — Efficiency meets Cyberpunk.*  
