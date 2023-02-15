package de.pdinklag.mcstats;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.function.Function;

/**
 * A ranking of players.
 */
public class Ranking {
    /**
     * A single entry in a ranking.
     */
    public class Entry {
        private final Player player;
        private final int score;

        private Entry(Player player, int score) {
            this.player = player;
            this.score = score;
        }

        /**
         * Gets the player represented by the entry.
         * @return the player represented by the entry
         */
        public Player getPlayer() {
            return player;
        }

        /**
         * Gets the score that the player was entered with.
         * @return the score that the player was entered with
         */
        public int getScore() {
            return score;
        }
    }

    private final ArrayList<Entry> orderedEntries;

    /**
     * Computes a ranking for the given players and score function.
     * @param players the players to be ranked
     * @param score the score function reporting each player's scoring data value
     */
    public Ranking(Collection<Player> players, Function<Player, DataValue> score) {
        orderedEntries = new ArrayList<>(players.size());
        players.forEach(player -> {
            final int playerScore = score.apply(player).toInt();
            if(playerScore > 0) {
                orderedEntries.add(new Entry(player, playerScore));
            }
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

    /**
     * Reports the ordered list of entries in the ranking.
     * @return the ordered list of entries in the ranking
     */
    public List<Entry> getOrderedEntries() {
        return Collections.unmodifiableList(orderedEntries);
    }
}
