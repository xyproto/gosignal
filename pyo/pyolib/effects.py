"""
Objects to perform specific audio signal processing effects such
as distortions, delays, chorus and reverbs.

"""

"""
Copyright 2010 Olivier Belanger

This file is part of pyo, a python module to help digital signal
processing script creation.

pyo is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyo is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyo.  If not, see <http://www.gnu.org/licenses/>.
"""
from _core import *
from _maps import *

class Disto(PyoObject):
    """
    Arc tangent distortion.

    Apply an arc tangent distortion with controllable drive to the input signal. 

    :Parent: :py:class:`PyoObject`

    :Args:

        input : PyoObject
            Input signal to process.
        drive : float or PyoObject, optional
            Amount of distortion applied to the signal, between 0 and 1. 
            Defaults to 0.75.
        slope : float or PyoObject, optional
            Slope of the lowpass filter applied after distortion, 
            between 0 and 1. Defaults to 0.5.

    >>> s = Server().boot()
    >>> s.start()
    >>> a = SfPlayer(SNDS_PATH + "/transparent.aif", loop=True)
    >>> lfo = Sine(freq=[.2,.25], mul=.5, add=.5)
    >>> d = Disto(a, drive=lfo, slope=.8, mul=.15).out()

    """
    def __init__(self, input, drive=.75, slope=.5, mul=1, add=0):
        PyoObject.__init__(self, mul, add)
        self._input = input
        self._drive = drive
        self._slope = slope
        self._in_fader = InputFader(input)
        in_fader, drive, slope, mul, add, lmax = convertArgsToLists(self._in_fader, drive, slope, mul, add)
        self._base_objs = [Disto_base(wrap(in_fader,i), wrap(drive,i), wrap(slope,i), wrap(mul,i), wrap(add,i)) for i in range(lmax)]

    def setInput(self, x, fadetime=0.05):
        """
        Replace the `input` attribute.
        
        :Args:

            x : PyoObject
                New signal to process.
            fadetime : float, optional
                Crossfade time between old and new input. Defaults to 0.05.

        """
        self._input = x
        self._in_fader.setInput(x, fadetime)
 
    def setDrive(self, x):
        """
        Replace the `drive` attribute.
        
        :Args:

            x : float or PyoObject
                New `drive` attribute.

        """
        self._drive = x
        x, lmax = convertArgsToLists(x)
        [obj.setDrive(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def setSlope(self, x):
        """
        Replace the `slope` attribute.
        
        :Args:

            x : float or PyoObject
                New `slope` attribute.

        """
        self._slope = x
        x, lmax = convertArgsToLists(x)
        [obj.setSlope(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def ctrl(self, map_list=None, title=None, wxnoserver=False):
        self._map_list = [SLMap(0., 1., 'lin', 'drive', self._drive),
                          SLMap(0., 0.999, 'lin', 'slope', self._slope),
                          SLMapMul(self._mul)]
        PyoObject.ctrl(self, map_list, title, wxnoserver)

    @property
    def input(self):
        """PyoObject. Input signal to process.""" 
        return self._input
    @input.setter
    def input(self, x): self.setInput(x)

    @property
    def drive(self):
        """float or PyoObject. Amount of distortion.""" 
        return self._drive
    @drive.setter
    def drive(self, x): self.setDrive(x)

    @property
    def slope(self):
        """float or PyoObject. Slope of the lowpass filter.""" 
        return self._slope
    @slope.setter
    def slope(self, x): self.setSlope(x)

class Delay(PyoObject):
    """
    Sweepable recursive delay.

    :Parent: :py:class:`PyoObject`

    :Args:

        input : PyoObject
            Input signal to delayed.
        delay : float or PyoObject, optional
            Delay time in seconds. Defaults to 0.25.
        feedback : float or PyoObject, optional
            Amount of output signal sent back into the delay line.
            Defaults to 0.
        maxdelay : float, optional
            Maximum delay length in seconds. Available only at initialization. 
            Defaults to 1.

    .. note::

        The minimum delay time allowed with Delay is one sample. It can be computed
        with :
            
        onesamp = 1.0 / s.getSamplingRate()
        
    .. seealso::
        
        :py:class:`SDelay`, :py:class:`Waveguide`

    >>> s = Server().boot()
    >>> s.start()
    >>> a = SfPlayer(SNDS_PATH + "/transparent.aif", loop=True, mul=.3).mix(2).out()
    >>> d = Delay(a, delay=[.15,.2], feedback=.5, mul=.4).out()

    """
    def __init__(self, input, delay=0.25, feedback=0, maxdelay=1, mul=1, add=0):
        PyoObject.__init__(self, mul, add)
        self._input = input
        self._delay = delay
        self._feedback = feedback
        self._maxdelay = maxdelay
        self._in_fader = InputFader(input)
        in_fader, delay, feedback, maxdelay, mul, add, lmax = convertArgsToLists(self._in_fader, delay, feedback, maxdelay, mul, add)
        self._base_objs = [Delay_base(wrap(in_fader,i), wrap(delay,i), wrap(feedback,i), wrap(maxdelay,i), wrap(mul,i), wrap(add,i)) for i in range(lmax)]

    def setInput(self, x, fadetime=0.05):
        """
        Replace the `input` attribute.
        
        :Args:

            x : PyoObject
                New signal to delayed.
            fadetime : float, optional
                Crossfade time between old and new input. Defaults to 0.05.

        """
        self._input = x
        self._in_fader.setInput(x, fadetime)

    def setDelay(self, x):
        """
        Replace the `delay` attribute.
        
        :Args:

            x : float or PyoObject
                New `delay` attribute.

        """
        self._delay = x
        x, lmax = convertArgsToLists(x)
        [obj.setDelay(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def setFeedback(self, x):
        """
        Replace the `feedback` attribute.
        
        :Args:

            x : float or PyoObject
                New `feedback` attribute.

        """
        self._feedback = x
        x, lmax = convertArgsToLists(x)
        [obj.setFeedback(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def reset(self):
        """
        Reset the memory buffer to zeros.
        
        """
        [obj.reset() for obj in self._base_objs]

    def ctrl(self, map_list=None, title=None, wxnoserver=False):
        self._map_list = [SLMap(0.001, self._maxdelay, 'log', 'delay',  self._delay),
                          SLMap(0., 1., 'lin', 'feedback', self._feedback),
                          SLMapMul(self._mul)]
        PyoObject.ctrl(self, map_list, title, wxnoserver)

    @property
    def input(self):
        """PyoObject. Input signal to delayed.""" 
        return self._input
    @input.setter
    def input(self, x): self.setInput(x)
 
    @property
    def delay(self):
        """float or PyoObject. Delay time in seconds.""" 
        return self._delay
    @delay.setter
    def delay(self, x): self.setDelay(x)

    @property
    def feedback(self):
        """float or PyoObject. Amount of output signal sent back into the delay line.""" 
        return self._feedback
    @feedback.setter
    def feedback(self, x): self.setFeedback(x)

class SDelay(PyoObject):
    """
    Simple delay without interpolation.

    :Parent: :py:class:`PyoObject`

    :Args:

        input : PyoObject
            Input signal to delayed.
        delay : float or PyoObject, optional
            Delay time in seconds. Defaults to 0.25.
        maxdelay : float, optional
            Maximum delay length in seconds. Available only at initialization. 
            Defaults to 1.

    .. seealso::
        
        :py:class:`Delay`, :py:class:`Delay1`

    >>> s = Server().boot()
    >>> s.start()
    >>> srPeriod = 1. / s.getSamplingRate()
    >>> dlys = [srPeriod * i * 5 for i in range(1, 7)]
    >>> a = SfPlayer(SNDS_PATH + "/transparent.aif", loop=True)
    >>> d = SDelay(a, delay=dlys, mul=.1).out(1)

    """
    def __init__(self, input, delay=0.25, maxdelay=1, mul=1, add=0):
        PyoObject.__init__(self, mul, add)
        self._input = input
        self._delay = delay
        self._maxdelay = maxdelay
        self._in_fader = InputFader(input)
        in_fader, delay, maxdelay, mul, add, lmax = convertArgsToLists(self._in_fader, delay, maxdelay, mul, add)
        self._base_objs = [SDelay_base(wrap(in_fader,i), wrap(delay,i), wrap(maxdelay,i), wrap(mul,i), wrap(add,i)) for i in range(lmax)]

    def setInput(self, x, fadetime=0.05):
        """
        Replace the `input` attribute.

        :Args:

            x : PyoObject
                New signal to process.
            fadetime : float, optional
                Crossfade time between old and new input. Defaults to 0.05.

        """
        self._input = x
        self._in_fader.setInput(x, fadetime)

    def setDelay(self, x):
        """
        Replace the `delay` attribute.

        :Args:

            x : float or PyoObject
                New `delay` attribute.

        """
        self._delay = x
        x, lmax = convertArgsToLists(x)
        [obj.setDelay(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def reset(self):
        """
        Reset the memory buffer to zeros.
        
        """
        [obj.reset() for obj in self._base_objs]

    def ctrl(self, map_list=None, title=None, wxnoserver=False):
        self._map_list = [SLMap(0.0001, self._maxdelay, 'log', 'delay',  self._delay),
                          SLMapMul(self._mul)]
        PyoObject.ctrl(self, map_list, title, wxnoserver)

    @property
    def input(self):
        """PyoObject. Input signal to delayed.""" 
        return self._input
    @input.setter
    def input(self, x): self.setInput(x)

    @property
    def delay(self):
        """float or PyoObject. Delay time in seconds.""" 
        return self._delay
    @delay.setter
    def delay(self, x): self.setDelay(x)

class Waveguide(PyoObject):
    """
    Basic waveguide model.

    This waveguide model consisting of one delay-line with a simple 
    lowpass filtering and lagrange interpolation.

    :Parent: :py:class:`PyoObject`

    :Args:

        input : PyoObject
            Input signal to process.
        freq : float or PyoObject, optional
            Frequency, in cycle per second, of the waveguide (i.e. the inverse 
            of delay time). Defaults to 100.
        dur : float or PyoObject, optional
            Duration, in seconds, for the waveguide to drop 40 dB below it's 
            maxima. Defaults to 10.
        minfreq : float, optional
            Minimum possible frequency, used to initialized delay length. 
            Available only at initialization. Defaults to 20.

    >>> s = Server().boot()
    >>> s.start()
    >>> sf = SfPlayer(SNDS_PATH + '/transparent.aif', speed=[.98,1.02], loop=True)
    >>> gt = Gate(sf, thresh=-24, risetime=0.005, falltime=0.01, lookahead=5, mul=.2)
    >>> w = Waveguide(gt, freq=[60,120.17,180.31,240.53], dur=20, minfreq=20, mul=.4).out()

    """
    def __init__(self, input, freq=100, dur=10, minfreq=20, mul=1, add=0):
        PyoObject.__init__(self, mul, add)
        self._input = input
        self._freq = freq
        self._dur = dur
        self._in_fader = InputFader(input)
        in_fader, freq, dur, minfreq, mul, add, lmax = convertArgsToLists(self._in_fader, freq, dur, minfreq, mul, add)
        self._base_objs = [Waveguide_base(wrap(in_fader,i), wrap(freq,i), wrap(dur,i), wrap(minfreq,i), wrap(mul,i), wrap(add,i)) for i in range(lmax)]

    def setInput(self, x, fadetime=0.05):
        """
        Replace the `input` attribute.
        
        :Args:

            x : PyoObject
                New signal to process.
            fadetime : float, optional
                Crossfade time between old and new input. Defaults to 0.05.

        """
        self._input = x
        self._in_fader.setInput(x, fadetime)

    def setFreq(self, x):
        """
        Replace the `freq` attribute.
        
        :Args:

            x : float or PyoObject
                New `freq` attribute.

        """
        self._freq = x
        x, lmax = convertArgsToLists(x)
        [obj.setFreq(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def setDur(self, x):
        """
        Replace the `dur` attribute.
        
        :Args:

            x : float or PyoObject
                New `dur` attribute.

        """
        self._dur = x
        x, lmax = convertArgsToLists(x)
        [obj.setDur(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def ctrl(self, map_list=None, title=None, wxnoserver=False):
        self._map_list = [SLMap(10, 500., 'log', 'freq',  self._freq),
                          SLMapDur(self._dur),
                          SLMapMul(self._mul)]
        PyoObject.ctrl(self, map_list, title, wxnoserver)

    @property
    def input(self):
        """PyoObject. Input signal to process.""" 
        return self._input
    @input.setter
    def input(self, x): self.setInput(x)
 
    @property
    def freq(self):
        """float or PyoObject. Frequency in cycle per second.""" 
        return self._freq
    @freq.setter
    def freq(self, x): self.setFreq(x)

    @property
    def dur(self):
        """float or PyoObject. Resonance duration in seconds.""" 
        return self._dur
    @dur.setter
    def dur(self, x): self.setDur(x)

class AllpassWG(PyoObject):
    """
    Out of tune waveguide model with a recursive allpass network.

    This waveguide model consisting of one delay-line with a 3-stages recursive
    allpass filter which made the resonances of the waveguide out of tune.

    :Parent: :py:class:`PyoObject`

    :Args:

        input : PyoObject
            Input signal to process.
        freq : float or PyoObject, optional
            Frequency, in cycle per second, of the waveguide (i.e. the inverse 
            of delay time). Defaults to 100.
        feed : float or PyoObject, optional
            Amount of output signal (between 0 and 1) sent back into the delay line.
            Defaults to 0.95.
        detune : float or PyoObject, optional
            Control the depth of the allpass delay-line filter, i.e. the depth of 
            the detuning. Should be in the range 0 to 1. Defaults to 0.5.
        minfreq : float, optional
            Minimum possible frequency, used to initialized delay length. 
            Available only at initialization. Defaults to 20.

    >>> s = Server().boot()
    >>> s.start()
    >>> sf = SfPlayer(SNDS_PATH + '/transparent.aif', speed=[.98,1.02], loop=True)
    >>> gt = Gate(sf, thresh=-24, risetime=0.005, falltime=0.01, lookahead=5, mul=.2)
    >>> rnd = Randi(min=.5, max=1.0, freq=[.13,.22,.155,.171])
    >>> rnd2 = Randi(min=.95, max=1.05, freq=[.145,.2002,.1055,.071])
    >>> fx = AllpassWG(gt, freq=rnd2*[74.87,75,75.07,75.21], feed=1, detune=rnd, mul=.15).out()

    """
    def __init__(self, input, freq=100, feed=0.95, detune=0.5, minfreq=20, mul=1, add=0):
        PyoObject.__init__(self, mul, add)
        self._input = input
        self._freq = freq
        self._feed = feed
        self._detune = detune
        self._in_fader = InputFader(input)
        in_fader, freq, feed, detune, minfreq, mul, add, lmax = convertArgsToLists(self._in_fader, freq, feed, detune, minfreq, mul, add)
        self._base_objs = [AllpassWG_base(wrap(in_fader,i), wrap(freq,i), wrap(feed,i), wrap(detune,i), wrap(minfreq,i), wrap(mul,i), wrap(add,i)) for i in range(lmax)]

    def setInput(self, x, fadetime=0.05):
        """
        Replace the `input` attribute.

        :Args:

            x : PyoObject
                New signal to process.
            fadetime : float, optional
                Crossfade time between old and new input. Defaults to 0.05.

        """
        self._input = x
        self._in_fader.setInput(x, fadetime)

    def setFreq(self, x):
        """
        Replace the `freq` attribute.

        :Args:

            x : float or PyoObject
                New `freq` attribute.

        """
        self._freq = x
        x, lmax = convertArgsToLists(x)
        [obj.setFreq(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def setFeed(self, x):
        """
        Replace the `feed` attribute.

        :Args:

            x : float or PyoObject
                New `feed` attribute.

        """
        self._feed = x
        x, lmax = convertArgsToLists(x)
        [obj.setFeed(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def setDetune(self, x):
        """
        Replace the `detune` attribute.

        :Args:

            x : float or PyoObject
                New `detune` attribute.

        """
        self._detune = x
        x, lmax = convertArgsToLists(x)
        [obj.setDetune(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def ctrl(self, map_list=None, title=None, wxnoserver=False):
        self._map_list = [SLMap(20., 500., 'log', 'freq',  self._freq),
                          SLMap(0., 1., 'lin', 'feed', self._feed),
                          SLMap(0., 1., 'lin', 'detune', self._detune),
                          SLMapMul(self._mul)]
        PyoObject.ctrl(self, map_list, title, wxnoserver)

    @property
    def input(self):
        """PyoObject. Input signal to process.""" 
        return self._input
    @input.setter
    def input(self, x): self.setInput(x)

    @property
    def freq(self):
        """float or PyoObject. Frequency in cycle per second.""" 
        return self._freq
    @freq.setter
    def freq(self, x): self.setFreq(x)

    @property
    def feed(self):
        """float or PyoObject. Amount of output signal sent back into the delay line.""" 
        return self._feed
    @feed.setter
    def feed(self, x): self.setFeed(x)

    @property
    def detune(self):
        """float or PyoObject. Depth of the detuning.""" 
        return self._detune
    @detune.setter
    def detune(self, x): self.setDetune(x)

class Freeverb(PyoObject):
    """
    Implementation of Jezar's Freeverb.

    Freeverb is a reverb unit generator based on Jezar's public domain 
    C++ sources, composed of eight parallel comb filters, followed by four 
    allpass units in series. Filters on each stream are slightly detuned 
    in order to create multi-channel effects.

    :Parent: :py:class:`PyoObject`

    :Args:

        input : PyoObject
            Input signal to process.
        size : float or PyoObject, optional
            Controls the length of the reverb,  between 0 and 1. A higher 
            value means longer reverb. Defaults to 0.5.
        damp : float or PyoObject, optional
            High frequency attenuation, between 0 and 1. A higher value 
            will result in a faster decay of the high frequency range. 
            Defaults to 0.5.
        bal : float or PyoObject, optional
            Balance between wet and dry signal, between 0 and 1. 0 means no 
            reverb. Defaults to 0.5.

    >>> s = Server().boot()
    >>> s.start()
    >>> a = SfPlayer(SNDS_PATH + "/transparent.aif", loop=True, mul=.4)
    >>> b = Freeverb(a, size=[.79,.8], damp=.9, bal=.3).out()

    """
    def __init__(self, input, size=.5, damp=.5, bal=.5, mul=1, add=0):
        PyoObject.__init__(self, mul, add)
        self._input = input
        self._size = size
        self._damp = damp
        self._bal = bal
        self._in_fader = InputFader(input)
        in_fader, size, damp, bal, mul, add, lmax = convertArgsToLists(self._in_fader, size, damp, bal, mul, add)
        self._base_objs = [Freeverb_base(wrap(in_fader,i), wrap(size,i), wrap(damp,i), wrap(bal,i), wrap(mul,i), wrap(add,i)) for i in range(lmax)]

    def setInput(self, x, fadetime=0.05):
        """
        Replace the `input` attribute.
        
        :Args:

            x : PyoObject
                New signal to process.
            fadetime : float, optional
                Crossfade time between old and new input. Defaults to 0.05.

        """
        self._input = x
        self._in_fader.setInput(x, fadetime)
 
    def setSize(self, x):
        """
        Replace the `size` attribute.
        
        :Args:

            x : float or PyoObject
                New `size` attribute.

        """
        self._size = x
        x, lmax = convertArgsToLists(x)
        [obj.setSize(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def setDamp(self, x):
        """
        Replace the `damp` attribute.
        
        :Args:

            x : float or PyoObject
                New `damp` attribute.

        """
        self._damp = x
        x, lmax = convertArgsToLists(x)
        [obj.setDamp(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def setBal(self, x):
        """
        Replace the `bal` attribute.
        
        :Args:

            x : float or PyoObject
                New `bal` attribute.

        """
        self._bal = x
        x, lmax = convertArgsToLists(x)
        [obj.setMix(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def ctrl(self, map_list=None, title=None, wxnoserver=False):
        self._map_list = [SLMap(0., 1., 'lin', 'size',  self._size),
                          SLMap(0., 1., 'lin', 'damp',  self._damp),
                          SLMap(0., 1., 'lin', 'bal',  self._bal),
                          SLMapMul(self._mul)]
        PyoObject.ctrl(self, map_list, title, wxnoserver)

    @property
    def input(self):
        """PyoObject. Input signal to process.""" 
        return self._input
    @input.setter
    def input(self, x): self.setInput(x)

    @property
    def size(self):
        """float or PyoObject. Room size.""" 
        return self._size
    @size.setter
    def size(self, x): self.setSize(x)

    @property
    def damp(self):
        """float or PyoObject. High frequency damping.""" 
        return self._damp
    @damp.setter
    def damp(self, x): self.setDamp(x)

    @property
    def bal(self):
        """float or PyoObject. Balance between wet and dry signal.""" 
        return self._bal
    @bal.setter
    def bal(self, x): self.setBal(x)

class Convolve(PyoObject):
    """
    Implements filtering using circular convolution.

    A circular convolution is defined as the integral of the product of two 
    functions after one is reversed and shifted.

    :Parent: :py:class:`PyoObject`

    :Args:

        input : PyoObject
            Input signal to process.
        table : PyoTableObject
            Table containning the impulse response.
        size : int
            Length, in samples, of the convolution. Available at initialization 
            time only. 
            
            If the table changes during the performance, its size must egal or 
            greater than this value. 
            
            If greater only the first `size` samples will be used.

    .. note::

        Convolution is very expensive to compute, so the impulse response must
        be kept very short to run in real time.

        Usually convolution generates a high amplitude level, take care of the
        `mul` parameter!
        
    .. seealso::
        
        :py:class:`Follower`

    >>> s = Server().boot()
    >>> s.start()
    >>> snd = SNDS_PATH + '/transparent.aif'
    >>> sf = SfPlayer(snd, speed=[.999,1], loop=True, mul=.25).out()
    >>> a = Convolve(sf, SndTable(SNDS_PATH+'/accord.aif'), size=512, mul=.2).out()

    """
    def __init__(self, input, table, size, mul=1, add=0):
        PyoObject.__init__(self, mul, add)
        self._input = input
        self._table = table
        self._size = size
        self._in_fader = InputFader(input)
        in_fader, table, size, mul, add, lmax = convertArgsToLists(self._in_fader, table, size, mul, add)                     
        self._base_objs = [Convolve_base(wrap(in_fader,i), wrap(table,i), wrap(size,i), wrap(mul,i), wrap(add,i)) for i in range(lmax)]

    def setInput(self, x, fadetime=0.05):
        """
        Replace the `input` attribute.
        
        :Args:

            x : PyoObject
                New signal to process.
            fadetime : float, optional
                Crossfade time between old and new input. Default to 0.05.

        """
        self._input = x
        self._in_fader.setInput(x, fadetime)

    def setTable(self, x):
        """
        Replace the `table` attribute.
        
        :Args:

            x : PyoTableObject
                new `table` attribute.
        
        """
        self._table = x
        x, lmax = convertArgsToLists(x)
        [obj.setTable(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    @property
    def input(self):
        """PyoObject. Input signal to filter.""" 
        return self._input
    @input.setter
    def input(self, x): self.setInput(x)

    @property
    def table(self):
        """PyoTableObject. Table containing the impulse response.""" 
        return self._table
    @table.setter
    def table(self, x): self.setTable(x)

class WGVerb(PyoObject):
    """
    8 delay line mono FDN reverb.

    8 delay line FDN reverb, with feedback matrix based upon physical 
    modeling scattering junction of 8 lossless waveguides of equal 
    characteristic impedance.

    :Parent: :py:class:`PyoObject`

    :Args:

        input : PyoObject
            Input signal to process.
        feedback : float or PyoObject, optional
            Amount of output signal sent back into the delay lines.
            Defaults to 0.5.

            0.6 gives a good small "live" room sound, 0.8 a small hall, 
            and 0.9 a large hall.
        cutoff : float or PyoObject, optional
            cutoff frequency of simple first order lowpass filters in the 
            feedback loop of delay lines, in Hz. Defaults to 5000.
        bal : float or PyoObject, optional
            Balance between wet and dry signal, between 0 and 1. 0 means no 
            reverb. Defaults to 0.5.

    >>> s = Server().boot()
    >>> s.start()
    >>> a = SfPlayer(SNDS_PATH + "/transparent.aif", loop=True)
    >>> d = WGVerb(a, feedback=[.74,.75], cutoff=5000, bal=.25, mul=.3).out()

    """
    def __init__(self, input, feedback=0.5, cutoff=5000, bal=0.5, mul=1, add=0):
        PyoObject.__init__(self, mul, add)
        self._input = input
        self._feedback = feedback
        self._cutoff = cutoff
        self._bal = bal
        self._in_fader = InputFader(input)
        in_fader, feedback, cutoff, bal, mul, add, lmax = convertArgsToLists(self._in_fader, feedback, cutoff, bal, mul, add)
        self._base_objs = [WGVerb_base(wrap(in_fader,i), wrap(feedback,i), wrap(cutoff,i), wrap(bal,i), wrap(mul,i), wrap(add,i)) for i in range(lmax)]

    def setInput(self, x, fadetime=0.05):
        """
        Replace the `input` attribute.
        
        :Args:

            x : PyoObject
                New signal to process.
            fadetime : float, optional
                Crossfade time between old and new input. Defaults to 0.05.

        """
        self._input = x
        self._in_fader.setInput(x, fadetime)

    def setFeedback(self, x):
        """
        Replace the `feedback` attribute.
        
        :Args:

            x : float or PyoObject
                New `feedback` attribute.

        """
        self._feedback = x
        x, lmax = convertArgsToLists(x)
        [obj.setFeedback(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def setCutoff(self, x):
        """
        Replace the `cutoff` attribute.
        
        :Args:

            x : float or PyoObject
                New `cutoff` attribute.

        """
        self._cutoff = x
        x, lmax = convertArgsToLists(x)
        [obj.setCutoff(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def setBal(self, x):
        """
        Replace the `bal` attribute.
        
        :Args:

            x : float or PyoObject
                New `bal` attribute.

        """
        self._bal = x
        x, lmax = convertArgsToLists(x)
        [obj.setMix(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def ctrl(self, map_list=None, title=None, wxnoserver=False):
        self._map_list = [SLMap(0., 1., 'lin', 'feedback', self._feedback),
                          SLMap(500., 15000., 'log', 'cutoff', self._cutoff),
                          SLMap(0., 1., 'lin', 'bal', self._bal),
                          SLMapMul(self._mul)]
        PyoObject.ctrl(self, map_list, title, wxnoserver)

    @property
    def input(self):
        """PyoObject. Input signal to process.""" 
        return self._input
    @input.setter
    def input(self, x): self.setInput(x)

    @property
    def feedback(self):
        """float or PyoObject. Amount of output signal sent back into the delay lines.""" 
        return self._feedback
    @feedback.setter
    def feedback(self, x): self.setFeedback(x)

    @property
    def cutoff(self):
        """float or PyoObject. Lowpass filter cutoff in Hz.""" 
        return self._cutoff
    @cutoff.setter
    def cutoff(self, x): self.setCutoff(x)

    @property
    def bal(self):
        """float or PyoObject. wet - dry balance.""" 
        return self._bal
    @bal.setter
    def bal(self, x): self.setBal(x)

class Chorus(PyoObject):
    """
    8 modulated delay lines chorus processor.

    A chorus effect occurs when individual sounds with roughly the same timbre and 
    nearly (but never exactly) the same pitch converge and are perceived as one.
    
    :Parent: :py:class:`PyoObject`

    :Args:

        input : PyoObject
            Input signal to process.
        depth : float or PyoObject, optional
            Chorus depth, between 0 and 5. Defaults to 1.
        feedback : float or PyoObject, optional
            Amount of output signal sent back into the delay lines.
            Defaults to 0.25.
        bal : float or PyoObject, optional
            Balance between wet and dry signals, between 0 and 1. 0 means no 
            chorus. Defaults to 0.5.

    >>> s = Server().boot()
    >>> s.start()
    >>> sf = SfPlayer(SNDS_PATH + '/transparent.aif', loop=True, mul=.5)
    >>> chor = Chorus(sf, depth=[1.5,1.6], feedback=0.5, bal=0.5).out()

    """
    def __init__(self, input, depth=1, feedback=0.25, bal=0.5, mul=1, add=0):
        PyoObject.__init__(self, mul, add)
        self._input = input
        self._depth = depth
        self._feedback = feedback
        self._bal = bal
        self._in_fader = InputFader(input)
        in_fader, depth, feedback, bal, mul, add, lmax = convertArgsToLists(self._in_fader, depth, feedback, bal, mul, add)
        self._base_objs = [Chorus_base(wrap(in_fader,i), wrap(depth,i), wrap(feedback,i), wrap(bal,i), wrap(mul,i), wrap(add,i)) for i in range(lmax)]

    def setInput(self, x, fadetime=0.05):
        """
        Replace the `input` attribute.

        :Args:

            x : PyoObject
                New signal to process.
            fadetime : float, optional
                Crossfade time between old and new input. Defaults to 0.05.

        """
        self._input = x
        self._in_fader.setInput(x, fadetime)

    def setDepth(self, x):
        """
        Replace the `depth` attribute.

        :Args:

            x : float or PyoObject
                New `depth` attribute.

        """
        self._depth = x
        x, lmax = convertArgsToLists(x)
        [obj.setDepth(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def setFeedback(self, x):
        """
        Replace the `feedback` attribute.

        :Args:

            x : float or PyoObject
                New `feedback` attribute.

        """
        self._feedback = x
        x, lmax = convertArgsToLists(x)
        [obj.setFeedback(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def setBal(self, x):
        """
        Replace the `bal` attribute.

        :Args:

            x : float or PyoObject
                New `bal` attribute.

        """
        self._bal = x
        x, lmax = convertArgsToLists(x)
        [obj.setMix(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def ctrl(self, map_list=None, title=None, wxnoserver=False):
        self._map_list = [SLMap(0., 5., 'lin', 'depth', self._depth),
                          SLMap(0., 1., 'lin', 'feedback', self._feedback),
                          SLMap(0., 1., 'lin', 'bal', self._bal),
                          SLMapMul(self._mul)]
        PyoObject.ctrl(self, map_list, title, wxnoserver)

    @property
    def input(self):
        """PyoObject. Input signal to process.""" 
        return self._input
    @input.setter
    def input(self, x): self.setInput(x)

    @property
    def depth(self):
        """float or PyoObject. Chorus depth, between 0 and 5.""" 
        return self._depth
    @depth.setter
    def depth(self, x): self.setDepth(x)

    @property
    def feedback(self):
        """float or PyoObject. Amount of output signal sent back into the delay lines.""" 
        return self._feedback
    @feedback.setter
    def feedback(self, x): self.setFeedback(x)

    @property
    def bal(self):
        """float or PyoObject. wet - dry balance.""" 
        return self._bal
    @bal.setter
    def bal(self, x): self.setBal(x)

class Harmonizer(PyoObject):
    """
    Generates harmonizing voices in synchrony with its audio input.

    :Parent: :py:class:`PyoObject`

    :Args:

        input : PyoObject
            Input signal to process.
        transpo : float or PyoObject, optional
           Transposition factor in semitone. Defaults to -7.0.
        feedback : float or PyoObject, optional
            Amount of output signal sent back into the delay line.
            Defaults to 0.
        winsize : float, optional
            Window size in seconds (max = 1.0). 
            Defaults to 0.1.

    >>> s = Server().boot()
    >>> s.start()
    >>> sf = SfPlayer(SNDS_PATH + '/transparent.aif', loop=True, mul=.3).out()
    >>> harm = Harmonizer(sf, transpo=-5, winsize=0.05).out(1)

    """
    def __init__(self, input, transpo=-7.0, feedback=0, winsize=0.1, mul=1, add=0):
        PyoObject.__init__(self, mul, add)
        self._input = input
        self._transpo = transpo
        self._feedback = feedback
        self._winsize = winsize
        self._in_fader = InputFader(input)
        in_fader, transpo, feedback, winsize, mul, add, lmax = convertArgsToLists(self._in_fader, transpo, feedback, winsize, mul, add)
        self._base_objs = [Harmonizer_base(wrap(in_fader,i), wrap(transpo,i), wrap(feedback,i), wrap(winsize,i), wrap(mul,i), wrap(add,i)) for i in range(lmax)]

    def setInput(self, x, fadetime=0.05):
        """
        Replace the `input` attribute.

        :Args:

            x : PyoObject
                New signal to process.
            fadetime : float, optional
                Crossfade time between old and new input. Defaults to 0.05.

        """
        self._input = x
        self._in_fader.setInput(x, fadetime)

    def setTranspo(self, x):
        """
        Replace the `transpo` attribute.

        :Args:

            x : float or PyoObject
                New `transpo` attribute.

        """
        self._transpo = x
        x, lmax = convertArgsToLists(x)
        [obj.setTranspo(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def setFeedback(self, x):
        """
        Replace the `feedback` attribute.

        :Args:

            x : float or PyoObject
                New `feedback` attribute.

        """
        self._feedback = x
        x, lmax = convertArgsToLists(x)
        [obj.setFeedback(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def setWinsize(self, x):
        """
        Replace the `winsize` attribute.

        :Args:

            x : float
                New `winsize` attribute.

        """
        self._winsize = x
        x, lmax = convertArgsToLists(x)
        [obj.setWinsize(wrap(x,i)) for i, obj in enumerate(self._base_objs)]

    def ctrl(self, map_list=None, title=None, wxnoserver=False):
        self._map_list = [SLMap(-24.0, 24.0, 'lin', 'transpo',  self._transpo),
                          SLMap(0., 1., 'lin', 'feedback', self._feedback),
                          SLMap(0.001, 1, 'log', 'winsize',  self._winsize, dataOnly=True),
                          SLMapMul(self._mul)]
        PyoObject.ctrl(self, map_list, title, wxnoserver)

    @property
    def input(self):
        """PyoObject. Input signal to delayed.""" 
        return self._input
    @input.setter
    def input(self, x): self.setInput(x)

    @property
    def transpo(self):
        """float or PyoObject. Transposition factor in semitone.""" 
        return self._transpo
    @transpo.setter
    def transpo(self, x): self.setTranspo(x)

    @property
    def feedback(self):
        """float or PyoObject. Amount of output signal sent back into the delay line.""" 
        return self._feedback
    @feedback.setter
    def feedback(self, x): self.setFeedback(x)

    @property
    def winsize(self):
        """float. Window size in seconds (max = 1.0).""" 
        return self._winsize
    @winsize.setter
    def winsize(self, x): self.setWinsize(x)

class Delay1(PyoObject):
    """
    Delays a signal by one sample.
 
    :Parent: :py:class:`PyoObject`
   
    :Args:
    
        input : PyoObject
            Input signal to process.
    
    >>> s = Server().boot()
    >>> s.start()
    >>> # 50th order FIR lowpass filter
    >>> order = 50
    >>> objs = [Noise(.3)]
    >>> for i in range(order):
    ...     objs.append(Delay1(objs[-1], add=objs[-1]))
    ...     objs.append(objs[-1] * 0.5)    
    >>> out = Sig(objs[-1]).out()

    """
    def __init__(self, input, mul=1, add=0):
        PyoObject.__init__(self, mul, add)
        self._input = input
        self._in_fader = InputFader(input)
        in_fader, mul, add, lmax = convertArgsToLists(self._in_fader, mul, add)
        self._base_objs = [Delay1_base(wrap(in_fader,i), wrap(mul,i), wrap(add,i)) for i in range(lmax)]

    def setInput(self, x, fadetime=0.05):
        """
        Replace the `input` attribute.
        
        :Args:

            x : PyoObject
                New signal to process.
            fadetime : float, optional
                Crossfade time between old and new input. Default to 0.05.

        """
        self._input = x
        self._in_fader.setInput(x, fadetime)

    @property
    def input(self):
        """PyoObject. Input signal to delayed.""" 
        return self._input
    @input.setter
    def input(self, x): self.setInput(x)

class STRev(PyoObject):
    """
    Stereo reverb.

    Stereo reverb based on WGVerb (8 delay line FDN reverb). A mono
    input will produce two audio streams, left and right channels.
    Therefore, a stereo input will produce four audio streams, left
    and right channels for each input channel. Position of input 
    streams can be set with the `inpos` argument. To achieve a stereo
    reverb, delay line lengths are slightly differents on both channels,
    but also, pre-delays length and filter cutoff of both channels will 
    be affected to reflect the input position. 

    :Parent: :py:class:`PyoObject`

    :Args:

        input : PyoObject
            Input signal to process.
        inpos : float or PyoObject, optional
            Position of the source, between 0 and 1. 0 means fully left
            and 1 means fully right. Defaults to 0.5.
        revtime : float or PyoObject, optional
            Duration, in seconds, of the reverberated sound, defined as 
            the time needed to the sound to drop 40 dB below its peak. 
            Defaults to 1.
        cutoff : float or PyoObject, optional
            cutoff frequency, in Hz, of a first order lowpass filters in the 
            feedback loop of delay lines. Defaults to 5000.
        bal : float or PyoObject, optional
            Balance between wet and dry signal, between 0 and 1. 0 means no 
            reverb. Defaults to 0.5.
        roomSize : float, optional
            Delay line length scaler, between 0.25 and 4. Values higher than
            1 make the delay lines longer and simulate larger rooms. Defaults to 1.
        firstRefGain : float, optional
            Gain, in dB, of the first reflexions of the room. Defaults to -3.

    >>> s = Server().boot()
    >>> s.start()
    >>> t = SndTable(SNDS_PATH + "/transparent.aif")
    >>> sf = Looper(t, dur=t.getDur()*2, xfade=0, mul=0.5)
    >>> rev = STRev(sf, inpos=0.25, revtime=2, cutoff=5000, bal=0.25, roomSize=1).out()

    """
    def __init__(self, input, inpos=0.5, revtime=1, cutoff=5000, bal=.5, roomSize=1, firstRefGain=-3, mul=1, add=0):
        PyoObject.__init__(self, mul, add)
        self._input = input
        self._inpos = inpos
        self._revtime = revtime
        self._cutoff = cutoff
        self._bal = bal
        self._roomSize = roomSize
        self._firstRefGain = firstRefGain
        self._in_fader = InputFader(input)
        in_fader, inpos, revtime, cutoff, bal, roomSize, firstRefGain, mul, add, lmax = convertArgsToLists(self._in_fader, inpos, revtime, cutoff, bal, roomSize, firstRefGain, mul, add)
        self._base_players = [STReverb_base(wrap(in_fader,i), wrap(inpos,i), wrap(revtime,i), wrap(cutoff,i), wrap(bal,i), wrap(roomSize,i), wrap(firstRefGain,i)) for i in range(lmax)]
        self._base_objs = [STRev_base(wrap(self._base_players,i), j, wrap(mul,i), wrap(add,i)) for i in range(lmax) for j in range(2)]

    def setInput(self, x, fadetime=0.05):
        """
        Replace the `input` attribute.
        
        :Args:

            x : PyoObject
                New signal to process.
            fadetime : float, optional
                Crossfade time between old and new input. Defaults to 0.05.

        """
        self._input = x
        self._in_fader.setInput(x, fadetime)

    def setInpos(self, x):
        """
        Replace the `inpos` attribute.
        
        :Args:

            x : float or PyoObject
                New `inpos` attribute.

        """
        self._inpos = x
        x, lmax = convertArgsToLists(x)
        [obj.setInpos(wrap(x,i)) for i, obj in enumerate(self._base_players)]
 
    def setRevtime(self, x):
        """
        Replace the `revtime` attribute.
        
        :Args:

            x : float or PyoObject
                New `revtime` attribute.

        """
        self._revtime = x
        x, lmax = convertArgsToLists(x)
        [obj.setRevtime(wrap(x,i)) for i, obj in enumerate(self._base_players)]

    def setCutoff(self, x):
        """
        Replace the `cutoff` attribute.
        
        :Args:

            x : float or PyoObject
                New `cutoff` attribute.

        """
        self._cutoff = x
        x, lmax = convertArgsToLists(x)
        [obj.setCutoff(wrap(x,i)) for i, obj in enumerate(self._base_players)]

    def setBal(self, x):
        """
        Replace the `bal` attribute.
        
        :Args:

            x : float or PyoObject
                New `bal` attribute.

        """
        self._bal = x
        x, lmax = convertArgsToLists(x)
        [obj.setMix(wrap(x,i)) for i, obj in enumerate(self._base_players)]

    def setRoomSize(self, x):
        """
        Set the room size scaler, between 0.25 and 4.
        
        :Args:

            x : float
                Room size scaler, between 0.25 and 4.0.

        """
        self._roomSize = x
        x, lmax = convertArgsToLists(x)
        [obj.setRoomSize(wrap(x,i)) for i, obj in enumerate(self._base_players)]

    def setFirstRefGain(self, x):
        """
        Set the gain of the first reflexions.
        
        :Args:

            x : float
                Gain, in dB, of the first reflexions.

        """
        self._firstRefGain = x
        x, lmax = convertArgsToLists(x)
        [obj.setFirstRefGain(wrap(x,i)) for i, obj in enumerate(self._base_players)]

    def ctrl(self, map_list=None, title=None, wxnoserver=False):
        self._map_list = [SLMap(0., 1., 'lin', 'inpos',  self._inpos),
                          SLMap(0.01, 120., 'log', 'revtime',  self._revtime),
                          SLMap(500., 15000., 'log', 'cutoff',  self._cutoff),
                          SLMap(0., 1., 'lin', 'bal',  self._bal),
                          SLMap(0.25, 4., 'lin', 'roomSize',  self._roomSize, dataOnly=True),
                          SLMap(-48, 12, 'lin', 'firstRefGain', self._firstRefGain, dataOnly=True),
                          SLMapMul(self._mul)]
        PyoObject.ctrl(self, map_list, title, wxnoserver)

    @property
    def input(self):
        """PyoObject. Input signal to process.""" 
        return self._input
    @input.setter
    def input(self, x): self.setInput(x)

    @property
    def inpos(self):
        """float or PyoObject. Position of the source.""" 
        return self._inpos
    @inpos.setter
    def inpos(self, x): self.setInpos(x)

    @property
    def revtime(self):
        """float or PyoObject. Room size.""" 
        return self._revtime
    @revtime.setter
    def revtime(self, x): self.setRevtime(x)

    @property
    def cutoff(self):
        """float or PyoObject. High frequency damping.""" 
        return self._cutoff
    @cutoff.setter
    def cutoff(self, x): self.setCutoff(x)

    @property
    def bal(self):
        """float or PyoObject. Balance between wet and dry signal.""" 
        return self._bal
    @bal.setter
    def bal(self, x): self.setBal(x)

    @property
    def roomSize(self):
        """float. Room size scaler, between 0.25 and 4.0.""" 
        return self._roomSize
    @roomSize.setter
    def roomSize(self, x): self.setRoomSize(x)

    @property
    def firstRefGain(self):
        """float. Gain, in dB, of the first reflexions.""" 
        return self._firstRefGain
    @firstRefGain.setter
    def firstRefGain(self, x): self.setFirstRefGain(x)
