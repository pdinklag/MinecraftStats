import base64
import json
import urllib.request

profile_api_url = 'https://sessionserver.mojang.com/session/minecraft/profile/'

# get player profile via Mojang's API
# the returned object is the first property ("textures") decoded
# may raise an error on failure
def get_player_profile(uuid):
    compact_uuid = uuid.replace('-', '')

    response_str = False
    with urllib.request.urlopen(profile_api_url + compact_uuid) as response:
        response_str = response.read().decode()

    if response_str:
        profile = json.loads(response_str)

        # FIXME: this is some heavy hardcoding right here, but what the API returns
        # does not seem to follow any reasonnable logic
        return json.loads(
            base64.b64decode(profile['properties'][0]['value']).decode())
    else:
        return False
