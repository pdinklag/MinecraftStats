from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'noteblock',
        {
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:custom','minecraft:tune_noteblock']),
            mcstats.StatReader(['minecraft:custom','minecraft:play_noteblock'])])
    ))
