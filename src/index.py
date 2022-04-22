from tkinter import Tk
from ui.tkinter_ui import UI



def main():
    window = Tk()

    window.title("TkInter example")

    ui = UI(window)

    ui.start()

    window.mainloop()


if __name__ == '__main__':
    main()