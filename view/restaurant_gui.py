import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
from pathlib import Path

class RestaurantApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Delicious Bites - Restaurant Ordering System")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Modern color scheme
        self.colors = {
            'bg': '#1a1a1a',
            'fg': '#ffffff',
            'accent': '#ff6b35',
            'secondary': '#2d2d2d',
            'hover': '#5E6CEB',
            'success': '#4caf50',
            'warning': '#ff9800',
            'error': '#f44336',
            'card': '#252525'
        }
        
        # Configure root
        self.root.configure(bg=self.colors['bg'])
        
        # Data storage
        self.menu_items = self.load_menu()
        self.cart = []
        self.current_category = "All"
        self.total_amount = 0.0
        
        # Setup UI
        self.setup_styles()
        self.create_widgets()

    # ===== INITIALIZATION & SETUP =====
    
    def load_menu(self):
        """Load menu items"""
        return {
            "Appetizers": [
                {"name": "Buffalo Wings", "price": 12.99, "description": "Spicy chicken wings with blue cheese dip", "image": "🍗"},
                {"name": "Mozzarella Sticks", "price": 8.99, "description": "Crispy fried mozzarella with marinara sauce", "image": "🧀"},
                {"name": "Loaded Nachos", "price": 10.99, "description": "Tortilla chips with cheese, jalapeños, and sour cream", "image": "🌮"},
                {"name": "Calamari Rings", "price": 11.99, "description": "Golden fried squid rings with spicy mayo", "image": "🦑"}
            ],
            "Main Courses": [
                {"name": "Grilled Salmon", "price": 24.99, "description": "Atlantic salmon with lemon butter and vegetables", "image": "🐟"},
                {"name": "Ribeye Steak", "price": 32.99, "description": "12oz ribeye with garlic mashed potatoes", "image": "🥩"},
                {"name": "Chicken Parmesan", "price": 18.99, "description": "Breaded chicken with marinara and mozzarella", "image": "🍗"},
                {"name": "Vegetarian Pasta", "price": 16.99, "description": "Penne pasta with seasonal vegetables and pesto", "image": "🍝"},
                {"name": "BBQ Ribs", "price": 26.99, "description": "Full rack of ribs with coleslaw and fries", "image": "🍖"}
            ],
            "Desserts": [
                {"name": "Chocolate Cake", "price": 7.99, "description": "Rich chocolate cake with vanilla ice cream", "image": "🍰"},
                {"name": "Cheesecake", "price": 6.99, "description": "New York style cheesecake with berry sauce", "image": "🍰"},
                {"name": "Ice Cream Sundae", "price": 5.99, "description": "Three scoops with hot fudge and whipped cream", "image": "🍨"},
                {"name": "Tiramisu", "price": 8.99, "description": "Classic Italian dessert with coffee and mascarpone", "image": "🍮"}
            ],
            "Beverages": [
                {"name": "Craft Beer", "price": 4.99, "description": "Local IPA on tap", "image": "🍺"},
                {"name": "House Wine", "price": 6.99, "description": "Red or white wine by the glass", "image": "🍷"},
                {"name": "Fresh Lemonade", "price": 3.99, "description": "Freshly squeezed lemonade", "image": "🍋"},
                {"name": "Coffee", "price": 2.99, "description": "Premium roasted coffee", "image": "☕"},
                {"name": "Soft Drinks", "price": 2.49, "description": "Coke, Pepsi, Sprite, Orange", "image": "🥤"}
            ]
        }
        
    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for ttk widgets
        style.configure('Modern.TFrame', background=self.colors['bg'])
        style.configure('Sidebar.TFrame', background=self.colors['secondary'])
        style.configure('Card.TFrame', background=self.colors['card'])
        style.configure('Modern.TLabel', background=self.colors['bg'], 
                       foreground=self.colors['fg'], font=('Segoe UI', 10))
        style.configure('Title.TLabel', background=self.colors['bg'], 
                       foreground=self.colors['fg'], font=('Segoe UI', 18, 'bold'))
        style.configure('Price.TLabel', background=self.colors['card'], 
                       foreground=self.colors['accent'], font=('Segoe UI', 12, 'bold'))
        style.configure('Item.TLabel', background=self.colors['card'], 
                       foreground=self.colors['fg'], font=('Segoe UI', 11, 'bold'))
        style.configure('Desc.TLabel', background=self.colors['card'], 
                       foreground='#cccccc', font=('Segoe UI', 9))

    def run(self):
        """Start the application"""
        self.root.mainloop()

    # ===== UI CREATION =====
    
    def create_widgets(self):
        """Create the main UI structure"""
        # Main container
        main_frame = ttk.Frame(self.root, style='Modern.TFrame')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Create header, content, and cart areas
        self.create_header(main_frame)
        self.create_content_area(main_frame)
        
    def create_header(self, parent):
        """Create the header with restaurant info and navigation"""
        header_frame = ttk.Frame(parent, style='Modern.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Restaurant title
        title_label = ttk.Label(header_frame, text="🍽️ Delicious Bites", 
                               style='Title.TLabel')
        title_label.pack(side='left')
        
        # Order info
        order_info = ttk.Frame(header_frame, style='Modern.TFrame')
        order_info.pack(side='right')
        
        self.order_time_label = ttk.Label(order_info, 
                                         text=f"Order Time: {datetime.now().strftime('%H:%M')}", 
                                         style='Modern.TLabel')
        self.order_time_label.pack(side='right', padx=(20, 0))
        
    def create_content_area(self, parent):
        """Create the main content area with menu and cart"""
        content_frame = ttk.Frame(parent, style='Modern.TFrame')
        content_frame.pack(fill='both', expand=True)
        
        # Left side - Menu
        self.create_menu_section(content_frame)
        
        # Right side - Cart
        self.create_cart_section(content_frame)

    # ===== MENU SECTION =====
    
    def create_menu_section(self, parent):
        """Create the menu browsing section"""
        menu_frame = ttk.Frame(parent, style='Modern.TFrame')
        menu_frame.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        # Category navigation
        self.create_category_nav(menu_frame)
        
        # Menu items display
        self.create_menu_display(menu_frame)
        
    def create_category_nav(self, parent):
        """Create category navigation buttons"""
        nav_frame = ttk.Frame(parent, style='Modern.TFrame')
        nav_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(nav_frame, text="Menu Categories", 
                 style='Modern.TLabel', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(0, 10))
        
        # Store the button frame for later updates
        self.button_frame = ttk.Frame(nav_frame, style='Modern.TFrame')
        self.button_frame.pack(fill='x')
        
        self.create_category_buttons()
        
    def create_category_buttons(self):
        """Create the actual category buttons"""
        categories = ["All"] + list(self.menu_items.keys())
        
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        
        for category in categories:
            btn = tk.Button(self.button_frame, text=category, 
                          command=lambda c=category: self.show_category(c),
                          bg=self.colors['accent'] if category == self.current_category else self.colors['secondary'],
                          fg=self.colors['fg'],
                          font=('Segoe UI', 10, 'bold'), bd=0, pady=8, padx=15,
                          activebackground=self.colors['hover'],
                          activeforeground=self.colors['fg'],
                          cursor='hand2')
            btn.pack(side='left', padx=(0, 10))
            
    def create_menu_display(self, parent):
        """Create scrollable menu items display"""
        # Create main frame for menu display
        menu_display_frame = ttk.Frame(parent, style='Modern.TFrame')
        menu_display_frame.pack(fill='both', expand=True)
        
        # Create scrollable frame
        self.menu_canvas = tk.Canvas(menu_display_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(menu_display_frame, orient="vertical", command=self.menu_canvas.yview)
        self.menu_content_frame = ttk.Frame(self.menu_canvas, style='Modern.TFrame')
        
        self.menu_content_frame.bind(
            "<Configure>",
            lambda e: self.menu_canvas.configure(scrollregion=self.menu_canvas.bbox("all"))
        )
        
        self.menu_canvas.create_window((0, 0), window=self.menu_content_frame, anchor="nw")
        self.menu_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.menu_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Improved mousewheel binding for menu area
        self.setup_menu_mousewheel(menu_display_frame)
        
        self.display_menu_items()
        
    def display_menu_items(self):
        """Display menu items based on current category"""
        # Clear existing items
        for widget in self.menu_content_frame.winfo_children():
            widget.destroy()
            
        items_to_show = []
        if self.current_category == "All":
            for category_items in self.menu_items.values():
                items_to_show.extend(category_items)
        else:
            items_to_show = self.menu_items.get(self.current_category, [])
            
        # Create grid of menu items
        columns = 2
        for i, item in enumerate(items_to_show):
            row = i // columns
            col = i % columns
            self.create_menu_item_card(self.menu_content_frame, item, row, col)
            
    def create_menu_item_card(self, parent, item, row, col):
        """Create a menu item card WITHOUT hover effects"""
        card_frame = tk.Frame(parent, bg=self.colors['card'], relief='flat', bd=1)
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky='ew', ipadx=15, ipady=15)
        
        # Configure column weights
        parent.grid_columnconfigure(col, weight=1)
        
        # Bind mousewheel to the card frame
        self.bind_menu_item_mousewheel(card_frame)
        
        # Item image/emoji
        image_label = tk.Label(card_frame, text=item['image'], 
                              bg=self.colors['card'], fg=self.colors['fg'],
                              font=('Segoe UI', 24))
        image_label.pack()
        self.bind_menu_item_mousewheel(image_label)
        
        # Item name
        name_label = tk.Label(card_frame, text=item['name'],
                             bg=self.colors['card'], fg=self.colors['fg'],
                             font=('Segoe UI', 12, 'bold'))
        name_label.pack(pady=(10, 5))
        self.bind_menu_item_mousewheel(name_label)
        
        # Item description
        desc_label = tk.Label(card_frame, text=item['description'],
                             bg=self.colors['card'], fg='#cccccc',
                             font=('Segoe UI', 9), wraplength=200)
        desc_label.pack(pady=(0, 10))
        self.bind_menu_item_mousewheel(desc_label)
        
        # Price and add button frame
        bottom_frame = tk.Frame(card_frame, bg=self.colors['card'])
        bottom_frame.pack(fill='x')
        self.bind_menu_item_mousewheel(bottom_frame)
        
        # Price
        price_label = tk.Label(bottom_frame, text=f"${item['price']:.2f}",
                              bg=self.colors['card'], fg=self.colors['accent'],
                              font=('Segoe UI', 14, 'bold'))
        price_label.pack(side='left')
        self.bind_menu_item_mousewheel(price_label)
        
        # Add to cart button
        add_btn = tk.Button(bottom_frame, text="Add to Cart",
                           command=lambda i=item: self.add_to_cart(i),
                           bg=self.colors['accent'], fg=self.colors['fg'],
                           font=('Segoe UI', 9, 'bold'), bd=0, pady=5, padx=10,
                           activebackground=self.colors['hover'],
                           activeforeground=self.colors['fg'],
                           cursor='hand2')
        add_btn.pack(side='right')
        self.bind_menu_item_mousewheel(add_btn)
        
        # NO HOVER EFFECTS FOR MENU ITEM CARDS - REMOVED COMPLETELY

    # ===== MENU NAVIGATION =====
    
    def show_category(self, category):
        """Show items from selected category"""
        self.current_category = category
        self.update_category_buttons()
        self.display_menu_items()
        self.reset_menu_scroll()
        
    def reset_menu_scroll(self):
        """Reset menu scroll position to top"""
        if hasattr(self, 'menu_canvas'):
            self.menu_canvas.yview_moveto(0.0)
            
    def update_category_buttons(self):
        """Update category button colors based on current selection"""
        for widget in self.button_frame.winfo_children():
            if isinstance(widget, tk.Button):
                category = widget.cget('text')
                if category == self.current_category:
                    widget.configure(bg=self.colors['accent'])
                else:
                    widget.configure(bg=self.colors['secondary'])

    # ===== CART SECTION =====
    
    def create_cart_section(self, parent):
        """Create the shopping cart section"""
        cart_frame = tk.Frame(parent, bg=self.colors['secondary'], width=350)
        cart_frame.pack(side='right', fill='y')
        cart_frame.pack_propagate(False)
        
        # Cart header
        cart_header = tk.Frame(cart_frame, bg=self.colors['secondary'])
        cart_header.pack(fill='x', padx=20, pady=(20, 10))
        
        tk.Label(cart_header, text="🛒 Your Order", 
                bg=self.colors['secondary'], fg=self.colors['fg'],
                font=('Segoe UI', 16, 'bold')).pack()
        
        # Create container for cart items (scrollable area)
        cart_items_container = tk.Frame(cart_frame, bg=self.colors['secondary'])
        cart_items_container.pack(fill='both', expand=True, padx=20)
        
        # Cart items display with scrollbar
        self.cart_canvas = tk.Canvas(cart_items_container, bg=self.colors['secondary'], highlightthickness=0)
        cart_scrollbar = ttk.Scrollbar(cart_items_container, orient="vertical", command=self.cart_canvas.yview)
        self.cart_content_frame = tk.Frame(self.cart_canvas, bg=self.colors['secondary'])
        
        self.cart_content_frame.bind(
            "<Configure>",
            lambda e: self.cart_canvas.configure(scrollregion=self.cart_canvas.bbox("all"))
        )
        
        self.cart_canvas.create_window((0, 0), window=self.cart_content_frame, anchor="nw")
        self.cart_canvas.configure(yscrollcommand=cart_scrollbar.set)
        
        self.cart_canvas.pack(side="left", fill="both", expand=True)
        cart_scrollbar.pack(side="right", fill="y")
        
        # Setup mousewheel for cart area
        self.setup_cart_mousewheel(cart_items_container)
        
        # Cart summary and checkout (fixed at bottom)
        self.create_cart_summary(cart_frame)
        
    def create_cart_summary(self, parent):
        """Create cart summary and checkout section"""
        # Create a fixed bottom section for summary and buttons
        summary_container = tk.Frame(parent, bg=self.colors['secondary'])
        summary_container.pack(fill='x', side='bottom', padx=20, pady=20)
        
        # Total amount display
        total_frame = tk.Frame(summary_container, bg=self.colors['secondary'])
        total_frame.pack(fill='x', pady=(0, 15))
        
        self.total_label = tk.Label(total_frame, text="Total: $0.00",
                                   bg=self.colors['secondary'], fg=self.colors['accent'],
                                   font=('Segoe UI', 18, 'bold'))
        self.total_label.pack()
        
        # Buttons frame
        buttons_frame = tk.Frame(summary_container, bg=self.colors['secondary'])
        buttons_frame.pack(fill='x')
        
        # Checkout button - Always visible, enabled based on cart contents
        self.checkout_btn = tk.Button(buttons_frame, text="🛒 Add items to checkout",
                                     command=self.open_checkout,
                                     bg='#666666', fg=self.colors['fg'],
                                     font=('Segoe UI', 12, 'bold'), bd=0, pady=12,
                                     activebackground=self.colors['hover'],
                                     activeforeground=self.colors['fg'],
                                     cursor='hand2', relief='flat', state='disabled')
        self.checkout_btn.pack(fill='x', pady=(0, 10))
        
        # Clear cart button
        self.clear_btn = tk.Button(buttons_frame, text="🗑️ Clear Cart",
                                  command=self.clear_cart,
                                  bg=self.colors['error'], fg=self.colors['fg'],
                                  font=('Segoe UI', 10), bd=0, pady=8,
                                  activebackground=self.colors['hover'],
                                  activeforeground=self.colors['fg'],
                                  cursor='hand2', relief='flat', state='disabled')
        self.clear_btn.pack(fill='x')
        
        # Add some helpful text when cart is empty
        self.empty_cart_label = tk.Label(summary_container, 
                                        text="👆 Add items from the menu above",
                                        bg=self.colors['secondary'], fg='#888888',
                                        font=('Segoe UI', 10))
        self.empty_cart_label.pack(pady=(10, 0))
        
        print("Cart summary section created with checkout button")  # Debug

    # ===== CART OPERATIONS =====
        
    def add_to_cart(self, item):
        """Add item to cart"""
        print(f"Adding {item['name']} to cart")  # Debug
        
        # Check if item already exists in cart
        existing_item = next((cart_item for cart_item in self.cart 
                             if cart_item['name'] == item['name']), None)
        
        if existing_item:
            existing_item['quantity'] += 1
            print(f"Updated quantity for {item['name']} to {existing_item['quantity']}")  # Debug
        else:
            cart_item = item.copy()
            cart_item['quantity'] = 1
            self.cart.append(cart_item)
            print(f"Added new item {item['name']} to cart")  # Debug
            
        self.update_cart_display()
        self.update_total()
        print(f"Cart now has {len(self.cart)} unique items")  # Debug
        
    def increase_quantity(self, item):
        """Increase item quantity"""
        item['quantity'] += 1
        self.update_cart_display()
        self.update_total()
        
    def decrease_quantity(self, item):
        """Decrease item quantity"""
        if item['quantity'] > 1:
            item['quantity'] -= 1
        else:
            self.cart.remove(item)
        self.update_cart_display()
        self.update_total()
        
    def clear_cart(self):
        """Clear all items from cart"""
        if self.cart and messagebox.askyesno("Clear Cart", "Are you sure you want to clear your cart?"):
            self.cart.clear()
            self.update_cart_display()
            self.update_total()

    # ===== CART DISPLAY =====
            
    def update_cart_display(self):
        """Update the cart items display"""
        # Clear existing cart items
        for widget in self.cart_content_frame.winfo_children():
            widget.destroy()
            
        if not self.cart:
            empty_label = tk.Label(self.cart_content_frame, text="Your cart is empty",
                                  bg=self.colors['secondary'], fg='#888888',
                                  font=('Segoe UI', 10))
            empty_label.pack(pady=20)
            return
            
        for item in self.cart:
            self.create_cart_item(self.cart_content_frame, item)
            
    def create_cart_item(self, parent, item):
        """Create a cart item widget"""
        item_frame = tk.Frame(parent, bg=self.colors['card'], relief='flat')
        item_frame.pack(fill='x', pady=5, padx=5, ipady=10, ipadx=10)
        
        # Item info
        info_frame = tk.Frame(item_frame, bg=self.colors['card'])
        info_frame.pack(fill='x')
        
        # Name and price
        tk.Label(info_frame, text=item['name'],
                bg=self.colors['card'], fg=self.colors['fg'],
                font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        
        price_qty_frame = tk.Frame(info_frame, bg=self.colors['card'])
        price_qty_frame.pack(fill='x', pady=(5, 0))
        
        tk.Label(price_qty_frame, text=f"${item['price']:.2f} each",
                bg=self.colors['card'], fg='#cccccc',
                font=('Segoe UI', 9)).pack(side='left')
        
        # Quantity controls
        qty_frame = tk.Frame(price_qty_frame, bg=self.colors['card'])
        qty_frame.pack(side='right')
        
        tk.Button(qty_frame, text="-", command=lambda i=item: self.decrease_quantity(i),
                 bg=self.colors['error'], fg=self.colors['fg'],
                 font=('Segoe UI', 8, 'bold'), bd=0, width=2,
                 cursor='hand2').pack(side='left')
        
        tk.Label(qty_frame, text=str(item['quantity']),
                bg=self.colors['card'], fg=self.colors['fg'],
                font=('Segoe UI', 10, 'bold'), width=3).pack(side='left', padx=5)
        
        tk.Button(qty_frame, text="+", command=lambda i=item: self.increase_quantity(i),
                 bg=self.colors['success'], fg=self.colors['fg'],
                 font=('Segoe UI', 8, 'bold'), bd=0, width=2,
                 cursor='hand2').pack(side='left')
        
        # Subtotal
        subtotal = item['price'] * item['quantity']
        tk.Label(info_frame, text=f"Subtotal: ${subtotal:.2f}",
                bg=self.colors['card'], fg=self.colors['accent'],
                font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(5, 0))

    # ===== CART STATE MANAGEMENT =====
        
    def update_total(self):
        """Update total amount"""
        self.total_amount = sum(item['price'] * item['quantity'] for item in self.cart)
        self.total_label.config(text=f"Total: ${self.total_amount:.2f}")
        self.update_button_states()
        
    def update_button_states(self):
        """Update button states based on cart contents"""
        if hasattr(self, 'checkout_btn'):  # Make sure button exists
            if self.cart:
                self.checkout_btn.config(state='normal', 
                                       bg=self.colors['success'],
                                       text=f"🛒 Checkout (${self.total_amount:.2f})")
                self.clear_btn.config(state='normal', bg=self.colors['error'])
                if hasattr(self, 'empty_cart_label'):
                    self.empty_cart_label.pack_forget()
            else:
                self.checkout_btn.config(state='disabled', 
                                       bg='#666666',
                                       text="🛒 Add items to checkout")
                self.clear_btn.config(state='disabled', bg='#444444')
                if hasattr(self, 'empty_cart_label'):
                    self.empty_cart_label.pack(pady=(10, 0))
            
            print(f"Button states updated. Cart has {len(self.cart)} items")  # Debug

    # ===== CHECKOUT FLOW =====
            
    def open_checkout(self):
        """Open checkout dialog"""
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Please add items to your cart first!")
            return
        
        print(f"Opening checkout with {len(self.cart)} items, total: ${self.total_amount:.2f}")  # Debug
        CheckoutDialog(self.root, self.cart, self.total_amount, self.colors, self.order_complete)
        
    def order_complete(self):
        """Handle order completion"""
        self.cart.clear()
        self.update_cart_display()
        self.update_total()
        messagebox.showinfo("Order Confirmed", "Thank you for your order! Your food will be ready in 20-30 minutes.")

    # ===== SCROLLING & MOUSE HANDLING =====
    
    def setup_menu_mousewheel(self, menu_frame):
        """Setup comprehensive mousewheel binding for the menu area"""
        def scroll_menu(event):
            # Only scroll if the canvas exists and has content
            if hasattr(self, 'menu_canvas'):
                # Linux uses Button-4 and Button-5 for scroll wheel
                if event.num == 4:
                    self.menu_canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    self.menu_canvas.yview_scroll(1, "units")
                else:
                    # Windows/Mac mousewheel
                    self.menu_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Store scroll function for global access
        self.menu_scroll_function = scroll_menu
        
        # Bind mousewheel events globally when in menu area
        def bind_menu_scroll(event=None):
            # Bind for all platforms
            self.root.bind_all("<MouseWheel>", scroll_menu)  # Windows/Mac
            self.root.bind_all("<Button-4>", scroll_menu)    # Linux scroll up
            self.root.bind_all("<Button-5>", scroll_menu)    # Linux scroll down
            self.menu_scroll_active = True
        
        def unbind_menu_scroll(event=None):
            # Only unbind if we're not in a child widget
            if hasattr(self, 'menu_scroll_active') and self.menu_scroll_active:
                self.root.after_idle(self._check_mouse_position)
        
        # Bind to the main menu frame
        menu_frame.bind('<Enter>', bind_menu_scroll)
        menu_frame.bind('<Leave>', unbind_menu_scroll)
        
        # Also bind to canvas
        self.menu_canvas.bind('<Enter>', bind_menu_scroll)
        self.menu_canvas.bind('<Leave>', unbind_menu_scroll)
        
    def _check_mouse_position(self):
        """Check if mouse is still in menu area before unbinding"""
        try:
            # Get mouse position relative to menu canvas
            x = self.menu_canvas.winfo_pointerx() - self.menu_canvas.winfo_rootx()
            y = self.menu_canvas.winfo_pointery() - self.menu_canvas.winfo_rooty()
            
            # Check if mouse is still within canvas bounds
            if (0 <= x <= self.menu_canvas.winfo_width() and 
                0 <= y <= self.menu_canvas.winfo_height()):
                # Mouse still in menu area, keep scrolling active
                return
            
            # Mouse has left menu area, unbind scrolling
            self.root.unbind_all("<MouseWheel>")
            self.root.unbind_all("<Button-4>")
            self.root.unbind_all("<Button-5>")
            self.menu_scroll_active = False
        except tk.TclError:
            # Widget might be destroyed, ignore
            pass
        
    def bind_menu_item_mousewheel(self, widget):
        """Simplified menu item mousewheel binding"""
        
    def setup_cart_mousewheel(self, cart_container):
        """Setup mousewheel binding for cart area"""
        def scroll_cart(event):
            if hasattr(self, 'cart_canvas'):
                # Linux uses Button-4 and Button-5 for scroll wheel
                if event.num == 4:
                    self.cart_canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    self.cart_canvas.yview_scroll(1, "units")
                else:
                    # Windows/Mac mousewheel
                    self.cart_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def bind_cart_scroll(event=None):
            # Bind for all platforms
            self.root.bind_all("<MouseWheel>", scroll_cart)  # Windows/Mac
            self.root.bind_all("<Button-4>", scroll_cart)    # Linux scroll up
            self.root.bind_all("<Button-5>", scroll_cart)    # Linux scroll down
            self.cart_scroll_active = True
        
        def unbind_cart_scroll(event=None):
            # Delayed unbinding to prevent conflicts
            self.root.after_idle(self._check_cart_mouse_position)
        
        cart_container.bind('<Enter>', bind_cart_scroll)
        cart_container.bind('<Leave>', unbind_cart_scroll)
        
        self.cart_canvas.bind('<Enter>', bind_cart_scroll)
        self.cart_canvas.bind('<Leave>', unbind_cart_scroll)
        
    def _check_cart_mouse_position(self):
        """Check if mouse is still in cart area before unbinding"""
        try:
            # Get mouse position relative to cart canvas
            x = self.cart_canvas.winfo_pointerx() - self.cart_canvas.winfo_rootx()
            y = self.cart_canvas.winfo_pointery() - self.cart_canvas.winfo_rooty()
            
            # Check if mouse is still within canvas bounds
            if (0 <= x <= self.cart_canvas.winfo_width() and 
                0 <= y <= self.cart_canvas.winfo_height()):
                # Mouse still in cart area, keep scrolling active
                return
            
            # Mouse has left cart area, unbind scrolling
            self.root.unbind_all("<MouseWheel>")
            self.root.unbind_all("<Button-4>")
            self.root.unbind_all("<Button-5>")
            self.cart_scroll_active = False
        except tk.TclError:
            # Widget might be destroyed, ignore
            pass

    # ===== UTILITY METHODS =====
        
    def get_all_children(self, widget):
        """Recursively get all child widgets"""
        children = []
        for child in widget.winfo_children():
            children.append(child)
            children.extend(self.get_all_children(child))
        return children


# ===== CHECKOUT DIALOGS =====

class CheckoutDialog:
    def __init__(self, parent, cart, total, colors, callback):
        self.cart = cart
        self.total = total
        self.colors = colors
        self.callback = callback
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Checkout - Payment")
        self.dialog.geometry("500x600")
        self.dialog.configure(bg=colors['bg'])
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (600 // 2)
        self.dialog.geometry(f"500x600+{x}+{y}")
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create checkout dialog widgets"""
        # Main scrollable frame
        main_canvas = tk.Canvas(self.dialog, bg=self.colors['bg'], highlightthickness=0)
        main_scrollbar = ttk.Scrollbar(self.dialog, orient="vertical", command=main_canvas.yview)
        main_frame = tk.Frame(main_canvas, bg=self.colors['bg'])
        
        main_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=main_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        
        main_canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        main_scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to checkout dialog
        self.bind_checkout_mousewheel(main_canvas)
        
        # Header
        tk.Label(main_frame, text="🍽️ Order Summary & Payment", 
                bg=self.colors['bg'], fg=self.colors['fg'],
                font=('Segoe UI', 16, 'bold')).pack(pady=(0, 20))
        
        # Order summary
        self.create_order_summary(main_frame)
        
        # Payment form
        self.create_payment_form(main_frame)
        
        # Buttons
        self.create_buttons(main_frame)
        
    def bind_checkout_mousewheel(self, canvas):
        """Bind mousewheel events to checkout canvas with smooth scrolling"""
        def scroll_checkout(event):
            # Cross-platform mousewheel support
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")
            else:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Store scroll function
        self.checkout_scroll_function = scroll_checkout
        
        def bind_checkout_scroll(event=None):
            # Bind for all platforms
            self.dialog.bind_all("<MouseWheel>", scroll_checkout)  # Windows/Mac
            self.dialog.bind_all("<Button-4>", scroll_checkout)    # Linux scroll up
            self.dialog.bind_all("<Button-5>", scroll_checkout)    # Linux scroll down
            self.checkout_scroll_active = True
        
        def unbind_checkout_scroll(event=None):
            # Delayed unbinding to prevent conflicts
            self.dialog.after_idle(self._check_checkout_mouse_position)
        
        # Bind when mouse enters the dialog
        self.dialog.bind('<Enter>', bind_checkout_scroll)
        self.dialog.bind('<Leave>', unbind_checkout_scroll)
        
        # Also bind to canvas
        canvas.bind('<Enter>', bind_checkout_scroll)
        canvas.bind('<Leave>', unbind_checkout_scroll)
        
        # Bind immediately when dialog opens
        bind_checkout_scroll()
        
    def _check_checkout_mouse_position(self):
        """Check if mouse is still in checkout dialog before unbinding"""
        try:
            # Get mouse position relative to dialog
            x = self.dialog.winfo_pointerx() - self.dialog.winfo_rootx()
            y = self.dialog.winfo_pointery() - self.dialog.winfo_rooty()
            
            # Check if mouse is still within dialog bounds
            if (0 <= x <= self.dialog.winfo_width() and 
                0 <= y <= self.dialog.winfo_height()):
                # Mouse still in dialog area, keep scrolling active
                return
            
            # Mouse has left dialog area, unbind scrolling
            self.dialog.unbind_all("<MouseWheel>")
            self.dialog.unbind_all("<Button-4>")
            self.dialog.unbind_all("<Button-5>")
            self.checkout_scroll_active = False
        except tk.TclError:
            # Widget might be destroyed, ignore
            pass
        
    def create_order_summary(self, parent):
        """Create order summary section"""
        summary_frame = tk.Frame(parent, bg=self.colors['secondary'], relief='flat')
        summary_frame.pack(fill='x', pady=(0, 20), ipady=15, ipadx=15)
        
        tk.Label(summary_frame, text="Order Summary", 
                bg=self.colors['secondary'], fg=self.colors['fg'],
                font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(0, 10))
        
        for item in self.cart:
            item_frame = tk.Frame(summary_frame, bg=self.colors['secondary'])
            item_frame.pack(fill='x', pady=2)
            
            item_text = f"{item['quantity']}x {item['name']}"
            tk.Label(item_frame, text=item_text,
                    bg=self.colors['secondary'], fg=self.colors['fg'],
                    font=('Segoe UI', 10)).pack(side='left')
            
            item_total = item['price'] * item['quantity']
            tk.Label(item_frame, text=f"${item_total:.2f}",
                    bg=self.colors['secondary'], fg=self.colors['accent'],
                    font=('Segoe UI', 10, 'bold')).pack(side='right')
        
        # Total
        total_frame = tk.Frame(summary_frame, bg=self.colors['secondary'])
        total_frame.pack(fill='x', pady=(10, 0))
        
        tk.Label(total_frame, text="Total:",
                bg=self.colors['secondary'], fg=self.colors['fg'],
                font=('Segoe UI', 12, 'bold')).pack(side='left')
        
        tk.Label(total_frame, text=f"${self.total:.2f}",
                bg=self.colors['secondary'], fg=self.colors['accent'],
                font=('Segoe UI', 12, 'bold')).pack(side='right')
        
    def create_payment_form(self, parent):
        """Create payment form"""
        form_frame = tk.Frame(parent, bg=self.colors['bg'])
        form_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(form_frame, text="Payment Information", 
                bg=self.colors['bg'], fg=self.colors['fg'],
                font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(0, 15))
        
        # Customer name
        tk.Label(form_frame, text="Customer Name:", 
                bg=self.colors['bg'], fg=self.colors['fg'],
                font=('Segoe UI', 10)).pack(anchor='w')
        self.name_entry = tk.Entry(form_frame, font=('Segoe UI', 10),
                                  bg=self.colors['secondary'], fg=self.colors['fg'],
                                  bd=0, relief='flat', insertbackground=self.colors['fg'])
        self.name_entry.pack(fill='x', pady=(5, 15), ipady=8, ipadx=10)
        
        # Phone number
        tk.Label(form_frame, text="Phone Number:", 
                bg=self.colors['bg'], fg=self.colors['fg'],
                font=('Segoe UI', 10)).pack(anchor='w')
        self.phone_entry = tk.Entry(form_frame, font=('Segoe UI', 10),
                                   bg=self.colors['secondary'], fg=self.colors['fg'],
                                   bd=0, relief='flat', insertbackground=self.colors['fg'])
        self.phone_entry.pack(fill='x', pady=(5, 15), ipady=8, ipadx=10)
        
        # Payment method
        tk.Label(form_frame, text="Payment Method:", 
                bg=self.colors['bg'], fg=self.colors['fg'],
                font=('Segoe UI', 10)).pack(anchor='w')
        
        self.payment_var = tk.StringVar(value="Credit Card")
        payment_frame = tk.Frame(form_frame, bg=self.colors['bg'])
        payment_frame.pack(fill='x', pady=(5, 15))
        
        for method in ["Credit Card", "Debit Card", "Cash", "Digital Wallet"]:
            tk.Radiobutton(payment_frame, text=method, variable=self.payment_var,
                          value=method, bg=self.colors['bg'], fg=self.colors['fg'],
                          selectcolor=self.colors['accent'], font=('Segoe UI', 10),
                          activebackground=self.colors['bg'],
                          activeforeground=self.colors['fg']).pack(anchor='w')
        
        # Card details (for card payments)
        self.card_frame = tk.Frame(form_frame, bg=self.colors['bg'])
        self.card_frame.pack(fill='x')
        
        tk.Label(self.card_frame, text="Card Number:", 
                bg=self.colors['bg'], fg=self.colors['fg'],
                font=('Segoe UI', 10)).pack(anchor='w')
        self.card_entry = tk.Entry(self.card_frame, font=('Segoe UI', 10),
                                  bg=self.colors['secondary'], fg=self.colors['fg'],
                                  bd=0, relief='flat', insertbackground=self.colors['fg'])
        self.card_entry.pack(fill='x', pady=(5, 10), ipady=8, ipadx=10)
        
        # Expiry and CVV
        exp_cvv_frame = tk.Frame(self.card_frame, bg=self.colors['bg'])
        exp_cvv_frame.pack(fill='x', pady=(0, 15))
        
        # Expiry
        exp_frame = tk.Frame(exp_cvv_frame, bg=self.colors['bg'])
        exp_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        tk.Label(exp_frame, text="Expiry (MM/YY):", 
                bg=self.colors['bg'], fg=self.colors['fg'],
                font=('Segoe UI', 10)).pack(anchor='w')
        self.expiry_entry = tk.Entry(exp_frame, font=('Segoe UI', 10),
                                    bg=self.colors['secondary'], fg=self.colors['fg'],
                                    bd=0, relief='flat', insertbackground=self.colors['fg'])
        self.expiry_entry.pack(fill='x', pady=(5, 0), ipady=8, ipadx=10)
        
        # CVV
        cvv_frame = tk.Frame(exp_cvv_frame, bg=self.colors['bg'])
        cvv_frame.pack(side='right', fill='x', expand=True)
        
        tk.Label(cvv_frame, text="CVV:", 
                bg=self.colors['bg'], fg=self.colors['fg'],
                font=('Segoe UI', 10)).pack(anchor='w')
        self.cvv_entry = tk.Entry(cvv_frame, font=('Segoe UI', 10), show="*",
                                 bg=self.colors['secondary'], fg=self.colors['fg'],
                                 bd=0, relief='flat', insertbackground=self.colors['fg'])
        self.cvv_entry.pack(fill='x', pady=(5, 0), ipady=8, ipadx=10)
        
        # Bind payment method change
        self.payment_var.trace('w', self.on_payment_method_change)
        
    def create_buttons(self, parent):
        """Create dialog buttons"""
        button_frame = tk.Frame(parent, bg=self.colors['bg'])
        button_frame.pack(fill='x', pady=20)
        
        # Cancel button
        cancel_btn = tk.Button(button_frame, text="Cancel", command=self.cancel,
                              bg=self.colors['secondary'], fg=self.colors['fg'],
                              font=('Segoe UI', 11), bd=0, pady=10, padx=20,
                              activebackground=self.colors['hover'],
                              activeforeground=self.colors['fg'],
                              cursor='hand2')
        cancel_btn.pack(side='right', padx=(10, 0))
        
        # Pay button
        pay_btn = tk.Button(button_frame, text=f"💳 Pay ${self.total:.2f}", 
                           command=self.process_payment,
                           bg=self.colors['success'], fg=self.colors['fg'],
                           font=('Segoe UI', 12, 'bold'), bd=0, pady=12, padx=30,
                           activebackground=self.colors['hover'],
                           activeforeground=self.colors['fg'],
                           cursor='hand2', relief='flat')
        pay_btn.pack(side='right')
        
        # Special offers info
        offer_frame = tk.Frame(parent, bg=self.colors['bg'])
        offer_frame.pack(fill='x', pady=(20, 0))
        
        tk.Label(offer_frame, text="🎉 Special Offers", 
                bg=self.colors['bg'], fg=self.colors['accent'],
                font=('Segoe UI', 12, 'bold')).pack(anchor='w')
        
        offers_text = "• Orders over $50: Free delivery\n• First-time customers: 10% off\n• Loyalty members: Earn 2x points"
        tk.Label(offer_frame, text=offers_text, 
                bg=self.colors['bg'], fg='#cccccc',
                font=('Segoe UI', 9), justify='left').pack(anchor='w', pady=(5, 0))
        
    def on_payment_method_change(self, *args):
        """Handle payment method change"""
        method = self.payment_var.get()
        if method in ["Credit Card", "Debit Card"]:
            self.card_frame.pack(fill='x')
        else:
            self.card_frame.pack_forget()
            
    def validate_form(self):
        """Validate form inputs"""
        if not self.name_entry.get().strip():
            messagebox.showerror("Validation Error", "Please enter your name!")
            return False
            
        if not self.phone_entry.get().strip():
            messagebox.showerror("Validation Error", "Please enter your phone number!")
            return False
            
        payment_method = self.payment_var.get()
        if payment_method in ["Credit Card", "Debit Card"]:
            if not self.card_entry.get().strip():
                messagebox.showerror("Validation Error", "Please enter your card number!")
                return False
            if not self.expiry_entry.get().strip():
                messagebox.showerror("Validation Error", "Please enter card expiry date!")
                return False
            if not self.cvv_entry.get().strip():
                messagebox.showerror("Validation Error", "Please enter CVV!")
                return False
                
        return True
        
    def process_payment(self):
        """Process the payment"""
        if not self.validate_form():
            return
            
        # Show processing message
        processing_dialog = ProcessingDialog(self.dialog, self.colors)
        
        # Simulate payment processing
        self.dialog.after(3000, lambda: self.complete_payment(processing_dialog))
        
    def complete_payment(self, processing_dialog):
        """Complete the payment process"""
        processing_dialog.dialog.destroy()
        
        # Show success message
        success_dialog = PaymentSuccessDialog(self.dialog, self.colors, 
                                            self.name_entry.get(), 
                                            self.payment_var.get(),
                                            self.total)
        
        # Close checkout dialog and callback
        self.dialog.after(3000, lambda: self.finish_order())
        
    def finish_order(self):
        """Finish the order process"""
        self.dialog.destroy()
        self.callback()
        
    def cancel(self):
        """Cancel checkout"""
        if messagebox.askyesno("Cancel Order", "Are you sure you want to cancel your order?"):
            self.dialog.destroy()


class ProcessingDialog:
    def __init__(self, parent, colors):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Processing Payment")
        self.dialog.geometry("300x150")
        self.dialog.configure(bg=colors['bg'])
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (300 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (150 // 2)
        self.dialog.geometry(f"300x150+{x}+{y}")
        
        # Content
        main_frame = tk.Frame(self.dialog, bg=colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Processing animation (simple text animation)
        self.processing_label = tk.Label(main_frame, text="Processing payment", 
                                        bg=colors['bg'], fg=colors['fg'],
                                        font=('Segoe UI', 12, 'bold'))
        self.processing_label.pack(expand=True)
        
        self.animate_processing()
        
    def animate_processing(self):
        """Animate processing text"""
        current_text = self.processing_label.cget("text")
        if current_text.endswith("..."):
            self.processing_label.config(text="Processing payment")
        else:
            self.processing_label.config(text=current_text + ".")
        
        # Continue animation if dialog still exists
        try:
            self.dialog.after(500, self.animate_processing)
        except tk.TclError:
            pass


class PaymentSuccessDialog:
    def __init__(self, parent, colors, customer_name, payment_method, total):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Payment Successful")
        self.dialog.geometry("400x300")
        self.dialog.configure(bg=colors['bg'])
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"400x300+{x}+{y}")
        
        # Content
        main_frame = tk.Frame(self.dialog, bg=colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Success icon and message
        tk.Label(main_frame, text="✅", 
                bg=colors['bg'], fg=colors['success'],
                font=('Segoe UI', 48)).pack(pady=(0, 20))
        
        tk.Label(main_frame, text="Payment Successful!", 
                bg=colors['bg'], fg=colors['success'],
                font=('Segoe UI', 16, 'bold')).pack()
        
        # Order details
        details_frame = tk.Frame(main_frame, bg=colors['secondary'], relief='flat')
        details_frame.pack(fill='x', pady=20, ipady=15, ipadx=15)
        
        tk.Label(details_frame, text="Order Confirmation", 
                bg=colors['secondary'], fg=colors['fg'],
                font=('Segoe UI', 12, 'bold')).pack(pady=(0, 10))
        
        details_text = [
            f"Customer: {customer_name}",
            f"Payment Method: {payment_method}",
            f"Total Paid: ${total:.2f}",
            f"Order ID: #{datetime.now().strftime('%Y%m%d%H%M')}",
            f"Estimated Time: 20-30 minutes"
        ]
        
        for detail in details_text:
            tk.Label(details_frame, text=detail, 
                    bg=colors['secondary'], fg=colors['fg'],
                    font=('Segoe UI', 10)).pack(anchor='w', pady=2)
        
        tk.Label(main_frame, text="Thank you for your order!", 
                bg=colors['bg'], fg=colors['fg'],
                font=('Segoe UI', 12)).pack(pady=(10, 0))


