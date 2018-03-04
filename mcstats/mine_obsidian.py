from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'mine_obsidian',
        {
            'title': 'Obsidian Miner',
            'desc': 'Obsidian blocks mined',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:mined','minecraft:obsidian'])
    ))
