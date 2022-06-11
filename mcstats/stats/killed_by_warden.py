from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'killed_by_warden',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:killed_by','minecraft:warden']),
        3066 # wardens added in Deep Dark Experimental Snapshot 1
    ))
