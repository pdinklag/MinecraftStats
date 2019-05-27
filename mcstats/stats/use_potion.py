from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_potion',
        {
            'title': 'Alchemist',
            'desc': 'Potions used',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:used','minecraft:lingering_potion']),
            mcstats.StatReader(['minecraft:used','minecraft:potion']),
            mcstats.StatReader(['minecraft:used','minecraft:splash_potion'])
        ])
    ))
