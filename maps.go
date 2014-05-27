package gosignal

import (
	"math"
)

const (
	LOG_SCALE = true
	LIN_SCALE = false
)

type ScaleType bool

type Map struct {
	min, max float64
	scale    ScaleType
}

// Map object for converting a value between 0 and 1 on a logarithmic or linear scale.
func NewMap(min, max float64, scale ScaleType) *Map {
	return &Map{min, max, scale}
}

// Takes 'x' between 0 and 1 and returns a scaled value.
func (m *Map) Get(x float64) float64 {
	// Clamp
	if x < 0 {
		x = 0.0
	} else if x > 1 {
		x = 1.0
	}

	if m.scale == LOG_SCALE {
		return math.Pow(10, x*math.Log10(m.max/m.min)+math.Log10(m.min))
	}
	return (m.max-m.min)*x + m.min
}

// Takes 'x' in the real range and returns value unscaled (between 0 and 1).
func (m *Map) Set(x float64) float64 {
	if m.scale == LOG_SCALE {
		return math.Log10(x/m.min) / math.Log10(m.max/m.min)
	}
	return (x - m.min) / (m.max - m.min)
}

// Set the 'min' attribute.
func (m *Map) SetMin(min float64) {
	m.min = min
}

// Set the 'max' attribute.
func (m *Map) SetMax(max float64) {
	m.max = max
}

// Set the 'scale' attribute.
func (m *Map) SetScale(scale ScaleType) {
	m.scale = scale
}

// To fullfill the Property interface. (@property decorator)
// Returns the lowest value of the range.
func (m *Map) PropertyMin() float64 {
	return m.min
}

// To fullfill the Property interface. (@property decorator)
// Returns the highest value of the range.
func (m *Map) PropertyMax() float64 {
	return m.max
}

// To fullfill the Setter interface. (@min.setter decorator)
// Sets the lowerst value of the range.
func (m *Map) SetterMin(x float64) {
	m.SetMin(x)
}

// To fullfill the Setter interface. (@max.setter decorator)
func (m *Map) SetterMax(x float64) {
	m.SetMax(x)
}

// To fullfill the Property interface. (@property decorator)
// SCALE_LOG or SCALE_LIN scale.
func (m *Map) PropertyScale() ScaleType {
	return m.scale
}

// To fullfill the Setter interface. (@scale.setter decorator)
func (m *Map) SetterScale(scale ScaleType) {
	m.scale = scale
}

/*

class SLMap(Map):
    """
    Base Map class used to manage control sliders.

    Derived from Map class, a few parameters are added for sliders
    initialization.

    :Parent: :py:class:`Map`

    :Args:

        min : int or float
            Smallest value of the range.
        max : int or float
            Highest value of the range.
        scale : string {'lin', 'log'}
            Method used to scale the input value on the specified range.
        name : string
            Name of the attributes the slider is affected to.
        init : int or float
            Initial value. Specified in the real range, not between 0 and 1. Use
            the `set` method to retreive the normalized corresponding value.
        res : string {'int', 'float'}, optional
            Sets the resolution of the slider. Defaults to 'float'.
        ramp : float, optional
            Ramp time, in seconds, used to smooth the signal sent from slider
            to object's attribute. Defaults to 0.025.
        dataOnly : boolean, optional
            Set this argument to True if the parameter does not accept audio
            signal as control but discreet values. If True, label will be
            marked with a star symbol (*). Defaults to False.

    >>> s = Server().boot()
    >>> s.start()
    >>> ifs = [350,360,375,388]
    >>> maps = [SLMap(20., 2000., 'log', 'freq', ifs), SLMap(0, 0.25, 'lin', 'feedback', 0), SLMapMul(.1)]
    >>> a = SineLoop(freq=ifs, mul=.1).out()
    >>> a.ctrl(maps)

    """
    def __init__(self, min, max, scale, name, init, res='float', ramp=0.025, dataOnly=False):
        Map.__init__(self, min, max, scale)
        self._name, self._init, self._res, self._ramp, self._dataOnly = name, init, res, ramp, dataOnly

    @property
    def name(self):
        """string. Name of the parameter to control."""
        return self._name
    @property
    def init(self):
        """float. Initial value of the slider."""
        return self._init
    @property
    def res(self):
        """string. Slider resolution {int or float}."""
        return self._res
    @property
    def ramp(self):
        """float. Ramp time in seconds."""
        return self._ramp
    @property
    def dataOnly(self):
        """boolean. True if argument does not accept audio stream."""
        return self._dataOnly

class SLMapFreq(SLMap):
    """
    SLMap with normalized values for a 'freq' slider.

    :Parent: :py:class:`SLMap`

    :Args:

        init : int or float, optional
            Initial value. Specified in the real range, not between 0 and 1.
            Defaults to 1000.

    .. note::

        SLMapFreq values are:

        - min = 20.0
        - max = 20000.0
        - scale = 'log'
        - name = 'freq'
        - res = 'float'
        - ramp = 0.025

    """
    def __init__(self, init=1000):
        SLMap.__init__(self, 20., 20000., 'log', 'freq', init, 'float', 0.025)

class SLMapMul(SLMap):
    """
    SLMap with normalized values for a 'mul' slider.

    :Parent: :py:class:`SLMap`

    :Args:

        init : int or float, optional
            Initial value. Specified in the real range, not between 0 and 1.
            Defaults to 1.

    .. note::

        SLMapMul values are:

        - min = 0.0
        - max = 2.0
        - scale = 'lin'
        - name = 'mul'
        - res = 'float'
        - ramp = 0.025

    """
    def __init__(self, init=1.):
        SLMap.__init__(self, 0., 2., 'lin', 'mul', init, 'float', 0.025)

class SLMapPhase(SLMap):
    """
    SLMap with normalized values for a 'phase' slider.

    :Parent: :py:class:`SLMap`

    :Args:

        init : int or float, optional
            Initial value. Specified in the real range, not between 0 and 1.
            Defaults to 0.

    .. note::

        SLMapPhase values are:

        - min = 0.0
        - max = 1.0
        - scale = 'lin'
        - name = 'phase'
        - res = 'float'
        - ramp = 0.025

    """
    def __init__(self, init=0.):
        SLMap.__init__(self, 0., 1., 'lin', 'phase', init, 'float', 0.025)

class SLMapPan(SLMap):
    """
    SLMap with normalized values for a 'pan' slider.

    :Parent: :py:class:`SLMap`

    :Args:

        init : int or float, optional
            Initial value. Specified in the real range, not between 0 and 1.
            Defaults to 0.

    .. note::

        SLMapPhase values are:

        - min = 0.0
        - max = 1.0
        - scale = 'lin'
        - name = 'pan'
        - res = 'float'
        - ramp = 0.025

    """
    def __init__(self, init=0.):
        SLMap.__init__(self, 0., 1., 'lin', 'pan', init, 'float', 0.025)

class SLMapQ(SLMap):
    """
    SLMap with normalized values for a 'q' slider.

    :Parent: :py:class:`SLMap`

    :Args:

        init : int or float, optional
            Initial value. Specified in the real range, not between 0 and 1.
            Defaults to 1.

    .. note::

        SLMapQ values are:

        - min = 0.1
        - max = 100.0
        - scale = 'log'
        - name = 'q'
        - res = 'float'
        - ramp = 0.025

    """
    def __init__(self, init=1.):
        SLMap.__init__(self, 0.1, 100., 'log', 'q', init, 'float', 0.025)

class SLMapDur(SLMap):
    """
    SLMap with normalized values for a 'dur' slider.

    :Parent: :py:class:`SLMap`

    :Args:

        init : int or float, optional
            Initial value. Specified in the real range, not between 0 and 1.
            Defaults to 1.

    .. note::

        SLMapDur values are:

        - min = 0.
        - max = 60.0
        - scale = 'lin'
        - name = 'dur'
        - res = 'float'
        - ramp = 0.025

    """
    def __init__(self, init=1.):
        SLMap.__init__(self, 0., 60., 'lin', 'dur', init, 'float', 0.025)

*/
