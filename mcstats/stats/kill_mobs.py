from mcstats import mcstats

def create_score_stat(mobId, title, mobText):
    mcstats.registry.append(
        mcstats.MinecraftStat(
            'score_' + mobId,
            {
                'title': title,
                'desc': 'Score vs ' + mobText,
                'unit': 'int',
            },
            mcstats.StatDiffReader(
                mcstats.StatReader(['minecraft:killed','minecraft:' + mobId]),
                mcstats.StatReader(['minecraft:killed_by','minecraft:' + mobId]))
        ))

def create_kill_stat(mobId, title, mobText):
    mcstats.registry.append(
        mcstats.MinecraftStat(
            'kill_' + mobId,
            {
                'title': title,
                'desc': mobText + ' killed',
                'unit': 'int',
            },
            mcstats.StatReader(['minecraft:killed','minecraft:' + mobId])
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
create_score_stat('polar_bear','Polar Hunter','Polar Bears')
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
mcstats.registry.append(
    mcstats.MinecraftStat(
        'score_zombie',
        {
            'title': 'Zombie Grinder',
            'desc': 'Score vs Zombies/Husks',
            'unit': 'int',
        },
        mcstats.StatDiffReader(
            mcstats.StatSumReader([
                mcstats.StatReader(['minecraft:killed','minecraft:husk']),
                mcstats.StatReader(['minecraft:killed','minecraft:zombie']),
                mcstats.StatReader(['minecraft:killed','minecraft:zombie_villager']),
            ]),
            mcstats.StatSumReader([
                mcstats.StatReader(['minecraft:killed_by','minecraft:husk']),
                mcstats.StatReader(['minecraft:killed_by','minecraft:zombie']),
                mcstats.StatReader(['minecraft:killed_by','minecraft:zombie_villager']),
            ]))
    ))

# Skeletons (including Strays)
mcstats.registry.append(
    mcstats.MinecraftStat(
        'score_skeleton',
        {
            'title': 'Bone Collector',
            'desc': 'Score vs Skeletons/Strays',
            'unit': 'int',
        },
        mcstats.StatDiffReader(
            mcstats.StatSumReader([
                mcstats.StatReader(['minecraft:killed','minecraft:skeleton']),
                mcstats.StatReader(['minecraft:killed','minecraft:stray']),
            ]),
            mcstats.StatSumReader([
                mcstats.StatReader(['minecraft:killed_by','minecraft:skeleton']),
                mcstats.StatReader(['minecraft:killed_by','minecraft:stray']),
            ]))
    ))

# Spiders (including Cave Spiders)
mcstats.registry.append(
    mcstats.MinecraftStat(
        'score_spider',
        {
            'title': 'Arachnophobia',
            'desc': 'Score vs Spiders',
            'unit': 'int',
        },
        mcstats.StatDiffReader(
            mcstats.StatSumReader([
                mcstats.StatReader(['minecraft:killed','minecraft:spider']),
                mcstats.StatReader(['minecraft:killed','minecraft:cave_spider']),
            ]),
            mcstats.StatSumReader([
                mcstats.StatReader(['minecraft:killed_by','minecraft:spider']),
                mcstats.StatReader(['minecraft:killed_by','minecraft:cave_spider']),
            ]))
    ))

# Guardians (including Elder Guardians)
mcstats.registry.append(
    mcstats.MinecraftStat(
        'score_guardian',
        {
            'title': 'Underwater Raider',
            'desc': 'Score vs Guardians',
            'unit': 'int',
        },
        mcstats.StatDiffReader(
            mcstats.StatSumReader([
                mcstats.StatReader(['minecraft:killed','minecraft:guardian']),
                mcstats.StatReader(['minecraft:killed','minecraft:elder_guardian']),
            ]),
            mcstats.StatSumReader([
                mcstats.StatReader(['minecraft:killed_by','minecraft:guardian']),
                mcstats.StatReader(['minecraft:killed_by','minecraft:elder_guardian']),
            ]))
    ))

# Illagers (all types)
mcstats.registry.append(
    mcstats.MinecraftStat(
        'score_illagers',
        {
            'title': 'Cleanser',
            'desc': 'Score vs Illagers',
            'unit': 'int',
        },
        mcstats.StatDiffReader(
            mcstats.StatSumReader([
                mcstats.StatReader(['minecraft:killed','minecraft:evoker']),
                mcstats.StatReader(['minecraft:killed','minecraft:vindicator']),
                mcstats.StatReader(['minecraft:killed','minecraft:pillager']),
                mcstats.StatReader(['minecraft:killed','minecraft:illusioner']),
                mcstats.StatReader(['minecraft:killed','minecraft:illager_beast']),
            ]),
            mcstats.StatSumReader([
                mcstats.StatReader(['minecraft:killed_by','minecraft:evoker']),
                mcstats.StatReader(['minecraft:killed_by','minecraft:vindicator']),
                mcstats.StatReader(['minecraft:killed_by','minecraft:pillager']),
                mcstats.StatReader(['minecraft:killed_by','minecraft:illusioner']),
                mcstats.StatReader(['minecraft:killed_by','minecraft:illager_beast']),
            ]))
    ))

# Fish mobs
mcstats.registry.append(
    mcstats.MinecraftStat(
        'kill_fish',
        {
            'title': 'Fish Catcher',
            'desc': 'Fish killed',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:killed','minecraft:cod_mob']),
            mcstats.StatReader(['minecraft:killed','minecraft:salmon_mob']),
            mcstats.StatReader(['minecraft:killed','minecraft:puffer_fish']),
            mcstats.StatReader(['minecraft:killed','minecraft:tropical_fish']),
        ]),
    ))
