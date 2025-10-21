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

class FirewallRulesPage(ttk.Frame):
    def __init__(self, parent):
        """
            Create firewal rules tab, this permit create, list and edit firewall rules on the hosts.
        """
        super().__init__(parent)
        ttk.Label(self, text="Firewall Test", font=("Arial", 12)).pack(pady=10)
        '''
                # Top frame for title. 
        frame_tittle = tk.Frame(self.firewall_rules)
        frame_tittle.pack(fill=tk.X)

        ttk.Label(frame_tittle, text="Edit firewall rules on host:", font=("Arial", 12, "bold")).pack(padx=10)
        #self.combobox_firewall_rules_host = ttk.Combobox(frame_tittle, values=self.hosts_display, width=25, state="readonly", style="TCombobox")
        self.combobox_firewall_rules_host = ttk.Combobox(frame_tittle, values=self.hosts, width=25, state="readonly", style="TCombobox")
        self.combobox_firewall_rules_host.pack(pady=10)
        #self.combobox_host_regra_firewall.current(0)
        self.combobox_firewall_rules_host.set("")

        self.combobox_firewall_rules_host.bind("<<ComboboxSelected>>", self.selected_host_on_combobox_tab_firewall_rules)

        #label_titulo = tk.Label(frame_titulo, text="Editar regras de firewall", font=("Arial", 12, "bold"))
        #label_titulo.pack(pady=5)

        # Creating frame for the labels
        frame_firewall_rules = ttk.LabelFrame(self.firewall_rules, text="Rules to be applied to the firewall")
        frame_firewall_rules.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.text_firewall_rules = tk.Text(frame_firewall_rules, wrap=tk.NONE, height=10, undo=True)
        self.text_firewall_rules.grid(row=0, column=0, sticky="nsew")

        scroll_y_firewall_rules = tk.Scrollbar(frame_firewall_rules, orient=tk.VERTICAL, command=self.text_firewall_rules.yview)
        scroll_y_firewall_rules.grid(row=0, column=1, sticky="ns")
        self.text_firewall_rules.config(yscrollcommand=scroll_y_firewall_rules.set)

        scroll_x_firewall_rules = tk.Scrollbar(frame_firewall_rules, orient=tk.HORIZONTAL, command=self.text_firewall_rules.xview)
        scroll_x_firewall_rules.grid(row=1, column=0, sticky="ew")
        self.text_firewall_rules.config(xscrollcommand=scroll_x_firewall_rules.set)

        self.reset_firewall = tk.IntVar()
        checkbtn_reset_firewall_rules = tk.Checkbutton(frame_firewall_rules, text="Automatically reset firewall rules – this should be in your script, but you can do it here.", variable=self.reset_firewall)
        checkbtn_reset_firewall_rules.grid(row=2, column=0, sticky="w")

        frame_firewall_rules.grid_columnconfigure(0, weight=1)
        frame_firewall_rules.grid_rowconfigure(0, weight=1)

        # Creating frame for the active rules
        frame_output_firewall_rules = ttk.LabelFrame(self.firewall_rules, text="Output ")
        frame_output_firewall_rules.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        #frame_ativas.pack_forget()  # Hide on the start

        def toggle_frame_output_on_rule_tab():
            """
                Change frame output to hide or show output text in firewall rule tab.
            """
            if frame_output_firewall_rules.winfo_ismapped():
                frame_output_firewall_rules.pack_forget()
                button_show_active_firewall_rules.config(text="Show output")
            else:
                frame_output_firewall_rules.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
                button_show_active_firewall_rules.config(text="Hide output")

        def select_all_text_on_rules_text(event):
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
        frame_buttons = tk.Frame(self.firewall_rules)
        frame_buttons.pack(pady=10)

        self.button_retrieve_firewall_rules = tk.Button(frame_buttons, text="Retrieve firewall rules", command=self.load_firewall_rules)
        self.button_retrieve_firewall_rules.pack(side=tk.LEFT, padx=10)
        self.button_retrieve_firewall_rules.config(state="disabled")

        self.button_deploy_firewall_rules = tk.Button(frame_buttons, text="Deploy firewall rules", command=self.apply_firewall_rules)
        self.button_deploy_firewall_rules.pack(side=tk.LEFT, padx=10)
        self.button_deploy_firewall_rules.config(state="disable")

        #self.btn_zerar = tk.Button(frame_botoes, text="Zerar Regras no firewall", command=self.zerar_regras_firewall)
        #self.btn_zerar.pack(side=tk.LEFT, padx=10)
        #self.btn_zerar.config(state="disable")

        button_show_active_firewall_rules = tk.Button(frame_buttons, text="Hide output", command=toggle_frame_output_on_rule_tab)
        button_show_active_firewall_rules.pack(side=tk.RIGHT, padx=10)
        '''