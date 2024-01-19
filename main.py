import os
import tkinter as tk
from tkinter import filedialog

import numpy as np
import pandas as pd
from PIL import Image, ImageTk, ImageDraw
import csv
def _onKeyRelease(event):
    ctrl = (event.state & 0x4) != 0
    if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
        event.widget.event_generate("<<Cut>>")

    if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")

    if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")

class ImageLabelingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Labeling Tool")

        self.image_path = ""
        self.current_index = 0
        self.labels = []

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Enter label:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self.root,width=30, font=('Arial 24'))
        self.entry.pack(pady=10)

        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)

        self.load_button = tk.Button(self.root, text="Load Images", command=self.load_images)
        self.load_button.pack(pady=10)

        self.next_button = tk.Button(self.root, text="Next Image", command=self.next_image)
        self.next_button.pack(pady=10)

    def load_images(self):
        self.image_path = filedialog.askdirectory()
        self.labels = []

        # Get a list of image files in the selected directory
        image_files = [
            f for f in os.listdir(self.image_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))
        ]
        if not image_files:
            tk.messagebox.showinfo("Error", "No images found in the selected directory.")
            return

        self.image_files = [os.path.join(self.image_path, f) for f in image_files]
        self.show_image()

    def show_image(self):
        if self.current_index < len(self.image_files):
            print(self.image_files[self.current_index])
            image = Image.open(self.image_files[self.current_index])
            image = image.resize((600, 600))
            draw = ImageDraw.Draw(image)

            # Specify the number of rows and columns
            rows = 5
            cols = 5

            # Calculate the width and height of each grid cell
            cell_width = image.width // cols
            cell_height = image.height // rows

            # Draw horizontal lines
            for i in range(1, rows):
                y = i * cell_height
                draw.line([(0, y), (image.width, y)], fill="white", width=2)

            # Draw vertical lines
            for j in range(1, cols):
                x = j * cell_width
                draw.line([(x, 0), (x, image.height)], fill="white", width=2)

            photo = ImageTk.PhotoImage(image)

            self.image_label.config(image=photo)
            self.image_label.image = photo

    def next_image(self):
        label = self.entry.get()
        self.labels.append(label)

        self.current_index += 1
        self.show_image()

        # If all images are labeled, display a message
        if self.current_index == len(self.image_files):
            all_labels=np.array(self.labels)
            all_images=np.array(self.image_files)

            df = pd.DataFrame({"name": all_images, "label": all_labels})
            df.to_csv("labels.csv", index=False)
            tk.messagebox.showinfo("Finished", "All images labeled!")
            return True

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x850")
    root.bind_all("<Key>", _onKeyRelease, "+")
    app = ImageLabelingApp(root)
    root.mainloop()
