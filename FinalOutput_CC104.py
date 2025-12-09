import tkinter as tk
from data import data
from playsound import playsound
import threading
import random
import time
from PIL import Image, ImageTk  # Only import what we use


# ---------------- QUIZ STATE ----------------
quiz_items = random.sample(list(data.items()), 20)
current_question = 0
score = 0
current_correct = None
skipped_items = []
leaderboard = []   # 👉 dito  ise-save lahat ng users at scores

# ---------------- GUI SETUP ----------------

root = tk.Tk()
root.title("Quiz App")
root.geometry("1000x1000")

# Load and resize the image to fit window
img = Image.open("C:\\Users\\user\\Downloads\\Powerpuff-Girls-PNG-Photos.png")
img = img.resize((1000, 1000), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(img)

# Display background
bg_label = tk.Label(root, image=bg_photo)
bg_label.image = bg_photo  # Keep reference
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

#---------------- LOGIN SCREEN ----------------
# Define a consistent transparent background color (use the root window's default background)
# This makes the widgets appear to float on the image.
TRANSPARENT_BG = root["bg"]
TEXT_COLOR = "#000000" # Black for contrast

# Changed: Set background to TRANSPARENT_BG
login_frame = tk.Frame(root, bg=TRANSPARENT_BG) 
login_frame.pack(expand=True)

# Changed: Set background to TRANSPARENT_BG and foreground to black for readability
tk.Label(login_frame, text=" Login", font=("Comic Sans MS", 28, "bold"), fg=TEXT_COLOR, bg=TRANSPARENT_BG).pack(pady=20)

# Changed: Set background to TRANSPARENT_BG and foreground to black
tk.Label(login_frame, text="Name:", font=("Comic Sans MS", 18, "bold"), fg=TEXT_COLOR, bg=TRANSPARENT_BG).pack()
name_entry = tk.Entry(login_frame, font=("Comic Sans MS", 16), width=30, bd=2, relief="groove") # Retain some border for entry visibility
name_entry.pack(pady=5, ipady=5)

# Changed: Set background to TRANSPARENT_BG and foreground to black
tk.Label(login_frame, text="Course, Year & Section:", font=("Comic Sans MS", 18, "bold"), fg=TEXT_COLOR, bg=TRANSPARENT_BG).pack()
course_entry = tk.Entry(login_frame, font=("Comic Sans MS", 16), width=30, bd=2, relief="groove")
course_entry.pack(pady=5, ipady=5)

# Changed: Set background to TRANSPARENT_BG and foreground to black
tk.Label(login_frame, text="Password:", font=("Comic Sans MS", 18, "bold"), fg=TEXT_COLOR, bg=TRANSPARENT_BG).pack()
# Changed: Set background to TRANSPARENT_BG
pwd_frame = tk.Frame(login_frame, bg=TRANSPARENT_BG) 
pwd_frame.pack(pady=5)

password_entry = tk.Entry(pwd_frame, show="*", font=("Comic Sans MS", 16), width=25, bd=2, relief="groove")
password_entry.pack(side="left", padx=4, ipady=4)


def toggle_password():
    if password_entry.cget("show") == "":
        password_entry.config(show="*")
        toggle_btn.config(text=" Show")
    else:
        password_entry.config(show="")
        toggle_btn.config(text=" Hide")

toggle_btn = tk.Button(pwd_frame, text=" Show", font=("Comic Sans MS", 10),
                       bg="#dcdcdc", command=toggle_password)
toggle_btn.pack(side="left", padx=1)

import re
import tkinter as tk

def login():
    global player_name, player_course
    name = name_entry.get().strip()
    course = course_entry.get().strip()
    pwd = password_entry.get().strip()

    if not name or not course or not pwd:
        login_feedback.config(text=" Please fill up all fields first", fg="red")
        return
    if not re.fullmatch(r"[A-Za-z\s]+", name):
        login_feedback.config(text=" Name must contain only letters", fg="red")
        return
    if not re.fullmatch(r"[A-Za-z0-9\s]+", course):
        login_feedback.config(text=" Course & Section must contain letters/numbers only", fg="red")
        return
    if not re.fullmatch(r"[A-Za-z0-9]+", pwd):
        login_feedback.config(text=" Password must contain letters/numbers only", fg="red")
        return

    player_name = name
    player_course = course
    login_feedback.config(text="✅ Login Successful!", fg="green")
    login_frame.pack_forget()
    start_background_music()  # Play looping background music
    start_quiz()

# Feedback label (transparent, walang pink bg)
login_feedback = tk.Label(login_frame, text="", font=("Comic Sans MS", 12))
login_feedback.pack(pady=5)

login_btn = tk.Button(login_frame, text="Login", font=("Comic Sans MS", 12),
                    bg="#90ee90", width=20, command=login)
login_btn.pack(pady=10)

# ---------------- QUIZ SCREEN ----------------
letters = ["A", "B", "C", "D"]

def start_quiz():
    global question_label, feedback_label, score_label, option_buttons, skip_btn

    login_frame.pack_forget()
    root.update()
    W = root.winfo_width()
    H = root.winfo_height()

    center_x = W // 2
    center_y = H // 2

    # TITLE
    quiz_title = tk.Label(root, text="📘 PowerPuff Quiz: Data Structure, Loops, Stacks, LinkedList, Recursion, Queue",
                          font=("Comic Sans MS", 20, "bold"),
                          fg="#000000", bg="#ffcccb", wraplength=900 )
    quiz_title.place(x=center_x, y=60, anchor="center")

    # QUESTION
    question_label = tk.Label(root, text="", wraplength=700,
                              font=("Comic Sans MS", 16, "bold"),
                              fg="#000", bg=root["bg"])
    question_label.place(x=center_x, y=150, anchor="center")

    # FEEDBACK
    feedback_label = tk.Label(root, text="", font=("Comic Sans MS", 14, "bold"),
                              fg="#000000", bg=root["bg"])
    feedback_label.place(x=center_x, y=230, anchor="center")

    # SCORE
    score_label = tk.Label(root, text="Score: 0",
                           font=("Comic Sans MS", 16, "bold"),
                           fg="#000", bg="white", padx=8, pady=4)
    score_label.place(x=center_x, y=290, anchor="center")

    # BUTTON STYLE
    button_style = {
        "width": 45,
        "font": ("Comic Sans MS", 12),
        "bg": "#FFDAC0",
        "fg": "#000",
        "activebackground": "#FF69B4",
        "bd": 3,
        "relief": "raised",
        "wraplength": 500,   # para mag line-break kapag mahaba
        "justify": "left"    # align sa kaliwa
    }

    # OPTION BUTTONS
    option_buttons = []
    start_y = 360
    for i, letter in enumerate(letters):
        btn = tk.Button(root,
                        text=f"{letter}. ",   # fixed prefix
                        command=lambda b=None: None,  # temporary, i-configure sa load_question
                        **button_style)
        btn.place(x=center_x, y=start_y + (i * 60), anchor="center")
        option_buttons.append(btn)

    # SKIP BUTTON
    skip_btn = tk.Button(root, text="⏭ Skip Question",
                         font=("Comic Sans MS", 12, "bold"),
                         bg="#ffcccb", fg="#000",
                         activebackground="#FF69B4", width=20,
                         command=skip_question)
    skip_btn.place(x=center_x, y=620, anchor="center")

    load_question()


# Helper: auto-shrink text if sobrang haba
def set_option_text(btn, letter, answer):
    size = 14
    if len(answer) > 40:
        size = 12
    if len(answer) > 60:
        size = 10
    btn.config(text=f"{letter}. {answer}",
               font=("Comic Sans MS", size),
               command=lambda ans=answer: check_answer(ans))


def skip_question():
    global current_question, quiz_items
    # kunin yung mga current na tanong
    skipped = quiz_items.pop(current_question)
    # idagdag sa dulo ng list yung mga tanong na na-skip
    quiz_items.append(skipped)
    # para hindi i-increment ang current_question (para lumipat sa susunod na tanong)
    root.after(500, load_question)

def load_question():
    global current_correct, correct_letter, current_question, quiz_items, skipped_items

    # Hide the feedback label each time a new question loads
    feedback_label.place_forget()
    
    if current_question >= len(quiz_items) and skipped_items:
        quiz_items.extend(skipped_items)
        skipped_items = []

    if current_question < len(quiz_items):
        q, data = quiz_items[current_question]
        question_label.config(text=f"Q{current_question + 1}: {q}")
        feedback_label.config(text="")
        shuffled = data["options"][:]
        random.shuffle(shuffled)
        current_correct = data["answer"]

        labels = ["a.", "b.", "c.", "d."]
        correct_letter = None
        for i, btn in enumerate(option_buttons):
            btn.config(text=f"{labels[i]} {shuffled[i]}", 
                      state="normal",
                      command=lambda ans=shuffled[i]: check_answer(ans))
            if shuffled[i] == current_correct:
                correct_letter = labels[i]
    else:
        with open("scores.txt", "a") as file:
            file.write(f"{player_name} ({player_course}) - Score: {score}/{len(quiz_items)}\n")
    # Save to leaderboard (name, course, score)
 
            # QUIZ FINISHED – SHOW RESULTS ONLY

    # Hide buttons
        for btn in option_buttons:
            btn.place_forget()

        skip_btn.place_forget()
        
        score_label.place_forget()
        
        leaderboard.append((player_name, player_course, score))
        leaderboard.sort(key=lambda x: x[1], reverse=True)

    # Display final score (pero wala nang leaderboard text)
        question_label.config(
            text=f" 🎉 QUIZ DONE! 🎉 \n\n"
            f"Name: {player_name}\n"
            f"Course/Section: {player_course}\n"
            f"Final Score: {score}/{len(quiz_items)}",
            font=("Comic Sans MS", 16 , "bold"),
            fg="#000000",
            bg=root["bg"],
            justify="center"
        )
        question_label.place(x=root.winfo_width()//2, y=250, anchor="center")

        # Add restart button
        restart_btn = tk.Button(root, text="🔄 Restart Quiz",
                               font=("Comic Sans MS", 14, "bold"),
                               bg="#90ee90", fg="#000",
                               activebackground="#32cd32", width=20,
                               command=restart_quiz)
        restart_btn.place(x=root.winfo_width()//2, y=620, anchor="center")
        
        return 
        
        
        
def play_bg_music():
    global stop_bg_music
    while not stop_bg_music:
        try:
            playsound("C:\\Users\\user\\OneDrive\\Documents\\My practicing programming\\final output\\game-music-loop-7-145285.mp3")
            time.sleep(0.1)  # Small delay between loops
        except:
            break

def start_background_music():
    global bg_music_thread, stop_bg_music
    stop_bg_music = False
    bg_music_thread = threading.Thread(target=play_bg_music, daemon=True)
    bg_music_thread.start()

def stop_background_music():
    global stop_bg_music
    stop_bg_music = True

def check_answer(selected_text):
    global current_question, score, current_correct, correct_letter

    # The selected_text is now just the answer text (no prefix)
    selected_text_clean = selected_text

    # Safe fallback kung walang correct_letter
    if correct_letter:
        display_letter = correct_letter.replace(".", "")
    else:
        display_letter = current_correct


    if selected_text_clean == current_correct:
        feedback_label.config(text="✅ Correct!", fg="green")
        feedback_label.place(x=root.winfo_width()//2, y=230, anchor="center")

        threading.Thread(
            target=playsound,
            args=("C:\\Users\\user\\OneDrive\\Documents\\My practicing programming\\361263__japanyoshithegamer__8-bit-correct-answer.wav",),
            daemon=True
           ).start()

        score += 1
    else:
        feedback_label.config(text=f"❌ Incorrect! Correct answer: {display_letter}", fg="red")
        feedback_label.place(x=root.winfo_width()//2, y=230, anchor="center")

        threading.Thread(
            target=playsound,
            args=("C:\\Users\\user\\OneDrive\\Documents\\My practicing programming\\419023__jacco18__acess-denied-buzz.mp3",),
            daemon=True
        ).start()

    score_label.config(text=f"Score: {score}")
    current_question += 1
    root.after(1000, load_question)

def restart_quiz():
    global current_question, score, quiz_items
    current_question = 0
    score = 0
    quiz_items = random.sample(list(data.items()), 20)
    random.shuffle(quiz_items)
    
    # Clear any existing restart button
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button) and "🔄 Restart Quiz" in widget.cget("text"):
            widget.destroy()
    
    # Show the quiz elements again
    question_label.place(x=root.winfo_width()//2, y=150, anchor="center")
    score_label.place(x=root.winfo_width()//2, y=290, anchor="center")
    skip_btn.place(x=root.winfo_width()//2, y=620, anchor="center")
    for btn in option_buttons:
        btn.place(x=root.winfo_width()//2, y=360 + (option_buttons.index(btn) * 60), anchor="center")
    
    score_label.config(text="Score: 0")
    load_question()

# ---------------- START APP ----------------
root.mainloop()