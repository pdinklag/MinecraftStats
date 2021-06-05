from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_mineral_block',
        {
            'title': 'Compressor',
            'desc': 'Mineral blocks crafted',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:crafted','minecraft:coal_block']),
            mcstats.StatReader(['minecraft:crafted','minecraft:copper_block']),
            mcstats.StatReader(['minecraft:crafted','minecraft:diamond_block']),
            mcstats.StatReader(['minecraft:crafted','minecraft:emerald_block']),
            mcstats.StatReader(['minecraft:crafted','minecraft:gold_block']),
            mcstats.StatReader(['minecraft:crafted','minecraft:iron_block']),
            mcstats.StatReader(['minecraft:crafted','minecraft:lapis_block']),
            mcstats.StatReader(['minecraft:crafted','minecraft:netherite_block']),
            mcstats.StatReader(['minecraft:crafted','minecraft:quartz_block']),
            mcstats.StatReader(['minecraft:crafted','minecraft:raw_copper_block']),
            mcstats.StatReader(['minecraft:crafted','minecraft:raw_gold_block']),
            mcstats.StatReader(['minecraft:crafted','minecraft:raw_iron_block']),
            mcstats.StatReader(['minecraft:crafted','minecraft:redstone_block']),
        ])
    ))
