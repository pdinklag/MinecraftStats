from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'enchant',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:enchant_item'])
    ))
