package de.pdinklag.mcstats;

/**
 * An enumeration of account types.
 */
public enum AccountType {
    /**
     * No information available (yet).
     */
    UNKNOWN,

    /**
     * This player is known to be a Mojang player (e.g., because the Mojang API gave
     * a response for the UUID).
     */
    MOJANG,

    /**
     * This player is known to be an offline player (e.g., because the Mojang API
     * gave an empty response for the UUID).
     */
    OFFLINE,

    /**
     * This player is known to be a Floodgate player (because the UUID can be
     * identified as such).
     */
    FLOODGATE;

    // as per
    // https://wiki.geysermc.org/floodgate/setup/#obtaining-uuids-for-floodgate-players
    private static final String FLOODGATE_UUID_PREFIX = "00000000-0000-0000-";

    /**
     * Gets the account type for the given ordinal.
     * @param ordinal the ordinal
     * @return the associated account type
     */
    public static AccountType byOrdinal(int ordinal) {
        return AccountType.values()[ordinal];
    }

    /**
     * Attempt to detect the account type directly from a player UUID.
     * @param uuid the player UUID
     * @return the detected account type
     */
    public static AccountType detect(String uuid) {
        return uuid.startsWith(FLOODGATE_UUID_PREFIX) ? FLOODGATE : UNKNOWN;
    }

    /**
     * Could this be a Mojang account?
     * 
     * @return whether this could be a Mojang account
     */
    public boolean maybeMojangAccount() {
        switch (this) {
            case UNKNOWN:
            case MOJANG:
                return true;

            default:
                return false;
        }
    }

    /**
     * Can this account type only be detected by asking the Mojang API?
     * 
     * @return whether this account type is the result of a Mojang API call
     */
    public boolean isMojangAPIResult() {
        switch (this) {
            case MOJANG:
            case OFFLINE:
                return true;

            default:
                return false;
        }
    }
}
