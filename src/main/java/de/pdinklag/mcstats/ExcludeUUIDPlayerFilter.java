package de.pdinklag.mcstats;

import java.util.HashSet;

/**
 * A player filter that excludes certain players.
 */
public class ExcludeUUIDPlayerFilter implements PlayerFilter {
    private final HashSet<String> excludedUuids = new HashSet<>();

    /**
     * Constructs an empty filter.
     */
    public ExcludeUUIDPlayerFilter() {
    }

    /**
     * Adds a UUID to exclude.
     * @param uuid the uuid to exclude.
     */
    public void exclude(String uuid) {
        excludedUuids.add(uuid);
    }

    @Override
    public boolean filter(Player player) {
        return !excludedUuids.contains(player.getUuid());
    }
}
