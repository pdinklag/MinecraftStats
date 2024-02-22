package de.pdinklag.mcstats;

import java.util.function.Function;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Contains summarizing information about the winner of an Event.
 */
public class EventWinner {
    /**
     * Restores an event winner from a ranking in JSON format.
     *
     * @param ranking the ranking in JSON format
     * @param uuidToPlayer the function that translates a player's UUID to the corresponding Player object
     * @return the parsed event winner
     */
    public static EventWinner fromJsonRanking(JSONArray ranking, Function<String, Player> uuidToPlayer) {
        if (ranking.length() > 0) {
            final JSONObject first = ranking.getJSONObject(0);
            return new EventWinner(uuidToPlayer.apply(first.getString("uuid")), first);
        } else {
            return null;
        }
    }

    private final Player player;
    private final JSONObject json;

    private EventWinner(Player player, JSONObject json) {
        this.player = player;
        this.json = json;
    }

    public EventWinner(Ranking<?>.Entry e) {
        this.player = e.getPlayer();
        this.json = e.toJSON();
    }

    public Player getPlayer() {
        return player;
    }

    public JSONObject getJSON() {
        return json;
    }
}
