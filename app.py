import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw

class PixelArtEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PI Studio")
        self.geometry("500x400")

        self.pixel_size = 10  # Initial pixel size
        self.canvas_width = 32 * self.pixel_size
        self.canvas_height = 32 * self.pixel_size

        self.colors = ["black", "grey", "darkgrey", "red", "orange", "yellow", "green", "blue"]

        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.grid(row=0, column=1, padx=10, pady=10)

        self.palette_frame = tk.Frame(self)
        self.palette_frame.grid(row=0, column=0, padx=10, pady=10)

        for i, color in enumerate(self.colors):
            color_button = tk.Button(self.palette_frame, bg=color, width=3, command=lambda c=color: self.select_color(c))
            color_button.grid(row=i, column=0, padx=5, pady=5)

        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Export", command=self.export)
        file_menu.add_command(label="Exit", command=exit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)

        self.selected_color = self.colors[0]
        self.canvas.bind("<B1-Motion>", self.draw_pixel)

    def select_color(self, color):
        self.selected_color = color

    def draw_pixel(self, event):
        x = event.x // self.pixel_size
        y = event.y // self.pixel_size
        self.canvas.create_rectangle(x*self.pixel_size, y*self.pixel_size, (x+1)*self.pixel_size, (y+1)*self.pixel_size, fill=self.selected_color, outline="")

    def export(self):
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if filename:
            image = Image.new("RGBA", (self.canvas_width, self.canvas_height), (255, 255, 255, 0))
            draw = ImageDraw.Draw(image)

            pixels = self.canvas.find_all()
            if not pixels:
                # If canvas is empty, set the background to white
                draw.rectangle([0, 0, self.canvas_width, self.canvas_height], fill="white")
            else:
                for pixel in pixels:
                    x0, y0, x1, y1 = self.canvas.coords(pixel)
                    color = self.canvas.itemcget(pixel, "fill")
                    draw.rectangle([x0, y0, x1, y1], fill=color)

            image = image.resize((self.canvas_width // self.pixel_size, self.canvas_height // self.pixel_size), Image.NEAREST)
            image.save(filename)

if __name__ == "__main__":
    app = PixelArtEditor()
    app.mainloop()
