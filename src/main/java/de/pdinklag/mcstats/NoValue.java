package de.pdinklag.mcstats;

class NoValue implements DataValue {
    @Override
    public int toInt() {
        return 0;
    }

    @Override
    public Object toJSON() {
        return null;
    }
}
