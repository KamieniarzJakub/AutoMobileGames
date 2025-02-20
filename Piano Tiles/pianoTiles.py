import pyautogui
import numpy as np
import time


WHITE = (231, 231, 231)
BLACK = (0, 0, 0)

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
    
def start_game():
    x, y, game_width, game_height = get_game_size()
    sensors = [game_width//8, game_width//8*3, game_width//8*5, game_width//8*7]
    sensors_height = int(3/5*game_height)
    while True:
        game = np.array(pyautogui.screenshot(region=(x, y+sensors_height, game_width, 1)))
        for offset in sensors:
            #print(game[0][offset])
            if sum(game[0][offset])<500:
                pyautogui.click(x+offset, y+sensors_height+game_height//5)
        #print()


start_game()