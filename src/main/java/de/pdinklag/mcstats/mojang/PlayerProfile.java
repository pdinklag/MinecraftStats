package de.pdinklag.mcstats.mojang;

import java.net.URL;
import java.util.Base64;

import javax.net.ssl.HttpsURLConnection;

import org.json.JSONObject;

import de.pdinklag.mcstats.util.StreamUtils;

public class PlayerProfile {
    private static final String API_URL = "https://sessionserver.mojang.com/session/minecraft/profile/";
    private static final String SKIN_URL = "http://textures.minecraft.net/texture/";

    private String name;
    private String skin;

    public PlayerProfile(String uuid) throws APIException {
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
                name = obj.getString("name");

                String encProps = obj.getJSONArray("properties")
                        .getJSONObject(0)
                        .getString("value");

                String decProps = new String(Base64.getDecoder().decode(encProps));
                JSONObject props = new JSONObject(decProps);
                skin = props.getJSONObject("textures")
                        .getJSONObject("SKIN")
                        .getString("url")
                        .substring(SKIN_URL.length());
            } else {
                throw new APIException("no response for UUID: " + uuid);
            }
        } catch (Exception e) {
            throw new APIException(e);
        }
    }

    public String getName() {
        return name;
    }

    public String getSkin() {
        return skin;
    }
}
