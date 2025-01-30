import tkinter as tk
from welcome import WelcomeScreen

def main():
    root = tk.Tk()
    root.title("Algorithms of Operational Research")
    root.geometry("1000x700")
    root.configure(bg="#F4F6F6")

    # Show the welcome screen first
    welcome = WelcomeScreen(root)
    welcome.pack(fill="both", expand=True)

    # Start the main Tk event loop
    root.mainloop()

if __name__ == "__main__":
    main()
