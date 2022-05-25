import math

class Filter():
    def __init__(self, name, type, poles=[], zeros=[]):
        self.name = name
        self.filter_type = None
        self.filter_poles = poles
        self.filter_zeros = zeros

    def add_pole(self, pole):
        self.filter_poles.append(pole)

    def add_zero(self, zero):
        self.filter_zeros.append(zero)

    def remove_pole(self, pole):
        self.filter_poles.remove(pole)

    def remove_zero(self, zero):
        self.filter_zeros.remove(zero)

    def edit_pole(self, pole, new_pole):
        self.filter_poles[pole] = new_pole

    def edit_zero(self, zero, new_zero):
        self.filter_zeros[zero] = new_zero

    def filter_type(self ,self.filter_poles, self.filter_zeros):
        if len(self.filter_poles) == 0:
            self.filter_type = "FIR"
        else :
            self.filter_type = "IIR"

    def get_magnitude_response(self):
        # update equation and return based on filter type and poles and zeros
        return self.filter_magnitude_response

    def get_phase_response(self):
        # update equation and return based on filter type and poles and zeros
        return self.filter_phase_response

    def get_impulse_response(self):
        # update equation and return based on filter type and poles and zeros
        return self.filter_equation

    def filter_samples(self, samples):
        # filter signal here using obtained impulse response equation
        filtered_samples = []
        return filtered_samples

    def generate_filter_file(self):
        # generate filter file.txt
        # contains coefficients of filter?? idk
        return None
    def system_gain(self):
        # calculating the gain of the system mag response
        pass


def plot_magnitude_response(filter_response):
    # plot filter response
    return None


def plot_phase_response(filter_response):
    # plot filter response
    return None


def plot_z_transform(filter_response):
    # plot zeros
    # plot poles
    # plot unit circle
    return None
