from mcstats import __mcstats__

def createKillStat(name, title, mobId, mobName):
    __mcstats__.registry.append(
        __mcstats__.MinecraftStat(
            name,
            {
                'title': title,
                'desc': mobName + ' score',
                'unit': 'int',
            },
            __mcstats__.StatDiffReader(
                __mcstats__.StatReader(['minecraft:killed',mobId]),
                __mcstats__.StatReader(['minecraft:killed_by',mobId]))
        ))

createKillStat('kill_creeper','Creeper Creep','minecraft:creeper','Creeper')
createKillStat('kill_zombie','Zombie Grinder','minecraft:zombie','Zombie')
