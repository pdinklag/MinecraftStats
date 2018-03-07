from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'enchant',
        {
            'title': 'Enchanter',
            'desc': 'Items enchanted',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:enchant_item'])
    ))
