from modules.utility import print_debug, print_log
from interface import*
#WHERE DO I STORE CLIENT SIDE (GLOBAL) VARIABLES?
#

class Signal():
    """Represents a signal"""

    def __init__(self, magnitude=[], fsample=0, time=[]) -> None:

        self.magnitude = magnitude
        self.fsample = fsample
        self.time = time

        if self.fsample == 0:
            self.time = time
            if len(time) != 0:
                self.fsample = len(self.magnitude)/time[-1]

        if len(time) == 0:
            if len(magnitude) != 0:
                print_debug("Time axis auto generated")
                self.time = np.arange(0, len(magnitude))/fsample
            else:
                self.time = []

        # if (self.magnitude != [] and self.time == []) or (self.magnitude == [] and self.time != []):
        #     raise Exception("Signal must have a time or fsampling vector")

    def __len__(self):
        """Returns the length of the signal"""
        if self.magnitude != []:
            return len(self.magnitude)
        else:
            print_debug("Signal has 0 length")
            return 0

    def __getitem__(self, index):
        """Returns the signal at the given index"""
        return copy(Signal(self.magnitude[index], self.fsample, self.time[index]))

    def __add__(self, other):
        """Adds two signals"""
        if self.fsample == other.fsample:
            return Signal(self.magnitude + other.magnitude, self.fsample, self.time)
        else:
            raise Exception("Signals must have the same sampling frequency")

    def __subtract__(self, other):
        """Subtracts two signals"""
        if self.fsample == other.fsample:
            return Signal(self.magnitude - other.magnitude, self.fsample, self.time)
        else:
            raise Exception("Signals must have the same sampling frequency")

    def set_max_samples(self, max_samples):
        """Sets the maximum number of samples"""
        if len(self.magnitude) > max_samples:
            self.magnitude = self.magnitude[:max_samples]
            self.time = self.time[:max_samples]

    def __append__(self, other):
        """Appends two signals"""
        if self.fsample == other.fsample:
            return copy(Signal(self.magnitude + other.magnitude, self.fsample, self.time + other.time))
        else:
            raise Exception("Signals must have the same sampling frequency")

    def clip(self, direction, percentage):
        """Clips the signal"""
        percentage = percentage / 100
        if direction == "left":
            self.magnitude = self.magnitude[int(
                len(self.magnitude) * (1 - percentage)):]
            self.time = self.time[int(len(self.time) * (1 - percentage)):]
        elif direction == "right":
            self.magnitude = self.magnitude[:int(
                len(self.magnitude) * (1 - percentage))]
            self.time = self.time[:int(len(self.time) * (1 - percentage))]
        else:
            raise Exception("Direction must be left or right")

    def set_data(self, magnitude, time):
        """Sets the magnitdue and time of the signal"""
        self.magnitude = magnitude
        self.time = time
        if len(self.magnitude) != len(self.time):
            raise Exception("Signal must have the same length")
        if len(self.magnitude) != 0:
            self.fsample = len(self.magnitude)/time[-1]


class SignalProcessor():
    def __init__(self, filter_array, signal=Signal(), ):
        self.filter_array = filter_array
        self.original_signal = signal
        self.filtered_signal = []
        # self.filter_response = []
        # self.signal_response = []
        # self.magnitude_response = []
        # self.phase_response = []
        self.z_transform = []
