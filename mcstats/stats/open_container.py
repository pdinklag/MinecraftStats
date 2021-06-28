from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'open_container',
        {
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:custom','minecraft:open_chest']),
            mcstats.StatReader(['minecraft:custom','minecraft:open_shulker_box']),
            mcstats.StatReader(['minecraft:custom','minecraft:open_enderchest']),
            mcstats.StatReader(['minecraft:custom','minecraft:trigger_trapped_chest']),
        ])
    ))
