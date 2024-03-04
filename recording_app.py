import tkinter as tk
from tkinter import filedialog
import pyaudio
import wave

class SoundRecorder:
    def __init__(self, master):
        self.master = master
        master.title('Sound Recorder')
        master.geometry('300x130')

        self.recording = False
        self.frames = []
        self.stream = None
        self.eslaped_time = 0

        self.create_widgets()

    def create_widgets(self):
        self.time_label = tk.Label(self.master, text="00:00:00", font=('Calibri', '40'))
        self.time_label.pack()

        self.frame = tk.Frame(self.master)
        self.frame.pack(pady=10)

        self.record = tk.Button(self.frame, text="Record", command=self.toggle_recording)
        self.record.pack(padx=10, side='left')

        self.pause = tk.Button(self.frame, text="Pause", command=self.toggle_pause, state='disable')
        self.pause.pack(padx=10, side='left')

        self.stop = tk.Button(self.frame, text="Stop", command=self.stop_recording, state='disable')
        self.stop.pack(padx=10, side='left')

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.recording = True
        self.record['state'] = 'disable'
        self.pause['state'] = 'active'
        self.stop['state'] = 'active'

        self.frames.clear()
        self.stream = self.open_stream()

        while self.recording:  
            data = self.stream.read(3200)
            if data:
                self.frames.append(data)
                self.update_time()
            else:
                break 
        
    def open_stream(self):
        p = pyaudio.PyAudio()
        return p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=3200
        )

    def toggle_pause(self):
        self.recording = False if self.recording else True
        if self.recording:
            self.pause['text'] = 'Pause'
            self.update_time()
        else:
            self.pause['text'] = 'Resume'

    def stop_recording(self):
        self.recording = False
        self.record['state'] = 'active'
        self.pause['state'] = 'disable'
        self.stop['state'] = 'disable'
        self.time_label.config(text="00:00:00")
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        self.save_audio()

    def save_audio(self):
        if self.frames:
            file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
            if file_path:
                try:
                    with wave.open(file_path, 'wb') as obj:
                        obj.setnchannels(1)
                        obj.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
                        obj.setframerate(16000)
                        obj.writeframes(b"".join(self.frames))
                except Exception as e:
                    tk.messagebox.showerror("Error", f"An error occurred while saving the audio: {str(e)}")
                finally:
                    self.frames.clear()


    def update_time(self):
        if self.recording:
            self.eslaped_time += 1
            hours, remainder = divmod(self.eslaped_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            text = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.time_label.config(text=text)
            self.time_label.after(1000, self.update_time)


def main():
    root = tk.Tk()
    app = SoundRecorder(root)
    root.mainloop()

if __name__ == "__main__":
    main()
