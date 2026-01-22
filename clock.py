from datetime import datetime
import tkinter as tk
from tkinter import font

class DigitalClock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Smart Clock – Double-click the center dot to toggle fullscreen "
                         "(do NOT press the native close button while fullscreen)")
        self.root.configure(bg='black')

        # Initial window size and position
        self.window_width = 1024
        self.window_height = 512
        self.window_x = 450
        self.window_y = 260
        self.root.geometry(f"{self.window_width}x{self.window_height}+{self.window_x}+{self.window_y}")

        # Full-screen flag
        self.is_fullscreen = False

        # Mouse-drag support
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.dragging = False

        # Custom fonts
        self.time_font = font.Font(family='Arial', size=48, weight='bold')
        self.date_font = font.Font(family='Arial', size=15, weight='bold')
        self.status_font = font.Font(family='Arial', size=15, weight='bold')

        # Time label
        self.time_label = tk.Label(
            self.root,
            text="",
            font=self.time_font,
            fg='cyan',
            bg='black'
        )
        self.time_label.pack(pady=20)

        # Date label (includes weekday)
        self.date_label = tk.Label(
            self.root,
            text="",
            font=self.date_font,
            fg='white',
            bg='black'
        )
        self.date_label.pack(pady=10)

        # Close button for fullscreen mode
        self.close_btn = tk.Button(
            self.root,
            text="✕",
            command=self.on_close,
            bg='black',
            fg='white',
            font=('Arial', 16, 'bold'),
            relief='flat'
        )
        self.close_btn.place_forget()  # Hidden initially

        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Running...",
            font=self.status_font,
            fg='green',
            bg='black'
        )
        self.status_label.pack(side=tk.BOTTOM, pady=20)

        # Event bindings
        self.root.bind('<Double-Button-1>', self.toggle_fullscreen)
        self.root.bind("<ButtonPress-1>", self.start_drag)
        self.root.bind("<ButtonRelease-1>", self.stop_drag)
        self.root.bind("<B1-Motion>", self.do_drag)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.running = True
        self.update_clock()

    def update_clock(self):
        if self.running:
            now = datetime.now()
            self.time_label.config(text=now.strftime('%H:%M:%S'))
            weekdays = ["Monday", "Tuesday", "Wednesday",
                        "Thursday", "Friday", "Saturday", "Sunday"]
            date_str = now.strftime('%Y-%m-%d') + f" {weekdays[now.weekday()]}"
            self.date_label.config(text=date_str)
            self.root.after(1000, self.update_clock)

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)

        if self.is_fullscreen:
            self.time_font.configure(size=96)
            self.date_font.configure(size=30)
            self.status_font.configure(size=25)
            # Show close button in upper-right corner
            self.close_btn.place(x=self.root.winfo_screenwidth() - 100, y=20)
        else:
            self.time_font.configure(size=48)
            self.date_font.configure(size=15)
            self.status_font.configure(size=15)
            self.close_btn.place_forget()
            self.root.geometry(f"{self.window_width}x{self.window_height}+{self.window_x}+{self.window_y}")

    def start_drag(self, event):
        if not self.is_fullscreen:
            self.drag_start_x = event.x
            self.drag_start_y = event.y
            self.dragging = True

    def do_drag(self, event):
        if self.dragging and not self.is_fullscreen:
            x = self.root.winfo_x() + event.x - self.drag_start_x
            y = self.root.winfo_y() + event.y - self.drag_start_y
            self.root.geometry(f"+{x}+{y}")

    def stop_drag(self, event):
        self.dragging = False

    def on_close(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    clock = DigitalClock()
    clock.root.mainloop()
    
