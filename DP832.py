# Based on work by: Kearney Lackas
import pyvisa
import time

_delay = 0.01  # in seconds


class DP832:
    def __init__(self, usb_or_serial='USB0'):
        try:
            self.rm = pyvisa.ResourceManager('@py')
            self.instrument_list = self.rm.list_resources()

            self.address = [elem for elem in self.instrument_list if (elem.find('USB') != -1 and elem.find(
                usb_or_serial) != -1)]  # Search a instrument with USB and serial number in the instrument list

            if self.address.__len__() == 0:
                self.status = "Not Connected"
                # print("Could not connect to device")
            else:
                self.address = self.address[0]
                self.device = self.rm.open_resource(self.address)
                # print("Connected to " + self.address)
                self.status = "Connected"
                self.connected_with = 'USB'

        except:
            self.status = "Not Connected"
            # print("PyVISA is not able to find any devices")

    def __del__(self):
        self.rm.close()

    def set_output(self, chan, voltage, amp):
        self.set_voltage(chan,voltage)
        self.set_current(chan, amp)
        self.toggle_output(chan, True)

    def run_cmd(self, cmd):
        #TODO: Log here
        #logging.info(cmd)
        self.device.write(cmd)
        time.sleep(_delay) 

    def select_output(self, chan):
        # define a CHANNEL SELECT function
        self.run_cmd(':INST:NSEL %s' % chan)

    def toggle_output(self, chan, state:bool):
        # define a TOGGLE OUTPUT function
        command = ':OUTP CH%s,%s ' % (chan, 'ON' if state else 'OFF')
        self.run_cmd(command)

    def set_voltage(self, chan, val):
        # define a SET VOLTAGE function
        self.select_output(chan)
        command = ':VOLT %s' % val
        self.run_cmd(command)

    def set_current(self, chan, val):
        # define a SET CURRENT function
        self.select_output(chan)
        command = ':CURR %s' % val
        self.run_cmd(command)

    def set_ovp(self, chan,val, state:bool):
        # define a SET VOLT PROTECTION function
        self.select_output(chan)
        command = ':VOLT:PROT %s' % val
        self.run_cmd(command)
        command = ':VOLT:PROT:STAT %s' % state
        self.run_cmd(command)

    def toggle_ovp(self, state):
        # define a TOGGLE VOLTAGE PROTECTION function
        command = ':VOLT:PROT:STAT %s' % state
        self.run_cmd(command)

    def set_ocp(self, chan, val, state:bool):
        # define a SET CURRENT PROTECTION function
        self.select_output(chan)
        command = ':CURR:PROT %s' % val
        self.run_cmd(command)
        # Toggle the ocp
        command = ':CURR:PROT:STAT %s' % ('ON' if state else 'OFF')
        self.run_cmd(command)

    def toggle_ocp(self, state:bool):
        # define a TOGGLE CURRENT PROTECTION function
        command = ':CURR:PROT:STAT %s' % ('ON' if state else 'OFF')
        self.run_cmd(command)

    def measure_voltage(self, chan):
        # define a MEASURE VOLTAGE function
        command = ':MEAS:VOLT? CH%s' % chan
        volt = self.device.query(command)
        volt = float(volt)
        time.sleep(_delay)
        return volt

    def measure_current(self, chan):
        # define a MEASURE CURRENT function
        command = ':MEAS:CURR? CH%s' % chan
        curr = self.device.query(command)
        curr = float(curr)
        time.sleep(_delay)
        return curr

    def measure_power(self, chan):
        # define a MEASURE POWER function
        command = ':MEAS:POWE? CH%s' % chan
        power = self.device.query(command)
        power = float(power)
        time.sleep(_delay)
        return power