from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'eat_rawmeat',
        {
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:used','minecraft:porkchop']),
            mcstats.StatReader(['minecraft:used','minecraft:beef']),
            mcstats.StatReader(['minecraft:used','minecraft:chicken']),
            mcstats.StatReader(['minecraft:used','minecraft:mutton']),
            mcstats.StatReader(['minecraft:used','minecraft:rabbit']),
        ])
    ))
