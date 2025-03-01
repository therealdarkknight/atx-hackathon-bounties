import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

ANNOTATE_HAND = False

# For drawing the hand annotations on the image
mp_drawing = mp.solutions.drawing_utils

def count_fingers_up(hand_landmarks):
    landmarks = [(lm.x, lm.y) for lm in hand_landmarks.landmark]

    wrist_y = landmarks[0][1]

    fingers_up = 0

    thumb_tip_x = landmarks[4][0]

    if abs(thumb_tip_x - wrist_y) > 0.05:  
        fingers_up += 1

    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]

    for tip_idx, pip_idx in zip(finger_tips, finger_pips):
        tip_y = landmarks[tip_idx][1]
        pip_y = landmarks[pip_idx][1]
        if tip_y < pip_y:  
            fingers_up += 1

    return fingers_up


def classify_gesture(fingers_up, hand_landmarks):
    gestures = {
        "thumbs_up": 0.0,
        "thumbs_down": 0.0,
        "five_fingers": 0.0,
        "unknown": 0.0
    }

    if fingers_up == 5:
        gestures["five_fingers"] = 1.0
        return gestures

    elif fingers_up == 1:
        landmarks_list = [(lm.x, lm.y) for lm in hand_landmarks.landmark]
        wrist_y = landmarks_list[0][1]
        thumb_tip_y = landmarks_list[4][1]

        if thumb_tip_y < wrist_y:
            gestures["thumbs_up"] = 1.0
        else:
            gestures["thumbs_down"] = 1.0

        return gestures

    else:
        gestures["unknown"] = 1.0
        return gestures


def get_highest_confidence_gesture(gestures):
    return 


def main():
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    while True:
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Flip horizontally for a mirror-like effect
        frame = cv2.flip(frame, 1)

        # Convert the BGR image to RGB
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        curr_gesture = "no_hand"

        if results.multi_hand_landmarks:
            # For each hand detected
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks on the frame for visualization
                if ANNOTATE_HAND:
                    mp_drawing.draw_landmarks(
                        frame, 
                        hand_landmarks, 
                        mp_hands.HAND_CONNECTIONS
                    )

                # Count how many fingers are extended
                fingers_up = count_fingers_up(hand_landmarks)

                # Classify the gesture
                gesture_conf = classify_gesture(fingers_up, hand_landmarks)

                curr_gesture = max(gesture_conf, key=gesture_conf.get)


        # ['thumbs_up', 'thumbs_down', 'five_fingers', 'unknown', 'no_hand']
        print(f"Gesture: {curr_gesture}")

        cv2.imshow('Hand Gesture', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
