import tkinter as tk
from tkinter import ttk
import textwrap
import webbrowser

class AboutPage(ttk.Frame):
    def __init__(self, parent: ttk.Widget):
        
        """
        Create tab about to present some informations about the software interface like: author, description, licence, etc.
        """
        super().__init__(parent)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1) 

        content_frame = ttk.Frame(self)
        content_frame.grid(row=0, column=0, sticky="ew", padx=20)
        content_frame.columnconfigure(0, weight=1)

        row = 0
        
        def add_centered(label_text, font=None, is_link=None, bind_url=None, pady=(0, 2)):
                    nonlocal row
                    lbl = ttk.Label(content_frame, text=label_text, font=font, anchor="center", justify="center")
                    lbl.grid(row=row, column=0, pady=pady, sticky="ew")
                    if is_link and bind_url:
                        lbl.configure(foreground="blue", cursor="hand2")
                        lbl.bind("<Button-1>", lambda e: webbrowser.open_new_tab(bind_url))
                    row += 1
                    return lbl
        
        add_centered("About the Software", font=("Arial", 14, "bold"), )

        # --- Description ---
        description = (
            "This software was developed with the goal of strengthening network security "
            "through practical and efficient firewall testing. More than just a testing tool, "
            "it stands out as a valuable educational resource, designed to simplify and enhance "
            "the learning process about firewalls. Through an intuitive and interactive interface, "
            "students can visualize and experiment with the creation and application of firewall "
            "rules, making it easier to understand complex concepts and promoting deeper and more "
            "effective learning."
        )
        wrapped_text = textwrap.fill(description, width=70)
        bg_color = parent.cget("background")

        description_frame = ttk.Frame(content_frame)
        description_frame.grid(row=row, column=0, sticky="ew", pady=10)
        row += 1
        description_frame.columnconfigure(0, weight=1)
        description_frame.rowconfigure(0, weight=1)

        text_widget = tk.Text(
            description_frame, wrap="word", width=70, height=8,
            borderwidth=0, highlightthickness=0, background=bg_color
        )
        text_widget.insert("1.0", wrapped_text)
        text_widget.config(state="disabled")
        text_widget.grid(row=0, column=0, sticky="ew")
        text_widget.tag_configure("center", justify='center')
        text_widget.tag_add("center", "1.0", "end")
        
        add_centered("Developer:")
        add_centered("Prof. Luiz Arthur Feitosa dos Santos", font=("Arial", 12, "bold"))
        add_centered("luiz.arthur.feitosa.santos@gmail.com", is_link=True, bind_url="mailto:luiz.arthur.feitosa.santos@gmail.com")
        add_centered("Institution:")
        add_centered("UTFPR-CM", font=("Arial", 12, "bold"))
        add_centered("Project Link:")
        add_centered("https://github.com/luizsantos/firewallTester", is_link=True, bind_url="https://github.com/luizsantos/firewallTester")
        add_centered("License:")
        add_centered("GNU GPL v3", is_link=True, bind_url="https://www.gnu.org/licenses/gpl-3.0.html")

        # --- Help Button (centered) ---
        btn_help = ttk.Button(content_frame, text="Help", command=self.open_help)
        btn_help.grid(row=row, column=0, pady=(10, 0), sticky="n")  # small top margin; stays centered horizontally

    def open_help(self):
        webbrowser.open_new_tab("https://github.com/luizsantos/firewallTester")
