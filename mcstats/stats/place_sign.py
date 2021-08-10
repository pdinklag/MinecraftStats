from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_sign',
        {
            'title': 'README.TXT',
            'desc': 'Signs placed',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:used','minecraft:sign']), # before 18w43a
            mcstats.StatSumMatchReader(['minecraft:used'],['minecraft:.+_sign']), # since 18w43a
        ])
    )
)
