import tkinter as tk
from tkinter import filedialog, Text
import speech_recognition as sr
from pydub import AudioSegment
import os

# Set the path to ffmpeg executable
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"

# Initialize the main window
root = tk.Tk()
root.title("Speech to Text")
root.geometry("900x450+200+200")
root.resizable(False, False)
root.configure(bg="#305065")

# Create Recognizer
recognizer = sr.Recognizer()

def record_audio():
    with sr.Microphone() as source:
        try:
            text_area.delete(1.0, tk.END)  # Clear text box
            label_status.config(text="Listening...")
            audio = recognizer.listen(source, timeout=5)
            label_status.config(text="Transcribing...")

            text = recognizer.recognize_google(audio)

            # After transcription
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, text)
            label_status.config(text="Done")

            # Save As dialog after transcription is complete
            save_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")],
                title="Save transcription as"
            )
            if save_path:
                with open(save_path, "w", encoding="utf-8") as file:
                    file.write(text)

        except sr.UnknownValueError:
            text_area.insert(tk.END, "Sorry, could not understand audio.")
            label_status.config(text="Error")
        except sr.RequestError:
            text_area.insert(tk.END, "Speech service unavailable.")
            label_status.config(text="Error")
        except Exception as e:
            text_area.insert(tk.END, f"Error: {str(e)}")
            label_status.config(text="Error")

def upload_audio():
    file_path = filedialog.askopenfilename(
        initialdir=os.path.expanduser("~/Desktop"),
        filetypes=[("Audio Files", "*.wav *.mp3 *.flac")],
        title="Select an Audio File"
    )
    if file_path:
        file_ext = os.path.splitext(file_path)[1].lower()
        temp_file = None

        if file_ext in ['.mp3', '.flac']:
            audio = AudioSegment.from_file(file_path)
            temp_file = "temp.wav"
            audio.export(temp_file, format="wav")
            file_path = temp_file

        try:
            with sr.AudioFile(file_path) as source:
                label_status.config(text="Transcribing...")
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)

                # After transcription
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, text)
                label_status.config(text="Done")

                # Save As dialog after transcription
                save_path = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt")],
                    title="Save transcription as"
                )
                if save_path:
                    with open(save_path, "w", encoding="utf-8") as file:
                        file.write(text)

        except sr.UnknownValueError:
            text_area.insert(tk.END, "Could not understand the audio file.")
            label_status.config(text="Error")
        except sr.RequestError:
            text_area.insert(tk.END, "Speech service unavailable.")
            label_status.config(text="Error")
        except Exception as e:
            text_area.insert(tk.END, f"Error: {str(e)}")
            label_status.config(text="Error")
        finally:
            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)

# Top frame for title
top_frame = tk.Frame(root, bg="white", width=900, height=100)
top_frame.place(x=0, y=0)

label_title = tk.Label(top_frame, text="SPEECH TO TEXT", font="arial 20 bold", bg="white", fg="black")
label_title.place(x=100, y=30)

# Status Label
label_status = tk.Label(root, text="", font="arial 12 bold", bg="#305065", fg="white")
label_status.place(x=350, y=110)

# Text area to show transcription
text_area = Text(root, font="Roboto 20", bg="white", relief="groove", wrap="word")
text_area.place(x=10, y=150, width=500, height=250)

# Buttons
btn_record = tk.Button(root, text="Record", width=15, font="arial 14 bold", command=record_audio)
btn_record.place(x=550, y=200)

btn_upload = tk.Button(root, text="Upload Audio", width=15, font="arial 14 bold", bg="#39c790", command=upload_audio)
btn_upload.place(x=730, y=200)

# Run the window
root.mainloop()
