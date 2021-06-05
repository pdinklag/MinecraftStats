from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'mine_pointed_dripstone',
        {
            'title': 'Cave Dweller',
            'desc': 'Pointed Dripstone mined',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:mined','minecraft:pointed_dripstone']),
        2683 # added in 20w48a
    ))
