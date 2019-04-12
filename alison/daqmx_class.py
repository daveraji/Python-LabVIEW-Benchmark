import nidaqmx


class DaqmxSession:

    # Currently testing on simulated multifunction DAQ device.
    dev = "Dev1"
    chan = "ai0"
    physchan = dev + "/" + chan

    def open(self):
        self.task = nidaqmx.task.Task()
        self.task.ai_channels.add_ai_voltage_chan(self.physchan)
        # Add DAQmx Start Task here so that first iteration does not have to auto-start, skewing the results.

    def close(self):
        self.task.close()

    # ------ BENCHMARK TESTS --------

    def read_std(self):  # Not to be confused with stream reader reads, which are supposedly faster.
        self.data = self.task.read(100)

#    def write)std(self):
#        self.data = self.task.write(100)
# --------------------------------

# Testing methods....

# testsesh = DaqmxSession()
# print(testsesh.chan)
# print(testsesh.physchan)
# testsesh.open()
# testsesh.read_std()
# print(testsesh.data)
# time.sleep(5)
# testsesh.close()
