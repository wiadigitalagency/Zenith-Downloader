# app.py

import customtkinter
import downloader
import threading
import os
import json
from tkinter import filedialog
from ui_theme import SciFiTheme # Modular Architecture (SoC)

# --- CONFIGURATION MANAGER ---
class ConfigManager:
    """Handles loading and saving application configuration from a JSON file."""
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        """Loads configuration from the JSON file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Fallback to a default configuration if file is missing or corrupt
            # In a real-world scenario, you might want to create a default file here.
            print("ERROR: config.json not found or corrupted. Using fallback.")
            return json.loads("""
                {"general": {"app_name": "Zenith Downloader", "author": "Sardar Wafa Abbas", "config_file_name": "zenith_config.json"},
                 "downloader": {"quality_options": ["1080p", "720p", "Audio Only (MP3)"], "manual_mode_url_limit": 5, "bulk_mode_file": "links.txt", "default_output_path": "downloads", "video_subdirectory": "Video", "audio_subdirectory": "Audio"},
                 "ui_text": {"title_manual_mode": ">> ENTER URLS (MAX %d) <<", "title_bulk_mode": ">> BULK MODE <<", "bulk_mode_label": "Bulk Mode (from %s)"}}
            """)

    def get(self, key, default=None):
        """Get a value from the nested config dictionary."""
        keys = key.split('.')
        value = self.config
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default


# --- MAIN APPLICATION ---
class App(customtkinter.CTk):
    def __init__(self, config: ConfigManager):
        super().__init__()
        
        self.config = config
        self.stop_event = threading.Event()
        self.output_path_config_file = self.config.get('general.config_file_name', 'zenith_config.json')
        self.output_path = self._load_saved_output_path()
        os.makedirs(self.output_path, exist_ok=True)
        
        self.configure(fg_color=SciFiTheme.BG_COLOR)
        customtkinter.set_appearance_mode("Dark")

        self.title(f"{self.config.get('general.app_name')} :: By {self.config.get('general.author')}")
        self.geometry("820x550")
        self.grid_columnconfigure(0, weight=1)

        # Modular UI creation for better SoC
        self._create_input_frame()
        self._create_options_frame()
        self._create_path_frame()
        self._create_action_buttons()
        self._create_progress_dashboard()
        self._create_footer()

    # --- UI Creation Methods (SoC Principle) ---
    def _create_input_frame(self):
        self.input_frame = customtkinter.CTkFrame(self, fg_color=SciFiTheme.FRAME_BG_COLOR, border_color=SciFiTheme.FRAME_BORDER_COLOR, border_width=2, corner_radius=0)
        self.input_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        url_limit = self.config.get('downloader.manual_mode_url_limit', 5)
        self.title_label_text = self.config.get('ui_text.title_manual_mode', '>> ENTER URLS (MAX %d) <<') % url_limit
        self.title_label = customtkinter.CTkLabel(self.input_frame, text=self.title_label_text, font=SciFiTheme.title_font(), text_color=SciFiTheme.ACCENT_COLOR)
        self.title_label.grid(row=0, column=0, padx=20, pady=(10, 5))
        
        self.url_textbox = customtkinter.CTkTextbox(self.input_frame, font=SciFiTheme.body_font(), height=120, corner_radius=0, border_width=1, border_color=SciFiTheme.FRAME_BORDER_COLOR, text_color=SciFiTheme.TEXT_COLOR, fg_color=SciFiTheme.BG_COLOR)
        self.url_textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.url_textbox.insert("0.0", "https://www.youtube.com/watch?v=...\n")

    def _create_options_frame(self):
        self.options_frame = customtkinter.CTkFrame(self, fg_color=SciFiTheme.BG_COLOR)
        self.options_frame.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        self.options_frame.grid_columnconfigure((0, 1), weight=1)
        
        quality_options = self.config.get('downloader.quality_options', [])
        self.quality_menu = customtkinter.CTkOptionMenu(self.options_frame, values=quality_options, font=SciFiTheme.body_font(), corner_radius=0, fg_color=SciFiTheme.FRAME_BG_COLOR, button_color=SciFiTheme.FRAME_BORDER_COLOR, button_hover_color=SciFiTheme.BUTTON_HOVER_COLOR, text_color=SciFiTheme.TEXT_COLOR, dropdown_font=SciFiTheme.body_font(), dropdown_fg_color=SciFiTheme.FRAME_BG_COLOR, dropdown_hover_color=SciFiTheme.FRAME_BORDER_COLOR)
        self.quality_menu.grid(row=0, column=0, sticky="ew", ipady=5, padx=(0, 5))
        
        bulk_file = self.config.get('downloader.bulk_mode_file', 'links.txt')
        bulk_label_text = self.config.get('ui_text.bulk_mode_label', 'Bulk Mode (from %s)') % bulk_file
        self.bulk_mode_switch = customtkinter.CTkSwitch(self.options_frame, text=bulk_label_text, font=SciFiTheme.body_font(), text_color=SciFiTheme.SECONDARY_TEXT_COLOR, progress_color=SciFiTheme.ACCENT_COLOR, command=self.toggle_bulk_mode)
        self.bulk_mode_switch.grid(row=0, column=1, sticky="e", padx=(5, 0))
    
    def _create_path_frame(self):
        self.path_frame = customtkinter.CTkFrame(self, fg_color=SciFiTheme.FRAME_BG_COLOR, border_color=SciFiTheme.FRAME_BORDER_COLOR, border_width=1, corner_radius=0)
        self.path_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        self.path_frame.grid_columnconfigure(0, weight=1)

        self.output_path_label = customtkinter.CTkLabel(self.path_frame, text=f"Output: {os.path.abspath(self.output_path)}", font=SciFiTheme.status_font(), text_color=SciFiTheme.SECONDARY_TEXT_COLOR, anchor="w", wraplength=600)
        self.output_path_label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        self.change_folder_button = customtkinter.CTkButton(self.path_frame, text="Change Folder", font=SciFiTheme.body_font(), command=self.select_output_folder, corner_radius=0, fg_color=SciFiTheme.FRAME_BG_COLOR, border_width=1, border_color=SciFiTheme.FRAME_BORDER_COLOR, hover_color=SciFiTheme.FRAME_BORDER_COLOR)
        self.change_folder_button.grid(row=0, column=1, padx=10, pady=5)
    
    def _create_action_buttons(self):
        self.button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.download_button = customtkinter.CTkButton(self.button_frame, text="INITIATE DOWNLOAD", font=SciFiTheme.title_font(), command=self.start_download_thread, corner_radius=0, fg_color=SciFiTheme.FRAME_BORDER_COLOR, hover_color=SciFiTheme.BUTTON_HOVER_COLOR, text_color="#000000")
        self.download_button.pack(fill="x", ipady=8)
        self.stop_button = customtkinter.CTkButton(self.button_frame, text="HALT DOWNLOAD", font=SciFiTheme.title_font(), command=self.stop_download, corner_radius=0, fg_color=SciFiTheme.STOP_BUTTON_COLOR, hover_color=SciFiTheme.STOP_BUTTON_HOVER_COLOR, text_color="#000000")

    def _create_progress_dashboard(self):
        self.progress_dashboard = customtkinter.CTkFrame(self, fg_color=SciFiTheme.FRAME_BG_COLOR, border_color=SciFiTheme.FRAME_BORDER_COLOR, border_width=2, corner_radius=0)
        self.progress_dashboard.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="nsew")
        self.progress_dashboard.grid_columnconfigure(0, weight=1)
        
        self.video_title_label = customtkinter.CTkLabel(self.progress_dashboard, text="TARGET: awaiting coordinates...", anchor="w", wraplength=780, font=SciFiTheme.body_font(), text_color=SciFiTheme.TEXT_COLOR)
        self.video_title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 2), sticky="ew")
        self.status_label = customtkinter.CTkLabel(self.progress_dashboard, text="SYS.STATUS: Idle", anchor="w", font=SciFiTheme.status_font(), text_color=SciFiTheme.SECONDARY_TEXT_COLOR)
        self.status_label.grid(row=1, column=0, columnspan=3, padx=10, pady=2, sticky="ew")
        
        self.progress_bar = customtkinter.CTkProgressBar(self.progress_dashboard, corner_radius=0, fg_color=SciFiTheme.BG_COLOR, progress_color=SciFiTheme.ACCENT_COLOR)
        self.progress_bar.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.progress_bar.set(0)
        self.percentage_label = customtkinter.CTkLabel(self.progress_dashboard, text="0.0%", font=SciFiTheme.body_font(), text_color=SciFiTheme.ACCENT_COLOR)
        self.percentage_label.grid(row=2, column=2, padx=(5, 10), sticky="e")
        
        self.stats_frame = customtkinter.CTkFrame(self.progress_dashboard, fg_color="transparent")
        self.stats_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        self.stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.size_label = customtkinter.CTkLabel(self.stats_frame, text="SIZE: 0 / 0", font=SciFiTheme.status_font(), text_color=SciFiTheme.SECONDARY_TEXT_COLOR)
        self.size_label.grid(row=0, column=0, sticky="w")
        self.speed_label = customtkinter.CTkLabel(self.stats_frame, text="SPEED: 0 MB/s", font=SciFiTheme.status_font(), text_color=SciFiTheme.SECONDARY_TEXT_COLOR)
        self.speed_label.grid(row=0, column=1, sticky="w")
        self.eta_label = customtkinter.CTkLabel(self.stats_frame, text="ETA: --s", font=SciFiTheme.status_font(), text_color=SciFiTheme.SECONDARY_TEXT_COLOR)
        self.eta_label.grid(row=0, column=2, sticky="w")
    
    def _create_footer(self):
        self.footer_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.footer_frame.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="se")
        credit_text = f"By: {self.config.get('general.author', 'Anonymous')}"
        self.credit_label = customtkinter.CTkLabel(self.footer_frame, text=credit_text, font=SciFiTheme.status_font(), text_color=SciFiTheme.SECONDARY_TEXT_COLOR)
        self.credit_label.grid(row=0, column=0, sticky="e")

    # --- Helper & Logic Methods ---
    def _format_bytes(self, size):
        """BUG FIX: Implemented missing utility function to format bytes."""
        if size is None: return "0 B"
        power, n = 1024, 0
        power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while size > power and n < len(power_labels):
            size /= power
            n += 1
        return f"{size:.2f} {power_labels[n]}B"

    def _load_saved_output_path(self):
        """Loads the last used output path from a simple text file."""
        try:
            with open(self.output_path_config_file, "r") as f:
                path = f.read().strip()
                if path and os.path.isdir(path): return path
        except FileNotFoundError:
            pass
        return self.config.get('downloader.default_output_path', 'downloads')

    def _save_output_path(self):
        """Saves the current output path for future sessions."""
        with open(self.output_path_config_file, "w") as f:
            f.write(self.output_path)

    def select_output_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path = path
            self.output_path_label.configure(text=f"Output: {os.path.abspath(self.output_path)}")
            self._save_output_path()

    def toggle_bulk_mode(self):
        if self.bulk_mode_switch.get() == 1:
            bulk_mode_title = self.config.get('ui_text.title_bulk_mode', '>> BULK MODE ENGAGED <<')
            bulk_mode_file = self.config.get('downloader.bulk_mode_file', 'links.txt')
            self.title_label.configure(text=bulk_mode_title)
            self.url_textbox.configure(state="disabled", text_color="gray")
            self.url_textbox.delete("0.0", "end")
            self.url_textbox.insert("0.0", f"BULK MODE ACTIVE: Sourcing URLs from {bulk_mode_file}")
        else:
            self.title_label.configure(text=self.title_label_text)
            self.url_textbox.configure(state="normal", text_color=SciFiTheme.TEXT_COLOR)
            self.url_textbox.delete("0.0", "end")
            self.url_textbox.insert("0.0", "https://www.youtube.com/watch?v=...\n")

    def reset_progress_ui(self):
        self.status_label.configure(text="SYS.STATUS: standby...")
        self.video_title_label.configure(text="TARGET: awaiting coordinates...")
        self.progress_bar.set(0)
        self.percentage_label.configure(text="0.0%")
        self.size_label.configure(text="SIZE: 0 / 0")
        self.speed_label.configure(text="SPEED: 0 B/s")
        self.eta_label.configure(text="ETA: --s")
        self.update_idletasks() # Ensures UI updates are rendered immediately

    def start_download_thread(self):
        self.stop_event.clear()
        self.url_textbox.configure(state="disabled")
        self.download_button.pack_forget()
        self.stop_button.pack(fill="x", ipady=8)
        self.reset_progress_ui()
        threading.Thread(target=self.run_downloader, daemon=True).start()

    def stop_download(self):
        self.status_label.configure(text="SYS.STATUS: Halting process... Awaiting current file to finish.")
        self.stop_event.set()
        self.stop_button.configure(state="disabled", text="...HITTING THE BRAKES...")

    def run_downloader(self):
        # Robustness: Use try-finally to ensure UI is always restored
        try:
            urls = self._get_urls_from_source()
            if not urls:
                self.restore_ui_state()
                return # Exit if no URLs were found or validation failed
            
            selected_quality = self.quality_menu.get()
            total_targets = len(urls)
            video_subdir = self.config.get('downloader.video_subdirectory', 'Video')
            audio_subdir = self.config.get('downloader.audio_subdirectory', 'Audio')
            
            for i, url in enumerate(urls, 1):
                if self.stop_event.is_set():
                    self.status_label.configure(text=f"SYS.STATUS: Download halted by user. {i-1} targets processed.")
                    break
                
                self.status_label.configure(text=f"SYS.STATUS: Processing target {i} of {total_targets}...")
                self.video_title_label.configure(text=f"TARGET: {url}...")
                self.update_idletasks()

                downloader.download_video(url, self.output_path, selected_quality,
                                          progress_callback=self.update_progress,
                                          video_subdir=video_subdir, audio_subdir=audio_subdir)
            
            if not self.stop_event.is_set():
                self.status_label.configure(text=f"SYS.STATUS: All {total_targets} transfers complete. Mission accomplished.")
        
        except Exception as e:
            self.status_label.configure(text=f"SYS.CRITICAL_ERROR: {e}")
            print(f"A critical error occurred in the download thread: {e}")
        
        finally:
            self.after(0, self.restore_ui_state)

    def _get_urls_from_source(self):
        """Modular logic to get URLs from either the textbox or bulk file."""
        if self.bulk_mode_switch.get() == 1:
            bulk_file = self.config.get('downloader.bulk_mode_file', 'links.txt')
            try:
                with open(bulk_file, "r") as f:
                    urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                if not urls:
                    self.status_label.configure(text=f"SYS.ERROR: {bulk_file} is empty or contains no valid URLs.")
                    return None
                return urls
            except FileNotFoundError:
                self.status_label.configure(text=f"SYS.ERROR: {bulk_file} not found.")
                return None
        else:
            urls = [url.strip() for url in self.url_textbox.get("1.0", "end").split("\n") if url.strip()]
            limit = self.config.get('downloader.manual_mode_url_limit', 5)
            if len(urls) > limit:
                self.status_label.configure(text=f"SYS.ERROR: Max {limit} links/playlists in manual mode.")
                return None
            if not urls:
                self.status_label.configure(text="SYS.ERROR: No target vectors provided.")
                return None
            return urls
            
    def update_progress(self, progress_dict):
        # GUI updates must run on the main thread, self.after ensures this.
        self.after(0, self.update_gui_elements, progress_dict)
    
    def update_gui_elements(self, p):
        """Refactored to safely handle progress dictionary keys."""
        status = p.get('status')
        info = p.get('info_dict', {})
        
        title = info.get('title', self.video_title_label.cget("text"))
        if 'playlist_index' in info and 'n_entries' in info:
            title = f"({info.get('playlist_index')}/{info.get('n_entries')}) {info.get('title', '')}"
        self.video_title_label.configure(text=f"TARGET: {title}")

        if status == 'downloading':
            dl_bytes = p.get('downloaded_bytes')
            total_bytes = p.get('total_bytes') or p.get('total_bytes_estimate')
            
            self.speed_label.configure(text=f"SPEED: {p.get('_speed_str', '-')}")
            self.eta_label.configure(text=f"ETA: {p.get('_eta_str', '-')}")
            
            if dl_bytes and total_bytes:
                progress = dl_bytes / total_bytes
                self.progress_bar.set(progress)
                self.percentage_label.configure(text=f"{progress * 100:.1f}%")
                self.size_label.configure(text=f"SIZE: {self._format_bytes(dl_bytes)} / {self._format_bytes(total_bytes)}")
        
        elif status == 'finished' and p.get('postprocessor') is None:
            total_bytes = p.get('total_bytes') or p.get('downloaded_bytes')
            self.progress_bar.set(1)
            self.percentage_label.configure(text="100.0%")
            if total_bytes:
                self.size_label.configure(text=f"SIZE: {self._format_bytes(total_bytes)} / {self._format_bytes(total_bytes)}")
            self.speed_label.configure(text="SPEED: complete")
            self.eta_label.configure(text="ETA: 0s")

    def restore_ui_state(self):
        """Restores the UI to its initial, ready state."""
        self.stop_button.pack_forget()
        self.download_button.pack(fill="x", ipady=8)
        self.stop_button.configure(state="normal", text="HALT DOWNLOAD")
        # Only re-enable the textbox if not in bulk mode
        if self.bulk_mode_switch.get() == 0:
            self.url_textbox.configure(state="normal")

if __name__ == "__main__":
    config_manager = ConfigManager()
    app = App(config=config_manager)
    app.mainloop()