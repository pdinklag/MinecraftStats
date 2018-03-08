import base64
import json
import urllib.request

profile_api_url = 'https://sessionserver.mojang.com/session/minecraft/profile/'

# get player profile via Mojang's API
# the returned object is the first property ("textures") decoded
# may raise an error on failure
def get_player_profile(uuid):
    compact_uuid = uuid.replace('-', '')
    with urllib.request.urlopen(profile_api_url + compact_uuid) as response:
        profile = json.loads(response.read().decode())

    # FIXME: this is some heavy hardcoding right here, but what the API returns
    # does not seem to follow any reasonnable logic
    return json.loads(
        base64.b64decode(profile['properties'][0]['value']).decode())
