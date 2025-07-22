
from view.restaurant_gui import RestaurantApp
def main():
    """Main function to run the restaurant application"""
    try:
        app = RestaurantApp()
        app.run()
    except ImportError as e:
        print(f"Import Error: {e}")
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
