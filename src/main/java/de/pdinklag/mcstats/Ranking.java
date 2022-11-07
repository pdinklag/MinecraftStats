package de.pdinklag.mcstats;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;

public class Ranking {
    public class Entry {
        private final Player player;
        private final int score;

        public Entry(Player player, int score) {
            this.player = player;
            this.score = score;
        }

        public Player getPlayer() {
            return player;
        }

        public int getScore() {
            return score;
        }
    }

    private final ArrayList<Entry> orderedEntries;

    public Ranking(Stat<?> stat, Map<Player, PlayerData> players) {
        orderedEntries = new ArrayList<>(players.size());
        players.forEach((player, data) -> {
            orderedEntries.add(new Entry(player, data.get(stat).toInt()));
        });
        orderedEntries.sort((a, b) -> {
            if (a.score != b.score) {
                // sort by score descending
                return Integer.compare(b.score, a.score);
            } else {
                // tie break comparing names lexicographically
                return a.player.getProfile().getName().compareTo(b.player.getProfile().getName());
            }
        });
    }

    public List<Entry> getOrderedEntries() {
        return Collections.unmodifiableList(orderedEntries);
    }
}
