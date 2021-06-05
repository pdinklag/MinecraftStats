from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'kill_any',
        {
            'title': 'Killing Spree!',
            'desc': 'Total mobs killed',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:mob_kills'])
    ))

def create_kill_stat(mobId, title, mobText, minVersion = 0, maxVersion = float("inf")):
    mcstats.registry.append(
        mcstats.MinecraftStat(
            'kill_' + mobId,
            {
                'title': title,
                'desc': mobText + ' killed',
                'unit': 'int',
            },
            mcstats.StatReader(['minecraft:killed','minecraft:' + mobId]),
            minVersion,
            maxVersion
        ))

# Hostiles
create_kill_stat('blaze','Extinguisher','Blazes')
create_kill_stat('creeper','Creeper Creep','Creepers')
create_kill_stat('endermite','End Ratter','Endermite')
create_kill_stat('ender_dragon','Dragon Hunter','Ender Dragons')
create_kill_stat('ghast','Tear Drinker','Ghasts')
create_kill_stat('magma_cube','Magma Cream','Magma Cubes')
create_kill_stat('phantom','Phantom Shooter','Phantoms',1467) # added in 18w07a
# Note: Ravagers had been added as Illager Beats in 18w43a (1901)
# support for that snapshot may be added on demand
create_kill_stat('ravager','Ravaging!','Ravagers',1930) # changed in 19w05a
create_kill_stat('shulker','Shulker Cracker','Shulkers')
create_kill_stat('silverfish','Nasty Little...','Silverfish')
create_kill_stat('slime','Swamp Lurker','Slimes')
create_kill_stat('vex','Vex Hunter','Vexes')
create_kill_stat('witch','Witch Hunter','Witches')
create_kill_stat('wither_skeleton','Wither Or Not','Wither Skeletons')

# Neutrals
create_kill_stat('bee','Beegone!','Bees',2200) # added in 19w34a
create_kill_stat('dolphin','Dolphin Hunter','Dolphins', 1482) # added in 18w15a
create_kill_stat('enderman','Enderman Ender','Endermen')
create_kill_stat('goat','G.O.A.T.','Goats', 2705) # added in 21w13a
create_kill_stat('iron_golem','Defense Down!','Iron Golems')
create_kill_stat('panda','Kung FU! Panda','Pandas',1901) # added in 18w43a
create_kill_stat('piglin','Die, Pig!','Piglins', 2506) # added in 20w07a
create_kill_stat('polar_bear','Polar Hunter','Polar Bears')
create_kill_stat('snow_golem','AntiFrosty','Snow Golems')
create_kill_stat('zombie_pigman','Nether Gang War','Zombie Pigmen',0,2510) # renamed to Zombified Piglin in 20w09a
create_kill_stat('zombified_piglin','Nether Gang War','Zombified Piglins',2510)   # added in 20w09a
create_kill_stat('piglin_brute','Brutal','Piglin Brutes',2569)   # added in 20w27a

# Passives
create_kill_stat('axolotl','Sir Axolot','Axolotls',2687) #added in 20w51a
create_kill_stat('bat','Bat Flap','Bats')
create_kill_stat('chicken','Chicken Griller','Chickens')
create_kill_stat('cow','Cow Tipper','Cows')
create_kill_stat('horse','Horse Hater','Horses')
create_kill_stat('fox','What Does The Fox Say?','Foxes',1932) # added in 19w07a
create_kill_stat('mooshroom','Mycelium Cowboy','Mooshrooms')
create_kill_stat('parrot','Stupid Bird!','Parrots')
create_kill_stat('pig','Pork Chopper','Pigs')
create_kill_stat('rabbit','Bunny Killer :(','Rabbits')
create_kill_stat('sheep','Big Bad Wolf','Sheep')
create_kill_stat('strider','Lava Pool Cleaner','Striders',2520) # added in 20w13a
create_kill_stat('turtle','Super Mario','Turtles',1467) # added in 18w07a
create_kill_stat('villager','Bully','Villagers')
create_kill_stat('wandering_trader','Trade Sanctions','Wandering Traders',1930) # added in 19w05a
create_kill_stat('wolf','Bad Dog!','Wolves and Dogs')

# Cats (including ozelots)
mcstats.registry.append(
    mcstats.MinecraftStat(
        'kill_ocelot',
        {
            'title': 'Kitty Killer',
            'desc': 'Ocelots and Cats killed',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:killed','minecraft:cat']),
            mcstats.StatReader(['minecraft:killed','minecraft:ocelot']),
        ])
    ))

# Llamas (including trader llamas)
mcstats.registry.append(
    mcstats.MinecraftStat(
        'kill_llama',
        {
            'title': 'Caravan Bandit',
            'desc': 'LLamas killed',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:killed','minecraft:llama']),
            mcstats.StatReader(['minecraft:killed','minecraft:trader_llama']),
        ])
    ))

# Zombies (including Husks and Zombie Villagers)
mcstats.registry.append(
    mcstats.MinecraftStat(
        'kill_zombie',
        {
            'title': 'Zombie Grinder',
            'desc': 'Zombies/Husks/Drowned killed',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:killed','minecraft:husk']),
            mcstats.StatReader(['minecraft:killed','minecraft:drowned']),
            mcstats.StatReader(['minecraft:killed','minecraft:zombie']),
            mcstats.StatReader(['minecraft:killed','minecraft:zombie_villager']),
        ])
    ))

# Skeletons (including Strays)
mcstats.registry.append(
    mcstats.MinecraftStat(
        'kill_skeleton',
        {
            'title': 'Bone Collector',
            'desc': 'Skeletons/Strays killed',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:killed','minecraft:skeleton']),
            mcstats.StatReader(['minecraft:killed','minecraft:stray']),
        ])
    ))

# Spiders (including Cave Spiders)
mcstats.registry.append(
    mcstats.MinecraftStat(
        'kill_spider',
        {
            'title': 'Arachnophobia',
            'desc': 'Spiders killed',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:killed','minecraft:spider']),
            mcstats.StatReader(['minecraft:killed','minecraft:cave_spider']),
        ])
    ))

# Guardians (including Elder Guardians)
mcstats.registry.append(
    mcstats.MinecraftStat(
        'kill_guardian',
        {
            'title': 'Underwater Raider',
            'desc': 'Score vs Guardians',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:killed','minecraft:guardian']),
            mcstats.StatReader(['minecraft:killed','minecraft:elder_guardian']),
        ])
    ))

# Illagers (all types)
mcstats.registry.append(
    mcstats.MinecraftStat(
        'kill_illagers',
        {
            'title': 'Cleanser',
            'desc': 'Illagers killed',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:killed','minecraft:evoker']),
            mcstats.StatReader(['minecraft:killed','minecraft:vindicator']),
            mcstats.StatReader(['minecraft:killed','minecraft:pillager']),
            mcstats.StatReader(['minecraft:killed','minecraft:illusioner']),
            mcstats.StatReader(['minecraft:killed','minecraft:illager_beast']),
        ])
    ))

# Hoglins and Zoglins (all types)
mcstats.registry.append(
    mcstats.MinecraftStat(
        'kill_hoglins',
        {
            'title': 'Hakuna Matata',
            'desc': 'Hoglins & Zoglins killed',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:killed','minecraft:hoglin']),
            mcstats.StatReader(['minecraft:killed','minecraft:zoglin']),
        ]),
        2504 # added in 20w06a
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
            mcstats.StatReader(['minecraft:killed','minecraft:cod']),
            mcstats.StatReader(['minecraft:killed','minecraft:salmon']),
            mcstats.StatReader(['minecraft:killed','minecraft:pufferfish']),
            mcstats.StatReader(['minecraft:killed','minecraft:tropical_fish']),
        ]),
        1471 # fish mobs added in 18w08b
    ))

# Squids (including glow squids)
mcstats.registry.append(
    mcstats.MinecraftStat(
        'kill_squid',
        {
            'title': 'Pool Cleaner',
            'desc': 'Squids killed',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:killed','minecraft:glow_squid']),
            mcstats.StatReader(['minecraft:killed','minecraft:squid']),
        ])
    ))
