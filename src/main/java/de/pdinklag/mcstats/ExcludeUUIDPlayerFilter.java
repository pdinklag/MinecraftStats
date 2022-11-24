package de.pdinklag.mcstats;

import java.util.Collection;
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

    /**
     * Adds UUIDs to exclude
     * @param uuids the uuids to exclude.
     */
    public void excludeAll(Collection<String> uuids) {
        excludedUuids.addAll(uuids);
    }

    @Override
    public boolean filter(Player player) {
        return !excludedUuids.contains(player.getUuid());
    }
}
