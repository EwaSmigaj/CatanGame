import time
import datetime
import threading
import sys
import pygame
pygame.init()
screen = pygame.display.set_mode((200, 200))


def display_txt(i):
    screen.fill((176, 224, 230))
    txt = str(i)
    font = pygame.font.SysFont(None, 30)
    text = font.render(txt, True, (255, 255, 255))
    screen.blit(text, (10, 10))

def pause(t):
    pygame.time.wait(2000)


i=0
while True:
    pygame.event.get()
    display_txt(i)
    pygame.display.flip()
    pause(2)
    i+=1
