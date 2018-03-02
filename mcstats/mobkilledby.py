from mcstats import __mcstats__

def createKilledByStat(name, title, mobId, mobName, iconPos):
    __mcstats__.registry.append(
        __mcstats__.MinecraftStat(
            name,
            {
                'title': title,
                'desc': 'Killed by ' + mobName,
                'icon': 'minecraft-wiki/EntityCSS.png',
                'iconPos': iconPos,
                'unit': 'event',
            },
            __mcstats__.StatReader(['minecraft:killed_by',mobId])
        ))

createKilledByStat('killedby_creeper','Crept','minecraft:creeper','Creepers',[16,16])
createKilledByStat('killedby_zombie','Infected','minecraft:zombie','Zombies',[128,0])
