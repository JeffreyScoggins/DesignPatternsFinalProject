import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from Menu import Menu 
from Order import Order 
from FoodCategory import FoodCategory 

class FoodOrderingGUI:
    def __init__(self):
        self.menu = Menu()
        self.current_order = None
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Food Ordering System")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_menu_tab()
        self.create_order_tab()
        self.create_add_item_tab()
    
    def create_menu_tab(self):
        """Create the menu browsing tab"""
        menu_frame = ttk.Frame(self.notebook)
        self.notebook.add(menu_frame, text="Menu")
        
        # Create canvas and scrollbar for scrollable content
        canvas = tk.Canvas(menu_frame, bg='white')
        scrollbar = ttk.Scrollbar(menu_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add menu items to scrollable frame
        row = 0
        for category in FoodCategory:
            items = self.menu.get_items_by_category(category)
            if items:
                # Category header
                header_frame = tk.Frame(scrollable_frame, bg='#2c3e50', height=40)
                header_frame.pack(fill='x', padx=5, pady=(10, 0))
                header_frame.pack_propagate(False)
                
                category_label = tk.Label(header_frame, text=category.value, 
                                        font=('Arial', 14, 'bold'),
                                        bg='#2c3e50', fg='white')
                category_label.pack(expand=True)
                
                # Items in category
                for item in items:
                    item_frame = tk.Frame(scrollable_frame, bg='white', relief='ridge', bd=1)
                    item_frame.pack(fill='x', padx=5, pady=2)
                    
                    # Item info
                    info_frame = tk.Frame(item_frame, bg='white')
                    info_frame.pack(side='left', fill='both', expand=True, padx=10, pady=5)
                    
                    name_price = tk.Label(info_frame, text=f"{item.name} - ${item.price:.2f}",
                                        font=('Arial', 11, 'bold'), bg='white')
                    name_price.pack(anchor='w')
                    
                    description = tk.Label(info_frame, text=item.description,
                                         font=('Arial', 9), fg='gray', bg='white')
                    description.pack(anchor='w')
                    
                    # Add button
                    add_btn = tk.Button(item_frame, text="Add to Order",
                                      command=lambda i=item: self.add_to_order(i),
                                      bg='#3498db', fg='white', font=('Arial', 9, 'bold'),
                                      relief='flat', padx=20)
                    add_btn.pack(side='right', padx=10, pady=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_order_tab(self):
        """Create the order management tab"""
        order_frame = ttk.Frame(self.notebook)
        self.notebook.add(order_frame, text="Current Order")
        
        # Customer info frame
        customer_frame = tk.Frame(order_frame, bg='#f0f0f0')
        customer_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(customer_frame, text="Customer Name:", font=('Arial', 12), bg='#f0f0f0').pack(side='left')
        self.customer_name_var = tk.StringVar()
        self.customer_entry = tk.Entry(customer_frame, textvariable=self.customer_name_var,
                                     font=('Arial', 12), width=25)
        self.customer_entry.pack(side='left', padx=10)
        
        new_order_btn = tk.Button(customer_frame, text="Start New Order",
                                command=self.start_new_order, bg='#27ae60', fg='white',
                                font=('Arial', 10, 'bold'), relief='flat', padx=20)
        new_order_btn.pack(side='left', padx=10)
        
        # Order display frame
        order_display_frame = tk.Frame(order_frame, bg='#f0f0f0')
        order_display_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(order_display_frame, text="Current Order:", font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(anchor='w')
        
        # Listbox with scrollbar
        list_frame = tk.Frame(order_display_frame)
        list_frame.pack(fill='both', expand=True, pady=10)
        
        self.order_listbox = tk.Listbox(list_frame, font=('Arial', 10), height=15)
        list_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.order_listbox.yview)
        self.order_listbox.configure(yscrollcommand=list_scrollbar.set)
        
        self.order_listbox.pack(side="left", fill="both", expand=True)
        list_scrollbar.pack(side="right", fill="y")
        
        # Order control buttons
        button_frame = tk.Frame(order_display_frame, bg='#f0f0f0')
        button_frame.pack(fill='x', pady=10)
        
        remove_btn = tk.Button(button_frame, text="Remove Selected",
                             command=self.remove_selected_item, bg='#e74c3c', fg='white',
                             font=('Arial', 10, 'bold'), relief='flat')
        remove_btn.pack(side='left', padx=(0, 10))
        
        clear_btn = tk.Button(button_frame, text="Clear Order",
                            command=self.clear_order, bg='#f39c12', fg='white',
                            font=('Arial', 10, 'bold'), relief='flat')
        clear_btn.pack(side='left')
        
        # Order summary
        summary_frame = tk.Frame(order_display_frame, bg='#f0f0f0')
        summary_frame.pack(fill='x', pady=10)
        
        self.total_label = tk.Label(summary_frame, text="Order Total: $0.00",
                                   font=('Arial', 14, 'bold'), bg='#f0f0f0')
        self.total_label.pack(anchor='w')
        
        self.prep_time_label = tk.Label(summary_frame, text="Estimated Prep Time: 0 minutes",
                                       font=('Arial', 12), bg='#f0f0f0')
        self.prep_time_label.pack(anchor='w')
        
        # Place order button
        place_order_btn = tk.Button(summary_frame, text="Place Order",
                                   command=self.place_order, bg='#2ecc71', fg='white',
                                   font=('Arial', 14, 'bold'), relief='flat', padx=30, pady=10)
        place_order_btn.pack(anchor='center', pady=20)
    
    def create_add_item_tab(self):
        """Create the add menu item tab"""
        add_item_frame = ttk.Frame(self.notebook)
        self.notebook.add(add_item_frame, text="Add Menu Item")
        
        # Title
        title_label = tk.Label(add_item_frame, text="Add New Menu Item",
                              font=('Arial', 18, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(add_item_frame, bg='#f0f0f0')
        form_frame.pack(pady=20)
        
        # Category
        tk.Label(form_frame, text="Category:", font=('Arial', 12), bg='#f0f0f0').grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(form_frame, textvariable=self.category_var,
                                    values=[cat.value for cat in FoodCategory],
                                    state="readonly", width=25)
        category_combo.grid(row=0, column=1, padx=10, pady=10)
        
        # Name
        tk.Label(form_frame, text="Name:", font=('Arial', 12), bg='#f0f0f0').grid(row=1, column=0, sticky='w', padx=10, pady=10)
        self.name_var = tk.StringVar()
        name_entry = tk.Entry(form_frame, textvariable=self.name_var, font=('Arial', 12), width=30)
        name_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Price
        tk.Label(form_frame, text="Price:", font=('Arial', 12), bg='#f0f0f0').grid(row=2, column=0, sticky='w', padx=10, pady=10)
        self.price_var = tk.StringVar()
        price_entry = tk.Entry(form_frame, textvariable=self.price_var, font=('Arial', 12), width=15)
        price_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        
        # Description
        tk.Label(form_frame, text="Description:", font=('Arial', 12), bg='#f0f0f0').grid(row=3, column=0, sticky='w', padx=10, pady=10)
        self.description_var = tk.StringVar()
        description_entry = tk.Entry(form_frame, textvariable=self.description_var, font=('Arial', 12), width=50)
        description_entry.grid(row=3, column=1, padx=10, pady=10)
        
        # Add button
        add_btn = tk.Button(form_frame, text="Add Item", command=self.add_new_menu_item,
                          bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                          relief='flat', padx=30, pady=10)
        add_btn.grid(row=4, column=1, pady=20)
        
        # Status label
        self.status_label = tk.Label(add_item_frame, text="", font=('Arial', 12), bg='#f0f0f0')
        self.status_label.pack(pady=10)
    
    def add_to_order(self, item):
        """Add an item to the current order"""
        if not self.current_order:
            messagebox.showwarning("No Order", "Please start a new order first!")
            return
        
        self.current_order.add_item(item)
        self.update_order_display()
        messagebox.showinfo("Item Added", f"Added {item.name} to order!", parent=self.root)
    
    def start_new_order(self):
        """Start a new order"""
        customer_name = self.customer_name_var.get().strip()
        if not customer_name:
            messagebox.showwarning("Missing Information", "Please enter a customer name!")
            return
        
        self.current_order = Order(customer_name)
        self.update_order_display()
        messagebox.showinfo("New Order", f"New order started for {customer_name}!")
    
    def remove_selected_item(self):
        """Remove selected item from order"""
        selection = self.order_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an item to remove!")
            return
        
        if not self.current_order:
            return
        
        selected_index = selection[0]
        if 0 <= selected_index < len(self.current_order.items):
            item_name = self.current_order.items[selected_index].name
            self.current_order.remove_item(item_name)
            self.update_order_display()
            messagebox.showinfo("Item Removed", f"Removed {item_name} from order!")
    
    def clear_order(self):
        """Clear the current order"""
        if not self.current_order:
            return
        
        if messagebox.askyesno("Clear Order", "Are you sure you want to clear the entire order?"):
            self.current_order.clear_order()
            self.update_order_display()
            messagebox.showinfo("Order Cleared", "Order cleared!")
    
    def place_order(self):
        """Place the current order"""
        if not self.current_order or not self.current_order.items:
            messagebox.showwarning("Empty Order", "No items in order!")
            return
        
        order_summary = f"Order for {self.current_order.customer_name}:\n\n"
        for item in self.current_order.items:
            order_summary += f"• {item.name} - ${item.price:.2f}\n"
        order_summary += f"\nTotal: ${self.current_order.total_price:.2f}"
        order_summary += f"\nEstimated prep time: {self.current_order.get_total_preparation_time()} minutes"
        
        messagebox.showinfo("Order Placed!", order_summary)
        
        # Reset for new order
        self.current_order = None
        self.customer_name_var.set("")
        self.update_order_display()
    
    def add_new_menu_item(self):
        """Add a new item to the menu"""
        try:
            category_str = self.category_var.get()
            name = self.name_var.get().strip()
            price_str = self.price_var.get().strip()
            description = self.description_var.get().strip()
            
            if not all([category_str, name, price_str]):
                self.status_label.config(text="Please fill in all required fields!", fg='red')
                return
            
            # Find the category enum
            category = None
            for cat in FoodCategory:
                if cat.value == category_str:
                    category = cat
                    break
            
            price = float(price_str)
            self.menu.add_item(category, name, price, description)
            
            self.status_label.config(text=f"Successfully added {name} to menu!", fg='green')
            
            # Clear form
            self.name_var.set("")
            self.price_var.set("")
            self.description_var.set("")
            
            messagebox.showinfo("Item Added", 
                              f"Added {name} to menu! Restart the application to see it in the menu tab.")
            
        except ValueError:
            self.status_label.config(text="Please enter a valid price!", fg='red')
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", fg='red')
    
    def update_order_display(self):
        """Update the order display"""
        self.order_listbox.delete(0, tk.END)
        
        if self.current_order:
            for item in self.current_order.items:
                self.order_listbox.insert(tk.END, f"{item.name} - ${item.price:.2f}")
            
            self.total_label.config(text=f"Order Total: ${self.current_order.total_price:.2f}")
            self.prep_time_label.config(text=f"Estimated Prep Time: {self.current_order.get_total_preparation_time()} minutes")
        else:
            self.total_label.config(text="Order Total: $0.00")
            self.prep_time_label.config(text="Estimated Prep Time: 0 minutes")
    
    def run(self):
        """Run the GUI application"""
        self.root.mainloop()