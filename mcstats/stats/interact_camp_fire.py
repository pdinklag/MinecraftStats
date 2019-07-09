from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'interact_camp_fire',
        {
            'title': 'Primitive Technology',
            'desc': 'Cap fire interactions',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:interact_with_campfire'])
    ))
