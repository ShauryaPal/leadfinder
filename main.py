import subprocess
import time
process = subprocess.Popen('/usr/local/bin/python3 "/Users/shaurya/Advestly/Python Lead Finder/LeadFinder.py"')
time.sleep(10)
process.kill()