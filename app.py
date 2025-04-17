import os
from dotenv import load_dotenv
import assemblyai as aai
from elevenlabs import generate, stream, set_api_key
import openai

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys from environment variables
assemblyai_api_key = os.getenv("55e3f0abc33c40a7817d5ab6083a6ea3")
elevenlabs_api_key = os.getenv("sk_e690f306367cd87c570de760cbe7cfdb996cb997e3cfa352")
openai_api_key = os.getenv("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")

# Set API keys for respective services
aai.settings.api_key = assemblyai_api_key
set_api_key(elevenlabs_api_key)
openai.api_key = openai_api_key

class AI_Assistant:
    def __init__(self):
        self.transcriber = None
        self.full_transcript = [
            {"role": "system", "content": "You are a front desk assistant."}
        ]

    def start_transcription(self):
        self.transcriber = aai.RealtimeTranscriber(
            sample_rate=16000,
            on_data=self.on_data,
            on_error=self.on_error,
            on_open=self.on_open,
            on_close=self.on_close,
            end_utterance_silence_threshold=1000
        )

        self.transcriber.connect()
        microphone_stream = aai.extras.MicrophoneStream(sample_rate=16000)
        self.transcriber.stream(microphone_stream)

    def stop_transcription(self):
        if self.transcriber:
            self.transcriber.close()
            self.transcriber = None

    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        # Session opened
        pass

    def on_data(self, transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return
        if isinstance(transcript, aai.RealtimeFinalTranscript):
            print(f"\nPatient: {transcript.text}")
            self.generate_ai_response(transcript.text)
        else:
            print(transcript.text, end="\r")

    def on_error(self, error: aai.RealtimeError):
        # Handle error
        print(f"An error occurred: {error}")

    def on_close(self):
        # Session closed
        pass

    def generate_ai_response(self, user_input):
        self.stop_transcription()
        self.full_transcript.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.full_transcript
        )
        ai_response = response.choices[0].message['content']
        self.generate_audio(ai_response)
        self.start_transcription()

    def generate_audio(self, text):
        self.full_transcript.append({"role": "assistant", "content": text})
        print(f"\nAI Receptionist: {text}")

        audio_stream = generate(
            text=text,
            voice="Rachel",
            stream=True
        )
        stream(audio_stream)

# Initialize and start the AI assistant
if __name__ == "__main__":
    greeting = "Thank you for calling Inpower. My name is Meeka, how may I help you?"
    ai_assistant = AI_Assistant()
    ai_assistant.generate_audio(greeting)
    ai_assistant.start_transcription()

