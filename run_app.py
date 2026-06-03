import subprocess
import sys
import os
import time

def main():
    print("Starting CardioCare App...")
    
    venv_python = os.path.join("venv_new", "Scripts", "python.exe")
    frontend_app = os.path.abspath(os.path.join("frontend", "app.py"))
    frontend_port = "8502"
    
    if not os.path.exists(venv_python):
        print("Virtual environment not found! Please run setup_env.ps1 first.")
        sys.exit(1)

    # Start FastAPI backend
    print("Launching Backend API (FastAPI)...")
    backend_process = subprocess.Popen(
        [venv_python, "-m", "uvicorn", "backend.main:app", "--reload", "--host", "0.0.0.0", "--port", "8001"],
        stdout=sys.stdout,
        stderr=sys.stderr
    )

    # Give backend a moment to start
    time.sleep(3)

    # Start Streamlit frontend using the venv Python interpreter directly
    print(f"Launching Frontend UI (Streamlit) on port {frontend_port}...")
    frontend_process = subprocess.Popen(
        [venv_python, "-m", "streamlit", "run", frontend_app, "--server.port", frontend_port],
        stdout=sys.stdout,
        stderr=sys.stderr
    )

    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down processes...")
        backend_process.terminate()
        frontend_process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main()
