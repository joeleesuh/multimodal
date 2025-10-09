# Quick Start Guide - Voice AI Agent

Get up and running in 5 minutes!

## 🎯 Goal
Run a voice-enabled AI agent that researches topics and generates articles using natural speech interaction.

## ⚡ 5-Minute Setup

### Step 1: Clone Repository (30 seconds)
```bash
git clone https://github.com/joeleesuh/multimodal.git
cd multimodal
```

### Step 2: Install Dependencies (2 minutes)

**macOS:**
```bash
brew install portaudio
pip install -r requirements.txt
```

**Ubuntu/Debian:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install -r requirements.txt
```

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
pip install -r requirements.txt
```

### Step 3: Configure API Key (30 seconds)
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your OpenAI API key
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

### Step 4: Run! (30 seconds)
```bash
python main_voice.py
```

## 🎤 First Use

1. **Choose input method**: Press ENTER for voice, or type "text"
2. **Speak your topic**: "What are the benefits of renewable energy?"
3. **Confirm**: Type 'y' when transcription is correct
4. **Wait**: Agents will research and write (~30 seconds)
5. **Listen**: Choose 'y' to hear the article via TTS

## 🔑 Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-`)
4. Add to `.env` file: `OPENAI_API_KEY=sk-...`

## 🎯 Example Topics to Try

- "AI ethics in healthcare"
- "Blockchain for supply chain"
- "Quantum computing applications"
- "Machine learning bias"
- "Cybersecurity in IoT"

## ⚠️ Troubleshooting

**"No module named 'whisper'"**
```bash
pip install openai-whisper
```

**"No default input device"**
- Check microphone is connected
- Grant microphone permissions
- Test: `python -c "import pyaudio; pyaudio.PyAudio()"`

**"OPENAI_API_KEY not set"**
```bash
export OPENAI_API_KEY="sk-your-key-here"
# Or add to .env file
```

**Recording too short**
- Speak louder or adjust `SILENCE_THRESHOLD` in code
- Increase `SILENCE_DURATION` for longer pauses

## 📖 Next Steps

- Read full documentation: `README.md`
- Review technical details: `docs/writeup.md`
- See example run: `examples/sample_run.md`
- Watch demo video: [YouTube link]

## 💡 Tips

- **Voice input**: Speak clearly at normal pace
- **Text input**: Use when in noisy environment
- **Silence detection**: System stops after 2 seconds of silence
- **TTS output**: Plays first 1000 characters to demo

## 🆘 Need Help?

- Check `README.md` for detailed docs
- See `PUSH_TO_GITHUB.md` for Git help
- Open issue: https://github.com/joeleesuh/multimodal/issues

---

**That's it! You're ready to go.** 🚀

Enjoy your voice-enabled AI agent!
