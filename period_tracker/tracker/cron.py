from django_cron import CronJobBase, Schedule
from .tasks import send_period_reminders

class SendReminderCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # Run once a day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'tracker.send_reminder'  # Unique code

    def do(self):
        send_period_reminders()
