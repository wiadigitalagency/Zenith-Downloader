# ui_theme.py

import customtkinter

class SciFiTheme:
    """
    Encapsulates all styling constants for the application UI.
    Configuration over code: All colors and fonts are centralized here.
    """
    # Colors
    BG_COLOR = "#0D0221"
    FRAME_BG_COLOR = "#000000"
    FRAME_BORDER_COLOR = "#00BFFF"
    TEXT_COLOR = "#FFFFFF"
    ACCENT_COLOR = "#00BFFF"
    SECONDARY_TEXT_COLOR = "#A9A9A9"
    BUTTON_HOVER_COLOR = "#00FFFF"
    STOP_BUTTON_COLOR = "#FF0055"
    STOP_BUTTON_HOVER_COLOR = "#FF6699"
    
    # Fonts
    MONO_FONT_FAMILY = ("Consolas", "Lucida Console", "Courier New")
    
    @staticmethod
    def title_font():
        return customtkinter.CTkFont(family=SciFiTheme.MONO_FONT_FAMILY, size=22, weight="bold")

    @staticmethod
    def body_font():
        return customtkinter.CTkFont(family=SciFiTheme.MONO_FONT_FAMILY, size=14)
        
    @staticmethod
    def status_font():
        return customtkinter.CTkFont(family=SciFiTheme.MONO_FONT_FAMILY, size=12, weight="normal")