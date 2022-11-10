package de.pdinklag.mcstats;

class DefaultReaders {
    public static final DataReader DATA_VERSION_READER = new IntReader("DataVersion");

    public static final DataReader PLAYTIME_READER = new SumReader(
        new IntReader("minecraft:custom", "minecraft:play_time"), // new in 21w16a (data version 2711)
        new IntReader("minecraft:custom", "minecraft:play_one_minute") // legacy
);
}
