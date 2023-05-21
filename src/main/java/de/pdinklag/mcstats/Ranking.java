package de.pdinklag.mcstats;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.function.Function;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * A ranking of players.
 */
public class Ranking<T extends DataValue> {
    /**
     * A single entry in a ranking.
     */
    public class Entry {
        private final Player player;
        private final T score;

        private Entry(Player player, T score) {
            this.player = player;
            this.score = score;
        }

        /**
         * Gets the player represented by the entry.
         * 
         * @return the player represented by the entry
         */
        public Player getPlayer() {
            return player;
        }

        /**
         * Gets the score that the player was entered with.
         * 
         * @return the score that the player was entered with
         */
        public T getScore() {
            return score;
        }

        /**
         * Gets a JSON object describing this entry.
         * 
         * @return a JSON object describing this entry
         */
        public JSONObject toJSON() {
            JSONObject obj = new JSONObject();
            obj.put("uuid", player.getUuid());
            obj.put("value", score.toJSON());
            return obj;
        }
    }

    private final ArrayList<Entry> orderedEntries;

    /**
     * Computes a ranking for the given players and score function.
     * 
     * @param players the players to be ranked
     * @param score   the score function reporting each player's scoring data value
     */
    public Ranking(Collection<Player> players, Function<Player, T> score) {
        orderedEntries = new ArrayList<>(players.size());
        players.forEach(player -> {
            final T playerScore = score.apply(player);
            if (playerScore.toInt() > 0) {
                orderedEntries.add(new Entry(player, playerScore));
            }
        });
        orderedEntries.sort((a, b) -> {
            if (a.score != b.score) {
                // sort by score descending
                return Integer.compare(b.score.toInt(), a.score.toInt());
            } else {
                // tie break comparing names lexicographically
                return a.player.getProfile().getName().compareTo(b.player.getProfile().getName());
            }
        });
    }

    /**
     * Reports the ordered list of entries in the ranking.
     * 
     * @return the ordered list of entries in the ranking
     */
    public List<Entry> getOrderedEntries() {
        return Collections.unmodifiableList(orderedEntries);
    }

    /**
     * Reports the ordered list of entries in the ranking in JSON format.
     * 
     * @return the ordered list of entries in the ranking
     */
    public JSONArray toJSON() {
        JSONArray array = new JSONArray(orderedEntries.size());
        orderedEntries.forEach(e -> {
            array.put(e.toJSON());
        });
        return array;
    }
}
