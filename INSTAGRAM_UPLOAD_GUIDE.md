# Instagram Upload & Scheduling Guide

Complete guide for automatically uploading Instagram Reels with scheduling.

## 🚀 Quick Start

### 1. Install Dependencies

All required packages are in `requirements.txt`:
```bash
pip install -r requirements.txt
```

This installs:
- `instagrapi` - Instagram API client
- `apscheduler` - Scheduling system
- `pytz` - Timezone support
- `pycryptodomex` - Encryption for Instagram
- `pysocks` - Proxy support

### 2. Configure Instagram Credentials

Edit `.env` file:
```env
# Instagram Credentials
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password

# Enable auto-upload after video generation
ENABLE_AUTO_UPLOAD=false

# Scheduler Configuration
ENABLE_SCHEDULER=false
DAILY_POST_TIME=10:00
TIMEZONE=UTC
```

## 📝 Usage Modes

### Mode 1: Manual Upload (After Generating Video)

1. Generate video first:
```bash
python main.py
```

2. Upload manually using uploader:
```bash
python src/uploader.py
```

Or upload programmatically:
```python
from src.uploader import upload_to_instagram

upload_to_instagram(
    video_path="data/output/your_video.mp4",
    caption="Your caption here",
    hashtags=["tech", "ai", "innovation"]
)
```

### Mode 2: Auto-Upload After Generation

Enable in `.env`:
```env
ENABLE_AUTO_UPLOAD=true
```

Then run:
```bash
python main.py
```

The video will be automatically uploaded after generation!

### Mode 3: Automated Daily Scheduling (24/7 Bot)

1. Configure in `.env`:
```env
ENABLE_SCHEDULER=true
DAILY_POST_TIME=10:00
TIMEZONE=America/New_York
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

2. Run scheduler:
```bash
python scheduler_bot.py
```

3. Keep it running! The bot will:
   - Generate videos daily at 10:00 AM
   - Automatically upload to Instagram
   - Log all uploads
   - Continue running 24/7

## 🌍 Timezone Configuration

### Common Timezones

| Location | Timezone Code |
|----------|---------------|
| New York, USA | `America/New_York` |
| Los Angeles, USA | `America/Los_Angeles` |
| Chicago, USA | `America/Chicago` |
| London, UK | `Europe/London` |
| Paris, France | `Europe/Paris` |
| Mumbai, India | `Asia/Kolkata` |
| Tokyo, Japan | `Asia/Tokyo` |
| Sydney, Australia | `Australia/Sydney` |
| UTC | `UTC` |

Full list: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

### Testing Timezone

Verify your timezone:
```bash
python -c "import pytz; print(pytz.timezone('America/New_York'))"
```

## 📊 Upload History

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

You can track:
- When each video was uploaded
- Which video file was uploaded
- Instagram Reel URL
- Account used

## 🔐 Security Best Practices

### 1. Use a Dedicated Bot Account
- Don't use your personal Instagram account
- Create a new account specifically for the bot
- Less risk if account gets flagged

### 2. Protect Your Credentials
```bash
# Never commit .env to git
echo ".env" >> .gitignore

# Set secure file permissions (Linux/Mac)
chmod 600 .env

# Keep credentials secure
# Don't share .env file
# Don't expose credentials in code
```

### 3. Session Management
- Bot saves session to `data/temp/instagram_session.json`
- Reuses session to avoid repeated logins
- Session stays valid for ~90 days
- Delete session file to force new login:
  ```bash
  rm data/temp/instagram_session.json
  ```

### 4. Rate Limiting
Instagram has rate limits:
- **Login:** Max 3-5 logins per hour
- **Upload:** Max 10-15 posts per day for new accounts
- **Upload:** Max 25-30 posts per day for established accounts

**Recommendations:**
- Post 1-3 times per day max
- Space posts at least 2-4 hours apart
- Don't post at exactly the same time every day

## 🐛 Troubleshooting

### Error: "Challenge Required"

**Cause:** Instagram requires verification (2FA, CAPTCHA, etc.)

**Solution:**
1. Open Instagram app on your phone
2. Login with bot account
3. Complete any challenges/verifications
4. Wait 10-15 minutes
5. Try running bot again

### Error: "Login Required"

**Cause:** Session expired or invalid

**Solution:**
```bash
# Delete old session
rm data/temp/instagram_session.json

# Run bot again (will create new session)
python main.py
```

### Error: "PleaseWaitFewMinutes"

**Cause:** Instagram rate limit hit

**Solution:**
- Wait 15-30 minutes
- Don't spam uploads
- Reduce posting frequency

### Error: "Feedback Required"

**Cause:** Account temporarily restricted

**Solution:**
1. Login to Instagram app
2. Follow any instructions from Instagram
3. Wait 24-48 hours
4. Try again

### Upload Successful But Reel Not Visible

**Cause:** Instagram processing delay

**Solution:**
- Wait 5-10 minutes
- Check Instagram app (not web)
- Reel may be under review
- Check if account is public

## 📈 Optimizing for Growth

### Best Posting Times
- **Morning:** 6-9 AM (local time)
- **Lunch:** 12-1 PM
- **Evening:** 6-9 PM
- **Weekends:** Higher engagement

### Hashtag Strategy
Default hashtags (in `src/uploader.py`):
```python
hashtags = [
    "technews",
    "tech",
    "technology",
    "ai",
    "innovation",
    "trending",
    "reels",
    "viral"
]
```

**Tips:**
- Use 5-10 relevant hashtags
- Mix popular and niche hashtags
- Update based on trending topics
- Don't spam hashtags

### Caption Best Practices
- Start with attention-grabbing hook
- Keep it concise (2-3 sentences)
- Include call-to-action
- Use emojis sparingly
- Ask questions to boost engagement

## 🔄 Advanced Scheduling

### Multiple Daily Posts

Edit `scheduler_bot.py` to add multiple jobs:

```python
# Morning post at 9 AM
scheduler.add_daily_job(
    job_func=scheduled_post_job,
    hour=9,
    minute=0,
    job_id="morning_post"
)

# Evening post at 6 PM
scheduler.add_daily_job(
    job_func=scheduled_post_job,
    hour=18,
    minute=0,
    job_id="evening_post"
)
```

### Interval-Based Posting

Post every X hours instead of daily:

```python
# Post every 6 hours
scheduler.add_interval_job(
    job_func=scheduled_post_job,
    hours=6,
    job_id="interval_post"
)
```

### Running as Background Service

#### Windows (Task Scheduler)
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: At system startup
4. Action: Start a program
   - Program: `C:\path\to\python.exe`
   - Arguments: `C:\path\to\InstaBot\scheduler_bot.py`

#### Linux (systemd)
Create `/etc/systemd/system/instabot.service`:
```ini
[Unit]
Description=Instagram News Reel Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/InstaBot
ExecStart=/path/to/venv/bin/python scheduler_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable instabot
sudo systemctl start instabot
```

#### Using Screen (Linux/Mac)
```bash
# Start new screen session
screen -S instabot

# Run bot
python scheduler_bot.py

# Detach: Press Ctrl+A, then D

# Reattach later
screen -r instabot
```

## 📞 Support

If you encounter issues:

1. Check troubleshooting section above
2. Review Instagram API documentation: https://github.com/adw0rd/instagrapi
3. Check logs in terminal output
4. Review `data/upload_history.json` for past uploads

## ✅ Checklist

Before running automated bot:

- [ ] Instagram credentials configured in `.env`
- [ ] `ENABLE_SCHEDULER=true` in `.env`
- [ ] Valid timezone set (test with `pytz`)
- [ ] Posting time configured (`DAILY_POST_TIME`)
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Tested manual upload first
- [ ] Using dedicated bot account (not personal)
- [ ] Understand Instagram rate limits
- [ ] `.env` file secured (not in git)

Ready to go! 🚀

```bash
python scheduler_bot.py
```
