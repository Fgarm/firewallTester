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


class FirewallPage(ttk.Frame):
    def __init__(self, parent: ttk.Widget, simulation: SimulationManager):
        """
            Create the firewall tests tab.
        """
        super().__init__(parent)
        
        self.simulation = simulation
        
        #ttk.Label(self, text="Firewall Test", font=("Arial", 12)).pack(pady=10)
        # Frame for input fields
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        content_frame = ScrollablePage(self)
        self.content_frame = content_frame
        
        ttk.Label(content_frame, text="Firewall Test", font=("Arial", 12)).grid(row=0, column=0, pady=10)
        
        frame_botton = ttk.Frame(self.content_frame)
        
        #frame_entrada.pack(fill="x", padx=10, pady=5)
        frame_botton.grid(row=1, column=0, pady=10)
        
        ## List values in the Combobox (hostname + IP)
        #if self.containers_data:
        #    self.hosts_display = [f"{c['hostname']} ({c['ip']})" for c in self.containers_data]
        #else: # If there are no elements it displays a message.
        #    self.hosts_display = ["HOSTS (0.0.0.0)", "HOSTS (0.0.0.0)"]
        #    messagebox.showerror("Warning", "Something seems to be wrong! \n Is GNS3 or the hosts turned on?")
        ## Sort the list of hosts in ascending order.

        protocols = ["TCP", "UDP", "ICMP"]
        
        # setting style - so readonly doesn't turn gray
        style = ttk.Style()
        style.map("TCombobox", fieldbackground=[("readonly", "white")])
        # background color of the selected line - so as not to cover the test color


        # Inputs components
        ttk.Label(frame_botton, text="Source IP:").grid(row=0, column=0)
        self.src_ip = ttk.Combobox(frame_botton, values=self.simulation.hosts_display, width=25, state="readonly", style="TCombobox")
        self.src_ip.current(0)
        self.src_ip.grid(row=1, column=0)
        
        ttk.Label(frame_botton, text="Destination IP:").grid(row=0, column=1)
        self.dst_ip = ttk.Combobox(frame_botton, values=self.simulation.hosts_display, width=25)
        #containers_data = containers.extract_containerid_hostname_ips() # Está estático, não é a melhor forma de fazer
        if len(simulation.containers_data) > 1: # checks if there is more than one element in the host list, if there isn't, you can't set the second one as default.
            self.dst_ip.current(1)
        else:
            self.dst_ip.current(0)

        self.dst_ip.grid(row=1, column=1)
        # Binds the selection event
        self.dst_ip["state"] = "normal"
        
        ttk.Label(frame_botton, text="Protocol:").grid(row=0, column=2)
        self.protocol = ttk.Combobox(frame_botton, values=protocols, width=6, state="readonly", style="TCombobox")
        self.protocol.current(0)
        self.protocol.grid(row=1, column=2)

        ttk.Label(frame_botton, text="Src Port:").grid(row=0, column=3)
        self.src_port = ttk.Entry(frame_botton, width=11)
        self.src_port.insert(0, "*")
        self.src_port.config(state="disabled")
        self.src_port.grid(row=1, column=3)

        ttk.Label(frame_botton, text="Dst Port:").grid(row=0, column=4)
        self.dst_port = ttk.Entry(frame_botton, width=11)
        self.dst_port.insert(0, "80")
        self.dst_port.grid(row=1, column=4)

        ttk.Label(frame_botton, text="Expected success?").grid(row=0, column=5)
        self.expected = tk.StringVar(value="yes")
        ttk.Radiobutton(frame_botton, text="Yes", variable=self.expected, value="yes").grid(row=1, column=5)
        ttk.Radiobutton(frame_botton, text="No", variable=self.expected, value="no").grid(row=1, column=6)

        # Frame to display added tests
        self.tests_frame = ttk.Frame(self.content_frame)
        self.tests_frame.grid(row=2, column=0, padx=10, pady=10)
        #self.tests_frame.pack(fill="x", padx=10, pady=10)

        # Intermediate frame to center the buttons
        self.button_frame = tk.Frame(self.tests_frame)
        self.button_frame.grid(row=0, column=0, pady=10)
        #self.button_frame.pack(pady=10)  # Centraliza verticalmente
        

        button_size=15
        # Creating and adding buttons inside the intermediate frame
        self.button_tree_add = tk.Button(self.button_frame, text="Add", command=self.firewall_test_tree_add_line_test, width=button_size, underline=0)
        self.button_tree_add.grid(row=0, column=0, padx=5)
        #self.button_tree_add.pack(side="left", padx=5)
        # TODO: see this bind as well
        # TODO: Implement this one, because it was implemented before
        #parent.bind("<Alt-a>", lambda event: self.firewall_test_tree_add_line_test())

        self.button_tree_edit = tk.Button(self.button_frame, text="Edit", command=self.firewall_test_tree_edit_line_test, width=button_size, underline=0)
        self.button_tree_edit.grid(row=0, column=1, padx=5)
        #self.button_tree_edit.pack(side="left", padx=5)
        # # TODO - you have to think about when to enable and disable binds, because the way it is it works everywhere!
        #self.root.bind("<Alt-e>", lambda event: self.edit_entry())

        self.button_tree_del = tk.Button(self.button_frame, text="Delete", command=self.firewall_test_tree_delete_line_test, width=button_size, underline=0)
        self.button_tree_del.grid(row=0, column=2, padx=5)
        #self.root.bind("<Alt-d>", lambda event: self.delete_entry())

        self.button_tree_test = tk.Button(self.button_frame, text="Test Line", command=self.firewall_tests_run_test_line, width=button_size, underline=8)
        self.button_tree_test.grid(row=0, column=3, padx=5)
        #self.button_tree_test.pack(side="left", padx=5)
        #self.root.bind("<Alt-l>", lambda event: self.testar_linha_tree())

        self.button_tree_test_all = tk.Button(self.button_frame, text="Test All", command=self.firewall_tests_popup_for_run_all_tests_using_threads, width=button_size, underline=0)
        self.button_tree_test_all.grid(row=0, column=4, padx=5)
        #self.button_tree_test_all.pack(side="left", padx=5)
        #self.root.bind("<Alt-l>", lambda event: self.executar_todos_testes())

        
        # Frame to display the tests added in the treeview
        #self.tests_frame_Tree = ttk.Frame(self.content_frame)
        #self.tests_frame_Tree.grid(row=2, column=0, )#padx=10, pady=10)
        
        #self.tests_frame_Tree.columnconfigure(0, weight=1)
        #self.tests_frame_Tree.rowconfigure(0, weight=1) 

        xScrollable = ScrollablePage(self.content_frame, posx=3, axis=tk.X)
        
        #xScrollable.columnconfigure(0, weight=1)
        #xScrollable.rowconfigure(0, weight=1) 
        
        self.hidden_data = {}  # Dictionary to store Container ID associated with Test ID
        self.entries = []
        visible_fields = ["#", "Container ID", "Source", "Destination", "Protocol", "Source Port", "Destination Port", "Expected", "Result", "flow", "data"]
        #self.tree = ttk.Treeview(self.tests_frame_Tree, columns=visible_fields, show="headings", )
        self.tree = ttk.Treeview(xScrollable, columns=visible_fields, show="headings", )

        font = ("TkDefaultFont", 10)
        tk_font = tk.font.Font(font=font)

        self.tree.heading("#", text="#")
        self.tree.column("#", width=30, anchor="e", stretch=False)

        if  self.simulation.current_settings["show_container_id"].get(): # Show or hide container ID in tree table.
            self.colunaContainerID=130 # show
        else:
            self.colunaContainerID=0 # hide.
            
        self.tree.heading("Container ID", text="Container ID")
        self.tree.column("Container ID", width=self.colunaContainerID, stretch=False)

        self.tree.heading("Source", text="Source")
        self.tree.column("Source", width=250, stretch=False)

        self.tree.heading("Destination", text="Destination")
        self.tree.column("Destination", width=250, stretch=False)

        self.tree.heading("Protocol", text="Protocol")
        self.tree.column("Protocol", width=80, anchor="center", stretch=False)

        self.tree.heading("Source Port", text="Src Port")
        self.tree.column("Source Port", width=80, anchor="center", stretch=False)

        self.tree.heading("Destination Port", text="Dst Port")
        self.tree.column("Destination Port", width=80, anchor="center", stretch=False)

        self.tree.heading("Expected", text="Expected")
        self.tree.column("Expected", width=80, anchor="center", stretch=False)

        self.tree.heading("Result", text="Result")
        self.tree.column("Result", width=80, anchor="w", stretch=False)

        self.tree.heading("flow", text="Network Flow")
        self.tree.column("flow", width=200, anchor="w", stretch=False)

        self.tree.heading("data", text="Network Data")
        self.tree.column("data", minwidth=100, width=200, anchor="w", stretch=True)

        #self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        scroll_y_firewall_rules = tk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scroll_y_firewall_rules.grid(row=3, column=1, sticky="ns")
        self.tree.config(yscrollcommand=scroll_y_firewall_rules.set)
        
        
        

        # Color definition
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.map("Treeview", background=[("selected", "#4a90e2")])
        self.tree.tag_configure("yes", background="lightgreen")
        self.tree.tag_configure("yesFail", background="lightblue")
        self.tree.tag_configure("no", background="salmon")
        self.tree.tag_configure("error", background="yellow")
        #self.tree.tag_configure("nat", background="lightblue")

        self.tree.bind("<<TreeviewSelect>>", self.firewall_test_tree_select_line_test)
        self.tree.bind("<Double-1>", self.firewall_test_tree_double_click_line_test)
        self.tree.bind('<Escape>', self.firewall_test_tree_select_line_test)

        btn_frame = tk.Frame(self.content_frame)
        btn_frame.grid(row=4, column=0, padx=10, pady=10)

        self.button_tree_edit.config(state="disabled")
        self.button_tree_del.config(state="disabled")
        self.button_tree_test.config(state="disabled")
        if not self.tree.get_children():
            self.button_tree_test_all.config(state="disabled")
            
            
        
        
        # Frame Legend
        self.frame_test_legend = ttk.LabelFrame(self.content_frame, text="Legenda")
        self.frame_test_legend.grid(row=5, column=0, padx=20, pady=15)
        self.frame_test_legend.pack_propagate(False)
        self.frame_test_legend.config(width=700, height=50)

        tk.Label(self.frame_test_legend, bg="lightgreen", width=2, height=1, font=("Arial", 6)).grid(row=0, column=0, padx=5)
        tk.Label(self.frame_test_legend, text="Test successfully completed - net flow allowed/accepted).", font=("Arial", 10)).grid(row=0, column=1)

        tk.Label(self.frame_test_legend, bg="lightblue", width=2, height=1, font=("Arial", 6)).grid(row=1, column=0, padx=5)
        tk.Label(self.frame_test_legend, text="Test successfully completed - net flow blocked/dropped).", font=("Arial", 10)).grid(row=1, column=1)

        tk.Label(self.frame_test_legend, bg="red", width=2, height=1, font=("Arial", 6)).grid(row=0, column=2, padx=5)
        tk.Label(self.frame_test_legend, text="Test failed.", font=("Arial", 10)).grid(row=0, column=3)

        tk.Label(self.frame_test_legend, bg="yellow", width=2, height=1, font=("Arial", 6)).grid(row=1, column=2, padx=5)
        tk.Label(self.frame_test_legend, text="Error (e.g., error in IP, GW, DNS, Server)", font=("Arial", 10)).grid(row=1, column=3)

        self.frame_button_save_tests = ttk.Frame(self.content_frame)
        self.frame_button_save_tests.grid(row=6, column=0,pady=10)

        self.button_save_tests = ttk.Button(self.frame_button_save_tests, text="Save Tests", command=self.firewall_tests_save_tests)
        self.button_save_tests.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.button_save_tests_as = ttk.Button(self.frame_button_save_tests, text="Save Tests As", command=self.firewall_tests_save_tests_as)
        self.button_save_tests_as.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        self.button_load_tests = ttk.Button(self.frame_button_save_tests, text="Open Tests", command=self.firewall_tests_open_test_file)
        self.button_load_tests.grid(row=0, column=5, padx=10, pady=10, sticky="nsew")
    
    def firewall_tests_save_tests(self):
        #TODO: Implement
        pass
    def firewall_tests_save_tests_as(self):
        #TODO: Implement
        pass
    def firewall_tests_open_test_file(self):
        #TODO: Implement
        pass
    def firewall_test_tree_select_line_test(self):
        #TODO: Implement
        pass
    def firewall_test_tree_double_click_line_test(self):
        #TODO: Implement
        pass
    def firewall_test_tree_select_line_test(self):
        #TODO: Implement
        pass
    
    def firewall_test_tree_add_line_test(self):
        """
            Add a line/test on treeview firewall tests.
        """
        #print("add_line_on_tree_test_firewall")
        
        src_ip = self.src_ip.get()
        dst_ip = self.dst_ip.get()
        protocol = self.protocol.get()
        src_port = self.src_port.get()
        dst_port = self.dst_port.get()
        expected = self.expected.get()

        if self.firewall_tests_validate_entrys() != 0: return # test values

        # Gets the ID of the container selected in the Combobox
        selected_index = self.src_ip.current()
        if selected_index >= 0 and selected_index < len(self.simulation.containers_data):
            container_id = self.simulation.containers_data[selected_index]["id"]
            print(f"container_data selected_index{selected_index} -  {self.simulation.containers_data[selected_index]}")
        else:
            container_id = "N/A"  # If no container is selected
        
        row_index = len(self.tree.get_children()) + 1 # tree line index

        values = [src_ip, dst_ip, protocol, src_port, dst_port, expected, "-", " ", " "]

        for item in self.tree.get_children(): # avoid duplicate testing
            existing_values = self.tree.item(item, "values")
            #print(f"Values\n{values}\n{existing_values[2:]}")
            if tuple(values) == existing_values[2:]:
                #print(f"egual values - \n{values}\n{existing_values}")
                messagebox.showwarning("Warning", "This entry already exists in the table!")
                return

        values=[]
        self.tree.insert("", "end", values=[row_index, container_id, src_ip, dst_ip, protocol, src_port, dst_port, expected, "-", " ", " "])
        #self.tree.column("Container ID", width=self.colunaContainerID, stretch=False)
        
        self.firewall_tests_buttons_set_normal_state()
    
    def firewall_tests_buttons_set_normal_state(self):
        """
            Defines the state of the firewall test buttons when adding a line/test. This is the normal state when using the Estes interface (startup state).
        """
        self.tree.selection_set(())
        self.button_tree_add.config(state="normal")
        self.button_tree_edit.config(state="disable")
        self.button_tree_del.config(state="disable")
        self.button_tree_test.config(state="disabled")
        self.button_tree_edit.config(text="Editar")
        if not self.tree.get_children():
            self.button_tree_test_all.config(state="disabled")
        else:
            self.button_tree_test_all.config(state="normal")

    def firewall_tests_validate_entrys(self):
        """
            Checks if the IPs, domains and ports have the expected values. If all fields have been filled in, etc.
        """
        # Check if the required fields are filled in

        if not self.src_ip.get() or not self.dst_ip.get() or not self.protocol.get() or not self.dst_port.get():
            messagebox.showwarning("Mandatory fields", "Please fill in all mandatory fields.")
            return -1
        if not self.dst_port.get().isdigit():
            messagebox.showwarning("Mandatory fields", "The port must be a number between 1-65535.")
            return -1
        try:
            porta = int(self.dst_port.get())
            if porta < 1 or porta > 65535:
                messagebox.showwarning("Mandatory fields", "The port must be a number between 1-65535.")
                return -1
        except ValueError:
            messagebox.showwarning("Invalid port: conversion error.")
            return -1
        
        if self.dst_ip.get() not in self.simulation.hosts_display:
            if self.validate_ip_or_domain(self.dst_ip.get()) == False:
                messagebox.showwarning(f"Invalid address", "The address must either: \n1. Be on the list, \n2. Be an IP (8.8.8.8), \n3. Be a domain (www.google.com.br).")
                return -1
            else: # If it is outside the list of hosts in the scenario, for now it is only possible to perform ping tests.
                if self.protocol.get() != "ICMP":
                    messagebox.showwarning(f"Invalid protocol", "Unfortunately, in this version, only ICMP (ping) can be used to test external hosts.")
                    return -1
                
        return 0
        # TODO - if the destination is changed, in this version of the system, you can only use the ICMP protocol, you cannot use TCP or UDP, because the server (if it exists) will not recognize the message sent.
        # If all fields are filled in, call the firewall_test_tree_edit_line_test (old add_edit_test method)
        
    def validate_ip_or_domain(self, ip_or_domain):
        """
            Validate IP or domain. Method used, for example, to validate whether an IP or domain chosen or entered by the user is valid for test processing. Validate only IPv4 address not IPv6.

            Arg:
                ip_or_domain: IP or Domain to be validate.
        """
        # Regex to IP (IPv4)
        regex_ip = r'^\d+\.\d+\.\d+\.\d+$'
        
        # Regex do domain (ex: google.com, www.example.com)
        regex_domain = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(regex_ip, ip_or_domain):
            return True
        elif re.match(regex_domain, ip_or_domain):
            return True
        else:
            return False
    
    def firewall_test_tree_edit_line_test(self):
        #TODO: Implement
        pass
    def firewall_test_tree_delete_line_test(self):
        #TODO: Implement
        pass
    def firewall_tests_run_test_line(self):
        #TODO: Implement
        pass
    def firewall_tests_popup_for_run_all_tests_using_threads(self):
        #TODO: Implement
        pass