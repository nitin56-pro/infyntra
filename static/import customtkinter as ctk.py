import customtkinter as ctk
import pyttsx3
import speech_recognition as sr
from PIL import Image, ImageTk, ImageSequence
import threading
import time
import datetime

# ----------------------------- AGNIX SETUP ----------------------------- #
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Text-to-speech setup
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 170)

def speak(text):
    status_label.configure(text=f"Agnix: {text}")
    engine.say(text)
    engine.runAndWait()

def greet_user():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        speak("Good morning! I am Agnix, your assistant.")
    elif 12 <= hour < 18:
        speak("Good afternoon! I am Agnix, your assistant.")
    else:
        speak("Good evening! I am Agnix, your assistant.")

# ----------------------------- GUI SETUP ----------------------------- #
class AgnixGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Agnix - Voice Assistant")
        self.geometry("500x600")
        self.resizable(False, False)

        self.icon_image = Image.open("agnix_icon.gif")
        self.icon_label = ctk.CTkLabel(self, text="")
        self.icon_label.pack(pady=20)
        self.animate_icon()

        self.title_label = ctk.CTkLabel(self, text="AGNIX", font=("Arial Black", 30))
        self.title_label.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="Click start to speak", font=("Arial", 16))
        self.status_label.pack(pady=10)
        global status_label
        status_label = self.status_label

        self.start_button = ctk.CTkButton(self, text="🎙 Start Listening", command=self.start_listening)
        self.start_button.pack(pady=20)

        self.stop_button = ctk.CTkButton(self, text="❌ Stop", command=self.stop_listening)
        self.stop_button.pack(pady=10)

        self.listening = False
        greet_user()

    def animate_icon(self):
        self.frames = [ImageTk.PhotoImage(img.resize((150, 150))) for img in ImageSequence.Iterator(self.icon_image)]
        self.index = 0
        self.update_icon()

    def update_icon(self):
        frame = self.frames[self.index]
        self.icon_label.configure(image=frame)
        self.index = (self.index + 1) % len(self.frames)
        self.after(100, self.update_icon)

    def start_listening(self):
        self.listening = True
        threading.Thread(target=self.listen_command).start()

    def stop_listening(self):
        self.listening = False
        status_label.configure(text="Listening stopped.")

    def listen_command(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        while self.listening:
            with mic as source:
                status_label.configure(text="Listening...")
                recognizer.adjust_for_ambient_noise(source)
                try:
                    audio = recognizer.listen(source, timeout=5)
                    command = recognizer.recognize_google(audio).lower()
                    status_label.configure(text=f"You: {command}")
                    self.respond(command)
                except sr.UnknownValueError:
                    status_label.configure(text="Sorry, I didn't understand.")
                except sr.WaitTimeoutError:
                    status_label.configure(text="Timeout. No speech detected.")
                except Exception as e:
                    status_label.configure(text=f"Error: {e}")
            time.sleep(1)

    def respond(self, command):
        if "hello" in command:
            speak("Hello! How can I assist you?")
        elif "your name" in command:
            speak("My name is Agnix. I am your smart assistant.")
        elif "time" in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {now}.")
        elif "stop" in command or "exit" in command:
            speak("Goodbye!")
            self.destroy()
        else:
            speak("Sorry, I don't understand that yet.")

# ----------------------------- MAIN ----------------------------- #
if __name__ == "__main__":
    app = AgnixGUI()
    app.mainloop()
