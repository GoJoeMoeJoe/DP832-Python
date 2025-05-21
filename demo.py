import time
from DP832 import *

try:
    PSU = DP832()
    #OR if you know your address you can advoid some warnings
    #PSU = DP832('USB0::0000::0000::XXXXXXXXXXXXXX::0::INSTR')
    print(PSU.status)

except Exception as e:
    print(f"Error: {e}")
    exit()

PSU.set_output(1, 2.222, 1.11)
print(PSU.measure_current(1))
time.sleep(10) 
PSU.toggle_output(1, False)