import tkinter as tk
from tkinter import ttk

class ScrollablePage(ttk.Frame):
    def __init__(self, parent: ttk.Widget):
        my_canvas = tk.Canvas(parent, borderwidth=0, highlightthickness=0)
        my_canvas.grid(row=0, column=0, sticky="nsew", padx=20)
        
        scroll_bar_frame = tk.Scrollbar(parent, orient="vertical", takefocus=0, command=my_canvas.yview,)
        scroll_bar_frame.grid(row=0, column=1, sticky="nsew")
        my_canvas.configure(yscrollcommand=scroll_bar_frame.set)
                
        super().__init__(parent)
        
        self.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
        
        #content_frame.grid(row=0, column=0, padx=20, sticky="new")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        window_id = my_canvas.create_window((0, 0), window=self, anchor="center", tags="window")
        my_canvas.bind('<Configure>', lambda e: my_canvas.itemconfigure(window_id, width=e.width))