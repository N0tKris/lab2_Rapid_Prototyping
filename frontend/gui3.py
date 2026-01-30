import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Backend URL - change this if your port is different
URL = "http://localhost:8080/api/catalog"

class CatalogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Catalog Manager")
        self.root.geometry("650x450")
        
        # Title label
        tk.Label(root, text="Catalog Management System", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Treeview (table) frame
        frame = tk.Frame(root)
        frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        # Create treeview with columns
        columns = ('id', 'name', 'description')
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', height=10)
        
        # Define headings
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Name')
        self.tree.heading('description', text='Description')
        
        # Column widths
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('name', width=150)
        self.tree.column('description', width=350)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Entry fields frame
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5)
        self.name_entry = tk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(input_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        self.desc_entry = tk.Entry(input_frame, width=30)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Buttons frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Load Items", command=self.load_data).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Add", command=self.add_item).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Update", command=self.update_item).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_item).pack(side=tk.LEFT, padx=5)
        
        # Status label at bottom
        self.status = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load data when app starts
        self.load_data()
    
    def load_data(self):
        """Get all items from backend and show in treeview"""
        try:
            response = requests.get(URL)
            items = response.json()
            
            # Clear current items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Add items to treeview
            for item in items:
                self.tree.insert('', tk.END, values=(item['id'], item['name'], item['description']))
            
            self.status.config(text=f"Loaded {len(items)} items")
        except Exception as e:
            messagebox.showerror("Error", f"Could not connect to backend: {e}")
            self.status.config(text="Connection failed")
    
    def get_selected_id(self):
        """Get the ID of currently selected item"""
        try:
            selected = self.tree.selection()
            if not selected:
                return None
            # Get the values tuple (id, name, description) and return id
            return self.tree.item(selected[0])['values'][0]
        except:
            return None
    
    def add_item(self):
        """Add new item to catalog"""
        name = self.name_entry.get().strip()
        desc = self.desc_entry.get().strip()
        
        if not name or not desc:
            messagebox.showwarning("Warning", "Please enter both name and description")
            return
        
        try:
            response = requests.post(URL, json={"name": name, "description": desc})
            if response.status_code == 201:
                messagebox.showinfo("Success", "Item added!")
                self.name_entry.delete(0, tk.END)
                self.desc_entry.delete(0, tk.END)
                self.load_data()
            else:
                messagebox.showerror("Error", "Failed to add item")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def update_item(self):
        """Update existing item"""
        item_id = self.get_selected_id()
        if not item_id:
            messagebox.showwarning("Warning", "Please select an item first")
            return
        
        name = self.name_entry.get().strip()
        desc = self.desc_entry.get().strip()
        
        if not name or not desc:
            messagebox.showwarning("Warning", "Please enter both name and description")
            return
        
        try:
            response = requests.put(f"{URL}/{item_id}", json={"name": name, "description": desc})
            if response.status_code == 200:
                messagebox.showinfo("Success", "Item updated!")
                self.load_data()
            else:
                messagebox.showerror("Error", "Failed to update")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def delete_item(self):
        """Delete selected item"""
        item_id = self.get_selected_id()
        if not item_id:
            messagebox.showwarning("Warning", "Please select an item first")
            return
        
        # Ask for confirmation
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this item?"):
            return
        
        try:
            response = requests.delete(f"{URL}/{item_id}")
            if response.status_code == 200:
                messagebox.showinfo("Success", "Item deleted!")
                self.load_data()
            else:
                messagebox.showerror("Error", "Failed to delete")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Main program
if __name__ == "__main__":
    window = tk.Tk()
    app = CatalogApp(window)
    window.mainloop()