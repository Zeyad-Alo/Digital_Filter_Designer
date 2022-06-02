import cmath
from numpy import conjugate
from scipy import signal as sg
from dataclasses import dataclass, asdict, field
import copy


@dataclass
class Filter():
    filter_poles: list = field(default_factory=list, repr=True)
    filter_zeros: list = field(default_factory=list, repr=True)

    conjugate_enable: bool = field(default=False, repr=False)
    conjugate_poles: list = field(default_factory=list, repr=False)
    conjugate_zeros: list = field(default_factory=list, repr=False)
    sampling_freq: int = 44100
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

    def update_conjugates(self):
        if self.conjugate_enable:
            
            self.filter_pole_new=list(set(self.filter_poles).symmetric_difference(set(self.conjugate_poles)))
            self.filter_zeros_new=list(set(self.filter_zeros).symmetric_difference(set(self.conjugate_zeros)))
        
            temp_filter_poles=copy.copy(self.filter_poles)
            temp_filter_zeros=copy.copy(self.filter_zeros)

            for pole in temp_filter_poles:
                self.add_conjugate('Pole', pole)
            for zero in  temp_filter_zeros:
                self.add_conjugate('Zero', zero)
        else:
            for pole in self.conjugate_poles:
                self.filter_poles.remove(pole)
            for zero in self.conjugate_zeros:
                self.filter_zeros.remove(zero)

            self.conjugate_poles = []
            self.conjugate_zeros = []

        self.update_filter_from_zeropole()

    # TODO

    def add_pole(self, pole):
        if self.conjugate_enable:
            # self.add_conjugate(pole)
            self.filter_poles.append(pole)
            self.update_conjugates()
        else:
            self.filter_poles.append(pole)
        self.update_filter_from_zeropole()
        # self.update_conjugates()

    # TODO
    def add_zero(self, zero):
        if self.conjugate_enable:
            # self.add_conjugate(zero)
            self.filter_zeros.append(zero)
            self.update_conjugates()

        else:
            self.filter_zeros.append(zero)
        self.update_filter_from_zeropole()

    # TODO
    def add_conjugate(self, pole_zero='Pole', input=None):
        print("entered  add_conjgate    aaaaaa ")
        if pole_zero == 'Pole':
            # if input is None:
            #     return
            self.conjugate_poles.append(conjugate(input))
            self.filter_poles.append(conjugate(input))
            return
        elif pole_zero == 'Zero':
            # if input is None:
            #     return
            self.conjugate_zeros.append(conjugate(input))
            self.filter_zeros.append(conjugate(input))
            return
    # DONE

    def enable_conjugates(self, boolean: bool = False):
        self.conjugate_enable = boolean
        self.update_conjugates()

    # TODO must work with conjugates

    def remove_pole(self, pole):
        self.filter_poles.remove(pole)
        self.update_conjugates()

    # TODO must work with conjugates
    def remove_zero(self, zero):
        self.filter_zeros.remove(zero)
        self.update_conjugates()

    # TODO
    def remove_conjugate(self, polezero='Pole', input=None):
        if polezero == 'Pole':
            # if input is None:
            #     return
            self.conjugate_poles.remove(input)
            self.filter_poles.remove(input)
        elif polezero == 'Zero':
            # if input is None:
            #     return
            self.conjugate_zeros.remove(input)
            self.filter_zeros.remove(input)

    # TODO must work with conjugates and updaters
    def edit_pole(self, pole, new_pole):
        self.filter_poles[pole] = new_pole
        self.update_filter_from_zeropole()

    # TODO must work with conjugates and updaters
    def edit_zero(self, zero, new_zero):
        self.filter_zeros[zero] = new_zero
        self.update_filter_from_zeropole()

    def filter_type(self):
        if len(self.filter_poles) == 0:
            self.filter_type = "FIR"
        else:
            self.filter_type = "IIR"
    

# Clears the filter   
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
        # filter signal here using obtained impulse response equation
        filtered_samples = []
        return filtered_samples

    def get_filter_dict(self):
        return asdict(self)
