import pyautogui
import numpy as np
import time
import cv2
import easyocr

WHITE = (231, 231, 231)
BLACK = (0, 0, 0)

THRESHOLD = 1000000

pyautogui.PAUSE = 0

def get_game_size():
    screenWidth, screenHeight = pyautogui.size()
    x, y, game_width, game_height = pyautogui.locateOnScreen("logo.png", confidence=0.9)
    x, y, game_width, game_height = int(x), int(y), int(game_width), int(game_height)
    while y<screenHeight and pyautogui.pixelMatchesColor(x, y, WHITE, tolerance=10):
        y+=1
    while x>0 and pyautogui.pixelMatchesColor(x, y-1, WHITE, tolerance=10):
        x-=1
    game_width = 1
    while x+game_width<screenWidth and pyautogui.pixelMatchesColor(x+game_width, y-1, WHITE, tolerance=15):
        game_width+=1
    while y<screenHeight and pyautogui.pixelMatchesColor(x+game_width//2, y, BLACK, tolerance=10):
        y+=1
    k=x
    while x<screenWidth and pyautogui.pixelMatchesColor(x, y, BLACK, tolerance=10):
        x+=1
    game_width-=2*(x-k)
    game_height = int(2.1*game_width)    
    return (x, y, game_width, game_height)
    

def play_game():
    x, y, game_width, game_height = get_game_size()
    left_region = (x+game_width//6, y+int(game_height*0.52), game_width//6, int(game_height*0.05))
    background_left = np.array(pyautogui.screenshot(region=left_region)).reshape(-1)
    game_left = np.array(pyautogui.screenshot(region=left_region)).reshape(-1)
    right_region = (x+game_width//6*4, y+int(game_height*0.52), game_width//6, int(game_height*0.05))
    background_right = np.array(pyautogui.screenshot(region=right_region)).reshape(-1)
    game_right = np.array(pyautogui.screenshot(region=right_region)).reshape(-1)
    pyautogui.moveTo(x+game_width//4, y+int(game_height*0.52))
    time.sleep(2)
    pyautogui.moveTo(x+game_width//4, y+int(game_height*0.57))
    time.sleep(2)
    while True:
    #for i in range(1,500):
        if np.sum(abs(game_left-background_left)) <= np.sum(abs(game_right-background_right)):
            pyautogui.moveTo(x+game_width//4, y+int(game_height*0.52))
            time.sleep(0.02)
            pyautogui.click(x+game_width//4, y+int(game_height*0.52))
            print("IF", np.sum(abs(game_left-background_left)), np.sum(abs(game_right-background_right)))
        else:
            pyautogui.moveTo(x+game_width//4*3, y+int(game_height*0.52))
            time.sleep(0.02)
            pyautogui.click(x+game_width//4*3, y+int(game_height*0.52))
            print("ELSE", np.sum(abs(game_left-background_left)), np.sum(abs(game_right-background_right)))
            
        game_left = np.array(pyautogui.screenshot(region=left_region))
        game_right = np.array(pyautogui.screenshot(region=right_region))
        
        game_left = game_left.reshape(-1)
        game_right = game_right.reshape(-1)
        #pyautogui.screenshot(f"game{i}.png", region=(x, y, game_width, game_height))
        time.sleep(0.1)

        
        
play_game()