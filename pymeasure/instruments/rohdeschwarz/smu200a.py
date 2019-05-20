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

from pymeasure.instruments import Instrument, discreteTruncate, RangeException


class SMU200A(Instrument):
    """ Represents the R&S Signal Generator SMU200A with two output port
    """
    port1_power = Instrument.control(
        ":SOUR1:POW?;", ":SOUR1:POW %g dBm;",
        """ A floating point property that represents the output power
        in dBm. This property can be set. """
    )

    port1_frequency = Instrument.control(
        ":SOUR1:FREQ?;", ":SOUR1:FREQ  %e Hz;",
        """ A floating point property that represents the output frequency
        in Hz. This property can be set. """
    )

    port2_power = Instrument.control(
        ":SOUR1:POW?;", ":SOUR1:POW %g dBm;",
        """ A floating point property that represents the output power
        in dBm. This property can be set. """
    )

    port2_frequency = Instrument.control(
        ":SOUR1:FREQ?;", ":SOUR1:FREQ  %e Hz;",
        """ A floating point property that represents the output frequency
        in Hz. This property can be set. """
    )

    def __init__(self, resourceName, **kwargs):
        super(SMU200A, self).__init__(
            resourceName,
            "R&S Signal Generator SMU200A ",
            **kwargs
        )


    def loadwavefile(self, port = 1, filepath = "C://wave/lte500.wav"):
        """Load wave file to modulation port
        """
        self.write(":SOUR" + str(port) + ":BB:ARB:WAV:SEL '" + str(filepath) + "'")

    @property
    def port1_modulation_state(self):
        """Port1 modulation state
        """
        return ':SOUR1:BB:ARB:STAT?' == 1

    @port1_modulation_state.setter
    def port1_modulation_state(self,value):
        if value:
            self.write(":SOUR1:BB:ARB:STAT ON")
        else:
            self.write(":SOUR1:BB:ARB:STAT OFF")

    @property
    def port2_modulation_state(self):
        """Port1 modulation state
        """
        return ':SOUR2:BB:ARB:STAT?' == 1

    @port2_modulation_state.setter
    def port2_modulation_state(self, value):
        if value:
            self.write(":SOUR2:BB:ARB:STAT ON")
        else:
            self.write(":SOUR2:BB:ARB:STAT OFF")

    def enable_modulation(self, port):
        if port == 1:
            self.port1_modulation_state = True
        else:
            self.port2_modulation_state = True

    def disable_modulation(self, port):
        if port == 1:
            self.port1_modulation_state = False
        else:
            self.port2_modulation_state = False

    @property
    def port1_output(self):
        """ A boolean property that represents the signal output state.
        This property can be set to control the output.
        """
        return int(self.ask(":OUTP1?")) == 1

    @port1_output.setter
    def port1_output(self, value):
        if value:
            self.write(":OUTP1 ON")
        else:
            self.write(":OUTP1 OFF")

    @property
    def port2_output(self):
        """ A boolean property that represents the signal output state.
        This property can be set to control the output.
        """
        return int(self.ask(":OUTP2?")) == 1

    @port2_output.setter
    def port2_output(self, value):
        if value:
            self.write(":OUTP2 ON")
        else:
            self.write(":OUTP2 OFF")

    def enable(self, port = 1):
        """ Enables the signal output.
        """
        if port == 1:
            self.port1_output = True
        else:
            self.port2_output = True

    def disable(self, port = 1):
        """ Disables the signal output.
        """
        if port == 1:
            self.port1_output = False
        else:
            self.port2_output = False

    def shutdown(self):
        """ Shuts down the instrument, putting it in a safe state.
        """
        self.disable_modulation(1)
        self.disable_modulation(2)
        self.disable(1)
        self.disable(2)