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


class FirewallPage(ttk.Frame):
    def __init__(self, parent):
        """
            Create the firewall tests tab.
        """
        super().__init__(parent)
        ttk.Label(self, text="Firewall Test", font=("Arial", 12)).pack(pady=10)
        # Frame for input fields
        frame_botton = ttk.Frame(self)
        #frame_entrada.pack(fill="x", padx=10, pady=5)
        frame_botton.pack(pady=10)
        
        '''
        # List values in the Combobox (hostname + IP)
        if self.containers_data:
            self.hosts_display = [f"{c['hostname']} ({c['ip']})" for c in self.containers_data]
        else: # If there are no elements it displays a message.
            self.hosts_display = ["HOSTS (0.0.0.0)", "HOSTS (0.0.0.0)"]
            messagebox.showerror("Warning", "Something seems to be wrong! \n Is GNS3 or the hosts turned on?")
        # Sort the list of hosts in ascending order.

        protocols = ["TCP", "UDP", "ICMP"]

        # setting style - so readonly doesn't turn gray
        style = ttk.Style()
        style.map("TCombobox", fieldbackground=[("readonly", "white")])
        # background color of the selected line - so as not to cover the test color


        # Inputs components
        ttk.Label(frame_botton, text="Source IP:").grid(row=0, column=0)
        self.src_ip = ttk.Combobox(frame_botton, values=self.hosts_display, width=25, state="readonly", style="TCombobox")
        self.src_ip.current(0)
        self.src_ip.grid(row=1, column=0)


        ttk.Label(frame_botton, text="Destination IP:").grid(row=0, column=1)
        self.dst_ip = ttk.Combobox(frame_botton, values=self.hosts_display, width=25)
        if len(self.containers_data) > 1: # checks if there is more than one element in the host list, if there isn't, you can't set the second one as default.
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
        self.tests_frame = ttk.Frame(self.firewall_frame)
        self.tests_frame.pack(fill="x", padx=10, pady=10)

        # Intermediate frame to center the buttons
        self.button_frame = tk.Frame(self.tests_frame)
        self.button_frame.pack(pady=10)  # Centraliza verticalmente

        button_size=15
        # Creating and adding buttons inside the intermediate frame
        self.button_tree_add = tk.Button(self.button_frame, text="Add", command=self.firewall_test_tree_add_line_test, width=button_size, underline=0)
        self.button_tree_add.pack(side="left", padx=5)
        self.root.bind("<Alt-a>", lambda event: self.firewall_test_tree_add_line_test())

        self.button_tree_edit = tk.Button(self.button_frame, text="Edit", command=self.firewall_test_tree_edit_line_test, width=button_size, underline=0)
        self.button_tree_edit.pack(side="left", padx=5)
        # # TODO - you have to think about when to enable and disable binds, because the way it is it works everywhere!
        #self.root.bind("<Alt-e>", lambda event: self.edit_entry())

        self.button_tree_del = tk.Button(self.button_frame, text="Delete", command=self.firewall_test_tree_delete_line_test, width=button_size, underline=0)
        self.button_tree_del.pack(side="left", padx=5)
        #self.root.bind("<Alt-d>", lambda event: self.delete_entry())

        self.button_tree_test = tk.Button(self.button_frame, text="Test Line", command=self.firewall_tests_run_test_line, width=button_size, underline=8)
        self.button_tree_test.pack(side="left", padx=5)
        #self.root.bind("<Alt-l>", lambda event: self.testar_linha_tree())

        self.button_tree_test_all = tk.Button(self.button_frame, text="Test All", command=self.firewall_tests_popup_for_run_all_tests_using_threads, width=button_size, underline=0)
        self.button_tree_test_all.pack(side="left", padx=5)
        #self.root.bind("<Alt-l>", lambda event: self.executar_todos_testes())


        # Frame to display the tests added in the treeview
        self.tests_frame_Tree = ttk.Frame(self.firewall_frame)
        self.tests_frame_Tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.hidden_data = {}  # Dictionary to store Container ID associated with Test ID
        self.entries = []
        visible_fields = ["#", "Container ID", "Source", "Destination", "Protocol", "Source Port", "Destination Port", "Expected", "Result", "flow", "data"]
        self.tree = ttk.Treeview(self.tests_frame_Tree, columns=visible_fields, show="headings")

        font = ("TkDefaultFont", 10)
        tk_font = tk.font.Font(font=font)

        self.tree.heading("#", text="#")
        self.tree.column("#", width=30, anchor="e", stretch=False)

        if  self.config_show_container_id_var.get(): # Show or hide container ID in tree table.
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
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll_vertical_tree = tk.Scrollbar(self.tests_frame_Tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_vertical_tree)
        scroll_vertical_tree.pack(side=tk.RIGHT, fill=tk.Y)

        frame_horizontal = ttk.Frame(self.firewall_frame) # Frame para a barra de rolagem horizontal
        frame_horizontal.pack(fill=tk.X)

        # TODO - scroll is not adjusting when data exceeds the window size!
        scroll_horizontal_tree = tk.Scrollbar(frame_horizontal, orient=tk.HORIZONTAL, command=self.tree.xview)
        #self.tree.configure(xscrollcommand=scroll_horizontal_tree.set)
        scroll_horizontal_tree.pack(side=tk.BOTTOM, fill=tk.X, expand=True)

        self.tree.configure(yscrollcommand=scroll_vertical_tree.set, xscrollcommand=scroll_horizontal_tree.set)

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

        btn_frame = tk.Frame(parent)
        btn_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        self.button_tree_edit.config(state="disabled")
        self.button_tree_del.config(state="disabled")
        self.button_tree_test.config(state="disabled")
        if not self.tree.get_children():
            self.button_tree_test_all.config(state="disabled")

        # Frame Legend
        self.frame_test_legend = ttk.LabelFrame(self.firewall_frame, text="Legenda")
        self.frame_test_legend.pack(side="bottom", fill="x", padx=20, pady=15)
        self.frame_test_legend.pack_propagate(False)
        self.frame_test_legend.config(width=700, height=50)

        tk.Label(self.frame_test_legend, bg="lightgreen", width=2, height=1, font=("Arial", 6)).pack(side="left", padx=5)
        tk.Label(self.frame_test_legend, text="Test successfully completed - net flow allowed/accepted).", font=("Arial", 10)).pack(side="left")

        tk.Label(self.frame_test_legend, bg="lightblue", width=2, height=1, font=("Arial", 6)).pack(side="left", padx=5)
        tk.Label(self.frame_test_legend, text="Test successfully completed - net flow blocked/dropped).", font=("Arial", 10)).pack(side="left")

        tk.Label(self.frame_test_legend, bg="red", width=2, height=1, font=("Arial", 6)).pack(side="left", padx=5)
        tk.Label(self.frame_test_legend, text="Test failed.", font=("Arial", 10)).pack(side="left")

        tk.Label(self.frame_test_legend, bg="yellow", width=2, height=1, font=("Arial", 6)).pack(side="left", padx=5)
        tk.Label(self.frame_test_legend, text="Error (e.g., error in IP, GW, DNS, Server)", font=("Arial", 10)).pack(side="left")

        self.frame_button_save_tests = ttk.Frame(self.firewall_frame)
        self.frame_button_save_tests.pack(pady=10)

        self.button_save_tests = ttk.Button(self.frame_button_save_tests, text="Save Tests", command=self.firewall_tests_save_tests)
        self.button_save_tests.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.button_save_tests_as = ttk.Button(self.frame_button_save_tests, text="Save Tests As", command=self.firewall_tests_save_tests_as)
        self.button_save_tests_as.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        self.button_load_tests = ttk.Button(self.frame_button_save_tests, text="Open Tests", command=self.firewall_tests_open_test_file)
        self.button_load_tests.grid(row=0, column=5, padx=10, pady=10, sticky="nsew")
        '''