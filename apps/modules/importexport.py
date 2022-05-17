# TODO: NEEDS REIMPLEMENTATION IN DASH/FLASK FRAMEWORK


# from PyQt5.QtWidgets import QFileDialog
# import numpy as np

# from modules.utility import print_debug
# from modules.curvefit import *
# from modules import curvefit
# import wfdb
# import csv

# MAX_SAMPLES = 300


# def browse_window(self):
#     """Open file dialog to select a file"""
#     self.graph_empty = False
#     self.filename = QFileDialog.getOpenFileName(
#         None, 'open the signal file', './', filter="Raw Data(*.hea *.dat *.csv *.txt *.xls)")
#     path = self.filename[0]
#     print_debug("Selected path: " + path)
#     open_file(self, path)


# def open_file(self, path):
#     """Open the file and read the data"""

#     temp_time = []
#     temp_magnitude = []
#     temp_fsample = 0

#     filetype = path[-3:]

#     if path == '' or filetype not in ['hea', 'dat', 'csv', 'txt', 'xls']:
#         print_debug("No file selected")
#         return

#     if filetype == "rec" or filetype == "dat" or filetype == "hea":

#         # open wfdb file
#         self.record = wfdb.rdrecord(path[:-4], channels=[0])

#         # update signal object
#         temp_magnitude = np.concatenate(
#             self.record.p_signal)

#         self.signal = Signal(magnitude=temp_magnitude, fsample=self.record.fs)

#     if filetype == "csv" or filetype == "txt" or filetype == "xls":
#         with open(path, 'r') as csvFile:    # 'r' its a mode for reading and writing
#             csvReader = csv.reader(csvFile, delimiter=',')
#             for line in csvReader:
#                 temp_magnitude.append(
#                     float(line[1]))
#                 temp_time.append(
#                     float(line[0]))
#         self.signal = Signal(magnitude=temp_magnitude, time=temp_time)

#     print_debug("Record loaded")

#     self.signal.set_max_samples(MAX_SAMPLES)
#     self.signal_processor = SignalProcessor(self.signal)

#     curvefit.update_graph(self)
