#test file forvolume control for linux
import subprocess


def get_volume_range():
    """Get current volume and range using PulseAudio (pactl)."""
    result = subprocess.run(["pactl", "list", "sinks"], capture_output=True, text=True)
    for line in result.stdout.split("\n"):
        if "Volume:" in line:
            print(line.strip())  # Print volume information

# get_volume_range()

def set_volume(volume_percent):
    """Set system volume in Linux using pactl."""
    volume_percent = max(0, min(100, volume_percent))  # Ensure volume is within 0-100%
    subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{volume_percent}%"])

def get_volume():
    """Get current system volume using pactl."""
    result = subprocess.run(["pactl", "get-sink-volume", "@DEFAULT_SINK@"], capture_output=True, text=True)
    return result.stdout

# Example Usage:
get_volume_range()

set_volume(20)
