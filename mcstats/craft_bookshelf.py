from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'craft_bookshelf',
        {
            'title': 'Librarian',
            'desc': 'Bookshelves crafted',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:crafted','minecraft:bookshelf'])
    ))
