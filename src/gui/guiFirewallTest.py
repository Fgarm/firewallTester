#!/usr/bin/python

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
    Program Name: Firewall Tester - Graphical Interface
    Description: This is the graphical interface and the main part of the firewall rule testing software.
    Author: Luiz Arthur Feitosa dos Santos - luiz.arthur.feitosa.santos@gmail.com / luizsantos@utfpr.edu.br
    License: GNU General Public License v3.0
    Version: 1.0
"""


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from tkinter import filedialog
from simulation import SimulationManager
from pages.firewall import FirewallPage
from pages.about import AboutPage
from pages.config import ConfigPage
from pages.firewallRules import FirewallRulesPage
from pages.hosts import HostsPage
import os
import containers
import json
import re
import threading
import webbrowser
import textwrap



class FirewallTesterGUI(tk.Tk):
    """
        Class to work with firewall tester interface.
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.geometry("800x600")
        self.title("Firewall Tester")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        
        # Creating Notebook tab
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.notebook.grid(column=0, row=0)
        self.notebook.rowconfigure(0, weight = 1)
        self.notebook.columnconfigure(0, weight = 1)
        
        
        self.simulation = SimulationManager()
        
        
        
        # Criando as abas
        self.firewallPage = FirewallPage(self, self.simulation) 
        self.firewallRulesPage = FirewallRulesPage(self, self.simulation) 
        self.hostsPage = HostsPage(self, self.simulation)
        self.configPage = ConfigPage(self, self.simulation)
        self.aboutPage = AboutPage(self)
        
        self.notebook.add(self.firewallPage, text="Firewall Test")
        self.notebook.add(self.firewallRulesPage, text="Firewall Rules")
        self.notebook.add(self.hostsPage, text="Hosts")
        self.notebook.add(self.configPage, text="Settings")
        self.notebook.add(self.aboutPage, text="About")

        # Frame under tabs
        frame_botton = ttk.Frame(self, borderwidth=1)
        frame_botton.grid(column=0, row=1)
        self.notebook.rowconfigure(index=1, minsize=10, weight = 0)
        self.notebook.columnconfigure(index=1, weight = 0)
        
        # TODO - when updating host data, it may be necessary to change test data, especially container IDs and perhaps host IPs - just as it has to be done when loading tests from a file - think of a single solution for both problems - perhaps user intervention is needed.
        
        self.button_uptate_host = ttk.Button(frame_botton, text="Update Hosts", command=self.simulation.update_hosts)
        self.button_uptate_host.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.button_quit = ttk.Button(frame_botton, text="Exit", command=self.confirm_exit)
        self.button_quit.grid(row=0, column=6, padx=10, pady=10, sticky="nsew")
        
        #self.simulation.current_settings["show_container_id"].trace_add('write',) #TODO> When in firewall page, this will be needed
        self.simulation.hosts.trace_add('write', callback=self.update_hosts)
        
    def update_hosts(self):
        #TODO> move hosts update screen logic to a callback when changed self.hosts
        print("Update hosts in screen called")
        # self.simulation.update_hosts() # should be both not needed and not cause problems
        self.hostsPage.hosts_update(self.simulation)
    
    def confirm_exit(self):
        """
            A window opens asking if you really want to exit the firewall tester program.
        """
        if messagebox.askyesno("Confirmation", "Do you really want to exit the program?"):
            self.destroy()
    
    
    
    
    
    


if __name__ == "__main__":
    #root = tk.Tk()
    app = FirewallTesterGUI()
    app.mainloop()