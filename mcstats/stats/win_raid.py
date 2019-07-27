from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'win_raid',
        {
            'title': 'Hero',
            'desc': 'Raids won',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:raid_win']),
        1912 # raids added in 18w47a
    ))
