from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'interact_brewing_stand',
        {
            'title': 'Brewer',
            'desc': 'Brewing Stand interactions',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:interact_with_brewingstand']),
    ))
