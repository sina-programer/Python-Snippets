from win32con import SW_HIDE
import win32gui

def hide_window():
    pid = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(pid , SW_HIDE)
