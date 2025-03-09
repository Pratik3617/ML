import cv2
import numpy as np

keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["Z", "X", "C", "V", "B", "N", "M", "<-"],
    ["SPACE"]
]

color = "Red"
drawing_color = (0, 0, 255)
drawing_thickness = 8
eraser_thickness = 40  # Increased eraser thickness
eraser = False

key_width, key_height = 120, 120
spacing = 10
keyboard_width = len(keys[0]) * (key_width + spacing) - spacing
keyboard_height = len(keys) * (key_height + spacing) - spacing
screen_width, screen_height = 1920, 1080
start_x = (screen_width - keyboard_width) // 2
start_y = screen_height - keyboard_height - 100

color = "Red"
eraser = False

def draw_key(img, x, y, width, height, key):
    shadow_offset = 8
    cv2.rectangle(img, (x + shadow_offset, y + shadow_offset),
                  (x + width + shadow_offset, y + height + shadow_offset),
                  (80, 80, 80), -1, cv2.LINE_AA)
    cv2.rectangle(img, (x, y), (x + width, y + height), (255, 255, 255), -1, cv2.LINE_AA)
    cv2.rectangle(img, (x, y), (x + width, y + height), (0, 0, 0), 3, cv2.LINE_AA)
    text_x = x + width // 3
    text_y = y + height - 40
    if key == "SPACE":
        text_x = x + width // 3
        text_y = y + height // 2 + 10
    cv2.putText(img, key, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 4, cv2.LINE_AA)


def draw_keyboard(img):
    for row_index, row in enumerate(keys):
        for col_index, key in enumerate(row):
            x = start_x + col_index * (key_width + spacing)
            y = start_y + row_index * (key_height + spacing)
            if key == "SPACE":
                key_width_space = key_width * 6 + spacing * 5
                draw_key(img, x, y, key_width_space, key_height, "SPACE")
            else:
                draw_key(img, x, y, key_width, key_height, key)


def check_key_press(x, y):
    for row_index, row in enumerate(keys):
        for col_index, key in enumerate(row):
            x1 = start_x + col_index * (key_width + spacing)
            y1 = start_y + row_index * (key_height + spacing)
            x2 = x1 + key_width
            y2 = y1 + key_height
            if key == "SPACE":
                x2 = x1 + key_width * 6 + spacing * 5
            if x1 < x < x2 and y1 < y < y2:
                return key
    return None


def draw_mode_switch_buttons(img,drawing_mode):
    button_width, button_height = 200, 100
    type_button_x = screen_width - button_width - 300
    draw_button_x = screen_width - button_width - 100
    button_y = 50

    # Type Mode Button
    cv2.rectangle(img, (type_button_x, button_y), (type_button_x + button_width, button_y + button_height),
                  (0, 128, 0) if not drawing_mode else (100, 100, 100), -1, cv2.LINE_AA)
    cv2.rectangle(img, (type_button_x, button_y), (type_button_x + button_width, button_y + button_height),
                  (255,255,255), 3, cv2.LINE_AA)
    cv2.putText(img, "Type Mode", (type_button_x + 20, button_y + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 4, cv2.LINE_AA)

    # Draw Mode Button
    cv2.rectangle(img, (draw_button_x, button_y), (draw_button_x + button_width, button_y + button_height),
                  (0, 128, 0) if drawing_mode else (100, 100, 100), -1, cv2.LINE_AA)
    cv2.rectangle(img, (draw_button_x, button_y), (draw_button_x + button_width, button_y + button_height),
                  (255,255,255), 3, cv2.LINE_AA)
    cv2.putText(img, "Draw Mode", (draw_button_x + 20, button_y + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 4, cv2.LINE_AA)

    return [(type_button_x, button_y, button_width, button_height, "type"),
            (draw_button_x, button_y, button_width, button_height, "draw")]


import cv2
import numpy as np

def color_buttons(img, x=None, y=None, color="Red", eraser=False, drawing_color=(0, 0, 255)):
    radius = 50
    red_color_center = (100, 100)
    blue_color_center = (220, 100)
    purple_color_center = (340, 100)
    eraser_top_left = (420, 60)
    eraser_bottom_right = (520, 140)

    # Draw color buttons
    cv2.circle(img, red_color_center, radius, (0, 0, 255), -1, cv2.LINE_AA)  # Red
    cv2.circle(img, blue_color_center, radius, (255, 0, 0), -1, cv2.LINE_AA)  # Blue
    cv2.circle(img, purple_color_center, radius, (255, 0, 255), -1, cv2.LINE_AA)  # Purple
    cv2.rectangle(img, eraser_top_left, eraser_bottom_right, (255, 255, 255), -1)  # Eraser

    # Highlight selected color
    if color == "Red":
        cv2.circle(img, red_color_center, radius, (255, 255, 255), 3, cv2.LINE_AA)
    elif color == "Blue":
        cv2.circle(img, blue_color_center, radius, (255, 255, 255), 3, cv2.LINE_AA)
    elif color == "Purple":
        cv2.circle(img, purple_color_center, radius, (255, 255, 255), 3, cv2.LINE_AA)

    if eraser:
        cv2.rectangle(img, eraser_top_left, eraser_bottom_right, (0, 0, 255), 3)

    # Check selection
    if x is not None and y is not None:
        if np.linalg.norm(np.array([x, y]) - np.array(red_color_center)) < radius:
            return "Red", False, (0, 0, 255)
        elif np.linalg.norm(np.array([x, y]) - np.array(blue_color_center)) < radius:
            return "Blue", False, (255, 0, 0)
        elif np.linalg.norm(np.array([x, y]) - np.array(purple_color_center)) < radius:
            return "Purple", False, (255, 0, 255)
        elif eraser_top_left[0] < x < eraser_bottom_right[0] and eraser_top_left[1] < y < eraser_bottom_right[1]:
            return color, True, drawing_color  # Keep color, enable eraser

    return color, eraser, drawing_color  # Return the same values if no button is pressed


def detect_v_gesture(lmList):
    """Detects a 'V' gesture by checking if index and middle fingers are extended and separated."""
    if len(lmList) < 12:
        return False
    
    index_tip = lmList[8]
    middle_tip = lmList[12]
    index_mcp = lmList[5]  # Base of index finger
    middle_mcp = lmList[9]  # Base of middle finger
    
    # Ensure both fingers are up
    if index_tip[2] < index_mcp[2] and middle_tip[2] < middle_mcp[2]:
        # Check if they are separated
        if abs(index_tip[1] - middle_tip[1]) > 40:
            return True
    
    return False



