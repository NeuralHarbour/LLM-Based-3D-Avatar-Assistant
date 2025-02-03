# main.py
from .reminder_agent import ReminderAgent
from .reminder_monitor import ReminderMonitor
from .utils import ensure_file_exists
import os
import time
import importlib.util
from pathlib import Path
from dotenv import load_dotenv
import sys

current_dir = Path(__file__).parent
project_root = current_dir.parent
    
env_path = project_root / "API_KEYS.env"
if not env_path.exists():
    raise FileNotFoundError(f"Environment file not` found at {env_path}")
    
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



if __name__ == "__main__":
    reminder_file = "reminders.yaml"
    ensure_file_exists(reminder_file)

    agent = ReminderAgent(base_data.llm)
    monitor = ReminderMonitor(reminder_file)
    
    # Run monitor in separate thread
    from threading import Thread
    monitor_thread = Thread(target=monitor.run, daemon=True)
    monitor_thread.start()
    
    print("Reminder system is running. Press Ctrl+C to exit.")
    try:
        while True:
            user_input = input("Enter reminder command (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                break
            result = agent.run(user_input)
            print(result['output'])
    except KeyboardInterrupt:
        print("\nExiting reminder system...")
#Remind me to drink water every 30 minutes