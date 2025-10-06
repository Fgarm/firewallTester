import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from tkinter import filedialog
import os
import containers
import json
import re
import threading
import webbrowser
import textwrap

class ConfigPage(ttk.Frame):
    def __init__(self, parent: ttk.Widget):
        """
            Create and configura settings for this software.
        """
        super().__init__(parent)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1) 

        content_frame = ttk.Frame(self)
        content_frame.grid(row=0, column=0, sticky="ew", padx=20)
        content_frame.columnconfigure(0, weight=1)
        
        #tittle_frame = tk.Frame(content_frame)
        #tittle_frame.grid(row=0, column=0, pady=(0, 10), sticky="ew")
        
        
        
    def load_settings(self):
        try:
            with open(self.SETTINGS_FILE, "r") as f:
                #print(json.load(f))
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return self.DEFAULT_SETTINGS.copy()