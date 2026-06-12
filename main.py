import sys
import subprocess
import os

def print_usage():
    print("Usage: main.py [mobile|pc] [num_searches] [/shutdown] [/shutdowntime:<seconds>]")
    print("Example: main.py mobile 20 /shutdown /shutdowntime:120")

if len(sys.argv) < 2 or sys.argv[1] not in ("mobile", "pc"):
    print_usage()
    sys.exit(1)

mode = sys.argv[1]
args = sys.argv[2:]

# Parse shutdown options
shutdown = False
shutdowntime = 60  # default
filtered_args = []
for arg in args:
    if arg.lower() == "/shutdown":
        shutdown = True
    elif arg.lower().startswith("/shutdowntime:"):
        try:
            shutdowntime = int(arg.split(":", 1)[1])
        except ValueError:
            pass
    else:
        filtered_args.append(arg)

if mode == "mobile":
    script = "search_mobile.py"
elif mode == "pc":
    script = "search_pc.py"

cmd = [sys.executable, script] + filtered_args
subprocess.run(cmd)

if shutdown:
    print(f"The computer will shut down in {shutdowntime} seconds. Save your work!")
    os.system(f"shutdown /s /t {shutdowntime}") 