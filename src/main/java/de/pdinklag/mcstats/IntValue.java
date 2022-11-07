package de.pdinklag.mcstats;

public class IntValue implements IValue {
    private final int value;

    public IntValue(int value) {
        this.value = value;
    }

    @Override
    public int toInt() {
        return value;
    }
}
