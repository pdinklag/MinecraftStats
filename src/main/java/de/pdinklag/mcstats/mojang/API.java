package de.pdinklag.mcstats.mojang;

import java.net.URL;
import java.util.Base64;

import javax.net.ssl.HttpsURLConnection;

import org.json.JSONObject;

import de.pdinklag.mcstats.PlayerProfile;
import de.pdinklag.mcstats.util.StreamUtils;

/**
 * Mojang API.
 */
public class API {
    private static final String API_URL = "https://sessionserver.mojang.com/session/minecraft/profile/";
    private static final String SKIN_URL = "http://textures.minecraft.net/texture/";

    /**
     * Requests a player profile from the Mojang API.
     * @param uuid the UUID of the player in question
     * @return the player profile associated to the given UUID.
     * @throws APIRequestException in case any error occurs trying to request the profile
     */
    public static PlayerProfile requestPlayerProfile(String uuid) throws APIRequestException {
        try {
            final String response;
            {
                URL url = new URL(API_URL + uuid);
                HttpsURLConnection conn = (HttpsURLConnection) url.openConnection();
                response = StreamUtils.readStreamFully(conn.getInputStream());
                conn.disconnect();
            }

            if (!response.isEmpty()) {
                JSONObject obj = new JSONObject(response);
                String name = obj.getString("name");

                String encProps = obj.getJSONArray("properties")
                        .getJSONObject(0)
                        .getString("value");

                String decProps = new String(Base64.getDecoder().decode(encProps));
                JSONObject props = new JSONObject(decProps);
                String skin = props.getJSONObject("textures")
                        .getJSONObject("SKIN")
                        .getString("url")
                        .substring(SKIN_URL.length());

                return new PlayerProfile(name, skin);
            } else {
                throw new APIRequestException("no response for UUID: " + uuid);
            }
        } catch (Exception e) {
            throw new APIRequestException(e);
        }
    }
}
