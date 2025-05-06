# scripts_to_run_files/launch_correct_env.py
import subprocess

PYTHON_ENV = r"C:\Users\PC\AppData\Local\Programs\Python\Python310\python.exe"
SCRIPT = r"C:\Users\PC\Desktop\phaseB\VisoSpeak\scripts_to_run_files\run_mouth_extraction.py"

subprocess.run([PYTHON_ENV, SCRIPT])
