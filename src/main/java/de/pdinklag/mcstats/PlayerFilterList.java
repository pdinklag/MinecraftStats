package de.pdinklag.mcstats;

import java.util.ArrayList;

/**
 * Filters players using a list of filters.
 */
public class PlayerFilterList implements PlayerFilter {
    private final ArrayList<PlayerFilter> filters = new ArrayList<>();

    @Override
    public boolean filter(Player player) {
        for (PlayerFilter filter : filters) {
            if (!filter.filter(player)) {
                return false;
            }
        }
        return true;
    }

    public void add(PlayerFilter filter) {
        filters.add(filter);
    }
}
