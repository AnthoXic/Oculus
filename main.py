# main.py

def main():
    print("Python environment ready!")

    # Test imports basiques
    try:
        import sys
        print(f"Python version: {sys.version}")

        import numpy as np
        print(f"NumPy version: {np.__version__}")

        print("\nEnvironment setup successful!")
        return True

    except ImportError as e:
        print(f"Import error: {e}")
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("\nReady to start development!")
    else:
        print("\nPlease check your installation")