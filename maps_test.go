package gosignal

import "testing"

/*
 * >>> m = Map(20., 20000., 'log')
 * >>> print m.get(.5)
 * 632.455532034
 * >>> print m.set(12000)
 * 0.926050416795
 */
func TestMap(t *testing.T) {
	m := NewMap(20., 20000., LOG_SCALE)
	retval := m.Get(.5)
	answer := 632.4555320336759
	if retval != answer {
		t.Errorf("Retval is %v but should be %v!\n", retval, answer)
	}
	retval = m.Set(12000)
	answer = 0.9260504167945478
	if retval != answer {
		t.Errorf("Retval is %v but should be %v!\n", retval, answer)
	}
}

