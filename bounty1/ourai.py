
from openai import OpenAI
from oursecrets import OPENAI_API_KEY
import time
import json
import random
import pygame

client = OpenAI(api_key=OPENAI_API_KEY)


def oai_analyze_transcript(transcript):

    schema = {
        "type": "object",
        "properties": {
            "conclusion": {
                "type": ["string"],
                "description": "The conclusion you have reached upon analyzing the transcript",
                "enum": ["BORDER_INSPECTION", "NOTHING_NOTABLE"]
            }
        },
        "required": ["conclusion"],
        "additionalProperties": False
    }

    system_prompt = f"""
    You are an expert in analyzing the transcript of all audio that is recorded in a truck driver's seat. You will be given an unlabeled transcript of this type.
    Output a JSON object with a field "conclusion" that is your conclusion upon analyzing the transcript of the conversation.
    This field should be "BORDER_INSPECTION" if you conclude that a border inspection is currently going on, based on whether the transcript would reasonably appear in (and only appear in) a conversation between a customs agent at the border and a truck driver.
    This field should be "NOTHING_NOTABLE" if none of the above described situations are occurring.
    """

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "developer", "content": f"{system_prompt}"},
            {"role": "user", "content": f"{transcript}"}
        ],
        response_format={ "type": "json_schema", "json_schema": { "name": "transcript_response", "strict": True, "schema": schema} }
    )

    ret = completion.choices[0].message.content
    ret_dict = json.loads(ret)
    
    conclusion = ret_dict.get('conclusion', 'NOTHING_NOTABLE')
    return conclusion



def agent_loop():
    INSPECTION_DONE = False

    while True:
        with open("transcript.txt", "r", encoding="utf-8") as file:
            transcript = file.read()

            conclusion = oai_analyze_transcript(transcript)
            
            print(f"<SensorData>\n\t<Speed>{round(random.uniform(45, 65), 1)}</Speed>\n</SensorData>")
            print(f"<Conclusion>\n\t{conclusion}\n</Conclusion>\n\n")

            if conclusion == "BORDER_INSPECTION" and not INSPECTION_DONE:
            # if conclusion == "NOTHING_NOTABLE" and not INSPECTION_DONE:
                INSPECTION_DONE = True
                pygame.mixer.init()
                pygame.mixer.music.load("voice1.mp3")
                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)  # Check every 100ms
                
                # Sleep for 10 seconds before playing the next file
                time.sleep(7)
                
                # Play second file
                pygame.mixer.music.load("voice2.mp3")
                pygame.mixer.music.play()


            time.sleep(10)


if __name__ == "__main__":
    agent_loop()
    # test_transcript = f"""Good morning. Papers, please. Morning. Here you go—manifest, passport, and truck registration. Thanks. Where are you coming from today? Left Laredo early this morning. Headed up to Dallas. And what are you hauling? Auto parts, mostly engine components. Got everything listed on the manifest. Any hazardous materials, alcohol, or tobacco? No, just the parts. Been on this route before? Yeah, I make this run a couple times a month. Everything's usually in order. Mind if I take a look inside? Sure, go ahead. Just pop the back for me. Alright, give me a sec. Here you go. Looks good. Any stops after this or straight through to Dallas? Just a quick fuel stop, then straight through. Alright, you’re all set. Safe travels. Appreciate it. Have a good one."""
    # ret = oai_analyze_transcript(test_transcript)

    # print(ret)