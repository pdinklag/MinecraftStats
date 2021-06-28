from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_respawn_anchor',
        {
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:crafted','minecraft:respawn_anchor']),
        ]),
        2515 # introduced in 20w12a
    ))
