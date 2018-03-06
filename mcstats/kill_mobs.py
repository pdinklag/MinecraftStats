from mcstats import __mcstats__

def create_score_stat(mobId, title, mobText):
    __mcstats__.registry.append(
        __mcstats__.MinecraftStat(
            'score_' + mobId,
            {
                'title': title,
                'desc': 'Score against ' + mobText,
                'unit': 'int',
            },
            __mcstats__.StatDiffReader(
                __mcstats__.StatReader(['minecraft:killed','minecraft:' + mobId]),
                __mcstats__.StatReader(['minecraft:killed_by','minecraft:' + mobId]))
        ))

def create_kill_stat(mobId, title, mobText):
    __mcstats__.registry.append(
        __mcstats__.MinecraftStat(
            'kill_' + mobId,
            {
                'title': title,
                'desc': mobText + ' killed',
                'unit': 'int',
            },
            __mcstats__.StatReader(['minecraft:killed','minecraft:' + mobId])
        ))

# According to MC-33710, the following mobs are not tracked and therefore
# there are no stats for them:
# - Ender Dragon
# - Illusioners
# - Iron Golems
# - Snow Golems
# - Wither Skeletons

# Hostiles
create_score_stat('blaze','Extinguisher','Blazes')
create_score_stat('creeper','Creeper Creep','Creepers')
create_score_stat('endermite','End Ratter','Endermite')
create_score_stat('ghast','Tear Drinker','Ghasts')
create_score_stat('magma_cube','Magma Cream','Magma Cubes')
create_score_stat('phantom','Phantom Shooter','Phantoms')
create_score_stat('shulker','Shulker Cracker','Shulkers')
create_score_stat('silverfish','Nasty Little...','Silverfish')
create_score_stat('slime','Swamp Lurker','Slimes')
create_score_stat('vex','Vex Hunter','Vexes')
create_score_stat('witch','Witch Hunter','Witches')

# Neutrals
create_score_stat('llama','Caravan Bandit','Llamas')
create_score_stat('enderman','Enderman Ender','Endermen')
create_score_stat('polar_bear','Eskimo','Polar Bears')
create_score_stat('zombie_pigman','Nether Gang War','Zombie Pigmen')

# Passives
create_kill_stat('bat','Bat Flap','Bats')
create_kill_stat('chicken','Chicken Griller','Chickens')
create_kill_stat('cow','Cow Tipper','Cows')
create_kill_stat('horse','Horse Hater','Horses')
create_kill_stat('mooshroom','Mycelium Cowboy','Mooshrooms')
create_kill_stat('ocelot','Kitty Killer','Ocelots and Cats')
create_kill_stat('parrot','Stupid Bird!','Parrots')
create_kill_stat('pig','Pork Chopper','Pigs')
create_kill_stat('rabbit','Bunny Killer :(','Rabbits')
create_kill_stat('sheep','Big Bad Wolf','Sheep')
create_kill_stat('squid','Pool Cleaner','Squids')
create_kill_stat('turtle','Super Mario','Turtles')
create_kill_stat('villager','Bully','Villagers')
create_kill_stat('wolf','Bad Dog!','Wolves and Dogs')

# Zombies (including Husks and Zombie Villagers)
__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'score_zombie',
        {
            'title': 'Zombie Grinder',
            'desc': 'Score against Zombies and Husks',
            'unit': 'int',
        },
        __mcstats__.StatDiffReader(
            __mcstats__.StatSumReader([
                __mcstats__.StatReader(['minecraft:killed','minecraft:husk']),
                __mcstats__.StatReader(['minecraft:killed','minecraft:zombie']),
                __mcstats__.StatReader(['minecraft:killed','minecraft:zombie_villager']),
            ]),
            __mcstats__.StatSumReader([
                __mcstats__.StatReader(['minecraft:killed_by','minecraft:husk']),
                __mcstats__.StatReader(['minecraft:killed_by','minecraft:zombie']),
                __mcstats__.StatReader(['minecraft:killed_by','minecraft:zombie_villager']),
            ]))
    ))

# Skeletons (including Strays)
__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'score_skeleton',
        {
            'title': 'Bone Collector',
            'desc': 'Score against Skeletons and Strays',
            'unit': 'int',
        },
        __mcstats__.StatDiffReader(
            __mcstats__.StatSumReader([
                __mcstats__.StatReader(['minecraft:killed','minecraft:skeleton']),
                __mcstats__.StatReader(['minecraft:killed','minecraft:stray']),
            ]),
            __mcstats__.StatSumReader([
                __mcstats__.StatReader(['minecraft:killed_by','minecraft:skeleton']),
                __mcstats__.StatReader(['minecraft:killed_by','minecraft:stray']),
            ]))
    ))

# Spiders (including Cave Spiders)
__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'score_spider',
        {
            'title': 'Arachnophobia',
            'desc': 'Score against Spiders',
            'unit': 'int',
        },
        __mcstats__.StatDiffReader(
            __mcstats__.StatSumReader([
                __mcstats__.StatReader(['minecraft:killed','minecraft:spider']),
                __mcstats__.StatReader(['minecraft:killed','minecraft:cave_spider']),
            ]),
            __mcstats__.StatSumReader([
                __mcstats__.StatReader(['minecraft:killed_by','minecraft:spider']),
                __mcstats__.StatReader(['minecraft:killed_by','minecraft:cave_spider']),
            ]))
    ))

# Guardians (including Elder Guardians)
__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'score_guardian',
        {
            'title': 'Underwater Raider',
            'desc': 'Score against Guardians',
            'unit': 'int',
        },
        __mcstats__.StatDiffReader(
            __mcstats__.StatSumReader([
                __mcstats__.StatReader(['minecraft:killed','minecraft:guardian']),
                __mcstats__.StatReader(['minecraft:killed','minecraft:elder_guardian']),
            ]),
            __mcstats__.StatSumReader([
                __mcstats__.StatReader(['minecraft:killed_by','minecraft:guardian']),
                __mcstats__.StatReader(['minecraft:killed_by','minecraft:elder_guardian']),
            ]))
    ))

# Illagers (all types)
__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'score_illagers',
        {
            'title': 'Cleanser',
            'desc': 'Score against Illagers',
            'unit': 'int',
        },
        __mcstats__.StatDiffReader(
            __mcstats__.StatSumReader([
                __mcstats__.StatReader(['minecraft:killed','minecraft:evocation_illager']),
                __mcstats__.StatReader(['minecraft:killed','minecraft:vindication_illager']),
            ]),
            __mcstats__.StatSumReader([
                __mcstats__.StatReader(['minecraft:killed_by','minecraft:evocation_illager']),
                __mcstats__.StatReader(['minecraft:killed_by','minecraft:vindication_illager']),
            ]))
    ))

# Fish mobs
__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'kill_fish',
        {
            'title': 'Fish Catcher',
            'desc': 'Fish killed',
            'unit': 'int',
        },
        __mcstats__.StatSumReader([
            __mcstats__.StatReader(['minecraft:killed','minecraft:cod_mob']),
            __mcstats__.StatReader(['minecraft:killed','minecraft:salmon_mob']),
            __mcstats__.StatReader(['minecraft:killed','minecraft:puffer_fish']),
        ]),
    ))
