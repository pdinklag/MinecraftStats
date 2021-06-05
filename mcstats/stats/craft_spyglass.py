from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_spyglass',
        {
            'title': 'Voyeur',
            'desc': 'Spyglasses crafted',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:crafted','minecraft:spyglass']),
        2681 # added in 20w45a
    ))
