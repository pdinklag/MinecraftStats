from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'mine_stone',
        {
            'title': 'Stonemason',
            'desc': 'Stone mined',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:mined','minecraft:stone']),
            mcstats.StatReader(['minecraft:mined','minecraft:andesite']),
            mcstats.StatReader(['minecraft:mined','minecraft:blackstone']),
            mcstats.StatReader(['minecraft:mined','minecraft:basalt']),
            mcstats.StatReader(['minecraft:mined','minecraft:calcite']),
            mcstats.StatReader(['minecraft:mined','minecraft:deepslate']),
            mcstats.StatReader(['minecraft:mined','minecraft:diorite']),
            mcstats.StatReader(['minecraft:mined','minecraft:dripstone']),
            mcstats.StatReader(['minecraft:mined','minecraft:granite']),
            mcstats.StatReader(['minecraft:mined','minecraft:smooth_basalt']),
            mcstats.StatReader(['minecraft:mined','minecraft:tuff']),
        ])
    ))
