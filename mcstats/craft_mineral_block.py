from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'craft_mineral_block',
        {
            'title': 'Compressor',
            'desc': 'Mineral blocks crafted',
            'unit': 'int',
        },
        __mcstats__.StatSumReader([
            __mcstats__.StatReader(['minecraft:crafted','minecraft:coal_block']),
            __mcstats__.StatReader(['minecraft:crafted','minecraft:iron_block']),
            __mcstats__.StatReader(['minecraft:crafted','minecraft:gold_block']),
            __mcstats__.StatReader(['minecraft:crafted','minecraft:diamond_block']),
            __mcstats__.StatReader(['minecraft:crafted','minecraft:emerald_block']),
            __mcstats__.StatReader(['minecraft:crafted','minecraft:lapis_block']),
            __mcstats__.StatReader(['minecraft:crafted','minecraft:redstone_block']),
            __mcstats__.StatReader(['minecraft:crafted','minecraft:quartz_block']),
        ])
    ))
