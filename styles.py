# button_styles.py
import tkinter.ttk as ttk

def configure_button_styles():
    style = ttk.Style()

    # Configure square button style
    style.configure("Square.TButton", 
                    width=10,    # Width of the button
                    height=10,   # Height of the button
                    padding=40,  # Padding inside the button
                    relief="raised")
    
    # Configure rectangular button style
    style.configure("RectSlim.TButton", 
                    width=10,    # Width of the button
                    height=10,   # Height of the button
                    padding=(40,3),  # Padding inside the button
                    relief="raised")
    
    style.configure("Rect.TButton", 
                    width=10,    # Width of the button
                    height=10,   # Height of the button
                    padding=(40,3),  # Padding inside the button
                    relief="raised")
