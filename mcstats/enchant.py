from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'enchant',
        {
            'title': 'Enchanter',
            'desc': 'Items enchanted',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:enchant_item'])
    ))
