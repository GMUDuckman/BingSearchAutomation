import subprocess
import sys
import time

def run_with_progress(script_name, description):
    """Run a script and show progress updates"""
    print(f"\n{'='*50}")
    print(f"Starting {description}")
    print(f"{'='*50}")
    
    # Start the subprocess with real-time output
    process = subprocess.Popen([sys.executable, script_name], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.STDOUT,
                              universal_newlines=True,
                              bufsize=0)  # Changed to unbuffered
    
    # Monitor the output for progress in real-time
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            # Print the output immediately (which includes progress from the script)
            print(output.rstrip())  # Use rstrip() to avoid double newlines
            # Force flush to ensure immediate display
            sys.stdout.flush()
    
    # Wait for the process to complete
    return_code = process.wait()
    
    if return_code != 0:
        print(f"\n {description} exited with code {return_code}")
        return False
    else:
        print(f"\n {description} completed successfully!")
        return True

# Determine which searches to run based on optional args
# Expected optional positional args:
#   argv[1] -> ONLYMOBILE ("true"/"false")
#   argv[2] -> ONLYPC ("true"/"false")

only_mobile_arg = None
only_pc_arg = None

if len(sys.argv) > 1:
    only_mobile_arg = str(sys.argv[1]).strip().lower()
if len(sys.argv) > 2:
    only_pc_arg = str(sys.argv[2]).strip().lower()

# Defaults: run both if no args provided
run_pc = True
run_mobile = True

if only_mobile_arg in ("true", "false") or only_pc_arg in ("true", "false"):
    # If any flag provided, interpret them
    only_mobile = (only_mobile_arg == "true") if only_mobile_arg in ("true", "false") else False
    only_pc = (only_pc_arg == "true") if only_pc_arg in ("true", "false") else False

    if only_mobile and not only_pc:
        run_mobile = True
        run_pc = False
    elif only_pc and not only_mobile:
        run_pc = True
        run_mobile = False
    elif only_mobile and only_pc:
        # Conflicting instructions; run both and log a note
        run_pc = True
        run_mobile = True
        print("Both ONLYMOBILE and ONLYPC were set to true; running both searches.")
    else:
        # both false or unspecified -> run both
        run_pc = True
        run_mobile = True

print("Starting Bing Search Automation")
if run_pc and run_mobile:
    print("This will run both PC and Mobile searches with progress indicators")
elif run_pc:
    print("This will run only PC searches with progress indicators")
elif run_mobile:
    print("This will run only Mobile searches with progress indicators")

pc_success = None
mobile_success = None

if run_pc:
    pc_success = run_with_progress('search_pc.py', 'PC Search')

if run_mobile:
    mobile_success = run_with_progress('search_mobile.py', 'Mobile Search')

# Final summary
print(f"\n{'='*50}")
print("🏁 SEARCH AUTOMATION COMPLETE")
print(f"{'='*50}")

if run_pc and run_mobile:
    if pc_success and mobile_success:
        print("Both PC and Mobile searches completed successfully!")
    elif pc_success and not mobile_success:
        print("PC search completed, but Mobile search failed")
    elif mobile_success and not pc_success:
        print("Mobile search completed, but PC search failed")
    else:
        print("Both searches failed")
elif run_pc:
    if pc_success:
        print("PC search completed successfully!")
    else:
        print("PC search failed")
elif run_mobile:
    if mobile_success:
        print("Mobile search completed successfully!")
    else:
        print("Mobile search failed")
else:
    print("No searches were executed. Please check input flags.")