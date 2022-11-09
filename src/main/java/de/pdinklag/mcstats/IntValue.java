package de.pdinklag.mcstats;

/**
 * Represents a simple integer data value.
 */
public class IntValue implements DataValue {
    private final int value;

    /**
     * Constructs an integer data value.
     * @param value the wrapped integer
     */
    public IntValue(int value) {
        this.value = value;
    }

    @Override
    public int toInt() {
        return value;
    }
}
