from mcstats import __mcstats__

def createKillStat(name, title, mobId, mobName, iconPos):
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

createKillStat('kill_creeper','Creeper Creep','minecraft:creeper','Creepers',[16,16])
createKillStat('kill_zombie','Zombie Grinder','minecraft:zombie','Zombies',[128,0])
