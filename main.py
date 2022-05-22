# import os
import os

import cv2

from bot import RiseOnlineBot, BotState
from detection import Detection
from vision import Vision
from windowcapture import WindowCapture
from time import time

DEBUG = False

# Changes the directory portion.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initializes WindowCapture object.
window_capture = WindowCapture(None)

# Loads the detector.
detector = Detection('cascade/cascade.xml')

# Loads an empty vision class.
vision_object = Vision()

# Initializes the bot object.
bot = RiseOnlineBot((window_capture.offset_x, window_capture.offset_y), (window_capture.w, window_capture.h))

window_capture.start()
detector.start()
bot.start()

loop_time = time()

while True:
    # Check if there is a screenshot. If not, it won't run the code.
    if window_capture.screenshot is None:
        continue

    # screenshot = np.array(ImageGrab.grab(bbox=(0, 40, 1366, 768)))
    # screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    # # Gives the detector the current screenshot to search for objects in.
    detector.update(window_capture.screenshot)
    #
    # Update the bot with the data it needs right now.
    if bot.state == BotState.INITIALIZING:
        # While bot is waiting to start, go ahead and start giving it some targets to work
        # on right away when it does start
        targets = vision_object.get_click_points(detector.rectangles)
        bot.update_targets(targets)
    elif bot.state == BotState.SEARCHING:
        # When searching for something to click on next, the bot needs to know what the click
        # points are for the current detection results. It also needs an updated screenshot
        # to verify the hover tooltip once it has moved the mouse to that position.
        targets = vision_object.get_click_points(detector.rectangles)
        bot.update_targets(targets)
        bot.update_screenshot(window_capture.screenshot)
    elif bot.state == BotState.MOVING:
        # When moving, we need fresh screenshots to determine when we've stopped moving.
        bot.update_screenshot(window_capture.screenshot)
    elif bot.state == BotState.MINING:
        # Nothing is needed while we wait for the mining to finish.
        pass

    if DEBUG:
        # Draws the detection results onto the original image.
        detection_image = vision_object.draw_rectangles(window_capture.screenshot, detector.rectangles)

        # Displays the image.
        cv2.imshow('Matches', window_capture.screenshot)

    key = cv2.waitKey(1) & 0xFF  # Waits 1ms every loop to process key presses.
    loop_time = time()
    if key == ord('z'):
        window_capture.stop()
        detector.stop()
        bot.stop()
        cv2.destroyAllWindows()
        break
    # elif key == ord('f'):
    #     cv2.imwrite('copperMines/positive/{}.jpg'.format(loop_time), window_capture.screenshot)
    #     print('Screenshot taken.')
    # elif key == ord('d'):
    #     cv2.imwrite('copperMines/negative/{}.jpg'.format(loop_time), window_capture.screenshot)
    #     print('Screenshot taken.')

print('Peacefully closing the app.')
