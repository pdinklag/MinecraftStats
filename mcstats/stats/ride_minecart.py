from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'ride_minecart',
        {
            'title': 'Public Transport',
            'desc': 'Distance gone in a minecart',
            'unit': 'cm',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:minecart_one_cm'])
    ))
