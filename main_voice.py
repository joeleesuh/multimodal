import os
import wave
import pyaudio
import whisper
import numpy as np
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

load_dotenv()

AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
SILENCE_THRESHOLD = 500
SILENCE_DURATION = 2.0

class VoiceInterface:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        print("Loading Whisper model...")
        self.whisper_model = whisper.load_model("base")
        
    def record_audio(self, filename="temp_recording.wav"):
        print("\n🎤 Listening... (speak now)")
        
        stream = self.audio.open(
            format=AUDIO_FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        frames = []
        silent_chunks = 0
        started_speaking = False
        
        try:
            while True:
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
                
                audio_data = np.frombuffer(data, dtype=np.int16)
                audio_level = np.abs(audio_data).mean()
                
                if audio_level > SILENCE_THRESHOLD:
                    started_speaking = True
                    silent_chunks = 0
                elif started_speaking:
                    silent_chunks += 1
                    
                if silent_chunks > (SILENCE_DURATION * RATE / CHUNK):
                    break
                    
        except KeyboardInterrupt:
            print("\nRecording stopped")
        finally:
            print("✓ Recording complete")
            stream.stop_stream()
            stream.close()
        
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(AUDIO_FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        return filename
        
    def transcribe_audio(self, audio_file):
        print("🔄 Transcribing audio...")
        
        with wave.open(audio_file, 'rb') as wf:
            audio_data = wf.readframes(wf.getnframes())
            audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
        
        result = self.whisper_model.transcribe(audio_array)
        transcription = result["text"].strip()
        print(f"📝 You said: {transcription}")
        return transcription
    
    def speak_text(self, text):
        print(f"\n📄 Article Preview:")
        print("=" * 60)
        preview = text[:500] + "..." if len(text) > 500 else text
        print(preview)
        print("=" * 60)
        
        try:
            import pyttsx3
            engine = pyttsx3.init()
            
            # Adjust speech rate (default is 200)
            engine.setProperty('rate', 180)  # Slightly slower for clarity
            
            # Read first 1000 characters (about 1-2 minutes of speech)
            speech_text = text[:1000] if len(text) > 1000 else text
            
            print(f"\n🔊 Speaking article (first 1000 characters)...")
            print("Please wait, this will take about 1-2 minutes...")
            
            engine.say(speech_text)
            engine.runAndWait()
            
            print("\n✅ TTS complete!")
            
        except Exception as e:
            print(f"⚠️  TTS error: {e}")
            print("Full text is displayed above and saved to file")
    
    def cleanup(self):
        self.audio.terminate()


def create_agents():
    persona = "You are an expert researcher and writer with experience in technology and policy"
    
    researcher = Agent(
        role="Research Lead",
        goal="Research and synthesize insights on the given topic",
        backstory=persona,
        tools=[],
        verbose=True
    )
    
    writer = Agent(
        role="Writer",
        goal="Write clear, well-structured articles",
        backstory=persona,
        tools=[],
        verbose=True
    )
    
    return researcher, writer


def create_tasks(researcher, writer, topic):
    research_task = Task(
        description=f"Research the topic: {topic}. Provide key insights, benefits, risks, case studies, and recommendations.",
        agent=researcher,
        expected_output="Comprehensive research findings"
    )
    
    writing_task = Task(
        description="Write a clear, well-structured article based on the research. Include an introduction, key sections with headers, and a conclusion.",
        agent=writer,
        expected_output="Professional article",
        output_file="ai_voice_article.md"
    )
    
    return [research_task, writing_task]


def main():
    print("=" * 60)
    print("🎙️  VOICE-ENABLED AI AGENT SYSTEM")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  Error: OPENAI_API_KEY not set")
        print("Please add it to your .env file")
        return
    
    voice = VoiceInterface()
    
    try:
        print("\n📋 How would you like to provide the research topic?")
        print("1. Voice input (press ENTER)")
        print("2. Text input (type 'text')")
        
        choice = input("\nChoice: ").strip().lower()
        
        if choice == 'text':
            topic = input("\n📝 Enter research topic: ").strip()
        else:
            print("\n🎤 When ready, speak your research topic...")
            input("Press ENTER to start recording...")
            
            audio_file = voice.record_audio()
            topic = voice.transcribe_audio(audio_file)
            
            print(f"\n✓ Research topic: {topic}")
            # Auto-continue with voice input, no confirmation needed
        
        if not topic:
            print("No topic provided. Exiting.")
            return
        
        print(f"\n✓ Topic: {topic}")
        print("\n🤖 Initializing AI agents...")
        
        researcher, writer = create_agents()
        tasks = create_tasks(researcher, writer, topic)
        
        crew = Crew(
            agents=[researcher, writer],
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        print("\n🚀 Starting research and writing process...")
        print("=" * 60)
        
        result = crew.kickoff()
        
        print("\n" + "=" * 60)
        print("✅ PROCESS COMPLETE!")
        print("=" * 60)
        
        if os.path.exists("ai_voice_article.md"):
            with open("ai_voice_article.md", 'r', encoding='utf-8') as f:
                article = f.read()
            
            print(f"\n📄 Article saved: ai_voice_article.md")
            print(f"📊 Length: {len(article)} characters")
            
            hear = input("\n🔊 Would you like to hear the article? (y/n): ")
            if hear.lower() == 'y':
                voice.speak_text(article)
            else:
                print("\n📖 You can read the full article in ai_voice_article.md")
        
        print("\n🎉 Session complete!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        voice.cleanup()


if __name__ == "__main__":
    main()
