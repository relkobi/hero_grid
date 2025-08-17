import sys
import os

# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
#     return os.path.join(base_path, relative_path)

# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     try:
#         # PyInstaller stores temp folder path in _MEIPASS
#         base_path = sys._MEIPASS
#     except AttributeError:
#         # When running normally, use the script directory
#         base_path = os.path.abspath(os.path.dirname(__file__))
    
#     return os.path.join(base_path, relative_path)
def resource_path(relative_path):
    """
    Get the absolute path to a resource, whether running as a PyInstaller EXE
    or as a normal Python script.
    """
    try:
        # PyInstaller creates a temporary folder and stores its path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # If not running as a PyInstaller EXE, use the current working directory
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ''

    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + ' '
    lines.append(current_line.strip())  # Add last line

    return lines


def brighten_color(color, amount=30):
    r = min(color[0] + amount, 255)
    g = min(color[1] + amount, 255)
    b = min(color[2] + amount, 255)
    return (r, g, b)


def darker_color(color, amount=30):
    r = max(color[0] - amount, 0)
    g = max(color[1] - amount, 0)
    b = max(color[2] - amount, 0)
    return (r, g, b)
