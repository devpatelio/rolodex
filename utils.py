
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import string
import pyttsx3 
import numpy as np
import random
import matplotlib.pyplot as plt
import json
import os
import face_recognition
from PIL import Image
from transformers import T5Tokenizer, T5ForConditionalGeneration
tokenizer = T5Tokenizer.from_pretrained('t5-small')
model = T5ForConditionalGeneration.from_pretrained('t5-small')


def generate_face_encodings(img_dir='directory/'):
    face_encodings = {}
    pth = img_dir+'images/'
    for img in os.listdir(pth):
        image = face_recognition.load_image_file(pth+img)
        face_encoding = face_recognition.face_encodings(image)[0]
        with open(f'{img_dir}/encodings/{img[:-4]}.npy', 'wb') as f:
            np.save(f, face_encoding)
        face_encodings[img[:-4]] = face_encoding
    return face_encodings

def recognize_face(img_pth, encoding_dir='directory/encodings/', image_dir='directory/images/'):
    face = face_recognition.load_image_file(img_pth)
    face_encoding = face_recognition.face_encodings(face)[0]
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))  # Create a subplot with 1 row and 2 columns
    input_img = Image.open(img_pth)
    axs[0].imshow(input_img)
    axs[0].set_title('Input Image')
    axs[0].axis('off')
    
    for encoding in os.listdir(encoding_dir):
        with open(os.path.join(encoding_dir, encoding), 'rb') as f:
            known_encoding = np.load(f)
            results = face_recognition.compare_faces([known_encoding], face_encoding)
            if results[0]:
                recognized_face_pth = os.path.join(image_dir, encoding.replace('.npy', '.jpg'))  # Assuming the image has a .jpg extension
                recognized_img = Image.open(recognized_face_pth)
                axs[1].imshow(recognized_img)
                axs[1].set_title(f"Recognized as {encoding[:-4]}")
                axs[1].axis('off')
                break
    plt.show()
    return True

recognize_face('faces/IMG_6481.jpg')

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