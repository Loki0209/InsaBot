# Automated AI News Reel Bot

An automated system that creates 9:16 vertical videos for Instagram based on trending Tech News.

## 🎯 Architecture

1. **Data Source**: NewsAPI - fetching trending tech news
2. **Scripting**: Google Gemini 2.5-Flash (FREE!) - generates viral scripts and visual prompts
3. **Audio**: EdgeTTS (FREE!) - Microsoft Edge Text-to-Speech with realistic voices
4. **Images**: Gradient Generator (with optional Pexels integration) - creates background images
5. **Editing**: MoviePy - stitches images and audio with **Ken Burns Effect** (cinematic zoom/pan animations)

## 📁 Project Structure

```
InstaBot/
├── src/
│   ├── fetcher.py          # NewsAPI integration
│   ├── scripter.py         # Gemini AI script generation
│   ├── generator.py        # Audio (EdgeTTS) + Images (Gradients/Pexels)
│   └── editor.py           # Video assembly (MoviePy)
├── data/
│   ├── temp/               # Temporary files (audio, images)
│   └── output/             # Final video outputs
├── main.py                 # Main pipeline orchestration
├── requirements.txt        # Python dependencies (pinned versions)
├── requirements-dev.txt    # Development dependencies
├── .env.example           # Environment variables template
├── .env                   # Your actual credentials (not committed)
└── README.md              # This file
```

## 🚀 Setup Instructions

### 1. Clone or navigate to the project directory

```bash
cd InstaBot
```

### 2. Create virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env`:
```bash
cp .env.example .env  # Linux/Mac
copy .env.example .env  # Windows
```

Fill in your API credentials in `.env`:

#### Required APIs:

**NewsAPI (100 requests/day - FREE)**
- Sign up: https://newsapi.org/register
- Get API key from dashboard
- Add to `.env`: `NEWSAPI_KEY=your_key_here`

**Google Gemini API (FREE with rate limits)**
- Get key: https://aistudio.google.com/app/apikey
- Add to `.env`: `GEMINI_API_KEY=your_key_here`
- **Rate Limits:** ~15 requests/minute, unlimited daily

**EdgeTTS Voice (OPTIONAL - Completely FREE!)**
- No API key needed! Uses Microsoft Edge Text-to-Speech
- No character limits, no monthly caps
- Very realistic neural voices
- Add to `.env` (optional):
  ```
  EDGE_TTS_VOICE=en-US-AriaNeural
  ```
- **Popular voices:**
  - `en-US-AriaNeural` - Female, American (default)
  - `en-US-GuyNeural` - Male, American
  - `en-US-JennyNeural` - Female, Assistant-style
  - `en-US-EricNeural` - Male, News-style
  - `en-GB-SoniaNeural` - Female, British
  - `en-GB-RyanNeural` - Male, British
- List all voices: `edge-tts --list-voices`

#### Optional APIs:

**Pexels API (Free stock photos)**
- Sign up: https://www.pexels.com/api/
- Add to `.env`: `PEXELS_API_KEY=your_key_here`
- If not set, gradient placeholders will be used

### 5. Run the bot

```bash
python main.py
```

## 💰 Cost Breakdown

| Service | Free Tier | Cost per Video | Notes |
|---------|-----------|----------------|-------|
| **NewsAPI** | 100 requests/day | $0.00 | Plenty for daily use |
| **Gemini API** | 15 RPM, unlimited daily | $0.00 | FREE forever! |
| **EdgeTTS** | UNLIMITED | $0.00 | No limits, completely free! |
| **Images** | Unlimited gradients | $0.00 | Or use free Pexels |
| **TOTAL** | - | **$0.00** | 🎉 Completely FREE! |

### Scaling (Optional)

- **NewsAPI Developer:** $449/month for 250,000 requests (only if creating hundreds of videos daily)

## ⚠️ API Rate Limits & Warnings

### Gemini API
- **Limit:** ~15 requests per minute
- **Impact:** Wait 60 seconds between video generations
- **Workaround:** Run bot once per minute max

### NewsAPI
- **Limit:** 100 requests per day
- **Impact:** Can create max 100 videos/day
- **Workaround:** Upgrade to paid plan if needed

### EdgeTTS
- **Limit:** NONE! Completely unlimited
- **Impact:** Generate unlimited videos with no monthly caps
- **Cost:** $0.00 - Forever free!

## 📝 Output

Videos are generated in **1080×1920 (9:16) format**, optimized for:
- ✅ Instagram Reels
- ✅ Instagram Stories
- ✅ TikTok
- ✅ YouTube Shorts

**File naming:** `news_reel_YYYYMMDD_HHMMSS.mp4`

**Example:** `news_reel_20251218_143522.mp4`

## 🎬 Ken Burns Effect (Cinematic Animations)

Your videos feature the **Ken Burns Effect** - professional cinematic animations that bring static images to life!

### What is Ken Burns Effect?
Named after documentary filmmaker Ken Burns, this technique creates slow, smooth zoom and pan movements on still images, making them feel dynamic and engaging.

### 8 Animation Patterns
Each scene automatically gets a different animation:

1. **Zoom In** - Classic slow zoom toward the subject
2. **Zoom Out** - Reveals more of the scene progressively
3. **Pan Right + Zoom** - Moves right while zooming in
4. **Pan Left + Zoom** - Moves left while zooming in
5. **Pan Up + Zoom** - Moves up while zooming in
6. **Pan Down + Zoom** - Moves down while zooming in
7. **Diagonal TL + Zoom** - Top-left diagonal movement with zoom
8. **Diagonal BR + Zoom** - Bottom-right diagonal movement with zoom

### Additional Effects
- **Smooth Easing** - Natural acceleration/deceleration (not linear)
- **Fade In/Out** - Smooth transitions between scenes
- **Text Overlays** - Animated captions with stroke
- **30 FPS** - High frame rate for buttery smooth animations

**Result:** Professional, broadcast-quality videos that grab attention! 🎥✨

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'moviepy'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "GEMINI_API_KEY not found"

**Solution:**
1. Check `.env` file exists
2. Verify `GEMINI_API_KEY=your_actual_key`
3. No spaces around `=`

### Issue: "429 Quota exceeded" (Gemini)

**Solution:**
- Wait 60 seconds between runs
- Or get a new API key: https://aistudio.google.com/app/apikey

### Issue: EdgeTTS audio not generating

**Solution:**
- Ensure `edge-tts` is installed: `pip install edge-tts`
- Check voice name is correct: `edge-tts --list-voices`
- Try default voice: `en-US-AriaNeural`

### Issue: "No images found"

**Solution:**
- Check `data/temp/` folder exists
- Run image generation test: `python src/generator.py`

### Issue: MoviePy encoding errors

**Solution:**
- Install ffmpeg: https://ffmpeg.org/download.html
- Ensure ffmpeg is in system PATH

### Issue: Windows PowerShell script execution disabled

**Solution:**
Use Command Prompt instead:
```bash
venv\Scripts\activate.bat
```

Or allow scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 🧪 Testing Individual Modules

Test each component separately:

```bash
# Test news fetching
python src/fetcher.py

# Test script generation
python src/scripter.py

# Test audio + image generation
python src/generator.py

# Test video assembly
python src/editor.py
```

## 🔧 Configuration Options

Edit `.env` to customize:

```env
NEWS_CATEGORY=technology        # Options: business, entertainment, health, science, sports, technology
POST_LIMIT=5                    # Number of articles to fetch (uses first one)
VIDEO_WIDTH=1080                # Output width (9:16 ratio)
VIDEO_HEIGHT=1920               # Output height
```

## 📚 Project Dependencies

- **google-generativeai**: Gemini AI for script generation
- **edge-tts**: Microsoft Edge Text-to-Speech (FREE!)
- **moviepy**: Video editing and assembly
- **pillow**: Image processing and gradient generation
- **requests**: HTTP requests for APIs
- **python-dotenv**: Environment variable management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational purposes. Ensure compliance with:
- NewsAPI Terms of Service
- Google Gemini API Terms
- Microsoft EdgeTTS Terms of Service
- Pexels License (if used)

## 🎓 Learning Resources

- **Gemini API Docs:** https://ai.google.dev/docs
- **EdgeTTS GitHub:** https://github.com/rany2/edge-tts
- **MoviePy Docs:** https://zulko.github.io/moviepy/
- **NewsAPI Docs:** https://newsapi.org/docs

## 🚀 Next Steps

1. **Test the bot:** Run `python main.py`
2. **Check output:** Look in `data/output/` folder
3. **Upload to Instagram:** Use Instagram app to post Reel
4. **Iterate:** Adjust scripts and prompts for better engagement

## ⭐ Tips for Viral Content

1. **Run during trending news:** Tech announcements, product launches
2. **Test different voices:** Try various EdgeTTS voices (run `python list_voices.py`)
3. **A/B test hooks:** Gemini generates different hooks each time
4. **Post consistently:** Daily or 3× per week for best engagement
5. **Add captions:** Instagram auto-captions increase views by 40%

---

**Built with ❤️ using free AI tools**

For issues or questions, check the troubleshooting guide above!
