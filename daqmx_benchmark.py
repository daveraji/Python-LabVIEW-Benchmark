import time
import sys
import pandas as pd
from pandas import DataFrame as df

from daqmx_session import DAQmxSession

# Configure Testing Parameters Here
samples = 10000  # samples per trial
trials = 100
device = 'Dev1'  # device alias as listed in NI MAX
channel = 'ao1'  # for digital tasks use 'port#/line#', for analog 'ao# or ai#'
clk_src = 'OnboardClock'  # can accept a physical channel
benchmark_method = 'analog_output'  # methods listed in daqmx_session.py
generate_report = True
device_model = "USB-6363"  # for documentation only


# Main benchmark function
def benchmark(session, method, device, channel, samples, trials, clk_src):
    results = []
    trials += 1  # Allows us to remove the first point which is cfg

    for trial in range(trials):
        sys.stdout.write("Trial Progress: %d of %d   \r" % (trial+1, trials))
        sys.stdout.flush()  # progress indicator
        t_start = time.perf_counter()
        method(device, channel, samples, trial, clk_src)  # calls target method
        t_end = time.perf_counter()
        t_elapsed = t_end - t_start
        results.append(t_elapsed)

    session.close()  # Close DAQ Session
    # print(results[0])  # Uncomment to see first iteration time
    results_no_cfg = results[1:]
    # Follow code is for console display until print statement
    sys.stdout.write("\n\n")  # Formatting
    data = df(results_no_cfg, columns=['Time'])  # Full results
    stats = data.Time.describe()  # Statistics of runs
    print(stats.to_csv(header=False, sep='\t'))

    # Generate report, can be made a separate script later if desired
    if generate_report:
        with pd.ExcelWriter(device_model + '_' + benchmark_method + '.xlsx') as writer:
            stats.to_excel(writer, sheet_name='Benchmark Stats')
            data.to_excel(writer, sheet_name='Raw Benchmark Data')


'''

MAIN FUNCTION

The following section of code configures and executes benchmarking function
with the configured parameters

'''

print("Starting...")

# Begin Benchmark Section
session = DAQmxSession()
benchmark(session, eval('session.' + benchmark_method),
          device, channel, samples, trials, clk_src)
