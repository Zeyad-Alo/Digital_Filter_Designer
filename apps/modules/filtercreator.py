import cmath
from numpy import conjugate
from scipy import signal as sg
from dataclasses import dataclass, asdict, field
import copy
import numpy as np


@dataclass
class Filter():
    filter_poles: list = field(default_factory=list, repr=True)
    filter_zeros: list = field(default_factory=list, repr=True)

    conjugate_enable: bool = field(default=False, repr=False)
    conjugate_poles: list = field(default_factory=list, repr=False)
    conjugate_zeros: list = field(default_factory=list, repr=False)
    sampling_freq: int = 600
    filter_type: str = field(default_factory=list, repr=False)

    numerator: list = field(default_factory=list, repr=False)
    denominator: list = field(default_factory=list, repr=False)

    w: list = field(default_factory=list, repr=False)
    filter_freq_response: list = field(
        default_factory=list, repr=False)
    filter_phase_response: list = field(
        default_factory=list, repr=False)
    filter_magnitude_response: list = field(
        default_factory=list, repr=False)

    def __post_init__(self):
        # check if filter already contains poles or zeros and update accordingly
        if len(self.filter_poles) > 0 or len(self.filter_zeros) > 0:
            self.update_filter_from_zeropole()

    # TODO dont forget to call this in the design tab???
    def update_filter_from_zeropole(self):
        '''Refresh filter variables from zeros and poles'''
        self.filter_magnitude_response = []
        self.filter_phase_response = []
        # update equation and return based on filter type and poles and zeros
        num, den = sg.zpk2tf(self.filter_zeros, self.filter_poles, 1)
        w, freq_resp = sg.freqz(num, den, self.sampling_freq)
        for h in freq_resp:
            freqs = cmath.polar(h)
            self.filter_magnitude_response.append(freqs[0])
            self.filter_phase_response.append(freqs[1])

        # update filter variables
        self.w = w
        self.numerator = num
        self.denominator = den
        self.filter_freq_response = freq_resp
        return

    # TODO CHECK IF ALL POLES HAVE A CONJUGATE OR NOT??

    def enable_conjugates(self, boolean: bool = False):
        self.conjugate_enable = boolean
        self.update_conjugates()

    def update_conjugates(self):
        if self.conjugate_enable:

            temp_poles = []
            temp_zeros = []

            # making filter_poles having the points and its conjugates
            for pole in self.filter_poles:
                if np.imag(pole) >= 0:
                    temp_poles.append(pole)

            temp_loop_poles = copy.copy(temp_poles)
            for pole in temp_loop_poles:
                if np.imag(pole) != 0:
                    temp_poles.append(conjugate(pole))

            self.filter_poles = temp_poles

            # making filter_zeros having the points and its conjugates
            for zero in self.filter_zeros:
                if np.imag(zero) >= 0:
                    temp_zeros.append(zero)

            temp_loop_zeros = copy.copy(temp_zeros)
            for zero in temp_loop_zeros:
                if np.imag(zero) != 0:
                    temp_zeros.append(conjugate(zero))

            self.filter_zeros = temp_zeros
        else:
            tmp_poles = copy.copy(self.filter_poles)
            for pole in tmp_poles:
                if np.imag(pole) < 0:
                    self.filter_poles.remove(pole)

            tmp_zeros = copy.copy(self.filter_zeros)
            for zero in tmp_zeros:
                if np.imag(zero) < 0:
                    self.filter_zeros.remove(zero)

        self.update_filter_from_zeropole()

    # ADDING A POLE OR A ZERO
# TODO  @NASSER bos 3ala el3azamaa

    def add_pole_zero(self, pole_or_zero, filter=[],filter_check=[]):
        if self.conjugate_enable:
            filter.append(pole_or_zero)
            self.update_conjugates()

        else:
            filter.append(pole_or_zero)

        if pole_or_zero in filter_check:
            self.Cancel_pole_zero(pole_or_zero)
        else:
            self.update_filter_from_zeropole()

    # DELETING A POLE OR A ZERO
# TODO  @NASSER bos 3ala el3azamaa
    def remove_pole_zero(self, pole_or_zero, filter):
        if self.conjugate_enable:
            filter.remove(pole_or_zero)
            filter.remove(conjugate(pole_or_zero))
        else:
            filter.remove(pole_or_zero)
        self.update_filter_from_zeropole()

    # TODO must work with conjugates and updaters

    def Cancel_pole_zero(self, pole_or_zero):
        self.filter_poles.remove(pole_or_zero)
        self.filter_zeros.remove(pole_or_zero)
        self.update_filter_from_zeropole()

    def edit_pole(self, pole, new_pole):
        for i in range(len(self.filter_poles)):

            # replace hardik with shardul
            if self.filter_poles[i] == pole:
                self.filter_poles[i] = new_pole
        self.update_conjugates()
        self.update_filter_from_zeropole()

    # TODO must work with conjugates and updaters
    def edit_zero(self, zero, new_zero):
        for i in range(len(self.filter_zeros)):

            # replace hardik with shardul
            if self.filter_zeros[i] == zero:
                self.filter_zeros[i] = new_zero
        self.update_conjugates()
        self.update_filter_from_zeropole()

    def clear_filter(self):
        self.filter_poles = []
        self.filter_zeros = []
        self.conjugate_poles = []
        self.conjugate_zeros = []
        self.update_filter_from_zeropole()

    def clear_poles(self):
        self.filter_poles = []
        self.conjugate_poles = []
        self.update_filter_from_zeropole()

    def clear_zeros(self):
        self.filter_zeros = []
        self.conjugate_zeros = []
        self.update_filter_from_zeropole()

    def filter_type(self):
        if len(self.filter_poles) == 0:
            self.filter_type = "FIR"
        else:
            self.filter_type = "IIR"

    def get_phase_response(self):
        return self.filter_phase_response, self.w

    # DONE
    def get_magnitude_response(self):
        return self.filter_magnitude_response, self.w

    # TODO @zeyad make this work with allpass filters, should store the modification in poles and zeros
    # and also in allpass zeros and poles to be able to remove them whenever we want to from the original poles and zeros
    def remove_allpass_filter(self, complex):
        z, p, k = sg.tf2zpk([-complex, 1.0], [1.0, -complex])
        self.filter_poles.remove(p)
        self.filter_zeros.remove(z)
        self.update_filter_from_zeropole()

    # TODO @zeyad make this work with allpass filters
    def add_allpass_filter(self, complex):
        z, p, k = sg.tf2zpk([-complex, 1.0], [1.0, -complex])

        self.filter_poles.append(p[0])
        self.filter_zeros.append(z[0])
        self.update_filter_from_zeropole()

    def filter_samples(self, samples):
        # filter signal

        filtered_samples = []

        filtered_samples = sg.lfilter(
            b=self.numerator, a=self.denominator, x=samples)

        return np.real(filtered_samples)

    def get_filter_dict(self):
        return asdict(self)

    def get_delay_count(self):
        dimension = max(len(self.denominator), len(self.numerator)) - 1
        return dimension
