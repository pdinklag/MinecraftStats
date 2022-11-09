package de.pdinklag.mcstats;

import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

/**
 * Represents a set of strings.
 */
public class StringSetValue implements DataValue {
    private final HashSet<String> set = new HashSet<>();

    /**
     * Constructs an empty set of strings.
     */
    public StringSetValue() {
    }

    /**
     * Adds a string to the set.
     * @param str the string to add
     */
    public void add(String str) {
        set.add(str);
    }

    /**
     * Adds a number of strings to the set.
     * @param strs the strings to add
     */
    public void addAll(Collection<String> strs) {
        set.addAll(strs);
    }

    /**
     * Provides read-only access to the string set.
     * @return the string set (unmodifiable)
     */
    public Set<String> getSet() {
        return Collections.unmodifiableSet(set);
    }

    @Override
    public int toInt() {
        return set.size();
    }
}
