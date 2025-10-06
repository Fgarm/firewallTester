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

from simulation import SimulationManager

class ConfigPage(ttk.Frame):
    
    simulation = None
    
    def __init__(self, parent: ttk.Widget, simulation: SimulationManager):
        """
            Create and configura settings for this software.
        """
        super().__init__(parent)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1) 

        content_frame = ttk.Frame(self)
        content_frame.grid(row=0, column=0, padx=20, sticky="new")
        content_frame.rowconfigure(0, weight=1)
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        
        #title_frame = tk.Frame(content_frame)
        #title_frame.grid(row=0, column=0, pady=(0, 10), sticky="ew")
        
        
        self.simulation = simulation
        settings = simulation.load_settings()
        
        print("settings loaded:")
        print("firewall_directory:", settings.get("firewall_directory", "").get())
        print("reset_rules_file:", settings.get("reset_rules_file", "").get())
        print("firewall_rules_file:", settings.get("firewall_rules_file", "").get())
        print("server_ports_file:", settings.get("server_ports_file", "").get())
        print("show_container_id:", settings.get("show_container_id", False).get())
        print("docker_image:", settings.get("docker_image", "").get())
        print("include_filter_table:", settings.get("include_filter_table", False).get())
        print("include_nat_table:", settings.get("include_nat_table", False).get())
        print("include_mangle_table:", settings.get("include_mangle_table", False).get())
        
        
        #self.config_firewall_dir_var = tk.StringVar(value=settings.get("firewall_directory", ""))
        #self.config_firewall_reset_rules_var = tk.StringVar(value=settings.get("reset_rules_file", ""))
        #self.config_firewall_rules_var = tk.StringVar(value=settings.get("firewall_rules_file", ""))
        #self.config_server_ports_var = tk.StringVar(value=settings.get("server_ports_file", ""))
        #self.config_show_container_id_var = tk.BooleanVar(value=settings.get("show_container_id", False))
        #self.config_docker_image_var = tk.StringVar(value=settings.get("docker_image", ""))
        #self.config_include_filter_var = tk.BooleanVar(value=settings.get("include_filter_table", False))
        #self.config_include_nat_var = tk.BooleanVar(value=settings.get("include_nat_table", False))
        #self.config_include_mangle_var = tk.BooleanVar(value=settings.get("include_mangle_table", False))

        # Developer Information
        lbl_title = ttk.Label(content_frame, text="Software Settings", font=("Arial", 14, "bold"), anchor="center", justify="center")
        lbl_title.grid(row=0, column=0, pady=(0, 10), sticky="ew")
        
        #buttons_frame = tk.Frame(content_frame)
        #buttons_frame.grid(row=10, column=0, pady=(0, 10), sticky="ew")
        
        ttk.Label(content_frame, text="Firewall Directory in the containers:", anchor="center", justify="center").grid(row=1, column=0, sticky="w")
        ttk.Entry(content_frame, textvariable=self.simulation.current_settings["firewall_directory"], width=40).grid(row=1, column=1)

        ttk.Label(content_frame, text="Reset Rules File:").grid(row=2, column=0, sticky="w")
        ttk.Entry(content_frame, textvariable=self.simulation.current_settings["reset_rules_file"], width=40).grid(row=2, column=1)

        ttk.Label(content_frame, text="Firewall Rules File:").grid(row=3, column=0, sticky="w")
        ttk.Entry(content_frame, textvariable=self.simulation.current_settings["firewall_rules_file"], width=40).grid(row=3, column=1)

        tk.Label(content_frame, text="Server Ports File:").grid(row=4, column=0, sticky="w")
        ttk.Entry(content_frame, textvariable=self.simulation.current_settings["server_ports_file"], width=40).grid(row=4, column=1)

        ttk.Label(content_frame, text="Docker Image Name:").grid(row=5, column=0, sticky="w")
        ttk.Entry(content_frame, textvariable=self.simulation.current_settings["docker_image"], width=40).grid(row=5, column=1)

        ttk.Checkbutton(content_frame, text="Show Container ID Column", variable=self.simulation.current_settings["show_container_id"]).grid(row=6, column=0, columnspan=2, sticky="ew")

        ttk.Checkbutton(content_frame, text="Include Filter Table in Firewall Listing", variable=self.simulation.current_settings["include_filter_table"]).grid(row=7, column=0, columnspan=2, sticky="ew")

        ttk.Checkbutton(content_frame, text="Include Filter NAT in Firewall Listing", variable=self.simulation.current_settings["include_nat_table"]).grid(row=8, column=0, columnspan=2, sticky="ew")

        ttk.Checkbutton(content_frame, text="Include Mangle Table in Firewall Listing", variable=self.simulation.current_settings["include_mangle_table"]).grid(row=9, column=0, columnspan=2, sticky="ew")

        ttk.Button(content_frame, text="Save Settings", command=self.simulation.save_settings).grid(row=10, column=0, columnspan=2, pady=5)
        ttk.Button(content_frame, text="Restore Defaults", command=self.simulation.restore_default_settings).grid(row=11, column=0, columnspan=2, pady=5,)
        
            
    