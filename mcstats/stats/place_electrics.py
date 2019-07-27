from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_electrics',
        {
            'title': 'Electrician',
            'desc': 'Redstone items placed',
            'unit': 'int',
        },
        # subtract mined from placed
        mcstats.StatDiffReader(
            mcstats.StatSumMatchReader(['minecraft:used'],[
                'minecraft:redstone',
                'minecraft:redstone_torch',
                'minecraft:.+_button',
                'minecraft:daylight_detector.*',
                'minecraft:detector_rail',
                'minecraft:lever',
                'minecraft:observer',
                'minecraft:comparator',
                'minecraft:repeater',
                'minecraft:.+_pressure_plate',
                ]),
            mcstats.StatSumMatchReader(['minecraft:mined'],[
                'minecraft:redstone',
                'minecraft:redstone_torch',
                'minecraft:.+_button',
                'minecraft:daylight_detector.*',
                'minecraft:detector_rail',
                'minecraft:lever',
                'minecraft:observer',
                'minecraft:comparator',
                'minecraft:repeater',
                'minecraft:.+_pressure_plate',
                ]),
        )
    ))
