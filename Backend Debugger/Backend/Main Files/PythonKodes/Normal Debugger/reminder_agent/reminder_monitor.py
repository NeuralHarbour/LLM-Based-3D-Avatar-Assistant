import logging
import datetime
import time
import yaml
from pathlib import Path
import os
from typing import Dict, Any
from datetime import date
from plyer import notification
from .utils import ensure_file_exists
import sys
from dotenv import load_dotenv
import importlib
current_dir = Path(__file__).parent
project_root = current_dir.parent
    
env_path = project_root / "API_KEYS.env"
if not env_path.exists():
    raise FileNotFoundError(f"Environment file not found at {env_path}")
    
load_dotenv(dotenv_path=str(env_path))
wolfram_api_key = os.environ.get("WOLFRAM_ALPHA_API_KEY")
    
if not wolfram_api_key:
    raise ValueError("WOLFRAM_ALPHA_API_KEY not found in environment variables")
base_data_path = project_root / "BASE_DATA.py"
if not base_data_path.exists():
    raise FileNotFoundError(f"BASE_DATA.py not found at {base_data_path}")
    
sys.path.insert(0, str(project_root))

try:
    spec = importlib.util.spec_from_file_location("BASE_DATA", base_data_path)
    base_data = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base_data)
except Exception as e:
    raise ImportError(f"Failed to import BASE_DATA: {str(e)}")

class ReminderMonitor:
    def __init__(self, reminder_file: str = "reminders.yaml"):
        self.reminder_file = reminder_file
        self.timers = {}
        ensure_file_exists(reminder_file)

    def log_overwrite(self, message: str, level="info"):
        """Overwrite logs dynamically in the same line."""
        log_function = getattr(logging, level)
        print(f"\r{message}", end="", flush=True)
        log_function(message)

    def start_timer(self, reminder: Dict[str, Any]):
        reminder_id = reminder['id']
        if reminder_id not in self.timers:
            self.timers[reminder_id] = {
                'start_time': datetime.datetime.now(),
                'last_trigger': None
            }
            self.log_overwrite(f"Started timer for reminder: {reminder['alias']}", "debug")

    def should_trigger(self, reminder: Dict[str, Any]) -> bool:
        reminder_id = reminder['id']
        if reminder_id not in self.timers:
            return False

        now = datetime.datetime.now()
        timer = self.timers[reminder_id]
        elapsed = now - timer['last_trigger'] if timer['last_trigger'] else now - timer['start_time']

        interval_value = reminder['recurring'].get('interval_value', 0)
        interval_unit = reminder['recurring'].get('interval_unit', 'once')

        self.log_overwrite(f"Checking reminder: {reminder['alias']}", "debug")

        if interval_unit == 'minute':
            return elapsed.total_seconds() >= interval_value * 60
        elif interval_unit == 'hour':
            return elapsed.total_seconds() / 3600 >= interval_value
        elif interval_unit == 'day':
            return elapsed.days >= interval_value
        elif interval_unit == 'once':
            trigger_time_str = reminder['date'].get('trigger_time')
            if trigger_time_str is None:
                self.log_overwrite(f"Error: Reminder '{reminder['alias']}' is missing 'trigger_time'.", "error")
                return False

            current_time_str = now.strftime("%H:%M")
            current_date = date.today().strftime("%d/%m/%Y")

            self.log_overwrite(f"Checking one-time reminder at {current_time_str} vs {trigger_time_str}", "debug")

            return current_time_str == trigger_time_str and current_date == reminder['date']['_date']

        return False

    def check_reminders(self):
        try:
            with open(self.reminder_file, 'r') as file:
                reminders = yaml.safe_load(file) or []

            updated_reminders = []

            for reminder in reminders:
                self.start_timer(reminder)
                if self.should_trigger(reminder):
                    self.log_overwrite(f"Triggering reminder: {reminder['alias']}", "info")
                    self.timers[reminder['id']]['last_trigger'] = datetime.datetime.now()

                    if reminder['recurring']['interval_unit'] == 'once':

                        response = base_data.llm.invoke(f"Generate a notification title and description based on the reminder: '{reminder['alias']}'. Provide the title and description separated by a semicolon.")
                        print(response)

                        if hasattr(response, 'content'):
                            content = response.content
                            print(f"Full response content: {content}")
                            try:
                                notification_title, notification_message = content.split(';')[0].strip(), content.split(';')[1].strip()
                                print(f"Notification Title: {notification_title}")
                                print(f"Notification Message: {notification_message}")
                            except IndexError:
                                print("Error: Couldn't split the response properly. Ensure the response has both title and message separated by a semicolon.")
                        else:
                            print("Error: 'response' doesn't have a 'content' attribute.")

                        notification.notify(
                            title=notification_title,
                            message=notification_message,
                            timeout=10,
                            toast=False
                        )

                        self.log_overwrite(f"Removing one-time reminder: {reminder['alias']}", "info")
                        continue

                updated_reminders.append(reminder)

            with open(self.reminder_file, 'w') as file:
                yaml.dump(updated_reminders, file)

        except Exception as e:
            self.log_overwrite(f"Error checking reminders: {str(e)}", "error")

    def run(self, check_interval: int = 1):
        self.log_overwrite("Starting reminder monitor...", "info")
        try:
            while True:
                self.check_reminders()
                time.sleep(check_interval)
        except KeyboardInterrupt:
            self.log_overwrite("Stopping reminder monitor...", "info")
