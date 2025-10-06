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



class SimulationManager:
    
    SETTINGS_FILE = "conf/config.json"
    
    DEFAULT_SETTINGS = {
        "firewall_directory": "/etc/",
        "reset_rules_file": "conf/firewall_reset.sh",
        "firewall_rules_file": "conf/firewall.sh",
        "server_ports_file": "conf/ports.conf",
        "show_container_id": False,
        "docker_image": "firewall_tester",
        "include_mangle_table": False,
        "include_nat_table": True,
        "include_filter_table": True
    }
    
    # file name path
    save_file_path = None

    # List to store tests
    tests = []
    
    # List of settings in Tkinter string value
    current_settings : dict[str, tk.Variable] = {}
    def __init__(self):
        self.load_settings()

    # buttons list from hosts
    #list_button_servers_onOff = []
    
    # get data from containers and hosts
    #self.containers_data = containers.extract_containerid_hostname_ips( )  # get hosts informations
    
    # get container_id and hostname - used for example to combobox in firewall rules.
    #self.container_hostname = containers.get_containerid_hostname() # container_id and hostname for operations
    #self.hosts = list(map(lambda x: x[1], self.container_hostname)) # hostnames to display
    def update_hosts():
        pass
    
    def load_settings(self) -> dict[str, tk.Variable]:
        settings = {}
        try:
            with open(self.SETTINGS_FILE, "r") as f:
                #print(json.load(f))
                settings = json.load(f)
                
        except (FileNotFoundError, json.JSONDecodeError): 
            settings = self.DEFAULT_SETTINGS.copy()
        
        self.current_settings["firewall_directory"] = tk.StringVar(value=settings.get("firewall_directory", ""))
        self.current_settings["reset_rules_file"] = tk.StringVar(value=settings.get("reset_rules_file", ""))
        self.current_settings["firewall_rules_file"] = tk.StringVar(value=settings.get("firewall_rules_file", ""))
        self.current_settings["server_ports_file"] = tk.StringVar(value=settings.get("server_ports_file", ""))
        self.current_settings["show_container_id"] = tk.BooleanVar(value=settings.get("show_container_id", False))
        self.current_settings["docker_image"] = tk.StringVar(value=settings.get("docker_image", ""))
        self.current_settings["include_filter_table"] = tk.BooleanVar(value=settings.get("include_filter_table", False))
        self.current_settings["include_nat_table"] = tk.BooleanVar(value=settings.get("include_nat_table", False))
        self.current_settings["include_mangle_table"] = tk.BooleanVar(value=settings.get("include_mangle_table", False))
        
        return self.current_settings
        
    def save_settings(self):
        settings = {
            "firewall_directory": self.config_firewall_dir_var.get(),
            "reset_rules_file": self.config_firewall_reset_rules_var.get(),
            "firewall_rules_file": self.config_firewall_rules_var.get(),
            "server_ports_file": self.config_server_ports_var.get(),
            "show_container_id": self.config_show_container_id_var.get(),
            "docker_image": self.config_docker_image_var.get(),
            "include_filter_table": self.config_include_filter_var.get(),
            "include_nat_table": self.config_include_nat_var.get(),
            "include_mangle_table": self.config_include_mangle_var.get()
        }
        with open(self.SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
        
        if self.config_show_container_id_var.get():
            self.tree.column("Container ID", width=130, minwidth=100)
        else:
            self.tree.column("Container ID", width=0, minwidth=0)
            
    def restore_default_settings(self):
        self.config_firewall_dir_var.set(self.simulation.DEFAULT_SETTINGS["firewall_directory"])
        self.config_firewall_reset_rules_var.set(self.simulation.DEFAULT_SETTINGS["reset_rules_file"])
        self.config_firewall_rules_var.set(self.simulation.DEFAULT_SETTINGS["firewall_rules_file"])
        self.config_server_ports_var.set(self.simulation.DEFAULT_SETTINGS["server_ports_file"])
        self.config_show_container_id_var.set(self.simulation.DEFAULT_SETTINGS["show_container_id"])
        self.config_docker_image_var.set(self.simulation.DEFAULT_SETTINGS["docker_image"])
        self.config_include_filter_var.set(self.simulation.DEFAULT_SETTINGS["include_filter_table"])
        self.config_include_nat_var.set(self.simulation.DEFAULT_SETTINGS["include_nat_table"])
        self.config_include_mangle_var.set(self.simulation.DEFAULT_SETTINGS["include_mangle_table"])
        self.save_settings()