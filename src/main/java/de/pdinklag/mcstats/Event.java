package de.pdinklag.mcstats;

import java.util.HashMap;

import org.json.JSONObject;

/**
 * Represents an event.
 */
public class Event {
    private final String id;
    private final String title;
    private final long startTime;
    private final long endTime;
    private final String linkedStatId;

    private final HashMap<String, Integer> initialScores = new HashMap<>();

    public Event(String id, String title, long startTime, long endTime, String linkedStatId) {
        this.id = id;
        this.title = title;
        this.startTime = startTime;
        this.endTime = endTime;
        this.linkedStatId = linkedStatId;
    }

    public String getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public long getStartTime() {
        return startTime;
    }

    public long getEndTime() {
        return endTime;
    }

    public String getLinkedStatId() {
        return linkedStatId;
    }

    public boolean hasStarted(long time) {
        return time >= startTime;
    }
    
    public boolean hasEnded(long time) {
        return time >= endTime;
    }

    public int getInitialScore(Player player) {
        return initialScores.getOrDefault(player.getUuid(), 0);
    }

    public void setInitialScore(Player player, int score) {
        initialScores.put(player.getUuid(), score);
    }

    public void setInitialScores(JSONObject obj) {
        obj.keySet().forEach(uuid -> {
            initialScores.put(uuid, obj.getInt(uuid));
        });
    }
}
