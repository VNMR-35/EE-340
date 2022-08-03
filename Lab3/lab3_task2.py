#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Lab 3 Task 2
# Author: Vinamra
# GNU Radio version: v3.8.2.0-57-gd71cd177

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import blocks
import pmt
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation

from gnuradio import qtgui

class lab3_task2(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Lab 3 Task 2")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Lab 3 Task 2")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "lab3_task2")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 44100

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=44100,
                decimation=5000000,
                taps=None,
                fractional_bw=None)
        self.low_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                10,
                5000000,
                30000,
                20000,
                firdes.WIN_HAMMING,
                6.76))
        self.iir_filter_xxx_0_0 = filter.iir_filter_ffd([1,-1], [1], True)
        self.iir_filter_xxx_0 = filter.iir_filter_ffd([1,-1], [1], True)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink('C:\\Users\\vinam\\Documents\\Semester_5\\EE 340\\Lab3\\task2.wav', 1, samp_rate, 8)
        self.blocks_transcendental_0 = blocks.transcendental('sqrt', "float")
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_multiply_xx_1_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_1 = blocks.multiply_vff(1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, 'C:\\Users\\vinam\\Documents\\Semester_5\\EE 340\\Lab3\\task1.dat', False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_abs_xx_0 = blocks.abs_ff(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_abs_xx_0, 0), (self.blocks_transcendental_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_multiply_xx_1_0, 1))
        self.connect((self.blocks_complex_to_real_0, 0), (self.iir_filter_xxx_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_multiply_xx_1_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_abs_xx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.blocks_transcendental_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.iir_filter_xxx_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.iir_filter_xxx_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.iir_filter_xxx_0, 0), (self.iir_filter_xxx_0_0, 0))
        self.connect((self.iir_filter_xxx_0_0, 0), (self.blocks_multiply_xx_1_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_throttle_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "lab3_task2")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)





def main(top_block_cls=lab3_task2, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
