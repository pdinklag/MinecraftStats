from mcstats import __mcstats__

def createMobKillStat(name, title, mobId, mobName, iconPos):
    __mcstats__.registry.append(
        __mcstats__.MinecraftStat(
            name,
            {
                'title': title,
                'desc': mobName + ' killed',
                'icon': 'minecraft-wiki/EntityCSS.png',
                'iconPos': iconPos,
                'unit': 'int',
            },
            __mcstats__.StatReader(['minecraft:killed',mobId])
        ))

# Creepers
createMobKillStat(
    'kill_creeper',
    'Creeper Creep',
    'minecraft:creeper',
    'Creepers',
    [16,16])

# Zombies
createMobKillStat(
    'kill_zombie',
    'Zombie Grinder',
    'minecraft:zombie',
    'Zombies',
    [128,0])
