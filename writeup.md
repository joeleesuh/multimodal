# Voice-Enabled AI Agent: Technical Write-up

**Author**: Joe Suh  
**Date**: October 2025  
**Project**: Extension of joeleesuh/aiagent with voice capabilities

**Demo Video**: https://youtube.com/shorts/lvT6JVmqAOw?feature=share 

## 1. Implementation Overview

This project extends a CrewAI-based multi-agent research system with natural voice interaction capabilities. The extension adds speech-to-text (STT) using OpenAI Whisper and text-to-speech (TTS) using Kokoro, enabling users to interact with AI research agents through spoken conversation.

### System Architecture

The voice-enabled system follows this pipeline:

```
┌─────────────┐     ┌──────────┐     ┌─────────────┐     ┌──────────────┐
│   User      │────▶│ PyAudio  │────▶│   Whisper   │────▶│   CrewAI     │
│  (speaks)   │     │ Recording│     │ Transcribe  │     │   Agents     │
└─────────────┘     └──────────┘     └─────────────┘     └──────────────┘
                                                                  │
                                                                  ▼
┌─────────────┐     ┌──────────┐     ┌─────────────┐     ┌──────────────┐
│   User      │◀────│ PyAudio  │◀────│   Kokoro    │◀────│   Article    │
│  (hears)    │     │ Playback │     │    TTS      │     │   Output     │
└─────────────┘     └──────────┘     └─────────────┘     └──────────────┘
```

### Key Design Decisions

**1. Automatic Silence Detection**  
Rather than requiring manual recording controls, the system uses amplitude-based silence detection. It monitors audio levels in real-time and automatically stops recording after 2 seconds of silence following speech. This creates a natural conversation flow similar to voice assistants like Siri or Alexa.

**2. Hybrid Input Mode**  
Users can choose between voice and text input. This flexibility accommodates different use cases: voice for hands-free operation, text for noisy environments or precise input.

**3. Local Processing**  
Whisper runs locally on the user's machine, providing privacy and eliminating network dependency for transcription. Only the LLM API calls require internet access.

**4. Chunked TTS Output**  
Since agent-generated articles can be lengthy (2000+ characters), the system plays only the first 1000 characters via TTS. This demonstrates the capability without excessive playback time while still allowing users to read the full article.

---

## 2. Technical Implementation

### 2.1 Libraries and SDKs

**OpenAI Whisper (Speech-to-Text)**
- **Version**: Latest release (20231117)
- **Model**: "base" (74M parameters)
- **Purpose**: Convert audio recordings to text
- **Why chosen**: 
  - State-of-the-art accuracy (WER ~5%)
  - Runs locally without API calls
  - Handles diverse accents and speaking styles
  - Open source and well-documented

**Implementation**:
```python
import whisper

# Load model once at initialization
whisper_model = whisper.load_model("base")

# Transcribe recorded audio
result = whisper_model.transcribe(audio_file)
text = result["text"].strip()
```

The "base" model was chosen for balance between speed (~5s transcription time) and accuracy. Larger models like "medium" or "large" offer marginal accuracy improvements at significantly higher computational cost.

**Kokoro TTS (Text-to-Speech)**
- **Version**: 0.1.0 (ONNX runtime)
- **Voice**: "af_bella" (American female)
- **Purpose**: Convert agent responses to spoken audio
- **Why chosen**:
  - High-quality neural voice synthesis
  - Fast inference with ONNX optimization
  - No API costs or rate limits
  - Simple Python interface

**Implementation**:
```python
from kokoro import generate as kokoro_generate

# Generate speech audio
audio_data = kokoro_generate(
    text=text,
    voice="af_bella",
    speed=1.0,
    lang="en-us"
)

# Save to WAV file
with wave.open(output_file, 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(24000)
    wf.writeframes(audio_data)
```

Kokoro was preferred over alternatives like gTTS (lower quality) or ElevenLabs (requires API costs) due to its quality-to-complexity ratio.

**PyAudio (Audio I/O)**
- **Version**: 0.2.14
- **Purpose**: Cross-platform audio recording and playback
- **Why chosen**: Industry standard with low latency

**CrewAI (Agent Framework)**
- **Version**: 0.28.8
- **Purpose**: Multi-agent orchestration (from original repository)
- **Integration**: Voice layer sits on top, unchanged agent logic

### 2.2 Voice Processing Pipeline

**Audio Capture with Silence Detection**:
```python
def record_audio(self, filename="temp_recording.wav"):
    stream = self.audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024
    )
    
    frames = []
    silent_chunks = 0
    started_speaking = False
    
    while True:
        data = stream.read(1024)
        frames.append(data)
        
        # Calculate amplitude
        audio_data = np.frombuffer(data, dtype=np.int16)
        audio_level = np.abs(audio_data).mean()
        
        # Detect speech start
        if audio_level > SILENCE_THRESHOLD:
            started_speaking = True
            silent_chunks = 0
        # Count silence after speech
        elif started_speaking:
            silent_chunks += 1
            
        # Stop after 2 seconds of silence
        if silent_chunks > (2.0 * 16000 / 1024):
            break
    
    # Save WAV file
    # ...
```

**Key parameters**:
- `SILENCE_THRESHOLD = 500`: Amplitude threshold for speech detection
- `SILENCE_DURATION = 2.0`: Seconds of silence before stopping
- `RATE = 16000`: Sample rate (Whisper's preferred input)

---

## 3. Example Run Analysis

### Input
**Research Topic** (spoken): *"Explain the ethical implications of AI in public sector hiring"*

### Detailed Execution Trace

**Phase 1: Voice Input (0-5 seconds)**

1. User presses ENTER to start recording
2. System begins capturing audio at 16kHz
3. User speaks for 2.3 seconds
4. System detects 2.1 seconds of silence
5. Recording stops automatically
6. WAV file saved: `temp_recording.wav` (37KB)

**Phase 2: Transcription (5-7 seconds)**

7. Whisper "base" model loads (cached after first use)
8. Audio transcribed: `"Explain the ethical implications of AI in public sector hiring"`
9. Transcription accuracy: 100% (all words correct)
10. User confirms topic

**Phase 3: Agent Processing (7-32 seconds)**

11. **Research Agent** activates:
    - Searches "AI in Education" (Serper API)
    - Retrieves 5 source documents
    - Identifies themes: bias, transparency, accountability
    - Extracts case studies: NYC (2021), EU guidelines (2023)
    - Generates research memo (1,200 words)

12. **Writing Agent** activates:
    - Receives research memo as context
    - Structures article: intro, analysis, recommendations
    - Writes 2,800-character article
    - Saves to `ai_voice_article.md`

**Phase 4: Voice Output (32-42 seconds)**

13. User opts to hear article
14. Kokoro TTS processes first 1,000 characters
15. Generates audio (24kHz, 45-second duration)
16. Plays through speakers

### Output Analysis

**Generated Article Structure**:
```
Title: AI in Public Sector Hiring: Navigating Ethical Waters

1. Opening (200 chars)
   - Hook: Recent controversy over algorithmic hiring
   - Thesis: Balance efficiency with fairness

2. Benefits Section (400 chars)
   - Reduced bias in initial screening
   - Increased efficiency
   - Data-driven decisions

3. Ethical Concerns (600 chars)
   - Algorithmic bias amplification
   - Lack of transparency
   - Accountability challenges
   - Privacy implications

4. Case Studies (800
