import os
import subprocess

def run_all_scripts(directory):
    # Get all Python files in the directory
    scripts = [f for f in os.listdir(directory) if f.endswith(".py")]
    
    if not scripts:
        print(f"No Python scripts found in the directory: {directory}")
        return

    # Run each script one by one
    for script in scripts:
        script_path = os.path.join(directory, script)
        print(f"Running: {script_path}")
        try:
            subprocess.run(["python", script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running {script}: {e}")
        except Exception as e:
            print(f"Unexpected error with {script}: {e}")

if __name__ == "__main__":
    # Folder containing the scripts
    scrappers_folder = "scrapers"  # Replace with the absolute path if necessary
    run_all_scripts(scrappers_folder)