from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_recovery_compass',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:crafted','minecraft:recovery_compass']),
        3088 # added in 22w14a
    ))
