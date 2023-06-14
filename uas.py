import tkinter as tk
from tkinter import filedialog
import os
import wave
import cv2
from pydub import AudioSegment

def extract_audio_from_video(video_path, audio_path):
    command = f'ffmpeg -i "{video_path}" -vn -acodec pcm_s16le -ar 44100 -ac 2 "{audio_path}"'
    os.system(command)

def remove_audio_from_video(video_path, video_path_without_audio):
    command = f'ffmpeg -i "{video_path}" -c copy -an "{video_path_without_audio}"'
    os.system(command)

def accelerate_audio(audio_path, accelerated_audio_path, acceleration_factor):
    audio = AudioSegment.from_file(audio_path)
    accelerated_audio = audio.speedup(playback_speed=acceleration_factor)
    accelerated_audio.export(accelerated_audio_path, format='wav')

def accelerate_video(video_path, accelerated_video_path, acceleration_factor):
    video = cv2.VideoCapture(video_path)

    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    new_fps = fps * acceleration_factor

    output = cv2.VideoWriter(accelerated_video_path, cv2.VideoWriter_fourcc(*'mp4v'), new_fps, (width, height))

    while True:
        ret, frame = video.read()

        if not ret:
            break

        output.write(frame)

    video.release()
    output.release()

def merge_video_with_audio(video_path, audio_path, final_video_path):
    command = f'ffmpeg -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac -strict experimental "{final_video_path}"'
    os.system(command)


root = tk.Tk()


def button_click():
  
    video_path = filedialog.askopenfilename(title="Pilih Video", filetypes=(("Video files", "*.mp4"), ("All files", "*.*")))

    if video_path:
       
        save_dir = filedialog.askdirectory(title="Pilih Direktori Penyimpanan")

        if save_dir:
            
            audio_path = os.path.join(save_dir, "audio.wav")
            video_path_without_audio = os.path.join(save_dir, "video_without_audio.mp4")
            extract_audio_from_video(video_path, audio_path)
            remove_audio_from_video(video_path, video_path_without_audio)

           
            acceleration_factor = 1.5
            accelerated_audio_path = os.path.join(save_dir, "accelerated_audio.wav")
            accelerate_audio(audio_path, accelerated_audio_path, acceleration_factor)

         
            accelerated_video_path = os.path.join(save_dir, "accelerated_video.mp4")
            accelerate_video(video_path_without_audio, accelerated_video_path, acceleration_factor)

       
            final_video_path = os.path.join(save_dir, "final_video.mp4")
            merge_video_with_audio(accelerated_video_path, accelerated_audio_path, final_video_path)

            print("Penggabungan audio dan video selesai.")
            print(f"Hasil disimpan di: {final_video_path}")


button = tk.Button(root, text="Percepat  Video", command=button_click)
button.pack(pady=20)


root.mainloop()
