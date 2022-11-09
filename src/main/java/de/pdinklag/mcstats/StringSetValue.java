package de.pdinklag.mcstats;

import java.util.Collection;
import java.util.HashSet;

public class StringSetValue implements DataValue {
    private final HashSet<String> set = new HashSet<>();

    public StringSetValue() {
    }

    public void add(String str) {
        set.add(str);
    }

    public void addAll(Collection<String> strs) {
        set.addAll(strs);
    }

    public Collection<String> getSet() {
        return set;
    }

    @Override
    public int toInt() {
        return set.size();
    }
}
