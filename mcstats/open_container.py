from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'open_container',
        {
            'title': 'Warehouse',
            'desc': 'Containers opened',
            'unit': 'int',
        },
        __mcstats__.StatSumReader([
            __mcstats__.StatReader(['minecraft:custom','minecraft:open_chest']),
            __mcstats__.StatReader(['minecraft:custom','minecraft:open_shulker_box']),
            __mcstats__.StatReader(['minecraft:custom','minecraft:open_enderchest']),
            __mcstats__.StatReader(['minecraft:custom','minecraft:trigger_trapped_chest']),
        ])
    ))
