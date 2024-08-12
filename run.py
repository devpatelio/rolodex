import asyncio
import frame_sdk
import random
import string
from db import *

from frameutils import *
from frame_sdk import Frame
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import pyttsx3 
from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained('t5-small')
model = T5ForConditionalGeneration.from_pretrained('t5-small')


PHOTO_PATH = "photo.jpg"

history = []

print(sd.query_devices()[0])

def generate_id(length=6):
    characters = string.ascii_letters + string.digits
    random_id = ''.join(random.choice(characters) for _ in range(length))
    return random_id

def record_audio(filename, duration=9, samplerate=44100, pth=""):
    print(f"Recording for {duration} seconds...")
    myrecording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float64')
    sd.wait() 
    print("Recording complete. Saving file...")
    sf.write(pth+filename, myrecording, samplerate)
    print(f"File saved as {pth+filename}")

def speak_text(command):
    engine = pyttsx3.init()
    engine.say(command) 
    engine.runAndWait()

def append_log_id(data_file, person_id, log_id):
    with open(data_file, 'r') as file:
        data = json.load(file)

    for entry in data:
        if entry['id'] == person_id:
            entry['log_ids'].append(log_id)
            break

    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)

def get_data_by_id(data_file, person_id):
    with open(data_file, 'r') as file:
        data = json.load(file)
    
    for entry in data:
        if entry['id'] == person_id:
            return entry
    return None

# Function to add a new log entry to logs/logs.json
def create_log_file(log_id, transcript_text):
    log_file = f"logs/{log_id}.json"
    log_entry = {
        "log_id": log_id,
        "transcript": transcript_text
    }
    
    with open(log_file, 'w') as file:
        json.dump(log_entry, file, indent=4)


def generate_text(input_text):
    prompt = f"""
                    correct, format, and ensure proper grammar and punctuation:
                    {input_text}
                    """

    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output_ids = model.generate(input_ids, max_length=512, num_beams=4, early_stopping=True)
    formatted_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    
    return formatted_text
 ### HERE ## 



async def main():
    intro_rolodex = "Welcome to the Rolodex!\nA new device for patients with dementia to remember the most important parts of their lives.\nThis device is designed to help patients remember their loved ones, their favorite memories, and their daily routines.\nThe Rolodex is a simple, easy-to-use device that can be customized to fit the needs of each patient."
    r = sr.Recognizer() 

    async with Frame() as f:
        log_id = generate_id()

        print(f'connected: {await f.get_battery_level()}')
        await f.run_lua("print('hello world')", await_print=True, timeout=5)
        # photo_bytes = await f.camera.take_photo(autofocus_seconds=5)
        # await f.display.show_text("Photo taken!", align=frame_sdk.display.Alignment.MIDDLE_CENTER)
        # f.camera.save_photo(photo_bytes, f"faces/{unique_id}.jpg")
        # await f.display.show_text("Photo saved!", align=frame_sdk.display.Alignment.MIDDLE_CENTER)

        # history.append(rolodex.append_data(unique_id, f"faces/{unique_id}.jpg", "Richa", "Wife", "Richa is my wife. She is very kind and caring.", log=None))
        # await f.display.show_text("Database updated!", align=frame_sdk.display.Alignment.MIDDLE_CENTER)
        await f.display.show_text("Tap to begin conversation...", align=frame_sdk.display.Alignment.MIDDLE_CENTER)
        await f.motion.wait_for_tap()
        await f.display.show_text("Capturing photo...", align=frame_sdk.display.Alignment.MIDDLE_CENTER)
        await f.camera.save_photo(f"faces/{log_id}.jpg")
        # await f.display.show_text("Photo saved!", align=frame_sdk.display.Alignment.MIDDLE_CENTER)
        ## ON TAP START RECORING
        duration = 29
        audio_file_path = "intermediate_audio.wav"
        await f.delay(seconds = 2)
        await f.display.show_text("Recording conversation...", align=frame_sdk.display.Alignment.MIDDLE_CENTER)
        await f.delay(seconds = 2)
        try:
            length = await f.microphone.save_audio_file(audio_file_path, max_length_in_seconds=duration+3)
            print(length)
        except:
            record_audio(audio_file_path, duration=duration)
        
        transcript = ""
        with sr.AudioFile(audio_file_path) as source:
            try:
                audio = r.record(source)
                tts = r.recognize_google(audio)

                history.append(tts)
                print("Text: " + tts)
                transcript = tts

            except Exception as e:
                print("Exception: " + str(e))

        ### RUN THE FACE FILTERING HERE AND GET THE CORRECT USER ID ON THE DATABASE ###
        
        await f.display.show_text("Conversation stored! Tap to Stop.", align=frame_sdk.display.Alignment.MIDDLE_CENTER)
        await f.display.show()
        await f.motion.wait_for_tap()
        await f.display.show_text("Exporting conversation...", align=frame_sdk.display.Alignment.MIDDLE_CENTER)

        id = 'wRMO80ACbQ'
        formatted_log = generate_text(transcript)
        print(formatted_log)
        await f.delay(seconds = 2)

        data_file = "faces/data.json"
        person_id = "wRMO80ACbQ"
        append_log_id(data_file, person_id, log_id)

        create_log_file(log_id, formatted_log)

        person_data = get_data_by_id(data_file, person_id)
        await f.display.show_text(f"{person_data['name']}\n{person_data['memory']}", align=frame_sdk.display.Alignment.MIDDLE_CENTER)
        await f.motion.wait_for_tap()
        
    print('disconnected')

asyncio.run(main())

