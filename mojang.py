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
        response = json.loads(response_str)
        
        if 'name' in response:
            # get player name
            profile = { 'name': response['name'] }

            # get player skin URL
            try:
                textures = json.loads(base64.b64decode(response['properties'][0]['value']).decode())
                profile['skin'] = textures['skin']['url'][38:] # remove URL prefix: http://textures.minecraft.net/texture/
            except Exception as e:
                print(e)
                pass

            return profile
    
    return False
