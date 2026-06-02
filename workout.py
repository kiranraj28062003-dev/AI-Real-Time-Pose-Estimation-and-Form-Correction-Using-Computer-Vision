import cv2
import mediapipe as mp
import time
import pyttsx3
import threading
from utils import calculate_angle
from db import save_workout
from datetime import datetime

# ================= VOICE =================
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak_async(text):
    def run():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run, daemon=True).start()

# ================= MEDIAPIPE =================
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# ================= MAIN =================
def start_workout(user, exercise):

    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)

    count = 0
    stage = None
    last_feedback = ""
    last_rep_time = 0

    # stability control
    stable_down = 0
    stable_up = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(img)

        feedback = "Adjust position"

        if results.pose_landmarks:

            mp_draw.draw_landmarks(frame,
                                   results.pose_landmarks,
                                   mp_pose.POSE_CONNECTIONS)

            lm = results.pose_landmarks.landmark

            if lm[12].visibility > 0.7 and lm[24].visibility > 0.7:

                # LANDMARKS
                shoulder = [lm[12].x, lm[12].y]
                elbow = [lm[14].x, lm[14].y]
                wrist = [lm[16].x, lm[16].y]

                hip = [lm[24].x, lm[24].y]
                knee = [lm[26].x, lm[26].y]
                ankle = [lm[28].x, lm[28].y]

                # ANGLES
                arm_angle = int(calculate_angle(shoulder, elbow, wrist))
                leg_angle = int(calculate_angle(hip, knee, ankle))

                # DISPLAY ANGLES
                cv2.putText(frame, f"Arm: {arm_angle}", (900,100),0,1,(255,255,255),2)
                cv2.putText(frame, f"Leg: {leg_angle}", (900,150),0,1,(255,255,255),2)

                now = time.time()

                # ================= UPPER BODY =================
                if exercise in ["Push-up","Pull-up","Bicep Curl","Shoulder Press"]:

                    # DOWN POSITION (relaxed)
                    if arm_angle > 150:
                        stable_down += 1
                        stable_up = 0
                        feedback = "Go Down Slowly"

                        if stable_down > 5:
                            stage = "down"

                    # UP POSITION
                    elif arm_angle < 80:
                        stable_up += 1
                        stable_down = 0

                        if stable_up > 5 and stage == "down" and now - last_rep_time > 1.5:
                            count += 1
                            stage = "up"
                            last_rep_time = now
                            feedback = "Good Rep"
                        else:
                            feedback = "Hold Position"

                    # MID RANGE
                    else:
                        stable_down = 0
                        stable_up = 0
                        feedback = "Complete Full Range"

                # ================= LOWER BODY =================
                else:

                    if leg_angle > 160:
                        stable_up += 1
                        stable_down = 0
                        feedback = "Stand Straight"

                        if stable_up > 5:
                            stage = "up"

                    elif leg_angle < 90:
                        stable_down += 1
                        stable_up = 0

                        if stable_down > 5 and stage == "up" and now - last_rep_time > 1.5:
                            count += 1
                            stage = "down"
                            last_rep_time = now
                            feedback = "Good Rep"
                        else:
                            feedback = "Hold Position"

                    else:
                        stable_up = 0
                        stable_down = 0
                        feedback = "Go Lower"

            else:
                feedback = "Full body not visible"

        else:
            feedback = "No person detected"

        # ================= VOICE =================
        if feedback != last_feedback:
            speak_async(feedback)
            last_feedback = feedback

        # ================= CALORIES =================
        calories = round(count * 0.5, 2)

        # ================= DISPLAY =================
        cv2.putText(frame, exercise, (20,50),0,1,(255,0,0),2)
        cv2.putText(frame, f"Reps: {count}", (20,100),0,1,(0,255,0),2)
        cv2.putText(frame, f"Calories: {calories}", (20,150),0,1,(0,255,255),2)
        cv2.putText(frame, feedback, (20,200),0,1,(0,0,255),2)

        cv2.imshow("AI Gym Trainer", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    save_workout(user, exercise, count, calories, str(datetime.now()))

    cap.release()
    cv2.destroyAllWindows()