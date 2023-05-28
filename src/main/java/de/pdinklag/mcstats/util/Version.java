package de.pdinklag.mcstats.util;

/**
 * Represents a semantic version number.
 */
public class Version implements Comparable<Version> {
    /**
     * Parses a semantic version number.
     * @param s the semantic version number as a string
     * @return the version
     */
    public static Version parse(String s) {
        final String[] tokens = s.split("\\.", 3);
        return new Version(
                Integer.parseInt(tokens[0]),
                Integer.parseInt(tokens[1]),
                Integer.parseInt(tokens[2]));
    }

    private final int major;
    private final int minor;
    private final int patch;

    public Version(int major, int minor, int patch) {
        this.major = major;
        this.minor = minor;
        this.patch = patch;
    }

    @Override
    public String toString() {
        return major + "." + minor + "." + patch;
    }

    @Override
    public int compareTo(Version o) {
        if(major != o.major) {
            return Integer.compare(major, o.major);
        } else if(minor != o.minor) {
            return Integer.compare(minor, o.minor);
        } else if(patch != o.patch) {
            return Integer.compare(patch, o.patch);
        } else {
            return 0;
        }
    }
}
