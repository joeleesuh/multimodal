# Demo Video Script Guide

Use this script to create your demo video showing the voice-enabled AI agent in action.

## 🎬 Video Requirements
- **Duration**: 3-5 minutes
- **Format**: MP4, 1080p recommended
- **Upload**: YouTube (unlisted)
- **Screen Recording**: Show terminal + audio waveform

## 📝 Recommended Script

### Introduction (30 seconds)
```
"Hi! Today I'm demonstrating a voice-enabled AI agent system that extends 
a CrewAI multi-agent research platform with speech-to-text and text-to-speech 
capabilities.

The system uses OpenAI Whisper for speech recognition and Kokoro TTS for 
generating natural voice responses. Let me show you how it works."
```

### Setup Display (20 seconds)
**Screen**: Show the project structure
```
"Here's the project structure. The main component is main_voice.py which 
integrates the voice interface with the existing CrewAI agent system."

[Show file tree]:
voice-ai-agent/
├── main_voice.py
├── requirements.txt
├── README.md
└── docs/
```

### Starting the Application (30 seconds)
**Screen**: Terminal showing startup
```
"Let's run the application."

[Terminal]:
$ python main_voice.py

"The system checks for required API keys and initializes the voice interface 
along with the Whisper speech recognition model."
```

### Voice Input Demo (60 seconds)
**Screen**: Terminal with audio input visualization (optional)
```
"I'll ask it to research AI ethics in autonomous vehicles using voice input."

[Press ENTER for voice mode]

🎤 When ready, speak your research topic...
[Press ENTER to start recording]

🎤 Listening... (speak now)

[Speak clearly]:
"What are the ethical implications of AI in autonomous vehicle decision-making?"

[System transcribes]:
📝 You said: What are the ethical implications of AI in autonomous vehicle 
decision-making?

"The transcription is accurate, so I'll confirm and continue."
[Type 'y' to confirm]
```

### Agent Processing (60 seconds)
**Screen**: Show agent work with verbose output
```
"Now the two agents begin their work. The Research Agent searches for 
information and synthesizes findings, while the Writing Agent transforms 
the research into an accessible article."

[Show scrolling output]:
[Research Agent]
> Entering: Ethics and Emerging Technology Research Lead
> Searching for: AI ethics autonomous vehicles
> Found 5 relevant sources...

[Writing Agent]
> Entering: Policy Communicator and Storyteller
> Structuring article...
> Writing introduction...

"This sequential process takes about 30 seconds as the agents collaborate 
to produce a comprehensive article."
```

### Article Output (30 seconds)
**Screen**: Show generated markdown file
```
"The system has generated a complete article saved as ai_voice_article.md"

[Open the file briefly to show]:
# AI in Autonomous Vehicle Decision-Making: Ethical Implications
...

"The article includes an introduction, benefits analysis, ethical 
considerations, real-world case studies, and actionable recommendations 
for stakeholders."
```

### Text-to-Speech Demo (45 seconds)
**Screen**: Terminal showing TTS prompt
```
"Finally, I can choose to hear the article spoken aloud using Kokoro TTS."

🔊 Would you like to hear the article? (y/n): y

🔊 Speaking: Artificial Intelligence in autonomous vehicles presents...

[Let audio play for 10-15 seconds]

"The text-to-speech uses a natural-sounding voice and properly pronounces 
technical terms like 'autonomous' and 'algorithmic bias'."
```

### Text Input Alternative (30 seconds)
**Screen**: Restart and show text mode
```
"The system also supports text input as an alternative to voice."

[Run again]:
$ python main_voice.py

Choice: text

📝 Enter research topic: Machine learning fairness in hiring

"This is useful in noisy environments or when precise input is needed."
```

### Technical Highlights (30 seconds)
**Screen**: Code snippets or architecture diagram
```
"Key technical features include:

1. Automatic silence detection - no manual stop button needed
2. Local Whisper processing for privacy
3. Kokoro TTS with natural voice synthesis
4. Full integration with existing CrewAI agents
5. Hybrid voice and text input modes"
```

### Conclusion (20 seconds)
```
"This voice-enabled AI agent demonstrates how speech interfaces can make 
multi-agent systems more accessible and natural to use.

The code, documentation, and setup instructions are available on GitHub. 
Thanks for watching!"

[Show GitHub repository URL on screen]
https://github.com/joeleesuh/multimodal
```

---

## 🎥 Recording Tips

### Tools
- **Screen Recording**: 
  - macOS: QuickTime Player, OBS Studio
  - Windows: OBS Studio, Xbox Game Bar
  - Linux: SimpleScreenRecorder, OBS Studio

- **Audio**: Use good microphone for voiceover

- **Editing**: 
  - Simple: iMovie (macOS), Windows Video Editor
  - Advanced: DaVinci Resolve (free), Adobe Premiere

### Best Practices

1. **Audio Quality**
   - Use a quiet environment
   - Test microphone levels first
   - Speak clearly and at moderate pace

2. **Screen Recording**
   - Use full screen or clean window
   - Increase terminal font size (18-20pt)
   - Hide sensitive information (.env files)

3. **Pacing**
   - Don't rush through demonstrations
   - Pause briefly between sections
   - Let key outputs stay visible for 2-3 seconds

4. **Visuals**
   - Show your face (optional but engaging)
   - Use cursor highlighting if available
   - Add text overlays for key points

5. **Post-Production**
   - Trim dead space and mistakes
   - Add simple transitions between sections
   - Include intro/outro cards with GitHub link

---

## 📋 Pre-Recording Checklist

- [ ] Test run application to ensure it works
- [ ] Clear terminal history
- [ ] Set terminal font size to 18-20pt
- [ ] Set terminal colors for good contrast
- [ ] Prepare .env file with valid API keys
- [ ] Test microphone audio levels
- [ ] Close unnecessary applications
- [ ] Disable notifications
- [ ] Have script/bullet points ready
- [ ] Practice run-through once

---

## 🎬 Post-Recording Steps

1. **Edit Video**
   - Trim mistakes and dead space
   - Add intro title card (3-5s)
   - Add outro with GitHub link (5s)
   - Export as MP4, 1080p

2. **Upload to YouTube**
   - Set visibility to "Unlisted"
   - Title: "Voice-Enabled AI Agent - Speech-to-Text Demo"
   - Description: Include GitHub link and brief explanation
   - Add tags: AI, voice interface, CrewAI, Whisper, TTS

3. **Update README**
   - Add YouTube link to README.md
   - Commit and push changes
   - Verify link works when clicked

4. **Test Share Link**
   - Copy unlisted link
   - Test in incognito/private browser
   - Confirm video plays without login

---

## 🎯 Key Points to Emphasize

✅ **Natural Voice Interaction**: No manual controls needed  
✅ **Privacy-Focused**: Whisper runs locally  
✅ **High Accuracy**: 95-98% transcription accuracy  
✅ **Quality TTS**: Natural-sounding voice synthesis  
✅ **Seamless Integration**: Works with existing agent system  
✅ **Flexible**: Voice or text input options  

---

## 📧 Example YouTube Description

```
Voice-Enabled AI Agent System Demonstration

This video demonstrates a multi-agent AI research system extended with 
voice capabilities using OpenAI Whisper (speech-to-text) and Kokoro TTS 
(text-to-speech).

Features:
• Automatic silence detection for natural conversations
• Local speech recognition with Whisper
• Natural voice synthesis with Kokoro TTS
• Multi-agent research and writing workflow
• Hybrid voice and text input modes

GitHub Repository:
https://github.com/joeleesuh/multimodal

Technical Stack:
- OpenAI Whisper (STT)
- Kokoro TTS
- CrewAI (agent framework)
- PyAudio (audio I/O)
- Python 3.8+

Documentation includes:
• Setup instructions
• Technical writeup
• Example runs
• Troubleshooting guide

#AI #VoiceInterface #MachineLearning #NLP #SpeechRecognition #TTS
```

---

Ready to record! 🎥
