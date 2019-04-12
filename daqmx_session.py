import nidaqmx
import numpy as np

random_analog = np.random.uniform(-1, 1, size=10000).tolist()
random_digital = np.random.choice(a=[True, False], size=10000).tolist()


class DAQmxSession:

    def __init__(self):
        print("DAQmx Session Initialized")

    def configure(self, device, channel):
        self.physical_channel = str(device) + "/" + str(channel)
        print("DAQmx Session Configured for " + self.physical_channel)

    def open(self, method):
        self.task = nidaqmx.task.Task()
        # Method lookup dictionary used to make the call dynamic
        self.methods = {
            "ai": "self.task.ai_channels.add_ai_voltage_chan(self.physical_channel)",
            "ao": "self.task.ao_channels.add_ao_voltage_chan(self.physical_channel)",
            "di": "self.task.di_channels.add_di_chan(self.physical_channel)",
            "do": "self.task.do_channels.add_do_chan(self.physical_channel)"
        }
        eval(self.methods[method])

    def close(self):
        self.task.close()

    '''

    Available methods for testing are below including Analog Input,
    Analog Output, Digial Input, and Digital Output

    '''
    def analog_input(self, device, channel,
                     samples, trial=0, clk_src='', rate=10000):
        # On the first trial we do configure and open
        if trial == 0:
            self.configure(device, channel)
            self.open("ai")
            self.task.timing.cfg_samp_clk_timing(rate, clk_src)
            self.data = self.task.read(samples)

        else:
            self.data = self.task.read(samples)

    def analog_output(self, device, channel,
                      samples, trial=0, clk_src='', rate=10000):

        # On the first trial we do configure and open
        if trial == 0:
            self.configure(device, channel)
            self.open("ao")
            self.task.timing.cfg_samp_clk_timing(rate, clk_src)
            self.task.wait_until_done(self.task.write(random_analog, auto_start=True))
            self.task.stop()

        else:
            self.task.wait_until_done(self.task.write(random_analog, auto_start=True))
            self.task.stop()

    def digital_input(self, device, channel,
                      samples, trial=0, clk_src='', rate=10000):
        # On the first trial we do configure and open
        if trial == 0:
            self.configure(device, channel)
            self.open("di")
            self.task.timing.cfg_samp_clk_timing(rate)
            self.data = self.task.read(samples, timeout=-1)

        else:
            self.data = self.task.read(samples, timeout=-1)

    def digital_output(self, device, channel,
                       samples, trial=0, clk_src='', rate=10000):
        # On the first trial we do configure and open
        if trial == 0:
            self.configure(device, channel)
            self.open("do")
            self.task.timing.cfg_samp_clk_timing(rate)
            self.task.write(random_digital, auto_start=True, timeout=-1)

        else:
            self.task.write(random_digital, auto_start=True, timeout=-1)
