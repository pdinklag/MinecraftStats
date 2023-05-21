package de.pdinklag.mcstats;

import org.json.JSONArray;

public class CrownScoreValue implements DataValue {
    private final int crownScore;
    private final int bronzeMedals;
    private final int silverMedals;
    private final int goldMedals;

    public CrownScoreValue(int numBronze, int numSilver, int numGold, Config config) {
        this.bronzeMedals = numBronze;
        this.silverMedals = numSilver;
        this.goldMedals = numGold;
        this.crownScore = numBronze * config.getBronzeMedalWeight() +
                numSilver * config.getSilverMedalWeight() +
                numGold * config.getGoldMedalWeight();
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
