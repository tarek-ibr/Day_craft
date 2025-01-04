from GUI import GUI
import ttkbootstrap as tkk
import db_functions as db
import pygame
def troll():
    pygame.mixer.init()
    pygame.mixer.music.load('peak.mp3')
    pygame.mixer.music.set_volume(.2)
    pygame.mixer.music.play(0)


if __name__ == '__main__':
    troll()
    root = tkk.Window(themename="darkly")
    app = GUI(root)
    root.mainloop()
