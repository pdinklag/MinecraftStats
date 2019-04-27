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

# Hostiles
create_kill_stat('blaze','Extinguisher','Blazes')
create_kill_stat('creeper','Creeper Creep','Creepers')
create_kill_stat('endermite','End Ratter','Endermite')
create_kill_stat('ghast','Tear Drinker','Ghasts')
create_kill_stat('magma_cube','Magma Cream','Magma Cubes')
create_kill_stat('phantom','Phantom Shooter','Phantoms')
create_kill_stat('ravager','Ravaging!','Ravagers')
create_kill_stat('shulker','Shulker Cracker','Shulkers')
create_kill_stat('silverfish','Nasty Little...','Silverfish')
create_kill_stat('slime','Swamp Lurker','Slimes')
create_kill_stat('vex','Vex Hunter','Vexes')
create_kill_stat('witch','Witch Hunter','Witches')
create_kill_stat('wither_skeleton','Wither Or Not','Wither Skeletons')

# Neutrals
create_kill_stat('dolphin','Dolphin Hunter','Dolphins')
create_kill_stat('llama','Caravan Bandit','Llamas')
create_kill_stat('enderman','Enderman Ender','Endermen')
create_kill_stat('iron_golem','Defense Down!','Iron Golems')
create_kill_stat('panda','Kung FU! Panda','Pandas')
create_kill_stat('polar_bear','Polar Hunter','Polar Bears')
create_kill_stat('snow_golem','AntiFrosty','Snow Golems')
create_kill_stat('zombie_pigman','Nether Gang War','Zombie Pigmen')

# Passives
create_kill_stat('bat','Bat Flap','Bats')
create_kill_stat('chicken','Chicken Griller','Chickens')
create_kill_stat('cow','Cow Tipper','Cows')
create_kill_stat('horse','Horse Hater','Horses')
create_kill_stat('fox','What Does The Fox Say?','Foxes')
create_kill_stat('mooshroom','Mycelium Cowboy','Mooshrooms')
create_kill_stat('ocelot','Kitty Killer','Ocelots and Cats')
create_kill_stat('parrot','Stupid Bird!','Parrots')
create_kill_stat('pig','Pork Chopper','Pigs')
create_kill_stat('rabbit','Bunny Killer :(','Rabbits')
create_kill_stat('sheep','Big Bad Wolf','Sheep')
create_kill_stat('squid','Pool Cleaner','Squids')
create_kill_stat('turtle','Super Mario','Turtles')
create_kill_stat('villager','Bully','Villagers')
create_kill_stat('wandering_trader','Trade Sanctions','Wandering Traders')
create_kill_stat('wolf','Bad Dog!','Wolves and Dogs')

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
    ))
