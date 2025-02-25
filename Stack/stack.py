import pyautogui
import time

CLICK_DELAY = 0.8

WHITE = (231, 231, 231)
BLACK = (0, 0, 0)

pyautogui.PAUSE = 0

def get_game_size():
    screenWidth, screenHeight = pyautogui.size()
    try:
        x, y, game_width, game_height = pyautogui.locateOnScreen("logo.png", confidence=0.9)
    except:
        x, y, game_width, game_height = pyautogui.locateOnScreen("logoWindows.png", confidence=0.9)
    x, y, game_width, game_height = int(x), int(y), int(game_width), int(game_height)
    while y<screenHeight and pyautogui.pixelMatchesColor(x, y, WHITE, tolerance=10):
        y+=1
    while x<screenWidth and pyautogui.pixelMatchesColor(x, y, BLACK, tolerance=10):
        x+=1
    game_width = 0
    while x+game_width<screenWidth and not pyautogui.pixelMatchesColor(x+game_width, y, BLACK, tolerance=10):
        game_width+=1
    game_height = int(2.22*game_width)    
    return (x, y, game_width, game_height)
    

def play_game():
    x, y, game_width, game_height = get_game_size()
    x_click = x+game_width//2
    y_click = y+game_height//2
    click_delay = CLICK_DELAY
    pyautogui.click(x_click, y_click)
    time.sleep(click_delay+0.05)
    for level in range(500):
        next_timestamp = time.perf_counter()+click_delay
        if not level%200:
            click_delay-=0.005
        pyautogui.click(x_click, y_click)
        time.sleep(max(next_timestamp-time.perf_counter(), 0))

play_game()