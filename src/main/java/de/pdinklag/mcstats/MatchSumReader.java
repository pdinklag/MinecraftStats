package de.pdinklag.mcstats;

import java.util.regex.Pattern;

import org.json.JSONObject;

public class MatchSumReader extends JSONDataReader {
    private final Pattern[] patterns;

    public MatchSumReader(String[] path, String[] patterns) {
        super(path);

        this.patterns = new Pattern[patterns.length];
        for (int i = 0; i < patterns.length; i++) {
            this.patterns[i] = Pattern.compile(patterns[i]);
        }
    }

    @Override
    protected DataValue getDefaultValue() {
        return new IntValue(0);
    }

    @Override
    protected DataValue read(JSONObject obj, String key) {
        obj = obj.getJSONObject(key);

        int sum = 0;
        for (String x : obj.keySet()) {
            for (Pattern p : patterns) {
                if (p.matcher(x).matches()) {
                    sum += obj.getInt(x);
                }
            }
        }
        return new IntValue(sum);
    }

    @Override
    public DataAggregator createDefaultAggregator() {
        return new IntSumAggregator();
    }

}
