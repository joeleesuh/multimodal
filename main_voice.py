"""
Voice-enabled AI Agent Extension
Adds speech-to-text and text-to-speech capabilities to the CrewAI agent system
"""

import os
import sys
import time
import wave
import pyaudio
import whisper
import numpy as np
from pathlib import Path
from crewai import Agent, Task, Crew, Process
from crewai.tools import SerperDevTool, FileWriterTool
from kokoro import generate as kokoro_generate

# === Voice Configuration ===
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
SILENCE_THRESHOLD = 500
SILENCE_DURATION = 2.0

class VoiceInterface:
    """Handles all voice input/output operations"""
    
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.whisper_model = whisper.load_model("base")
        self.recording = False
        
    def record_audio(self, filename="temp_recording.wav"):
        """Record audio from microphone until silence detected"""
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
        
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
            
            # Calculate audio level
            audio_data = np.frombuffer(data, dtype=np.int16)
            audio_level = np.abs(audio_data).mean()
            
            if audio_level > SILENCE_THRESHOLD:
                started_speaking = True
                silent_chunks = 0
            elif started_speaking:
                silent_chunks += 1
                
            # Stop after silence duration
            if silent_chunks > (SILENCE_DURATION * RATE / CHUNK):
                break
                
        print("✓ Recording complete")
        stream.stop_stream()
        stream.close()
        
        # Save recording
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(AUDIO_FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        return filename
    
    def transcribe_audio(self, audio_file):
        """Convert speech to text using Whisper"""
        print("🔄 Transcribing audio...")
        result = self.whisper_model.transcribe(audio_file)
        transcription = result["text"].strip()
        print(f"📝 You said: {transcription}")
        return transcription
    
    def speak_text(self, text, output_file="response.wav"):
        """Convert text to speech using Kokoro TTS"""
        print(f"\n🔊 Speaking: {text[:100]}...")
        
        try:
            # Generate speech with Kokoro
            audio_data = kokoro_generate(
                text=text,
                voice="af_bella",  # Female voice
                speed=1.0,
                lang="en-us"
            )
            
            # Save and play audio
            with wave.open(output_file, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(24000)
                wf.writeframes(audio_data)
            
            self._play_audio(output_file)
            
        except Exception as e:
            print(f"⚠️  TTS Error: {e}")
            print(f"📄 Text response: {text}")
    
    def _play_audio(self, filename):
        """Play audio file through speakers"""
        wf = wave.open(filename, 'rb')
        stream = self.audio.open(
            format=self.audio.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )
        
        data = wf.readframes(CHUNK)
        while data:
            stream.write(data)
            data = wf.readframes(CHUNK)
            
        stream.stop_stream()
        stream.close()
        wf.close()
    
    def cleanup(self):
        """Release audio resources"""
        self.audio.terminate()


def create_agents():
    """Initialize AI agents with persona context"""
    
    persona_context = """
    You are an expert who has:
    - Facilitated Stanford's Ethics, Technology, and Public Policy program
    - Worked as a U.S. Patent Examiner and GAO technology auditor
    - Led digital initiatives at the White House, OMB, and federal agencies
    - Guided human-centered design at IDEO
    - Supported civic innovation programs like U.S. Digital Corps
    """
    
    # Configure tools
    tools = []
    if os.getenv("SERPER_API_KEY"):
        tools.append(SerperDevTool())
    
    # Research Agent
    researcher = Agent(
        role="Ethics and Emerging Technology Research Lead",
        goal="Synthesize insights on AI governance, civic tech, and public interest innovation",
        backstory=persona_context + """
        Your expertise spans patent examination, congressional testimonies, 
        and Federal policy recommendations. You map ethical considerations 
        and frame opportunities for inclusive innovation.
        """,
        tools=tools,
        verbose=True
    )
    
    # Writer Agent
    writer = Agent(
        role="Policy Communicator and Storyteller",
        goal="Transform research into accessible narratives with actionable recommendations",
        backstory=persona_context + """
        You craft compelling narratives for diverse audiences including 
        technologists, policymakers, and community partners. Your writing 
        bridges complex concepts with practical next steps.
        """,
        tools=[FileWriterTool()],
        verbose=True
    )
    
    return researcher, writer


def create_tasks(researcher, writer, topic):
    """Define agent tasks"""
    
    research_task = Task(
        description=f"""
        Research the following topic: {topic}
        
        Provide:
        1. Key benefits and opportunities
        2. Ethical considerations and risks
        3. Governance approaches
        4. Real-world case studies
        5. Recommendations for stakeholders
        """,
        agent=researcher,
        expected_output="Comprehensive research memo with structured findings"
    )
    
    writing_task = Task(
        description="""
        Transform the research findings into an engaging article that:
        1. Opens with the key insight
        2. Explains concepts accessibly
        3. Provides concrete examples
        4. Offers actionable next steps
        5. Speaks to technologists, policymakers, and community leaders
        
        Write in a conversational yet authoritative tone.
        """,
        agent=writer,
        expected_output="Polished article saved as ai_voice_article.md",
        output_file="ai_voice_article.md"
    )
    
    return [research_task, writing_task]


def main():
    """Main execution flow with voice interface"""
    
    print("=" * 60)
    print("🎙️  VOICE-ENABLED AI AGENT SYSTEM")
    print("=" * 60)
    
    # Check API keys
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  Warning: OPENAI_API_KEY not set")
        print("Set it with: export OPENAI_API_KEY='your-key'")
        return
    
    # Initialize voice interface
    voice = VoiceInterface()
    
    try:
        # Get topic via voice or text
        print("\n📋 How would you like to provide the research topic?")
        print("1. Voice input (press ENTER)")
        print("2. Text input (type 'text')")
        
        choice = input("\nChoice: ").strip().lower()
        
        if choice == 'text':
            topic = input("\n📝 Enter research topic: ")
        else:
            print("\n🎤 When ready, speak your research topic...")
            input("Press ENTER to start recording...")
            
            audio_file = voice.record_audio()
            topic = voice.transcribe_audio(audio_file)
            
            # Confirm topic
            print(f"\n✓ Research topic: {topic}")
            confirm = input("Continue with this topic? (y/n): ")
            if confirm.lower() != 'y':
                topic = input("Enter topic manually: ")
        
        # Create and run agent crew
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
        print("✅ PROCESS COMPLETE")
        print("=" * 60)
        
        # Read and speak the article
        output_file = "ai_voice_article.md"
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                article = f.read()
            
            print(f"\n📄 Article saved to: {output_file}")
            print(f"📊 Length: {len(article)} characters")
            
            # Option to hear the article
            hear = input("\n🔊 Would you like to hear the article? (y/n): ")
            if hear.lower() == 'y':
                # Extract first few paragraphs for TTS (full article may be too long)
                summary = article[:1000] + "..."
                voice.speak_text(summary)
        else:
            print(f"\n⚠️  Article file not found: {output_file}")
        
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
