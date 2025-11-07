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

# TODO - would it be good to have a button to reset the firewall rules?
class FirewallRulesPage(ttk.Frame):
    
    combobox_firewall_rules_host : ttk.Combobox
    simulation : SimulationManager
    
    def selected_host_on_combobox_tab_firewall_rules(self, src_ip):
            """
                Treats the selected host in the combobox
            """
            #print("selected_host_on_combobox_tab_firewall_rules")
            selected_index = self.combobox_firewall_rules_host.current()
            if selected_index >= 0 and selected_index < len(self.simulation.container_hostname):
                container_id = [self.simulation.container_hostname[selected_index][0], self.simulation.container_hostname[selected_index][1]]
                #print(f"container_data selected_index{selected_index} -  {self.containers_data[selected_index]}")
            else:
                container_id = "N/A"  # Caso nenhum container seja selecionado
            #print(container_id)
            self.button_retrieve_firewall_rules.config(state="normal")
            self.button_deploy_firewall_rules.config(state="normal")
            self.button_list_firewall_rules.config(state="normal")
            #self.btn_zerar.config(state="normal")
            self.container_id_host_regras_firewall=container_id
    
    def __init__(self, parent, simulation : SimulationManager):
        """
            Create firewal rules tab, this permit create, list and edit firewall rules on the hosts.
        """
        super().__init__(parent)
        
        self.simulation = simulation
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1) 
        
        content_frame = ScrollablePage(self)
        content_frame.columnconfigure(0, weight=1)
        #content_frame.columnconfigure(1, weight=1)
        
        frame_title = tk.Frame(content_frame)
        frame_title.grid(row=0, column=0,)
        
        lbl_title = ttk.Label(frame_title, text="Edit firewall rules on host:", font=("Arial", 12, "bold"))
        lbl_title.grid(row=0, column=0, sticky="ew",)
        
        self.combobox_firewall_rules_host = ttk.Combobox(frame_title, values=simulation.hosts.get(), width=25, state="readonly", style="TCombobox")
        self.combobox_firewall_rules_host.grid(row=1, column=0, sticky="ew",)
        self.combobox_firewall_rules_host.set("")
        
        self.combobox_firewall_rules_host.bind("<<ComboboxSelected>>", self.selected_host_on_combobox_tab_firewall_rules)
        
        #label_titulo = tk.Label(frame_titulo, text="Editar regras de firewall", font=("Arial", 12, "bold"))
        #label_titulo.pack(pady=5)

        # Creating frame for the labels
        frame_firewall_rules = ttk.LabelFrame(content_frame, text="Rules to be applied to the firewall")
        frame_firewall_rules.grid(row=2, column=0, padx=10, pady=5)

        self.text_firewall_rules = tk.Text(frame_firewall_rules, wrap=tk.NONE, height=10, undo=True)
        self.text_firewall_rules.grid(row=0, column=0, sticky="nsew")

        scroll_y_firewall_rules = tk.Scrollbar(frame_firewall_rules, orient=tk.VERTICAL, command=self.text_firewall_rules.yview)
        scroll_y_firewall_rules.grid(row=0, column=1, sticky="ns")
        self.text_firewall_rules.config(yscrollcommand=scroll_y_firewall_rules.set)

        scroll_x_firewall_rules = tk.Scrollbar(frame_firewall_rules, orient=tk.HORIZONTAL, command=self.text_firewall_rules.xview)
        scroll_x_firewall_rules.grid(row=1, column=0, sticky="ew")
        self.text_firewall_rules.config(xscrollcommand=scroll_x_firewall_rules.set)

        self.reset_firewall = tk.IntVar()
        checkbtn_reset_firewall_rules = tk.Checkbutton(frame_firewall_rules, text="Automatically reset firewall rules - this should be in your script, but you can do it here.", variable=self.reset_firewall)
        checkbtn_reset_firewall_rules.grid(row=2, column=0, sticky="w")

        frame_firewall_rules.grid_columnconfigure(0, weight=1)
        frame_firewall_rules.grid_rowconfigure(0, weight=1)
        
        # Creating frame for the active rules
        frame_output_firewall_rules = ttk.LabelFrame(content_frame, text="Output ")
        frame_output_firewall_rules.grid(row=5, column=0, padx=10, pady=5)
        
        
        def toggle_frame_output_on_rule_tab():
            """
                Change frame output to hide or show output text in firewall rule tab.
            """
            if frame_output_firewall_rules.winfo_ismapped():
                frame_output_firewall_rules.grid_remove()
                button_show_active_firewall_rules.config(text="Show output")
            else:
                frame_output_firewall_rules.grid()
                button_show_active_firewall_rules.config(text="Hide output")

        def select_all_text_on_rules_text(event : tk.Event):
            """
                Selecte every texto inside texto firewall rule - for use with Ctrl+A
            """
            event.widget.tag_add("sel", "1.0", "end")
            return "break"

        self.text_active_firewall_rules = tk.Text(frame_output_firewall_rules, wrap=tk.NONE, height=10)
        self.text_active_firewall_rules.grid(row=0, column=0, sticky="nsew")
        self.text_active_firewall_rules.bind("<Control-a>", select_all_text_on_rules_text)

        self.text_firewall_rules.bind("<Control-a>", select_all_text_on_rules_text)

        scroll_y_active_firewall_rules = tk.Scrollbar(frame_output_firewall_rules, orient=tk.VERTICAL, command=self.text_active_firewall_rules.yview)
        scroll_y_active_firewall_rules.grid(row=0, column=1, sticky="ns")
        self.text_active_firewall_rules.config(yscrollcommand=scroll_y_active_firewall_rules.set)
        self.text_active_firewall_rules.config(state=tk.NORMAL) # I don't know why, but if you don't activate and deactivate text_actives, select all doesn't work in text_rules
        #self.text_ativas.config(state=tk.DISABLED)

        scroll_x_active_firewall_rules = tk.Scrollbar(frame_output_firewall_rules, orient=tk.HORIZONTAL, command=self.text_active_firewall_rules.xview)
        scroll_x_active_firewall_rules.grid(row=1, column=0, sticky="ew")
        self.text_active_firewall_rules.config(xscrollcommand=scroll_x_active_firewall_rules.set)

        frame_output_firewall_rules.grid_columnconfigure(0, weight=1)
        frame_output_firewall_rules.grid_rowconfigure(0, weight=1)
        self.button_list_firewall_rules = tk.Button(frame_output_firewall_rules, text="List firewall rules", command=self.list_firewall_rules_on_output)
        self.button_list_firewall_rules.grid(row=2, column=0)
        self.button_list_firewall_rules.config(state="disabled")

        # Creating buttons
        frame_buttons = tk.Frame(content_frame)
        frame_buttons.grid(row=4, column=0, pady=10)

        self.button_retrieve_firewall_rules = tk.Button(frame_buttons, text="Retrieve firewall rules", command=self.load_firewall_rules)
        self.button_retrieve_firewall_rules.grid(row=0, column=0, padx=10)
        self.button_retrieve_firewall_rules.config(state="disabled")

        self.button_deploy_firewall_rules = tk.Button(frame_buttons, text="Deploy firewall rules", command=self.apply_firewall_rules)
        self.button_deploy_firewall_rules.grid(row=0, column=1, padx=10)
        self.button_deploy_firewall_rules.config(state="disable")

        #self.btn_zerar = tk.Button(frame_botoes, text="Zerar Regras no firewall", command=self.zerar_regras_firewall)
        #self.btn_zerar.pack(side=tk.LEFT, padx=10)
        #self.btn_zerar.config(state="disable")

        button_show_active_firewall_rules = tk.Button(frame_buttons, text="Hide output", command=toggle_frame_output_on_rule_tab)
        button_show_active_firewall_rules.grid(row=0, column=2, padx=10)
        
    def update_hosts(self):
        self.combobox_firewall_rules_host['values']=self.simulation.hosts.get() # update combobox values
    
    def apply_firewall_rules(self):
        """
            Apply/execute rules firewall rules on host/container selected in the combobox on the firewall rules tab.
        """
        print(f"Apply rules on the firewall of host {self.container_id_host_regras_firewall[1]}")
        rules = self.text_firewall_rules.get("1.0", tk.END)
        file_rules= self.simulation.current_settings["reset_rules_file"].get()
        with open(file_rules, "w", encoding="utf-8") as file_name:
            file_name.write(rules)
        print(f"Rules saved in the file {file_rules}")
        if self.reset_firewall.get() == 1: # If the checkbox is checked, first reset the firewall, then apply the rules.
            self.sento_to_host_file_to_execute_firewall_rules(self.simulation.current_settings["reset_rules_file"].get(), 1)
        
        self.sento_to_host_file_to_execute_firewall_rules(file_rules, None)
        
        if self.reset_firewall.get() == 1:
            self.text_active_firewall_rules.insert(tk.END, f"\n>>Warning!<< The firewall rules of host {self.container_id_host_regras_firewall[1]} were reset via the interface, but this SHOULD be in your firewall commands because firewalls do not reset automatically in real life!\n\n")
            self.text_active_firewall_rules.see(tk.END) # scroll to the end to see the most recent text!
            
            
            
    def sento_to_host_file_to_execute_firewall_rules(self, file_rules, reset): # se for reset indica que o caminho é o arquivo de reset, caso contrário são regras
        """
            Send to save in the container/host the firewall rules in the firewall interface (tab firewall rules). The container/host is selected in the combobox on the firewall rules tab.

            Args:
                file_rules (string) - source file.
                reset - indicate if the firewall rules will be reseted or not by the interface.  If it is reset it indicates that the path is the reset file, otherwise it is rules.

        """
        print(f"Send and execute firewall rules on host {self.container_id_host_regras_firewall[1]}")
        
        file_reset = self.simulation.current_settings["firewall_directory"].get()+"/firewall_reset.sh"
        file = self.simulation.current_settings["firewall_directory"].get()+"/firewall.sh"

        if reset!=None:
            containers.copy_host2container(self.container_id_host_regras_firewall[0], file_rules, file_reset)
            command = ["docker", "exec", self.container_id_host_regras_firewall[0], "sh", file_reset]
        else:
            containers.copy_host2container(self.container_id_host_regras_firewall[0], file_rules, file)
            command = ["docker", "exec", self.container_id_host_regras_firewall[0], "sh", file]

        result = containers.run_command(command)

        self.text_active_firewall_rules.delete(1.0, tk.END)
        if result.stderr:
            self.text_active_firewall_rules.delete(1.0, tk.END)
            self.text_active_firewall_rules.insert(tk.END, f"\n* Error applying firewall rules - check if there is something wrong with the rules on host {self.container_id_host_regras_firewall[1]}:\n\n")
            self.text_active_firewall_rules.insert(tk.END, result.stderr)
            self.text_active_firewall_rules.see(tk.END) # scroll to the end to see the most recent text!
            messagebox.showinfo("Warning", "Something went wrong while executing the rules, check the output!")
        else:
            self.list_firewall_rules_on_output()
            self.text_active_firewall_rules.insert(tk.END, f"\n* Firewall status on host {self.container_id_host_regras_firewall[1]} after rules have been applied\n\n")
            self.text_active_firewall_rules.see(tk.END) # scroll to the end to see the most recent text!




    def list_firewall_rules_on_output(self):
        """
            List active firewall rules on the host and display in the output text on firewall rules tab. The container/host is selected in the combobox on the firewall rules tab.
        """
        print(f"List firewall rules for host {self.container_id_host_regras_firewall[1]}")
        
        self.text_active_firewall_rules.delete(1.0, tk.END)

        self.text_active_firewall_rules.tag_configure("bold", font=("TkDefaultFont", "10", "bold"))
        #self.text_active_firewall_rules.tag_configure("normal", font=("TkDefaultFont", "10"))

        #TODO: TEST if its returning the same thing as when it was using global variables
        if self.simulation.current_settings["include_mangle_table"].get() or self.simulation.current_settings["include_nat_table"].get() or self.simulation.current_settings["include_filter_table"].get():
            if self.simulation.current_settings["include_mangle_table"].get():
                command = ["docker", "exec", self.container_id_host_regras_firewall[0], "iptables", "-L", "-n", "-t", "mangle"]
                result = containers.run_command(command)
                self.text_active_firewall_rules.insert(tk.END, f"\n\u2022 Mangle Rules:", "bold")
                self.text_active_firewall_rules.insert(tk.END, f"\n - Result of the command iptables -t mangle -L on host {self.container_id_host_regras_firewall[1]}:\n\n")
                self.text_active_firewall_rules.insert(tk.END, result.stdout)    

            if self.simulation.current_settings["include_nat_table"].get():
                command = ["docker", "exec", self.container_id_host_regras_firewall[0], "iptables", "-L", "-n", "-t", "nat"]
                result = containers.run_command(command)
                self.text_active_firewall_rules.insert(tk.END, f"\n\u2022 NAT Rules:", "bold")
                self.text_active_firewall_rules.insert(tk.END, f"\n - Result of the command iptables -t nat -L on host {self.container_id_host_regras_firewall[1]}:\n\n")
                self.text_active_firewall_rules.insert(tk.END, result.stdout)
            
            if self.simulation.current_settings["include_filter_table"].get():
                command = ["docker", "exec", self.container_id_host_regras_firewall[0], "iptables", "-L", "-n"]
                result = containers.run_command(command)
                self.text_active_firewall_rules.insert(tk.END, f"\n\u2022 Filter Rules:", "bold")
                self.text_active_firewall_rules.insert(tk.END, f"\n - Result of the command iptables -L on host {self.container_id_host_regras_firewall[1]}:\n\n")
                self.text_active_firewall_rules.insert(tk.END, result.stdout)
        else:
            self.text_active_firewall_rules.insert(tk.END, f"\n* All firewall rule tables are disabled for listing in the settings tab - so if you want to list the rules enable them in the settings tab.\n\n")

        self.text_active_firewall_rules.see(tk.END) # rola o scroll para o final, para ver o texto mais recente!
        
    def load_firewall_rules(self):
        """
            Load firewall rules into container/host, this rules are present in the firewall rules texto component in the firewall rules tab. The container/host is selected in the combobox on the firewall rules tab.
        """
        print(f"Load firewall rules from hos {self.container_id_host_regras_firewall[1]}")

        resposta = messagebox.askyesno("Confirmation","This will overwrite the existing rules in the interface. Are you sure you want to continue?")
        # TODO - in UTPFR there was a problem when copying the file from the firewall to the container, it said it copied but didn't copy anything, it only copied when the file was touched - see this.
        if resposta:
            file = self.simulation.current_settings["firewall_directory"].get()+"/firewall.sh"
            command = ["docker", "exec", self.container_id_host_regras_firewall[0], "cat", file]
            result = containers.run_command(command)
            self.text_firewall_rules.delete(1.0, tk.END)
            self.text_firewall_rules.insert(tk.END, result.stdout)