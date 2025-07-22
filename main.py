
from view.restaurant_gui import RestaurantApp
def main():
    """Main function to run the restaurant application"""
    try:
        app = RestaurantApp()
        app.run()
    except ImportError as e:
        print(f"Import Error: {e}")
        print("\nPlease ensure the following:")
        print("1. The 'domains' folder is in the parent directory")
        print("2. The 'domains/menu' folder contains all required files:")
        print("   - __init__.py")
        print("   - base.py")
        print("   - menu_item_factory.py")
        print("   - menu_manager.py")
        print("3. The 'config' folder contains enums.py with FoodCategory")
        print("\nDirectory structure should be:")
        print("project/")
        print("├── domains/")
        print("│   └── menu/")
        print("│       ├── __init__.py")
        print("│       ├── base.py")
        print("│       ├── menu_item_factory.py")
        print("│       └── menu_manager.py")
        print("├── config/")
        print("│   └── enums.py")
        print("└── restaurant_gui.py")
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
