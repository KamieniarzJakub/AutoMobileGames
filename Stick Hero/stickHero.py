import pyautogui
import numpy as np
import time
import cv2
import easyocr

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
    
def get_platform_height(screenshot):
    for y in range(len(screenshot)):
        if np.array_equal(screenshot[y][0], BLACK):
            return y
    return 0

def get_platform_width(screenshot, platform_height):
    platform_x = len(screenshot[platform_height])//10
    while platform_x<len(screenshot[platform_height]) and sum(screenshot[platform_height+1][platform_x]>10):
        platform_x+=1
    for x in range(platform_x+1, len(screenshot[platform_height])):
        if sum(screenshot[platform_height+1][x])>10:
            return x
        
def get_gap_size(screenshot, platform_height, platform_width):
    for x in range(platform_width, len(screenshot[platform_height])):
        if sum(screenshot[platform_height+1][x])<10:
            for width in range(x, len(screenshot[platform_height])):
                if sum(screenshot[platform_height+1][width])>10:
                    return width-platform_width
    return 0

def play_game():
    x, y, game_width, game_height = get_game_size()
    #pyautogui.click(x+game_width//2, y+game_height//2)
    game = np.array(pyautogui.screenshot("game.png", region=(x, y, game_width, game_height)))
    score=0
    platform_height = get_platform_height(game)
    #pyautogui.click(x+platform_width+gap_size, y+platform_height)
    for i in range(100):
        platform_width = get_platform_width(game, platform_height)
        gap_size = get_gap_size(game, platform_height, platform_width)
        pyautogui.moveTo(x+platform_width, y+platform_height)
        time.sleep(0.5)
        
        touch_time = gap_size/500*((min(5+score//50, gap_size//40))/25+1)
        if gap_size<60:
            touch_time*=0.8
        if score>=50:
            touch_time*=0.9
        pyautogui.moveTo(x+platform_width, y+platform_height-gap_size)
        pyautogui.mouseDown()
        time.sleep(touch_time)
        pyautogui.mouseUp()
        print("Score:", score, "Gap size:", gap_size, "Gap%40 = ", gap_size%40, "Calculated touch time:", touch_time, "level:", i)
        time.sleep(1)
        #pyautogui.click()
        time.sleep(touch_time)
        #pyautogui.click()
        time.sleep(3)

        #print(x, y, game_width, game_height)
        game = np.array(pyautogui.screenshot("game.png", region=(x, y, game_width, game_height)))
        score_img = game[int(game_height*0.1):int(game_height*0.25), int(game_width*0.25):int(game_width*0.75)]
        score_img = cv2.cvtColor(score_img, cv2.COLOR_RGB2GRAY)
        # Apply threshold (adjust values if needed)
        _, score_img = cv2.threshold(score_img, 230, 255, cv2.THRESH_BINARY)
        cv2.imwrite("score.png", score_img)
        reader = easyocr.Reader(['en'])
        data = reader.readtext(score_img, allowlist="1234567890")
        try:
            score = int(data[0][1])
        except:
            print("Can't recognize score")
play_game()