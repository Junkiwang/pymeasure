#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2017 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
import logging
from time import sleep
import numpy as np
from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import (
    strict_discrete_set,
    truncated_discrete_set,
    truncated_range,
    joined_validators
)
import re

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class KeysightN9020A(Instrument):
    """Keysight N9020A Spectrum Analyzer."""

    ###########
    #  Modes  #
    ###########
    instrument_mode = Instrument.control(
        ":INST:SEL?", ":INST:SEL %d",
        "Configuration for basic mode",
        validator= strict_discrete_set,
        values = ["SA", "RTSA", "SEQAN", "EMI", "BASIC", "WCDMA", "EDGEGSM", "WIMAXOFDMA",
                  "VSA", "PNOISE", "NFIGure", "ADEMOD", "Tooth", "TDSCDMA ", "CDMA2K",
                  "CDMA1XEV", "LTE", "LTETDD", "LTEAFDD", "LTEATDD", "MSR", "DVB", "DTMB",
                  "DCATV", "ISDBT", "CMMB", "WLAN", "CWLAN", "CWIMAXOFDM", "WIMAXFIXED",
                  "IDEN", "RLC", "SCPILC", "VSA89601"]
    )

    measure_mode = Instrument.control(
        ":CONF?", ":CONF %d",
        "Configuration for measure mode",
        validator= strict_discrete_set,
        values = ["SAN","ACP", "PVT", "CHP", "OBW", "SEM", "SPUR", "EVM", "PST", "MON", "WAV" ]
    )

    center_frequency = Instrument.control(
        ":FREQ:CENT?",
        "FREQ:CENT %g Hz",
        """Center Frequency property 
        """,
        validator=truncated_range,
        values=[100000,12000000000]
    )

    attenuator = Instrument.control(
        ":POW:ATT?",
        ":POW:ATT %g",
        """Set input attenuator(dB)  
        """,
        validator=truncated_range,
        values=[-100, 100]
    )

    def set_frequency_span(self, frequency_span):
        self.write(self.measure_mode + 'FREQ:SPAN ' + str(frequency_span) + ' Hz')
