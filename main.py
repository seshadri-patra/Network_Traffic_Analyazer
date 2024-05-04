import psutil
import time
import pandas as pd
import tkinter as tk
from tkinter import ttk

UPDATE_DELAY = 1 # in seconds

def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024
        
def update_io():
    global io
    io_2 = psutil.net_io_counters(pernic=True)
    data = []
    for iface, iface_io in io.items():
        upload_speed, download_speed = io_2[iface].bytes_sent - iface_io.bytes_sent, io_2[iface].bytes_recv - iface_io.bytes_recv
        data.append({
            "Iface": iface,
            "Download": get_size(io_2[iface].bytes_recv),
            "Upload": get_size(io_2[iface].bytes_sent),
            "Upload Speed": f"{get_size(upload_speed / UPDATE_DELAY)}S",
            "Download Speed": f"{get_size(download_speed / UPDATE_DELAY)}S",
        })
    io = io_2
    df = pd.DataFrame(data)
    df.sort_values("Download", inplace=True, ascending=False)
    tree.delete(*tree.get_children())
    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))
    root.after(1000, update_io)

root = tk.Tk()
root.title("Network Statistics")

tree = ttk.Treeview(root, columns=("iface", "Download", "Upload", "Upload Speed", "Download Speed"))
tree.heading("iface", text="Interface")
tree.heading("Download", text="Download")
tree.heading("Upload", text="Upload")
tree.heading("Upload Speed", text="Upload Speed")
tree.heading("Download Speed", text="Download Speed")
tree.pack()
io = psutil.net_io_counters(pernic=True)
root.after(1000, update_io)
root.mainloop()
