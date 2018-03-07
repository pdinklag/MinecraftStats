from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_bread',
        {
            'title': 'Baker',
            'desc': 'Breads, cakes and cookies made',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:crafted','minecraft:bread']),
            mcstats.StatReader(['minecraft:crafted','minecraft:cake']),
            mcstats.StatReader(['minecraft:crafted','minecraft:cookie']),
        ])
    ))
