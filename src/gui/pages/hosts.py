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

class HostsPage(ttk.Frame):
    def __init__(self, parent):
        """
            Create Hosts tab, show informations about hosts and permit change some configurations like port and start/stop servers.
        """
        super().__init__(parent)
        ttk.Label(self, text="Network Containers Hosts:", font=("Arial", 12)).pack(pady=10)

        """
                    self.top_frame = tk.Frame(self.hosts_frame)
            self.top_frame.pack(pady=10)

            ttk.Label(self.top_frame, text="Network Containers Hosts:", font=("Arial", 12)).pack(padx=10)

            # Button to turn on all containers/servers
            ttk.Button(self.top_frame, text="Turn on servers", command=self.hosts_start_servers).pack(side=tk.LEFT, padx=10)

            self.frame_all_hosts = tk.Frame(self.hosts_frame)
            self.frame_all_hosts.pack(fill=tk.BOTH, expand=True) # Adicionado para expandir o frame

            # Criando um frame intermediário para centralizar tudo
            self.central_frame = tk.Frame(self.frame_all_hosts) 
            self.central_frame.place(relx=0.5, rely=0.5, anchor="center")

            self.canva_hosts = tk.Canvas(self.central_frame, width=500, height=800, takefocus=0, highlightthickness=0)
            self.canva_hosts.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.barra_vertical = ttk.Scrollbar(self.frame_all_hosts, orient="vertical", command=self.canva_hosts.yview)
            self.barra_vertical.pack(side=tk.RIGHT, fill=tk.Y)

            self.canva_hosts.configure(yscrollcommand=self.barra_vertical.set)

            self.frame_hosts_informations = tk.Frame(self.canva_hosts) # Frame para o conteúdo dentro do canvas
            self.canva_hosts.create_window((0, 0), window=self.frame_hosts_informations, anchor="n")

            #self.frame_hosts_informations.bind("<Configure>", lambda event: self.canva_hosts.configure(scrollregion=self.canva_hosts.bbox("all")))
            self.frame_hosts_informations.bind("<Configure>", self.scroll_ajust)

            self.hosts_show_host_informations_in_host_tab()
            """