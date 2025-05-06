import subprocess
import os

# ✅ Use the correct Python path
python_path = r"C:\Users\PC\AppData\Local\Programs\Python\Python310\python.exe"
pip_path = os.path.join(os.path.dirname(python_path), "Scripts", "pip.exe")

# ✅ Path to requirements.txt
requirements_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "requirements.txt"))

def install_requirements():
    print(f"📦 Installing requirements using pip from: {pip_path}")
    print(f"📄 Requirements file: {requirements_path}")

    if not os.path.exists(pip_path):
        print("❌ pip.exe not found at the expected location!")
        return

    try:
        subprocess.check_call([pip_path, "install", "-r", requirements_path])
        print("✅ All dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ pip failed with exit code {e.returncode}")

if __name__ == "__main__":
    install_requirements()
