from mcstats import mcstats

redstone_item_patterns = [
    'minecraft:redstone',
    'minecraft:redstone_torch',
    'minecraft:.+_button',
    'minecraft:daylight_detector.*',
    'minecraft:detector_rail',
    'minecraft:lever',
    'minecraft:observer',
    'minecraft:comparator',
    'minecraft:repeater',
    'minecraft:sculk_sensor',
    'minecraft:.+_pressure_plate',
    'minecraft:target',
]

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_electrics',
        {
            'title': 'Electrician',
            'desc': 'Redstone items placed',
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(['minecraft:used'], redstone_item_patterns)
    ))
