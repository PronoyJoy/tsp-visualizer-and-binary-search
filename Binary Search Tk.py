import tkinter as tk
from tkinter import messagebox

class BinarySearchVisualization:
    def __init__(self, root, array):
        self.root = root
        self.root.title("Binary Search Visualization")
        
        self.array = sorted(array)
        self.canvas = tk.Canvas(self.root, bg="white", width=600, height=400)
        self.canvas.pack(padx=10, pady=10)
        
        self.draw_array()
        
        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=20)
        
        self.search_btn = tk.Button(self.root, text="Search", command=self.perform_search)
        self.search_btn.pack()

    def draw_array(self):
        self.canvas.delete("all")
        bar_width = 600 // len(self.array)
        
        for i, value in enumerate(self.array):
            x0 = i * bar_width
            y0 = 400 - value
            x1 = (i + 1) * bar_width
            y1 = 400
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue", tags=f"bar{i}")
            self.canvas.create_text(x0 + bar_width // 2, y0 - 10, text=str(value), tags=f"label{i}")

    def perform_search(self):
        target = self.entry.get()
        if not target.isdigit():
            messagebox.showwarning("Invalid Input", "Please enter a valid number.")
            return
        
        target = int(target)
        left, right = 0, len(self.array) - 1
        
        while left <= right:
            mid = (left + right) // 2
            self.highlight_bar(mid, "yellow")
            
            if self.array[mid] == target:
                self.highlight_bar(mid, "green")
                messagebox.showinfo("Search Result", f"Found {target} at position {mid}")
                return
            elif self.array[mid] < target:
                left = mid + 1
                self.highlight_bar(mid, "red")
            else:
                right = mid - 1
                self.highlight_bar(mid, "red")
        
        messagebox.showinfo("Search Result", f"{target} not found in the array.")

    def highlight_bar(self, index, color):
        bar_width = 600 // len(self.array)
        x0 = index * bar_width
        y0 = 400 - self.array[index]
        x1 = (index + 1) * bar_width
        y1 = 400
        
        self.canvas.itemconfig(f"bar{index}", fill=color)
        self.root.update()
        self.root.after(1000)
        self.canvas.itemconfig(f"bar{index}", fill="blue")

if __name__ == "__main__":
    root = tk.Tk()
    app = BinarySearchVisualization(root, [10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    root.mainloop()
