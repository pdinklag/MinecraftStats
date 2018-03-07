from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_bookshelf',
        {
            'title': 'Librarian',
            'desc': 'Bookshelves crafted',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:crafted','minecraft:bookshelf'])
    ))
