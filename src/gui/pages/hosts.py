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
from utils import ScrollablePage

class HostsPage(ttk.Frame):
    def __init__(self, parent: ttk.Widget, simulation: SimulationManager):
        """
            Create Hosts tab, show informations about hosts and permit change some configurations like port and start/stop servers.
        """
        super().__init__(parent)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1) 
        
        content_frame = ScrollablePage(self)
        self.content_frame = content_frame
        #content_frame.columnconfigure(0, weight=1)
        #content_frame.columnconfigure(3, weight=1)
        
        self.top_frame = tk.Frame(content_frame)
        self.top_frame.grid(row=0, column=0,)
        
        ttk.Label(self.top_frame, text="Network Containers Hosts:", font=("Arial", 12)).grid(row=0, column=0,)

        # Button to turn on all containers/servers
        ttk.Button(self.top_frame, text="Turn on servers", command=simulation.hosts_start_servers).grid(row=1, column=0,)

        self.frame_all_hosts = tk.Frame(content_frame)
        self.frame_all_hosts.grid(row=1, column=0,)
        
        self.hosts_show_host_informations_in_host_tab(simulation)

    def hosts_show_host_informations_in_host_tab(self, simulation: SimulationManager):
        """
            Displays host information in the hosts tab.
        """
        
        # Load the icons
        self.power_icon = tk.PhotoImage(file="img/system-shutdown-symbolic.png")  
        self.power_icon_off = tk.PhotoImage(file="img/system-shutdown-symbolic-off.png") 
        status_on_icon = tk.PhotoImage(file="img/system-shutdown-symbolic.png")  
        status_off_icon = tk.PhotoImage(file="img/system-shutdown-symbolic.png") 
        
        
        #print(f"self.containers_data: {self.containers_data}")
        containers: list[dict[str, ]] = simulation.getContainersByImageName()
        #print(f"cont :  {json.dumps(cont, indent=4)}")
        
        self.list_button_servers_onOff = [] 
        
        row_index = 0  # Starting line on the grid

        
        
        for host in containers:
            print(f"ID: {host['id']}")
            print(f"Nome: {host['nome']}")
            print(f"Hostname: {host['hostname']}")
            print("Interfaces:")

            status = simulation.host_check_server_on_off(host['id'])

            container_id = host["id"]
            container_name = host["nome"]
            hostname = host["hostname"]

            if not self.frame_all_hosts.winfo_exists(): #or not self.canva_hosts.winfo_exists():
                print("Error: frame_all_hosts does not exist anymore!")
                #recriate 
                self.frame_all_hosts = tk.Frame(self.content_frame)
                self.frame_all_hosts.grid(row=1, column=0,)

            
            # Creating a frame for each host
            frame_item = ttk.Frame(self.frame_all_hosts)
            frame_item.grid(row=row_index, column=1, columnspan=1, sticky="ew", padx=10, pady=5)

            # Button to edit host ports
            btn = ttk.Button(frame_item, text=f"{hostname}", command=lambda cid=container_id: self.edit_host_ports(simulation, cid, hostname))
            btn.grid(row=0, column=0, padx=5, pady=2, sticky="w")

            # Label with container information
            lbl_container = ttk.Label(frame_item, text=f"Container: {container_id} - {container_name}", font=("Arial", 10))
            lbl_container.grid(row=0, column=1, padx=5, pady=2, sticky="w")

            row_index += 1  # Move to the next line

            if not host['interfaces']:
                # Creating a subframe to align interfaces and IPs together
                interface_frame = ttk.Frame(frame_item)
                interface_frame.grid(row=row_index, column=1, columnspan=2, sticky="w", padx=20)
                ip_index = 1
                lbl_interface = ttk.Label(interface_frame, text=f"Interface: None or Down", font=("Arial", 10, "bold"))
                lbl_interface.grid(row=0, column=0, sticky="w")

            else:
                for interface in host['interfaces']:
                    print(f"  - Interface: {interface['nome']}")
                    if_name = interface['nome']

                    # Creating a subframe to align interfaces and IPs together
                    interface_frame = ttk.Frame(frame_item)
                    interface_frame.grid(row=row_index, column=1, columnspan=2, sticky="w", padx=20)

                    # TODO - I noticed that the ip command shows the interface IPs even if this interface is turned off.
                    # Label with the interface name
                    lbl_interface = ttk.Label(interface_frame, text=f"Interface: {if_name}", font=("Arial", 10, "bold"))
                    lbl_interface.grid(row=0, column=0, sticky="w")

                    ip_index = 1
                    for ip in interface['ips']:
                        lbl_ip = ttk.Label(interface_frame, text=f"IP: {ip}", font=("Arial", 10))
                        lbl_ip.grid(row=ip_index, column=0, padx=20, sticky="w")
                        ip_index += 1

                    row_index += 2  # Move to the next line in the layout

            self.frame_all_hosts.columnconfigure(0, weight=1)
            self.frame_all_hosts.columnconfigure(2, weight=1)

            # Server status
            lbl_status = ttk.Label(interface_frame, text=f"Status from server: {status}", font=("Arial", 10))
            lbl_status.grid(row=ip_index, column=0, padx=5, sticky="w")

            # Power button with icon
            btn_toggle = ttk.Button(interface_frame, image=self.power_icon, command=lambda cid=container_id: self.host_toggle_server_and_button_between_onOff(simulation, cid, btn_toggle))
            btn_toggle.image = self.power_icon  # Keep the reference to avoid garbage collection
            btn_toggle.grid(row=ip_index, column=1, padx=10, pady=5, sticky="w")
            self.list_button_servers_onOff.append((container_id, btn_toggle, lbl_status))
            row_index += 1  # Extra line to separate hosts
            
            for container_id, btn, label_status in self.list_button_servers_onOff:
            #print(f"cid/btn {cid} - {btn}")
                btn.config(image=self.power_icon, text="liga")
                status = simulation.host_check_server_on_off(container_id)
                label_status.config(text=f"Server Status: {status}", font=("Arial", 10))
            
    def edit_host_ports(self, simulation: SimulationManager, container_id, hostname):
        """
            Opens a new window to edit host ports in the hosts tab.

            Args:
                container_id: Container ID.
                hostname: Hostname or container.
        """
        popup = tk.Toplevel(self.master)
        popup.title(f"Edit Ports for Container {container_id} - {hostname}:")
        popup.geometry("400x300")  

        ports = containers.get_port_from_container(container_id)
    
        ttk.Label(popup, text=f"Opened Ports from {hostname}", font=("Arial", 10)).grid(row=0, column=0, pady=5)

        # Create a Treeview to show network ports.
        colunas = ("Protocolo", "Porta")
        list_host_ports = ttk.Treeview(popup, columns=colunas, show="headings", selectmode="browse")
        list_host_ports.heading("Protocolo", text="Protocol")
        list_host_ports.heading("Porta", text="Port")
        list_host_ports.column("Protocolo", width=150, anchor=tk.CENTER)
        list_host_ports.column("Porta", width=100, anchor=tk.CENTER)
        list_host_ports.grid(row=1, column=0, pady=10)

        # Populate the Treeview with existing ports
        for protocol, port in ports:
            list_host_ports.insert("", tk.END, values=(protocol, port))

        # Create a frame to buttons
        frame_buttons = ttk.Frame(popup)
        frame_buttons.grid(row=2, column=0, pady=10)

        # Button to add line/port
        button_add = ttk.Button(frame_buttons, text="Add Port", command=lambda: self.add_line_treeview_host(list_host_ports))
        button_add.grid(row=0, column=1, pady=5)

        # Button to remove a line/port
        button_delete = ttk.Button(frame_buttons, text="Delete Port ", command=lambda: self.delete_line_treeview_host(list_host_ports))
        button_delete.grid(row=0, column=0, pady=5)

        ttk.Button(popup, text="Reload Ports", command=lambda: simulation.hosts_save_ports_in_file(container_id, list_host_ports)).grid(row=1, column=0, columnspan=2, pady=10)
        
    def add_line_treeview_host(self, ports_list):
        """
            Open a new window to add a port in a Treeview

            Args:
                ports_list: List of network ports.

        """
        popup = tk.Toplevel()
        popup.title("Add Port")
        popup.geometry("300x150")

        
        def add_port_on_host():
            """
                Validate and add the port.
            """
            protocol = combobox_protocol.get().strip().upper()
            port = entry_port.get().strip()

            # Validate protocol
            if protocol not in ["TCP", "UDP"]:
                messagebox.showerror("Error", "Invalid protocol! Choose TCP or UDP.")
                return

            # Validate port
            try:
                port = int(port)
                if port < 1 or port > 65535:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Invalid port! Must be a number between 0 and 65535.")
                return

            # Checks if the protocol/port combination already exists in the table
            for line in ports_list.get_children():
                values = ports_list.item(line, "values")
                if values[0].upper() == protocol and values[1] == str(port):
                    messagebox.showerror("Error", f"Port {port}/{protocol} already exists in the table!")
                    return

            # Add new port in the Treeview
            ports_list.insert("", tk.END, values=(protocol, port))
            popup.destroy()  # Close popup

        # Fields to select the protocol
        ttk.Label(popup, text="Protocol:").grid(row=0, column=0, pady=5)
        combobox_protocol = ttk.Combobox(popup, values=["TCP", "UDP"], state="readonly")
        combobox_protocol.set("TCP")  # Default value
        combobox_protocol.grid(row=1, column=0, pady=5)

        # Field to add port
        ttk.Label(popup, text="Port:").grid(row=2, column=0, pady=5)
        entry_port = ttk.Entry(popup)
        entry_port.grid(row=3, column=0, pady=5)

        # Button to add port
        ttk.Button(popup, text="Add", command=add_port_on_host).grid(row=4, column=0, pady=10)

    # Função para remover a linha selecionada
    def delete_line_treeview_host(self, ports_list):
        """
            Remove line/port from a host.
            
            Args:
                ports_list: List of network ports.
        """
        #print("Delete")
        selected = ports_list.selection()
        if selected:  # Verifica se há algo selecionado
            ports_list.delete(selected)

    def host_toggle_server_and_button_between_onOff(self, simulation : SimulationManager, container_id, button_on_off):
        """
            Toggles between on and off in the hosts tab (toggles the button)

            Args:
                container_id: Conteriner ID to start or stop server.
                button_on_off: Button on/off to be changed between on and off. 
        """
        print(f"Toggling server for container ID: {container_id}")  
        # Find the corresponding button in the list and change the image
        for cid, button_on_off, label_status in self.list_button_servers_onOff:
            #print(f"container_id/button {cid} - {button_on_off}")
            if cid == container_id:
                current_image = button_on_off["image"][0]
                if current_image == str(self.power_icon):
                    print("off")
                    label_status.config()
                    containers.stop_server(container_id)
                    button_on_off.config(image=self.power_icon_off)
                else:
                    print("on")
                    containers.start_server(container_id)
                    button_on_off.config(image=self.power_icon, text="liga")
                status = simulation.host_check_server_on_off(container_id)
                label_status.config(text=f"Server Status: {status}", font=("Arial", 10))
                break
            
    def hosts_update(self, simulation: SimulationManager):
        """
            Updates host/container data visualization in hosts tab
        """
        #print("update_hosts")

        for widget in self.frame_all_hosts.winfo_children():
            widget.destroy()

        simulation.update_hosts()
        
        self.containers_data = containers.extract_containerid_hostname_ips( )  # get hosts information (hostname, interfaces, ips)

        # get container_id and hostname - used for example to combobox in firewall rules.
        self.container_hostname = containers.get_containerid_hostname() # container_id and hostname for operations
        self.hosts = list(map(lambda x: x[1], self.container_hostname)) # hostnames to display
        
        #TODO: Aqui ele cria os hosts para as regras de firewall dps, mudar isso para o simulationManager
        #self.combobox_firewall_rules_host['values']=self.hosts # update combobox values

        #print(self.hosts)

        self.hosts_show_host_informations_in_host_tab(simulation)

        # List of values ​​displayed in Combobox (hostname + IP)
        #if self.containers_data:
        #    self.hosts_display = [f"{c['hostname']} ({c['ip']})" for c in self.containers_data]
        #else: # if there are no elements it displays a message
        #    self.hosts_display = ["HOSTS (0.0.0.0)", "HOSTS (0.0.0.0)"]
        #    messagebox.showerror("Error", "Unable to get a response from the hosts! \n Is GNS3 or the hosts running?")
        #self.src_ip["values"] = self.hosts_display
        #self.dst_ip["values"] = self.hosts_display
        #self.src_ip.current(0)
        #if len(self.containers_data) > 1: # checks if there is more than one element in the host list, if there isn't, you can't set the second one as default.
        #    self.dst_ip.current(1)
        #else:
        #    self.dst_ip.current(0)

        #self.root.update_idletasks() # was commented, as there was a problem with the hosts tab.