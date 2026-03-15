import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
import scipy.io.wavfile as wav
from google import genai

samplerate = 16000
record_seconds = 30
filename = "doctor_patient_conversation.wav"

print("Recording conversation...")

audio = sd.rec(
    int(record_seconds * samplerate),
    samplerate=samplerate,
    channels=1,
    dtype="int16"
)

sd.wait()

# This overwrites the file every time
wav.write(filename, samplerate, audio)

print("Recording saved and overwritten:", filename)

client = genai.Client(api_key="AIzaSyCPPC3h5Ujh6AFD6Flc4oN-SvVZwBWuEk0")

audio_file = client.files.upload(
    file="doctor_patient_conversation.wav"
)

prompt = """
Analyze this doctor–patient conversation audio.

Tasks:
1. Transcribe the conversation.
2. Identify medicines prescribed by the doctor.
3. Extract dosage, frequency, and duration.

Return the output in plain text format like this:

Patient Condition:
...

Medicines Prescribed:
1. Medicine - dosage - frequency - duration
2. Medicine - dosage - frequency - duration

Doctor Advice:
...
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        prompt,
        audio_file
    ]
)

# Print response
print(response.text)

# Save response to text file
with open("sri/consulting_summary.txt", "w", encoding="utf-8") as f:
    f.write(response.text)

print("Response saved to analysis_result.txt")