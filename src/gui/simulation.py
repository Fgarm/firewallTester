from collections import Counter
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
from utils import ListVar


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
    
    hosts : ListVar
    containers_data = []
    container_hostname = []
    containers : list[dict[str, ]]
    
    def __init__(self):
        
        self.load_settings()
        self.update_hosts()
        # get data from containers and hosts
        # get container_id and hostname - used for example to combobox in firewall rules.
        
    def update_hosts(self):
        """
            Updates all host/container data - checks for example if any container was created or deleted, if any network configuration changed, etc.
        """
        self.containers_data = containers.extract_containerid_hostname_ips()  # get hosts informations
        if self.containers_data:
            self.hosts_display = [f"{c['hostname']} ({c['ip']})" for c in self.containers_data]
        else: # if there are no elements it displays a message
            self.hosts_display = ["HOSTS (0.0.0.0)", "HOSTS (0.0.0.0)"]
            messagebox.showerror("Error", "Unable to get a response from the hosts! \n Is GNS3 or the hosts running?")
        
        self.container_hostname = containers.get_containerid_hostname() # container_id and hostname for operations
        #print(map(lambda x: x[1], self.container_hostname))
        print("aqui\n")
        #print(list(map(lambda x: x[1], self.container_hostname)))
        #print("aqui2\n")
        updated_hosts = ListVar(value=list(map(lambda x: x[1], self.container_hostname))) # hostnames to display
        try:
            if((Counter(self.hosts.get()) != Counter(updated_hosts.get()))):
                self.hosts.set(value=updated_hosts.get())
                self.hosts_start_servers()
            else:
                return
        except AttributeError:
            self.hosts = updated_hosts
        
    
    def getContainersByImageName(self) -> list[dict[str, ]]:
        self.containers : list[dict[str, ]] = containers.getContainersByImageName()
        return self.containers
    
    def host_check_server_on_off(self, container_id):
        """
            Checks if the server is on or off (server is serve.py in each container/host).

            Args:
                container_id: Container ID.
        """
        #print(f"Check if server is on or off at container {container_id}")
        cmd = 'docker exec '+ container_id +' ps ax | grep "/usr/local/bin/python ./server.py" | grep -v grep'
        result = containers.run_command_shell(cmd)
        if result !="":
            return "on"
        else:
            return "off"
    
    def hosts_start_servers(self):
        """
            Start all the servers in the containers, use server.py for this.
        """
        pass
        
        print("start_servers")
        # TODO - check if there was an error when starting the server and in which container.
        for container in self.containers_data:
            container_id = container["id"]
            containers.start_server(container_id)
        
        
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
            "firewall_directory": self.current_settings["firewall_directory"].get(),
            "reset_rules_file": self.current_settings["reset_rules_file"].get(),
            "firewall_rules_file": self.current_settings["firewall_rules_file"].get(),
            "server_ports_file": self.current_settings["server_ports_file"].get(),
            "show_container_id": self.current_settings["show_container_id"].get(),
            "docker_image": self.current_settings["docker_image"].get(),
            "include_filter_table": self.current_settings["include_filter_table"].get(),
            "include_nat_table": self.current_settings["include_nat_table"].get(),
            "include_mangle_table": self.current_settings["include_mangle_table"].get()
        }
        with open(self.SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
        
        #if self.current_settings["show_container_id"].get(): # Não necessário caso seja feito uso do trace
        #    self.tree.column("Container ID", width=130, minwidth=100)
        #else:
        #    self.tree.column("Container ID", width=0, minwidth=0)
            
    def restore_default_settings(self):
        self.current_settings["firewall_directory"].set(self.DEFAULT_SETTINGS["firewall_directory"])
        self.current_settings["reset_rules_file"].set(self.DEFAULT_SETTINGS["reset_rules_file"])
        self.current_settings["firewall_rules_file"].set(self.DEFAULT_SETTINGS["firewall_rules_file"])
        self.current_settings["server_ports_file"].set(self.DEFAULT_SETTINGS["server_ports_file"])
        self.current_settings["show_container_id"].set(self.DEFAULT_SETTINGS["show_container_id"])
        self.current_settings["docker_image"].set(self.DEFAULT_SETTINGS["docker_image"])
        self.current_settings["include_filter_table"].set(self.DEFAULT_SETTINGS["include_filter_table"])
        self.current_settings["include_nat_table"].set(self.DEFAULT_SETTINGS["include_nat_table"])
        self.current_settings["include_mangle_table"].set(self.DEFAULT_SETTINGS["include_mangle_table"])
        self.save_settings()
        
        
    def hosts_save_ports_in_file(self, container_id, ports_list : ttk.Treeview):
        """
            Saves the ports and protocols of the Treeview in a file, in the format "port/protocol".

            Args:
                ports_table: The Treeview containing the columns "Protocol" and "Port".
                file_name: Name of the file where the data will be saved.
        """
        settings = self.load_settings()
        file_name = settings.get("server_ports_file", "").get()
        try:
            with open(file_name, "w") as file:
                # Iterate through all rows of the Treeview
                for line in ports_list.get_children():
                    # Get the line values (protocol and port)
                    valores = ports_list.item(line, "values")
                    if len(valores) == 2:  # Check if there are two values ​​(protocol and port)
                        protocolo, porta = valores
                        # write in the file in the format "prot/protocol"
                        file.write(f"{porta}/{protocolo}\n")
            print(f"Ports successfully saved in file {file_name}!")
        except Exception as e:
            print(f"Error saving ports: {e}")
        
        # reload the ports in the container, starting all services on each port.
        self.reload_ports(container_id, file_name)
        # restart server
        containers.start_server(container_id)
        
    def hosts_save_ports_in_file_list(self, container_id, ports_list : list[tuple]):
        """
            Saves the ports and protocols of the Treeview in a file, in the format "port/protocol".

            Args:
                ports_table: The Treeview containing the columns "Protocol" and "Port".
                file_name: Name of the file where the data will be saved.
        """
        settings = self.load_settings()
        file_name = settings.get("server_ports_file", "").get()
        try:
            with open(file_name, "w") as file:
                # Iterate through all rows of the Treeview
                for portas in ports_list:
                    # Get the line values (protocol and port)
                    if len(portas) == 2:  # Check if there are two values ​​(protocol and port)
                        protocolo, porta = portas
                        # write in the file in the format "port/protocol"
                        file.write(f"{porta}/{protocolo}\n")
            print(f"Ports successfully saved in file {file_name}!")
        except Exception as e:
            print(f"Error saving ports: {e}")
        
        # reload the ports in the container, starting all services on each port.
        self.reload_ports(container_id, file_name)
        # restart server
        containers.start_server(container_id)
        
    def reload_ports(self, container_id, file_name):
        """
            Reload service ports in the container/host. It's made copying the file in the interface to the container.
            
            Args:
                container_id: container ID.
                file_name: File name.
        """
        print(f"Reload ports from {container_id}")
        containers.copy_ports2server(container_id, file_name)
        