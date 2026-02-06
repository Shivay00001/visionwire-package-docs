import os
import sys
import subprocess

def setup():
    print("🚀 Starting VisionWire AI Setup...")
    
    # 1. Verify Python Version
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required.")
        sys.exit(1)
    print("✅ Python version verified.")
    
    # 2. Create Directories
    directories = ['cache', 'output', 'logs']
    for d in directories:
        if not os.path.exists(d):
            os.makedirs(d)
    print("✅ Project directories created.")
    
    # 3. Create .env if it doesn't exist
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write("OPENROUTER_API_KEY=your_api_key_here\n")
        print("✅ Created .env template.")
    
    # 4. Install Dependencies
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed.")
    except Exception as e:
        print(f"⚠️ Warning: Could not install dependencies automatically. Please run 'pip install -r requirements.txt' manually.\nDetail: {e}")

    print("\n✨ Setup complete! Configure your API key in .env and run visionwire_universal_app.py")

if __name__ == "__main__":
    setup()
