package de.pdinklag.mcstats;

import org.json.JSONArray;

/**
 * Represents a crown score data value for the hall of fame.
 */
public class CrownScoreValue implements DataValue {
    private final int crownScore;
    private final int bronzeMedals;
    private final int silverMedals;
    private final int goldMedals;

    /**
     * Creates a new crown score value.
     * 
     * @param bronzeMedals the number of bronze medals
     * @param silverMedals the number of silver medals
     * @param goldMedals the number of gold medals
     * @param config the configuration to use to compute the crown score
     */
    public CrownScoreValue(int bronzeMedals, int silverMedals, int goldMedals, Config config) {
        this.bronzeMedals = bronzeMedals;
        this.silverMedals = silverMedals;
        this.goldMedals = goldMedals;
        this.crownScore = bronzeMedals * config.getBronzeMedalWeight() +
                silverMedals * config.getSilverMedalWeight() +
                goldMedals * config.getGoldMedalWeight();
    }

    @Override
    public int toInt() {
        return crownScore;
    }

    @Override
    public Object toJSON() {
        final JSONArray arr = new JSONArray(4);
        arr.put(crownScore);
        arr.put(goldMedals);
        arr.put(silverMedals);
        arr.put(bronzeMedals);
        return arr;
    }
}
