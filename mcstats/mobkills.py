from mcstats import __mcstats__

def createKillStat(name, title, mobId, mobName, iconPos):
    __mcstats__.registry.append(
        __mcstats__.MinecraftStat(
            name,
            {
                'title': title,
                'desc': mobName + ' score',
                'icon': 'minecraft-wiki/EntityCSS.png',
                'iconPos': iconPos,
                'unit': 'int',
            },
            __mcstats__.StatDiffReader(
                __mcstats__.StatReader(['minecraft:killed',mobId]),
                __mcstats__.StatReader(['minecraft:killed_by',mobId]))
        ))

createKillStat('kill_creeper','Creeper Creep','minecraft:creeper','Creeper',[16,16])
createKillStat('kill_zombie','Zombie Grinder','minecraft:zombie','Zombie',[128,0])
