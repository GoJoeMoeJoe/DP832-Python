import time
from DP832 import *

try:
    PSU = DP832()
    print(PSU.status)

except Exception as e:
    print(f"Error: {e}")
    exit()

PSU.set_output(1, 2.222, 1.11)
print(PSU.measure_current(1))
time.sleep(10) 
PSU.toggle_output(1, False)