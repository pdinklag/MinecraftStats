from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'kill_any',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:mob_kills'])
    ))

def create_kill_stat(mobId, minVersion = 0, maxVersion = float("inf")):
    reader = mcstats.StatReader(['minecraft:killed','minecraft:' + mobId])
    
    mcstats.registry.append(
        mcstats.MinecraftStat(
            'kill_' + mobId,
            {
                'unit': 'int',
            },
            mcstats.StatReader(['minecraft:killed','minecraft:' + mobId]),
            minVersion,
            maxVersion
        ))

# Hostiles
create_kill_stat('blaze')
create_kill_stat('creeper')
create_kill_stat('endermite')
create_kill_stat('ender_dragon')
create_kill_stat('ghast')
create_kill_stat('magma_cube')
create_kill_stat('phantom', 1467) # added in 18w07a
# Note: Ravagers had been added as Illager Beats in 18w43a (1901)
# support for that snapshot may be added on demand
create_kill_stat('ravager', 1930) # changed in 19w05a
create_kill_stat('shulker')
create_kill_stat('silverfish')
create_kill_stat('slime')
create_kill_stat('vex')
create_kill_stat('warden', 3082 ) # added in 22w12a
create_kill_stat('witch')
create_kill_stat('wither_skeleton')

# Neutrals
create_kill_stat('bee', 2200) # added in 19w34a
create_kill_stat('dolphin',  1482) # added in 18w15a
create_kill_stat('enderman')
create_kill_stat('goat',  2705) # added in 21w13a
create_kill_stat('iron_golem')
create_kill_stat('panda', 1901) # added in 18w43a
create_kill_stat('piglin',  2506) # added in 20w07a
create_kill_stat('polar_bear')
create_kill_stat('snow_golem')
create_kill_stat('zombie_pigman', 2510) # renamed to Zombified Piglin in 20w09a
create_kill_stat('zombified_piglin', 2510)   # added in 20w09a
create_kill_stat('piglin_brute', 2569)   # added in 20w27a

# Passives
create_kill_stat('allay', 3085) #added in 22w13a
create_kill_stat('axolotl', 2687) #added in 20w51a
create_kill_stat('bat')
create_kill_stat('chicken')
create_kill_stat('cow')
create_kill_stat('horse')
create_kill_stat('fox', 1932) # added in 19w07a
create_kill_stat('frog', 3080 ) # added in 22w11a
create_kill_stat('mooshroom')
create_kill_stat('parrot')
create_kill_stat('pig')
create_kill_stat('rabbit')
create_kill_stat('sheep')
create_kill_stat('strider', 2520) # added in 20w13a
create_kill_stat('tadpole', 3080 ) # added in 22w11a
create_kill_stat('turtle', 1467) # added in 18w07a
create_kill_stat('villager')
create_kill_stat('wandering_trader', 1930) # added in 19w05a
create_kill_stat('wolf')

# Cats (including ozelots)
mcstats.registry.append(
    mcstats.MinecraftStat(
        'kill_ocelot',
        {
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
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:killed','minecraft:glow_squid']),
            mcstats.StatReader(['minecraft:killed','minecraft:squid']),
        ])
    ))
