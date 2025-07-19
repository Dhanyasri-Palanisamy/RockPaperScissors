import cv2
import mediapipe as mp
import random
import time

# Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Gesture classifier
def classify(hand_landmarks):
    finger_up = []

    tip_ids = [4, 8, 12, 16, 20]
    for i in range(1, 5):
        if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y:
            finger_up.append(1)
        else:
            finger_up.append(0)

    if finger_up == [0, 0, 0, 0]: return "Rock"
    elif finger_up == [1, 1, 1, 1]: return "Paper"
    elif finger_up == [0, 1, 1, 0]: return "Scissors"
    else: return "Unknown"

# Game logic
def get_result(user, cpu):
    if user == cpu:
        return "Draw"
    elif (user == "Rock" and cpu == "Scissors") or \
         (user == "Paper" and cpu == "Rock") or \
         (user == "Scissors" and cpu == "Paper"):
        return "You Win!"
    else:
        return "You Lose!"

# Main
cap = cv2.VideoCapture(0)
prev_time = 0
cpu_choice = None
result = ""
timer = 0

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result_mp = hands.process(rgb)

    user_move = "Waiting..."

    if result_mp.multi_hand_landmarks:
        for handLms in result_mp.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
            user_move = classify(handLms)

            if timer == 0:
                cpu_choice = random.choice(["Rock", "Paper", "Scissors"])
                result = get_result(user_move, cpu_choice)
                timer = 60

    if timer > 0:
        timer -= 1

    # UI
    cv2.putText(frame, f"Your Move: {user_move}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    if cpu_choice:
        cv2.putText(frame, f"CPU: {cpu_choice}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 100), 2)
        cv2.putText(frame, f"{result}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    cv2.imshow("Stone Paper Scissors - CV", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
