from gui.panel import Panel

if __name__ == "__main__":
    try:
        Panel().root.mainloop()
    except Exception as e:
        print(e)