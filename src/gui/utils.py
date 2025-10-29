import tkinter as tk
from tkinter import ttk
import json

class ScrollablePage(ttk.Frame):
    """
    Create frame with capabilities of vertical scrolling and related scroll bar (needs to be alone in a frame)
    """
    def __init__(self, parent: ttk.Widget, posx=0, posy=0, axis=tk.Y):
        
        # create canvas for scrolling
        my_canvas = tk.Canvas(parent, borderwidth=0, highlightthickness=0)
        my_canvas.grid(row=posx, column=posy, sticky="nsew", padx=20)
        
        # create scroll bar
        scroll_bar_frame = tk.Scrollbar()
        if(axis == tk.Y):
            scroll_bar_frame = tk.Scrollbar(parent, orient="vertical", takefocus=0, command=my_canvas.yview,)
            my_canvas.configure(yscrollcommand=scroll_bar_frame.set)
            scroll_bar_frame.grid(row=posx+0, column=posy+1, sticky="nsew")
        else:
            scroll_bar_frame = tk.Scrollbar(parent, orient="horizontal", takefocus=0, command=my_canvas.xview,)
            my_canvas.configure(xscrollcommand=scroll_bar_frame.set)
            scroll_bar_frame.grid(row=posx+1, column=posy+0, sticky="nsew")
                
        super().__init__(parent) # initialize frame with parent
        
        self.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        #create window in canvas
        window_id = my_canvas.create_window((0, 0), window=self, anchor="center", tags="window")
        if(axis == tk.Y):
            my_canvas.bind('<Configure>', lambda e: my_canvas.itemconfigure(window_id, width=e.width))
        else:
            my_canvas.bind('<Configure>', lambda e: my_canvas.itemconfigure(window_id, height=e.height))
        
        
class ListVar(tk.StringVar):
    """
    Create class with StringVar conveniences such as callback but that stores a lists
    """
    def __init__(self, value = None, name = None):
        super().__init__(value=value)
        
    def get(self):
        """
        Return variable as a list
        """
        lista = f'[{super().get()[1:-1]}]'
        lista = json.loads(lista.replace("'", '"'))
        return lista
        