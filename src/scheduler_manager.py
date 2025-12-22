"""
Scheduler Manager Module

This module handles scheduling automated Instagram Reel posts using APScheduler.
It supports:
- Daily scheduled posts at specific times
- Interval-based posting (every X hours)
- Timezone support
- Job persistence and management

Author: AI News Reel Bot
"""

import os
import sys
from datetime import datetime, time
from typing import Optional, Callable

try:
    from apscheduler.schedulers.blocking import BlockingScheduler
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.cron import CronTrigger
    from apscheduler.triggers.interval import IntervalTrigger
    import pytz
except ImportError:
    print("[ERROR] APScheduler not installed. Run: pip install apscheduler pytz")
    sys.exit(1)


class SchedulerManager:
    """
    Scheduler Manager for automating Instagram Reel posts.

    Features:
    - Schedule posts at specific times daily
    - Interval-based scheduling (every X hours)
    - Timezone support
    - Background or blocking execution
    - Job management (add, remove, pause, resume)
    """

    def __init__(self, timezone: str = "UTC", background: bool = False):
        """
        Initialize scheduler.

        Args:
            timezone: Timezone for scheduling (e.g., "America/New_York", "Asia/Kolkata", "UTC")
            background: If True, use BackgroundScheduler (non-blocking), else BlockingScheduler
        """
        self.timezone = pytz.timezone(timezone)

        if background:
            self.scheduler = BackgroundScheduler(timezone=self.timezone)
        else:
            self.scheduler = BlockingScheduler(timezone=self.timezone)

        self.jobs = {}
        print(f"[INFO] Scheduler initialized (Timezone: {timezone}, Background: {background})")

    def add_daily_job(
        self,
        job_func: Callable,
        hour: int,
        minute: int = 0,
        job_id: str = "daily_post",
        **kwargs
    ):
        """
        Schedule a job to run daily at a specific time.

        Args:
            job_func: Function to execute
            hour: Hour (0-23)
            minute: Minute (0-59)
            job_id: Unique job identifier
            **kwargs: Additional arguments to pass to job_func
        """
        try:
            # Create cron trigger for daily execution
            trigger = CronTrigger(
                hour=hour,
                minute=minute,
                timezone=self.timezone
            )

            # Add job
            job = self.scheduler.add_job(
                job_func,
                trigger=trigger,
                id=job_id,
                kwargs=kwargs,
                replace_existing=True
            )

            self.jobs[job_id] = job

            # Calculate next run time
            next_run = job.next_run_time.strftime("%Y-%m-%d %H:%M:%S %Z")

            print("\n" + "=" * 60)
            print(f"[SUCCESS] Daily job scheduled!")
            print(f"Job ID: {job_id}")
            print(f"Schedule: Every day at {hour:02d}:{minute:02d}")
            print(f"Timezone: {self.timezone}")
            print(f"Next run: {next_run}")
            print("=" * 60 + "\n")

        except Exception as e:
            print(f"[ERROR] Failed to schedule daily job: {e}")

    def add_interval_job(
        self,
        job_func: Callable,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        job_id: str = "interval_post",
        **kwargs
    ):
        """
        Schedule a job to run at regular intervals.

        Args:
            job_func: Function to execute
            hours: Interval in hours
            minutes: Interval in minutes
            seconds: Interval in seconds
            job_id: Unique job identifier
            **kwargs: Additional arguments to pass to job_func
        """
        try:
            # Create interval trigger
            trigger = IntervalTrigger(
                hours=hours,
                minutes=minutes,
                seconds=seconds,
                timezone=self.timezone
            )

            # Add job
            job = self.scheduler.add_job(
                job_func,
                trigger=trigger,
                id=job_id,
                kwargs=kwargs,
                replace_existing=True
            )

            self.jobs[job_id] = job

            # Build interval description
            interval_parts = []
            if hours:
                interval_parts.append(f"{hours} hour(s)")
            if minutes:
                interval_parts.append(f"{minutes} minute(s)")
            if seconds:
                interval_parts.append(f"{seconds} second(s)")
            interval_str = ", ".join(interval_parts)

            # Calculate next run time
            next_run = job.next_run_time.strftime("%Y-%m-%d %H:%M:%S %Z")

            print("\n" + "=" * 60)
            print(f"[SUCCESS] Interval job scheduled!")
            print(f"Job ID: {job_id}")
            print(f"Interval: Every {interval_str}")
            print(f"Timezone: {self.timezone}")
            print(f"Next run: {next_run}")
            print("=" * 60 + "\n")

        except Exception as e:
            print(f"[ERROR] Failed to schedule interval job: {e}")

    def remove_job(self, job_id: str):
        """
        Remove a scheduled job.

        Args:
            job_id: Job identifier to remove
        """
        try:
            self.scheduler.remove_job(job_id)
            if job_id in self.jobs:
                del self.jobs[job_id]
            print(f"[INFO] Job '{job_id}' removed")
        except Exception as e:
            print(f"[ERROR] Failed to remove job: {e}")

    def pause_job(self, job_id: str):
        """
        Pause a scheduled job.

        Args:
            job_id: Job identifier to pause
        """
        try:
            self.scheduler.pause_job(job_id)
            print(f"[INFO] Job '{job_id}' paused")
        except Exception as e:
            print(f"[ERROR] Failed to pause job: {e}")

    def resume_job(self, job_id: str):
        """
        Resume a paused job.

        Args:
            job_id: Job identifier to resume
        """
        try:
            self.scheduler.resume_job(job_id)
            print(f"[INFO] Job '{job_id}' resumed")
        except Exception as e:
            print(f"[ERROR] Failed to resume job: {e}")

    def list_jobs(self):
        """List all scheduled jobs."""
        jobs = self.scheduler.get_jobs()

        if not jobs:
            print("[INFO] No scheduled jobs")
            return

        print("\n" + "=" * 60)
        print("SCHEDULED JOBS")
        print("=" * 60)

        for job in jobs:
            next_run = job.next_run_time.strftime("%Y-%m-%d %H:%M:%S %Z") if job.next_run_time else "Paused"
            print(f"\nJob ID: {job.id}")
            print(f"  Function: {job.func.__name__}")
            print(f"  Trigger: {job.trigger}")
            print(f"  Next run: {next_run}")

        print("=" * 60 + "\n")

    def start(self):
        """Start the scheduler (blocking)."""
        try:
            print("\n" + "=" * 60)
            print("SCHEDULER STARTED")
            print("=" * 60)
            print(f"Timezone: {self.timezone}")
            print(f"Current time: {datetime.now(self.timezone).strftime('%Y-%m-%d %H:%M:%S %Z')}")
            print("Press Ctrl+C to stop")
            print("=" * 60 + "\n")

            self.list_jobs()
            self.scheduler.start()

        except (KeyboardInterrupt, SystemExit):
            print("\n[INFO] Scheduler stopped by user")
            self.shutdown()

    def shutdown(self):
        """Shutdown the scheduler."""
        try:
            self.scheduler.shutdown()
            print("[INFO] Scheduler shut down")
        except Exception as e:
            print(f"[ERROR] Failed to shutdown scheduler: {e}")


# Example job function
def example_job(message: str = "Hello from scheduler!"):
    """Example job function."""
    print(f"\n[JOB EXECUTED] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Message: {message}")


# Example usage
if __name__ == "__main__":
    # Create scheduler (use your timezone)
    scheduler = SchedulerManager(timezone="UTC", background=False)

    # Schedule daily job at 10:00 AM
    scheduler.add_daily_job(
        job_func=example_job,
        hour=10,
        minute=0,
        job_id="morning_post",
        message="Good morning! Daily post at 10:00 AM"
    )

    # Schedule interval job (every 6 hours)
    scheduler.add_interval_job(
        job_func=example_job,
        hours=6,
        job_id="interval_post",
        message="Posting every 6 hours!"
    )

    # List scheduled jobs
    scheduler.list_jobs()

    # Start scheduler
    scheduler.start()
