from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'raids_won',
        {
            'title': 'Raider',
            'desc': 'Raids won',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:raid_win']),
    ))
