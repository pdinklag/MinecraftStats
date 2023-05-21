package de.pdinklag.mcstats;

/**
 * Interface for data values that can be represented as an integer.
 */
public interface DataValue {
    /**
     * Returns the integer representing the data value.
     * @return the integer representing the data value
     */
    public int toInt();

    /**
     * Returns the JSON representation of the data value.
     * @return the JSON representation of the data value.
     */
    public Object toJSON();
}
