import pyaudio
import wave
import whisper
import time
import os

# Audio recording parameters
CHUNK = 1024        # Number of frames per buffer
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 16000        # Whisper recommends 16kHz or 44100Hz
RECORD_SECONDS = 5  # How many seconds you want to record

def record_audio(filename="temp_audio.wav"):
    """
    Record audio from the microphone for RECORD_SECONDS
    and save it to a temporary WAV file.
    """
    p = pyaudio.PyAudio()

    # Open a new stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Recording...")
    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Write recorded data to a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe_audio(filename="temp_audio.wav", model_size="base"):
    """
    Load a Whisper model and transcribe the given audio file.
    """
    print("Loading model...")
    model = whisper.load_model(model_size)

    print("Transcribing audio...")
    result = model.transcribe(filename)
    return result["text"]

def main():
    # 1. Record audio from microphone
    temp_file = "temp_audio.wav"
    record_audio(filename=temp_file)

    # 2. Transcribe the recorded audio
    transcription = transcribe_audio(filename=temp_file, model_size="base")

    # 3. Print out the transcription
    print("Transcription:")
    print(transcription)

    # (Optional) Remove the temporary file
    if os.path.exists(temp_file):
        os.remove(temp_file)

if __name__ == "__main__":
    main()
