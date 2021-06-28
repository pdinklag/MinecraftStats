from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'eat_meat',
        {
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:used','minecraft:cooked_porkchop']),
            mcstats.StatReader(['minecraft:used','minecraft:cooked_beef']),
            mcstats.StatReader(['minecraft:used','minecraft:cooked_chicken']),
            mcstats.StatReader(['minecraft:used','minecraft:cooked_mutton']),
            mcstats.StatReader(['minecraft:used','minecraft:cooked_rabbit']),
            mcstats.StatReader(['minecraft:used','minecraft:porkchop']),
            mcstats.StatReader(['minecraft:used','minecraft:beef']),
            mcstats.StatReader(['minecraft:used','minecraft:chicken']),
            mcstats.StatReader(['minecraft:used','minecraft:mutton']),
            mcstats.StatReader(['minecraft:used','minecraft:rabbit']),
            mcstats.StatReader(['minecraft:used','minecraft:rabbit_stew']),
        ])
    ))
