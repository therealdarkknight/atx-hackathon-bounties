import assemblyai as aai
from oursecrets import ASSEMBLY_API_KEY
import os

aai.settings.api_key = ASSEMBLY_API_KEY

global_transcript = ""
TRANSCRIPT_FILE = "transcript.txt"


def on_open(session_opened: aai.RealtimeSessionOpened):
  "This function is called when the connection has been established."

  print("Session ID:", session_opened.session_id)

def on_data(transcript: aai.RealtimeTranscript):
  global global_transcript

  if not transcript.text:
    return

  if isinstance(transcript, aai.RealtimeFinalTranscript):
    # print(transcript.text, end="\r\n")
    global_transcript += transcript.text

    with open(TRANSCRIPT_FILE, "a") as f:
        f.write(transcript.text + "\n")

  else:
    print(transcript.text, end="\r")

def on_error(error: aai.RealtimeError):
  "This function is called when the connection has been closed."

  print("An error occured:", error)

def on_close():
  "This function is called when the connection has been closed."

  print("Closing Session")


# Create the Real-Time transcriber
transcriber = aai.RealtimeTranscriber(
  on_data=on_data,
  on_error=on_error,
  sample_rate=44_100,
  on_open=on_open, # optional
  on_close=on_close, # optional
)


if __name__ == "__main__":
    if os.path.exists(TRANSCRIPT_FILE):
        os.remove(TRANSCRIPT_FILE)

    # Create a new blank transcript file
    with open(TRANSCRIPT_FILE, "w") as f:
        pass  # Just create an empty file

    # Start the connection
    transcriber.connect()

    # Open a microphone stream
    microphone_stream = aai.extras.MicrophoneStream()

    # Press CTRL+C to abort
    print("Running...")
    transcriber.stream(microphone_stream)

    transcriber.close()