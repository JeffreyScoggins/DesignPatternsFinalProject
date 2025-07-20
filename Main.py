def main():
    """Main function to run the application"""
    try:
        from FoodOrderingGUI import FoodOrderingGUI
        app = FoodOrderingGUI()
        app.run()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()