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
        
        self.parent = parent
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
        #parent.bind("<Alt-a>", lambda event: self.firewall_test_tree_add_line_test())

        self.button_tree_edit = tk.Button(self.button_frame, text="Edit", command=self.firewall_test_tree_edit_line_test, width=button_size, underline=0)
        self.button_tree_edit.grid(row=0, column=1, padx=5)
        #self.button_tree_edit.pack(side="left", padx=5)
        # # TODO - you have to think about when to enable and disable binds, because the way it is it works everywhere!
        #self.parent.bind("<Alt-e>", lambda event: self.edit_entry())

        self.button_tree_del = tk.Button(self.button_frame, text="Delete", command=self.firewall_test_tree_delete_line_test, width=button_size, underline=0)
        self.button_tree_del.grid(row=0, column=2, padx=5)
        #self.parent.bind("<Alt-d>", lambda event: self.delete_entry())

        self.button_tree_test = tk.Button(self.button_frame, text="Test Line", command=self.firewall_tests_run_test_line, width=button_size, underline=8)
        self.button_tree_test.grid(row=0, column=3, padx=5)
        #self.button_tree_test.pack(side="left", padx=5)
        #self.parent.bind("<Alt-l>", lambda event: self.testar_linha_tree())

        self.button_tree_test_all = tk.Button(self.button_frame, text="Test All", command=self.firewall_tests_popup_for_run_all_tests_using_threads, width=button_size, underline=0)
        self.button_tree_test_all.grid(row=0, column=4, padx=5)
        #self.button_tree_test_all.pack(side="left", padx=5)
        #self.parent.bind("<Alt-l>", lambda event: self.executar_todos_testes())

        
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

            
        self.tree.heading("Container ID", text="Container ID")
        self.update_container_id()
        #self.tree.column("Container ID", width=self.colunaContainerID, stretch=False)

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

        self.button_load_tests = ttk.Button(self.frame_button_save_tests, text="Load Tests", command=self.firewall_tests_open_test_file)
        self.button_load_tests.grid(row=0, column=5, padx=10, pady=10, sticky="nsew")
    
    def update_combobox_ip(self):
        self.src_ip['values'] = self.simulation.hosts_display
        self.src_ip.current(0)
        
        self.dst_ip['values'] = self.simulation.hosts_display
        
        if len(self.simulation.containers_data) > 1: # checks if there is more than one element in the host list, if there isn't, you can't set the second one as default.
            self.dst_ip.current(1)
        else:
            self.dst_ip.current(0)
    
    def update_container_id(self, param1 = "", param2 = "", param3 = ""):
        
        if self.simulation.current_settings["show_container_id"].get(): # Show or hide container ID in tree table.
            self.tree.column("Container ID", width=130, stretch=False) # show
        else:
            self.tree.column("Container ID", width=0, stretch=False) # hide.
    
    def firewall_tests_save_tests(self):
        """
            Saves the Treeview data to a JSON file.
        """
        print("Saving tests...")
        if not self.save_file_path:
            self.firewall_tests_save_tests_as()
        else:
            items = self.tree.get_children()
            tests_data = []

            for item in items:
                values = self.tree.item(item, "values")
                if values:
                    # Recover the hidden Container ID
                    #teste_id = values[0]
                    #container_id = self.hidden_data.get(teste_id, "")  
                    teste_id, container_id, src_ip, dst_ip, protocol, src_port, dst_port, expected, result, dnat, observation = values

                    # Create the dictionary and add it to the list
                    tests_data.append({
                        "teste_id": teste_id,
                        "container_id": container_id,
                        "src_ip": src_ip,
                        "dst_ip": dst_ip,
                        "protocol": protocol,
                        "src_port": src_port,
                        "dst_port": dst_port,
                        "expected": expected,
                        "result": result,
                        "flow": dnat,
                        "data": observation
                    })

            # Write to JSON file
            with open(self.save_file_path, "w") as f:
                json.dump(tests_data, f, indent=4)

            print(f"Tests successfully saved in file: {self.save_file_path}")
            
    
    def firewall_tests_save_tests_as(self):
        """
            Opens a window to save the tests as to a JSON file.
        """
        file_path = filedialog.asksaveasfilename(
            title="Save test file",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if not file_path:  # If the user cancels, do nothing
            return

        self.save_file_path = file_path

        #print(f"Saving in the file: {self.save_file_path}")
        self.firewall_tests_save_tests()
    
    
    def firewall_tests_open_test_file(self):
        """
            Opens a window to select a JSON file and load the tests.
        """
        file_path = filedialog.askopenfilename(
            title="Open test file",
            filetypes=[("JSON file", "*.json"), ("All files", "*.*")]
        )

        if not file_path:  # If the user cancels, it does nothing.
            return

        self.save_file_path = file_path

        if (self.tree.get_children()):
            if messagebox.askyesno("Confirmation", "Do you want to override existing tests?"):
                self.delete_all_tests()
        
        print(f"Loading tests from file: {file_path}")

        self.firewall_tests_load_tests_from_file()
        
    # TODO - When loading, you have to check if the source still has the same container ID - because if it is on different machines or in different GNS3 projects - the container ID will change!
    # TODO - I would also have to see if the IPs still match, because in class, the teacher usually gives the name of the machine and not the IP, so I would have to check if the IPs are the same, if they are not, I would have to update the IP, probably with user interaction if the host has more than one IP (choose which IP is for the test, especially if it is the destination - at the source this will not make much difference)
    
    def firewall_tests_load_tests_from_file(self):
        """
            Loads data from the JSON file into the Treeview.
        """
        print("Loading tests...")

        if os.path.exists(self.save_file_path):
            with open(self.save_file_path, "r") as f:
                try:
                    tests_data = json.load(f)
                except json.JSONDecodeError:
                    print("Error loading the JSON file.")
                    return

            # Add items to the Treeview
            for test in tests_data:
                row_index = len(self.tree.get_children()) + 1
                source = self.extract_hostname(test["src_ip"])
                print(f"test source: {source}")
                container_id = self.find_container_id(source)
                is_duplicate = False
                values_check = [test["src_ip"], test["dst_ip"], test["protocol"], test["src_port"], test["dst_port"], test["expected"], "-", " ", " "]
                for item in self.tree.get_children():
                    if (self.check_is_duplicate(values_check, item)):
                        is_duplicate = True
                        break
                if(not is_duplicate):
                    if container_id:
                        item_id = self.tree.insert("", "end", values=[
                            row_index, container_id, test["src_ip"], test["dst_ip"], test["protocol"],
                            test["src_port"], test["dst_port"], test["expected"], test["result"], test["flow"], test["data"]
                        ])
                    else:
                        container_id, selected_host = self.ask_user_for_source_host(test["src_ip"], self.simulation.hosts_display, test)
                        
                        if selected_host is not None:
                            item_id = self.tree.insert("", "end", values=[
                                row_index, container_id, selected_host, test["dst_ip"], test["protocol"],
                                test["src_port"], test["dst_port"], test["expected"], test["result"], test["flow"], test["data"]
                            ])
                        else:
                            print(f"Test {test} ignored by user.")
                else:
                    print(f"Test {test} skipped as it was a duplicate.")

            print("Tests successfully loaded!")
            self.firewall_tests_buttons_set_normal_state()
        else:
            print("No test files found.")
            
    def extract_hostname(self, host_string : str):
        """
        Extracts the hostname from a string in the format "Host (address)".

        Args:
            host_string (str): The string containing the hostname and IP address.

        Returns:
            str: The hostname, or None if the string is not in the expected format.
        """
        try:
            hostname = host_string.split(" (")[0]
            return hostname
        except IndexError:
            return None  # Return None if the string is not in the expected format
        
    def find_container_id(self, search_hostname):
        """
        Finds the container_id associated with a hostname in the self.container_hostname list.

        Args:
            search_hostname (str): The hostname to search for.

        Returns:
            str or None: The container_id if the hostname is found, or None if not found.
        """
        for container_id, hostname in self.simulation.container_hostname:
            if hostname == search_hostname:
                return container_id
        return None  # Return None if hostname is not found
            
    def ask_user_for_source_host(self, source, available_hosts, test):
        """
        Opens a dialog to ask the user to select a host if no container_id is found during load file test process,
        displaying the test details.

        Args:
            source: the old source hostname, which was not found when the test was loaded from the file.
            available_hosts: list of host names available in the current network scenario.
            test: test data.

        Returns: Container id and hostname of the new source host that was chosen in the interface by the user.
        """
        dialog = tk.Toplevel(self)
        dialog.title("Select Host")
        dialog.geometry("400x400")
        dialog.transient(self.parent)  
        dialog.grab_set()  # block main window

        warning_text = ("Attention: When trying to load the test from the file, "
                    "no host was found matching the source hostname. "
                    "Please select a host from the list that corresponds "
                    "to the source host of the test, or ignore it to discard this test entry.")
        ttk.Label(dialog, text=warning_text, wraplength=380, justify="left", font=("Arial", 10, "bold")).pack(pady=5)
        
        test_info = (f"Test data:\n"
                    f"\tTest ID: {test['teste_id']}\n"
                    f"\tSource: {test['src_ip']}\n"
                    f"\tDestination: {test['dst_ip']}\n"
                    f"\tProtocol: {test['protocol']}\n"
                    f"\tSource Port: {test['src_port']}\n"
                    f"\tDestination Port: {test['dst_port']}\n"
                    f"\tExpected success for the test: {test['expected']}")
        ttk.Label(dialog, text=test_info, justify="left").pack(pady=5)

        ttk.Label(dialog, text=f"Then the source host ({source})\n" 
                                f"was not found in the test scenario.\n"
                                f"Please select a corresponding host or ignore.").pack(pady=5)
        
        host_var = tk.StringVar()
        combobox = ttk.Combobox(dialog, textvariable=host_var, values=available_hosts, state="readonly", width=30)
        combobox.pack(pady=5)
        combobox.set(available_hosts[0] if available_hosts else "")

        selected_host = None
        container_id = None
        
        def on_select():
            nonlocal selected_host
            nonlocal container_id
            selected_host = host_var.get()
            hostname = self.extract_hostname(selected_host)
            container_id = self.find_container_id(hostname)
            print(f"container_id on select {container_id}")
            #selected_host = self.replace_hostname(source, selected_host)
            dialog.destroy()

        def on_ignore():
            nonlocal selected_host
            selected_host = None
            dialog.destroy()

        ttk.Button(dialog, text="Select", command=on_select).pack(side="left", padx=10, pady=10)
        ttk.Button(dialog, text="Ignore", command=on_ignore).pack(side="right", padx=10, pady=10)

        dialog.wait_window()  # wait closing window
        
        return container_id,selected_host
    
    def firewall_test_tree_select_line_test(self, event):
        """
            Method executed when a row of the firewall test table is executed (on tab firewall test ).
        """
        #print("firewall_test_tree_select_line")
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            if item_values:
                #print(f"{item_values}")
                
                self.src_ip.set(item_values[2])

                self.dst_ip.delete(0, tk.END)
                self.dst_ip.insert(0, item_values[3])

                self.protocol.set(item_values[4])

                self.src_port.delete(0, tk.END)
                self.src_port.insert(0, item_values[5])

                self.dst_port.delete(0, tk.END)
                self.dst_port.insert(0, item_values[6])

                self.expected.set(item_values[7])

        if not self.tree.selection():
            self.button_tree_test.config(state="disabled")
        else:
            self.button_tree_test.config(state="normal")
            self.button_tree_test_all.config(state="normal")

        self.button_tree_add.config(state="normal")
        self.button_tree_edit.config(state="disable")
        self.button_tree_del.config(state="disable")
        
    
    def firewall_test_tree_double_click_line_test(self, event):
        """
            Treat double click in firewall teste tree
        """
        self.firewall_test_tree_select_line_test(event)
        self.firewall_tests_buttons_set_editing_state()
        
    def firewall_tests_buttons_set_editing_state(self):
        """
            Defines the state of the firewall test buttons when editing a line/test. 
            State used to prevent the user from running a test while the rule is malformed (under editing or deletion)
        """
        self.button_tree_edit.config(state="normal")
        self.button_tree_del.config(state="normal")
        self.button_tree_add.config(state="disabled")
        self.button_tree_test.config(state="disabled")
        self.button_tree_test_all.config(state="disabled")
        self.button_tree_edit.config(text="Save Edit")
    
    def firewall_test_tree_select_line_test(self, event):
        """
            Method executed when a row of the firewall test table is executed (on tab firewall test ).
        """
        #print("firewall_test_tree_select_line")
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            if item_values:
                #print(f"{item_values}")
                
                self.src_ip.set(item_values[2])

                self.dst_ip.delete(0, tk.END)
                self.dst_ip.insert(0, item_values[3])

                self.protocol.set(item_values[4])

                self.src_port.delete(0, tk.END)
                self.src_port.insert(0, item_values[5])

                self.dst_port.delete(0, tk.END)
                self.dst_port.insert(0, item_values[6])

                self.expected.set(item_values[7])

        if not self.tree.selection():
            self.button_tree_test.config(state="disabled")
        else:
            self.button_tree_test.config(state="normal")
            self.button_tree_test_all.config(state="normal")

        self.button_tree_add.config(state="normal")
        self.button_tree_edit.config(state="disable")
        self.button_tree_del.config(state="disable")
    
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
            if (self.check_is_duplicate(values, item)):
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
        """
            Edit a row/test of an existing item/test in the firewall test Treeview. The test to be edited is the one currently selected in the treeview.
        """
        selected_item = self.tree.selection()
        print(f"Selected item {selected_item}")
        if not selected_item:
            messagebox.showwarning("Warning", "Select an item to edit!")
            return
        
        src_ip = self.src_ip.get()
        dst_ip = self.dst_ip.get()
        protocol = self.protocol.get()
        src_port = self.src_port.get()
        dst_port = self.dst_port.get()
        expected = self.expected.get()

        if self.firewall_tests_validate_entrys() != 0: return # Test values

        values = [src_ip, dst_ip, protocol, src_port, dst_port, expected, "-", " ", " "]

        for item in self.tree.get_children():
            if (self.check_is_duplicate(values, item)):
                messagebox.showwarning("Warning", "This entry already exists in the table!")
                return

        # Gets the ID of the container selected in the Combobox
        selected_index = self.src_ip.current()
        if selected_index >= 0 and selected_index < len(self.simulation.containers_data):
            container_id = self.simulation.containers_data[selected_index]["id"]
        else:
            container_id = "N/A"  # If no container is selected
        
        values=[self.tree.item(selected_item, "values")[0], container_id, src_ip, dst_ip, protocol, src_port, dst_port, expected, "-", " ", " "]

        self.tree.item(selected_item, values=values)
        self.tree.item(selected_item, tags="")  # return the color to default
        

        self.firewall_tests_buttons_set_normal_state()
        
    
    def firewall_test_tree_delete_line_test(self): # TODO - renumber lines when removing a test
        """
            Delete a row/test of an existing item/test in the firewall test Treeview. The test to be deleted is the one currently selected in the treeview.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Select an item to delete!")
            return
        self.tree.delete(selected_item)

        self.firewall_tests_buttons_set_normal_state() 
    
    
    def firewall_tests_run_test_line(self):
        """
            Test only one row of the firewall test table. This row will be the currently selected row in the firewall test tree.
        """
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item, "values")
            print(f"Items to testing:: {values}")
            teste_id, container_id, src_ip, dst_ip, protocol, src_port, dst_port, expected, result, dnat, observation = values
            
            # if you were unable to extract the destination IP entered by the user to
            dst_ip = self.extract_destination_host(dst_ip)
            if dst_ip == None: return
            
            print(f"Test executed - Container ID: {container_id}, Dados: {src_ip} -> {dst_ip} [{protocol}] {src_port}:{dst_port} (Expected: {expected})")

            result_str = containers.run_client_test(container_id, dst_ip, protocol.lower(), dst_port, "1", "2025", "0")

            try:
                result = json.loads(result_str)
                print(f"The return of the command on the host is {result_str}")
            except (json.JSONDecodeError, TypeError) as e:
                print("Error processing JSON received from host:", e)
                messagebox.showerror("Error", "Could not get a response from the hosts! \n Is GNS3 or the hosts turned on?")
                result = None
                return

            self.firewall_tests_analyse_results_update_tree(expected, result, values, selected_item)
            self.tree.selection_set(())
            
    def firewall_tests_analyse_results_update_tree(self, expected, result, values, selected_item):
        """
            Analyze the test result and update the table with the fields and colors that represent these results in the firewall test tree.

            Args:
                expected: result that was expected from the test.
                result: result obtained in the test.
                values: values ​​used and obtained in the test, such as source, destination, etc. are the columns of the firewall test treeview.
                selected_item: Test line used and which will have its values ​​and color updated in the firewall test table.
        """
        # TODO - check whether all cases have been covered
        # TODO - improve logic for checking user errors - such as testing a port that is not connected!
        #print(values)
        update_values = list(values)
        tag = None

        if result["server_response"] == True: # if the server responded then put sent/receved, otherwise just Sent - TODO - there may be a case where it didn't even send, which would be the case of the error!
                    update_values[9] = "Sent/Receved" # The package was just sent and there was a response!
                    update_values[8] = "Pass"
        else:
                    update_values[9] = "Sent" # The package was just sent but there was no response!
                    update_values[8] = "Fail"

        network_data = result['client_ip']+':'+str(result['client_port'])+'->'+result['server_ip']+':'+str(result['server_port'])+'('+result['protocol']+')'+' - Server response? '+ str(result['server_response'])+ ' - Status: '+result['status_msg']
        update_values[-1] = network_data

        if (result["status"] != '0'):
            # an error occurred, such as the host network was not configured.
            print(f"\033[33mThere was an error with the host when sending the packet, such as a misconfigured network - IP, GW, etc.\033[0m")
            update_values[8] = "ERROR"
            update_values[9] = "Not Sent"
            tag = "error"
        elif (result["server_response"] == True and expected == "yes"):
            # test performed successfully and there was a response from the server.
            print(f"\033[32mThe SUCCESS test occurred as expected.\033[0m")
            tag = "yes"
        elif (result["server_response"] == False and expected == "no"):
            # # The packet sending test failed, but this was expected in the test, so this is a success!
            print(f"\033[32mThe FAIL test occurred as expected.\033[0m")
            tag = "yesFail"
        else: # TODO - I think the logic is wrong here (check the possible cases) - is that in client.py you had to remove status=1 because it said there was an error in a packet blocked by the firewall!
            print(f"\033[31mThe test did NOT occur as expected.\033[0m")
            tag = "no"


        if "dnat" in result: # dnat only happens if there is a response from the server so there is no need for result["server_response"] == True - this comes from server.py
                #print("dnat")
                # there was DNAT
                dnat_data = result["dnat"]
                network_data = result['client_ip']+':'+str(result['client_port'])+'->'+dnat_data['ip']+':'+str(dnat_data['port'])+'('+result['protocol']+')'+' - Server response? '+ str(result['server_response'])+ ' - Status: '+result['status_msg']
                update_values[-1] = network_data
                update_values[9] = "Sent/Receved (DNAT)"
        
        # update the test line in the firewall test tree.
        self.tree.item(selected_item, values=update_values, tags=(tag,))
        
    def extract_destination_host(self, destination):
        """
            Extract the target host.

            Args:
                dst_ip: destination, can be a IP, host (IP) or a domain.
        """
        temp_destination =  self.extract_ip_parenthesized_from_string(destination)
        #print(f"temp_dst_ip {temp_destination}")

        if temp_destination != None:
            destination = temp_destination
        else:
            # without parentheses
            temp_destination = self.extract_ip_from_string(destination)
            if temp_destination != None:
                destination = temp_destination
            else:
                # dpmain
                temp_destination = self.extract_domain(destination)
                if temp_destination != None:
                    destination = temp_destination
                else:
                    # invalid
                    print(f"\033[33mCould not extract the destination IP in the interface:\n\tThe destination address must be an IP or domain, such as: 8.8.8.8 or www.google.com.\033[0m")
                    return None
        return destination    
    
    def extract_ip_parenthesized_from_string(self,string):
        """
            Extract IPs from a string, this method expects the IP to be in parentheses, which is the host format presented in the comboboxes of the firewall testing tab. 
            So the string will be something like: Host1 (10.0.0.1), the method will return only 10.0.0.1. Only IPv4.

            Args:
                string: String to be parsed for IP
        """
        match = re.search(r'\((\d+\.\d+\.\d+\.\d+)\)', string)
        return match.group(1) if match else None
    
    def extract_ip_from_string(self, string):
        """
            Extract IPs from a string. Only IPv4.
            Args:
                string: String to be parsed for IP
        """
        match = re.search(r'\(?(\d+\.\d+\.\d+\.\d+)\)?', string)  
        return match.group(1) if match else None
    
    def firewall_tests_popup_for_run_all_tests_using_threads(self):
        """
            Starts a window with a progress bar that executes all the tests in the firewall test tree. Threads are used for the progress bar to work.
        """
        print("Thread to execute all tests.")
        popup_window = tk.Toplevel(self.parent)
        popup_window.title("Processing...")
        popup_window.geometry("300x120")
        popup_window.resizable(False, False)
        
        status_label = tk.Label(popup_window, text="Starting...", font=("Arial", 10))
        status_label.pack(pady=10)

        progress_bar = tk.IntVar()
        barra_progresso = ttk.Progressbar(popup_window, length=250, mode="determinate", variable=progress_bar)
        barra_progresso.pack(pady=5)

        self.tree.selection_set(())
        self.firewall_tests_update_tree()

        threading.Thread(target=self.firewall_tests_run_all_tests, args=(popup_window, progress_bar, status_label), daemon=True).start()
        
    def firewall_tests_update_tree(self):
        """
            Updates the treeview of tests in the firewall, in firewall tests tab.
        """
        itens = self.tree.get_children()

        for item in itens:
            self.tree.item(item, tags="")  # Sets tags to an empty list
            
    def firewall_tests_run_all_tests(self, popup_window : tk.Toplevel, progress_bar : tk.IntVar, status_label : tk.Label):
        """
            Run a all tests in the firewall test treeview.

            Args:
                popup_window: Pop up window used to show tests progress.
                progress_bar: Progress bar used in the popup to show tests progresses.
                status_label: Label used in the popup to show the tests progress.
        """
        index=0
        
        itens = self.tree.get_children()

        total_list = len(itens)
        for test in itens:
            values = self.tree.item(test, "values")
            teste_id, container_id, src_ip, dst_ip, protocol, src_port, dst_port, expected, result, dnat, observation = values
            print(f"Executing test - Container ID:  {container_id}, Data: {src_ip} -> {dst_ip} [{protocol}] {src_port}:{dst_port} (Expected: {expected})")
            
            # if you were unable to extract the destination IP entered by the user to
            dst_ip = self.extract_destination_host(dst_ip)
            if dst_ip == None: return

            print(f"Executing test - Container ID:  {container_id}, Data: {src_ip} -> {dst_ip} [{protocol}] {src_port}:{dst_port} (Expected: {expected})")

            result_str = containers.run_client_test(container_id, dst_ip, protocol.lower(), dst_port, "1", "2025", "0")

            try:
                result = json.loads(result_str)
            except (json.JSONDecodeError, TypeError) as e:
                print("Error processing the JSON received from the host:", e)
                messagebox.showerror("Error", "Unable to get a response from the hosts! \n Is GNS3 or the hosts running?")
                result = None
                return

            self.firewall_tests_analyse_results_update_tree(expected,result, values, test)

            index+=1
            percentage_compete = (index / total_list) * 100
            progress_bar.set(percentage_compete)  # Update progress bar
            status_label.config(text=f"Processing... {index}/{total_list}")
            

        status_label.config(text="Task completed!")
        progress_bar.set(100)  # Ensures the bar goes all the way to the end
        popup_window.destroy()
            
    def extract_domain(self, string):
        """
            Extract domain from a string. This method expects two or more words separated by a dot - this method is not perfect.
            Args:
                string: String to be parsed for domain
        """
        match = re.search(r'\(?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\)?', string)
        return match.group(1) if match else None
    
    def delete_all_tests(self):
        itens = self.tree.get_children()
        for test in itens:
            self.tree.delete(test)

    def check_is_duplicate(self, values : list[str], item):
        existing_values = self.tree.item(item, "values")
        if tuple(values) == existing_values[2:]:
            # messagebox.showwarning("Warning", "This entry already exists in the table!")
            return True
        else:
            return False