from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'place_sapling',
        {
            'title': 'Forester',
            'desc': 'Trees planted',
            'unit': 'int',
        },
        # subtract mined saplings from placed saplings
        __mcstats__.StatDiffReader(
            __mcstats__.StatSumMatchReader(
                ['minecraft:used'],
                ['minecraft:.+_sapling']),
            __mcstats__.StatSumMatchReader(
                ['minecraft:mined'],
                ['minecraft:.+_sapling'])),
    ))
