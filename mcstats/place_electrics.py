from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'place_electrics',
        {
            'title': 'Electrician',
            'desc': 'Redstone items placed',
            'unit': 'int',
        },
        # subtract mined from placed
        __mcstats__.StatDiffReader(
            __mcstats__.StatSumMatchReader(['minecraft:used'],[
                'minecraft:redstone',
                'minecraft:redstone_torch',
                'minecraft:.+_button',
                'minecraft:daylight_detector.*',
                'minecraft:detector_rail',
                'minecraft:lever',
                'minecraft:.+_pressure_plate',
                ]),
            __mcstats__.StatSumMatchReader(['minecraft:mined'],[
                'minecraft:redstone',
                'minecraft:redstone_torch',
                'minecraft:.+_button',
                'minecraft:daylight_detector.*',
                'minecraft:detector_rail',
                'minecraft:lever',
                'minecraft:.+_pressure_plate',
                ]),
        )
    ))
