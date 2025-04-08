import tkinter as tk

class MaskedEntry(tk.Entry):
    def __init__(self, master, mask, **kwargs):
        super().__init__(master, **kwargs)
        self.mask = mask
        self.bind("<KeyRelease>", self.format_input)

    def format_input(self, event):
        current = self.get().replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        formatted = ""
        mask_pos = 0
        
        for char in current:
            if mask_pos >= len(self.mask):
                break
            if self.mask[mask_pos] == "X":
                formatted += char
                mask_pos += 1
            else:
                formatted += self.mask[mask_pos]
                mask_pos += 1
                formatted += char
                mask_pos += 1
        
        self.delete(0, tk.END)
        self.insert(0, formatted)