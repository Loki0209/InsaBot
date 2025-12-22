# Automated AI News Reel Bot

An automated system that creates 9:16 vertical videos for Instagram based on trending Tech News with **automatic scheduling and upload**.

## 🎯 Architecture

1. **Data Source**: NewsAPI - fetching trending tech news
2. **Scripting**: Google Gemini 2.5-Flash (FREE!) - generates viral scripts and visual prompts
3. **Audio**: EdgeTTS (FREE!) - Microsoft Edge Text-to-Speech with realistic voices
4. **Images**: Gradient Generator (with optional Pexels integration) - creates background images
5. **Editing**: MoviePy - stitches images and audio with **Ken Burns Effect** (cinematic zoom/pan animations)
6. **Upload**: Instagrapi - automatic Instagram Reel upload
7. **Scheduling**: APScheduler - daily automated posting at specific times

## 📁 Project Structure

```
InstaBot/
├── src/
│   ├── fetcher.py              # NewsAPI integration
│   ├── scripter.py             # Gemini AI script generation
│   ├── generator.py            # Audio (EdgeTTS) + Images (Gradients/Pexels)
│   ├── editor.py               # Video assembly (MoviePy + Ken Burns)
│   ├── uploader.py             # Instagram upload (Instagrapi)
│   └── scheduler_manager.py   # Scheduling system (APScheduler)
├── data/
│   ├── temp/                   # Temporary files (audio, images, session)
│   ├── output/                 # Final video outputs
│   └── upload_history.json    # Upload log
├── main.py                     # Main pipeline (single run)
├── scheduler_bot.py            # Automated scheduler (24/7 posting)
├── requirements.txt            # Python dependencies (pinned versions)
├── requirements-dev.txt        # Development dependencies
├── .env.example               # Environment variables template
├── .env                       # Your actual credentials (not committed)
└── README.md                  # This file
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

**Instagram Credentials (for auto-upload)**
- Add your Instagram credentials to `.env`:
  ```
  INSTAGRAM_USERNAME=your_instagram_username
  INSTAGRAM_PASSWORD=your_instagram_password
  ```
- **⚠️ Security Warning:** Keep these credentials private! Never commit `.env` to version control.

### 5. Run the bot

#### Option A: Single Video Generation (Manual)

Generate one video without uploading:
```bash
python main.py
```

#### Option B: Single Video with Auto-Upload

Enable auto-upload in `.env`:
```
ENABLE_AUTO_UPLOAD=true
```

Then run:
```bash
python main.py
```

#### Option C: Automated Daily Scheduling (24/7 Bot)

Configure scheduler in `.env`:
```
ENABLE_SCHEDULER=true
DAILY_POST_TIME=10:00
TIMEZONE=UTC
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

Run the scheduler:
```bash
python scheduler_bot.py
```

The bot will now:
- ✅ Automatically generate videos daily at 10:00 AM (your timezone)
- ✅ Automatically upload to Instagram
- ✅ Run 24/7 in the background
- ✅ Log all uploads to `data/upload_history.json`

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

## 📱 Instagram Upload & Scheduling

### Automatic Instagram Upload

The bot can automatically upload generated videos to Instagram Reels using **Instagrapi**.

#### Features:
- ✅ **Session Persistence** - Login once, reuse session
- ✅ **Upload History** - Track all uploads in `data/upload_history.json`
- ✅ **Automatic Hashtags** - Tech-related hashtags added automatically
- ✅ **Caption Generation** - Uses AI-generated script as caption
- ✅ **Error Handling** - Graceful fallback if upload fails

#### Configuration:

1. Add Instagram credentials to `.env`:
```env
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password
ENABLE_AUTO_UPLOAD=true
```

2. Run the bot:
```bash
python main.py
```

The video will be automatically uploaded after generation!

### Automated Daily Scheduling

Run the bot 24/7 and post automatically every day at a specific time using **APScheduler**.

#### Features:
- ✅ **Daily Posting** - Set specific time (e.g., 10:00 AM)
- ✅ **Timezone Support** - Works with any timezone
- ✅ **Background Execution** - Runs continuously
- ✅ **Auto-Generation & Upload** - Fully automated pipeline
- ✅ **Error Recovery** - Continues even if one post fails

#### Configuration:

1. Configure scheduler in `.env`:
```env
ENABLE_SCHEDULER=true
DAILY_POST_TIME=10:00
TIMEZONE=America/New_York
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

2. Run the scheduler:
```bash
python scheduler_bot.py
```

3. The bot will now post automatically every day at 10:00 AM!

#### Timezone Examples:
- **UTC** - Coordinated Universal Time
- **America/New_York** - Eastern Time (US)
- **America/Los_Angeles** - Pacific Time (US)
- **Europe/London** - British Time
- **Asia/Kolkata** - Indian Time
- **Asia/Tokyo** - Japan Time

Full list: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

#### Stopping the Scheduler:
Press `Ctrl+C` to stop the scheduler.

### Upload History

All uploads are logged to `data/upload_history.json`:
```json
[
  {
    "timestamp": "2025-12-22T10:00:00",
    "video_path": "data/output/news_reel_20251222_100000.mp4",
    "caption": "Breaking tech news...",
    "media_code": "ABC123xyz",
    "instagram_url": "https://www.instagram.com/reel/ABC123xyz/",
    "username": "your_username"
  }
]
```

### Security Notes:

⚠️ **Important:**
- Never share your `.env` file
- Never commit `.env` to git (it's in `.gitignore`)
- Use a strong Instagram password
- Consider using a dedicated bot account
- Instagram may require 2FA verification on first login

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

### Issue: Instagram login failed / Challenge required

**Solution:**
1. **Two-Factor Authentication (2FA):**
   - Instagram may require 2FA verification on first login
   - Complete the challenge in the Instagram app
   - Try logging in again

2. **Rate Limiting:**
   - Instagram may block automated logins temporarily
   - Wait 15-30 minutes and try again
   - Don't login/logout too frequently

3. **Incorrect Credentials:**
   - Double-check `INSTAGRAM_USERNAME` and `INSTAGRAM_PASSWORD` in `.env`
   - Ensure no extra spaces

4. **Account Security:**
   - Use a dedicated bot account (recommended)
   - Avoid using your personal account
   - New accounts may have stricter limits

### Issue: "PleaseWaitFewMinutes" error

**Solution:**
- Instagram has rate-limited your account
- Wait 15-30 minutes before trying again
- Don't post too frequently (max 1-2 posts per hour recommended)

### Issue: Scheduler not running at specified time

**Solution:**
1. Check timezone is correct:
   ```bash
   python -c "import pytz; print(pytz.timezone('YOUR_TIMEZONE'))"
   ```
2. Verify `DAILY_POST_TIME` format is `HH:MM` (24-hour)
3. Ensure `ENABLE_SCHEDULER=true`
4. Keep the script running (don't close terminal)

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
