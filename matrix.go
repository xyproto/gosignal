package gosignal

/*

class NewMatrix(PyoMatrixObject):
    """
    Create a new matrix ready for recording.

    Optionally, the matrix can be filled with the contents of the 
    `init` parameter.

    See :py:class:`MatrixRec` to write samples in the matrix.

    :Parent: :py:class:`PyoMatrixObject`

    :Args:

        width : int
            Desired matrix width in samples.
        height : int
            Desired matrix height in samples.
        init : list of list of floats, optional
            Initial matrix. Defaults to None.

    .. seealso:: 
        
        :py:class:`MatrixRec`

    >>> s = Server().boot()
    >>> s.start()
    >>> SIZE = 256
    >>> mm = NewMatrix(SIZE, SIZE)
    >>> mm.genSineTerrain(freq=2, phase=16)
    >>> lfw = Sine([.1,.11], 0, .124, .25)
    >>> lfh = Sine([.15,.16], 0, .124, .25)
    >>> w = Sine(100, 0, lfw, .5)
    >>> h = Sine(10.5, 0, lfh, .5)
    >>> c = MatrixPointer(mm, w, h, mul=.2).out()

    """
    def __init__(self, width, height, init=None):
        PyoMatrixObject.__init__(self)
        self._size = (width, height)
        if init == None:
            self._base_objs = [NewMatrix_base(width, height)]
        else:
            self._base_objs = [NewMatrix_base(width, height, init)]
            
    def replace(self, x):
        """
        Replaces the actual matrix.
        
        :Args:
        
            x : list of list of floats
                New matrix. Must be of the same size as the actual matrix.

        """
        [obj.setMatrix(x) for obj in self._base_objs]
        self.refreshView()

    def getRate(self):
        """
        Returns the frequency (cycle per second) to give to an 
        oscillator to read the sound at its original pitch.
        
        """
        return self._base_objs[0].getRate()

    def genSineTerrain(self, freq=1, phase=0.0625):
        """
        Generates a modulated sinusoidal terrain.

        :Args:

            freq : float
                Frequency of sinusoids used to created the terrain.
                Defaults to 1.
            phase : float
                Phase deviation between rows of the terrain. Should be in
                the range 0 -> 1. Defaults to 0.0625.

        """
        [obj.genSineTerrain(freq, phase) for obj in self._base_objs]
        self.refreshView()

*/
