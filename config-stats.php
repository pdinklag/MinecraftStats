<?
    /**
     * Configuration of stats to be tracked.
     *
     * NOTE: The icons referred to in this file cannot be 
     * included in the repository for legal reasons.
     * 
     * Please replace them with your own.
     */
    
    function cmToDistance($cm) {
        if($cm > 100000) {
            return number_format($cm / 100000, 1) . "km";
        } else if($cm > 100) {
            return (int)($cm / 100) . "m";
        } else {
            return $cm . "cm";
        }
    }
    
    function breakToolProvider($json) {
        $sum =
            $json['stat.breakItem.minecraft.fishing_rod'] +
            $json['stat.breakItem.minecraft.shears'] +
            $json['stat.breakItem.minecraft.wooden_axe'] +
            $json['stat.breakItem.minecraft.wooden_hoe'] +
            $json['stat.breakItem.minecraft.wooden_pickaxe'] +
            $json['stat.breakItem.minecraft.wooden_shovel'] +
            $json['stat.breakItem.minecraft.stone_axe'] +
            $json['stat.breakItem.minecraft.stone_hoe'] +
            $json['stat.breakItem.minecraft.stone_pickaxe'] +
            $json['stat.breakItem.minecraft.stone_shovel'] +
            $json['stat.breakItem.minecraft.iron_axe'] +
            $json['stat.breakItem.minecraft.iron_hoe'] +
            $json['stat.breakItem.minecraft.iron_pickaxe'] +
            $json['stat.breakItem.minecraft.iron_shovel'] +
            $json['stat.breakItem.minecraft.golden_axe'] +
            $json['stat.breakItem.minecraft.golden_hoe'] +
            $json['stat.breakItem.minecraft.golden_pickaxe'] +
            $json['stat.breakItem.minecraft.golden_shovel'] +
            $json['stat.breakItem.minecraft.diamond_axe'] +
            $json['stat.breakItem.minecraft.diamond_hoe'] +
            $json['stat.breakItem.minecraft.diamond_pickaxe'] +
            $json['stat.breakItem.minecraft.diamond_shovel'];
            
        return ($sum > 0) ? $sum : FALSE;
    }
    
    function eatMeatProvider($json) {
        $sum =
            $json['stat.useItem.minecraft.cooked_chicken'] +
            $json['stat.useItem.minecraft.chicken'] +
            $json['stat.useItem.minecraft.cooked_beef'] +
            $json['stat.useItem.minecraft.beef'] +
            $json['stat.useItem.minecraft.cooked_mutton'] +
            $json['stat.useItem.minecraft.mutton'] +
            $json['stat.useItem.minecraft.cooked_porkchop'] +
            $json['stat.useItem.minecraft.porkchop'] +
            $json['stat.useItem.minecraft.cooked_rabbit'] +
            $json['stat.useItem.minecraft.rabbit'] +
            $json['stat.useItem.minecraft.rabbit_stew'];
            
        return ($sum > 0) ? $sum : FALSE;
    }
    
    function eatRawMeatProvider($json) {
        $sum =
            $json['stat.useItem.minecraft.chicken'] +
            $json['stat.useItem.minecraft.beef'] +
            $json['stat.useItem.minecraft.mutton'] +
            $json['stat.useItem.minecraft.porkchop'] +
            $json['stat.useItem.minecraft.rabbit'];
            
        return ($sum > 0) ? $sum : FALSE;
    }
    
    function eatVeggiesProvider($json) {
        $sum =
            $json['stat.useItem.minecraft.apple'] +
            $json['stat.useItem.minecraft.baked_potato'] +
            $json['stat.useItem.minecraft.break'] +
            $json['stat.useItem.minecraft.beef'] +
            $json['stat.useItem.minecraft.cake'] +
            $json['stat.useItem.minecraft.carrot'] +
            $json['stat.useItem.minecraft.cookie'] +
            $json['stat.useItem.minecraft.golden_apple'] +
            $json['stat.useItem.minecraft.golden_carrot'] +
            $json['stat.useItem.minecraft.melon'] +
            $json['stat.useItem.minecraft.mushroom_stew'] +
            $json['stat.useItem.minecraft.potato'] +
            $json['stat.useItem.minecraft.pumpkin_pie'];
            
        return ($sum > 0) ? $sum : FALSE;
    }
    
    function eatFishProvider($json) {
        $sum =
            $json['stat.useItem.minecraft.cooked_fished'] +
            $json['stat.useItem.minecraft.fish'];
            
        return ($sum > 0) ? $sum : FALSE;
    }
    
    function eatCrapProvider($json) {
        $sum =
            $json['stat.useItem.minecraft.rotten_flesh'] +
            $json['stat.useItem.minecraft.spider_eye'] +
            $json['stat.useItem.minecraft.poisonous_potato'];
            
        return ($sum > 0) ? $sum : FALSE;
    }
    
    function mineLogProvider($json) {
        $sum =
            $json['stat.mineBlock.minecraft.log'] +
            $json['stat.mineBlock.minecraft.log2'];
            
        return ($sum > 0) ? $sum : FALSE;
    }

    $stats = [
        [
            'id' => 'achievement.buildSword',
            'award' => 'Blacksmith',
            'desc'  => 'Swords crafted',
            'icon'  => 'items/stone_sword.png',
        ],
        [
            'id' => 'achievement.diamonds',
            'award' => 'Capitalist',
            'desc'  => 'Diamonds acquired',
            'icon'  => 'blocks/diamond_block.png',
        ],
        [
            'id' => 'achievement.diamondsToYou',
            'award' => 'Communist',
            'desc'  => 'Diamonds tossed to others',
            'icon'  => 'items/diamond.png',
        ],
        [
            'id' => 'achievement.ghast',
            'award' => 'Minecraft Open',
            'desc'  => 'Ghasts killed with own fireball',
            'icon'  => 'items/fireball.png',
        ],
        [
            'id' => 'achievement.openInventory',
            'award' => 'Where did I put...?',
            'desc'  => 'Times the inventory was opened',
            'icon'  => 'blocks/crafting_table_front.png',
        ],
        [
            'id' => 'achievement.portal',
            'award' => 'Multiworld',
            'desc'  => 'Number of portal uses',
            'icon'  => 'blocks/portal.png',
        ],
        [
            'id' => 'achievement.potion',
            'award' => 'Alchemist',
            'desc'  => 'Potions brewed',
            'icon'  => 'items/brewing_stand.png'
        ],
        [
            'id' => 'custom.breakTool',
            'award' => 'Wastrel',
            'desc'  => 'Tools broken',
            'icon'  => 'items/stick.png',
            'provider' => 'breakToolProvider',
        ],
        [
            'id' => 'custom.eatMeat',
            'award' => 'Meat on the Table',
            'desc'  => 'Meat items eaten',
            'icon'  => 'items/beef_cooked.png',
            'provider' => 'eatMeatProvider',
        ],
        [
            'id' => 'custom.eatRawMeat',
            'award' => 'Raw Eater',
            'desc'  => 'Raw meat items eaten',
            'icon'  => 'items/beef_raw.png',
            'provider' => 'eatRawMeatProvider',
        ],
        [
            'id' => 'custom.eatFish',
            'award' => 'Fish Gourmet',
            'desc'  => 'Fish eaten',
            'icon'  => 'items/fish_cod_cooked.png',
            'provider' => 'eatFishProvider',
        ],
        [
            'id' => 'custom.eatVeggies',
            'award' => 'Vegetarian',
            'desc'  => 'Veggie items eaten',
            'icon'  => 'items/apple.png',
            'provider' => 'eatVeggiesProvider',
        ],
        [
            'id' => 'custom.eatCrap',
            'award' => 'Bottom Feeder',
            'desc'  => 'Crap items eaten',
            'icon'  => 'items/rotten_flesh.png',
            'provider' => 'eatCrapProvider',
        ],
        [
            'id' => 'custom.mineBlock.log',
            'award' => 'Woodcutter',
            'desc'  => 'Logs cut',
            'icon'  => 'blocks/log_oak_top.png',
            'provider' => 'mineLogProvider',
        ],
        [
            'id' => 'stat.animalsBred',
            'award' => 'Animal Lover',
            'desc'  => 'Animals bred',
            'icon'  => 'items/wheat.png',
        ],
        [
            'id' => 'stat.boatOneCm',
            'award' => 'Sailor',
            'desc'  => 'Distance gone by boat',
            'icon'  => 'items/boat.png',
            'displayFunc' => 'cmToDistance',
        ],
        [
            'id' => 'stat.climbOneCm',
            'award' => 'Climber',
            'desc'  => 'Distance climbed',
            'icon'  => 'blocks/ladder.png',
            'displayFunc' => 'cmToDistance',
        ],
        [
            'id' => 'stat.craftItem.minecraft.clock',
            'award' => 'What time is it?',
            'desc'  => 'Clocks crafted',
            'icon'  => 'items/clock.png',
        ],
        [
            'id' => 'stat.craftItem.minecraft.compass',
            'award' => 'Where am I?',
            'desc'  => 'Compasses crafted',
            'icon'  => 'items/compass.png',
        ],
        [
            'id' => 'stat.craftItem.minecraft.ender_eye',
            'award' => 'Stronghold Radar',
            'desc'  => 'Ender Eyes crafted',
            'icon'  => 'items/ender_eye.png',
        ],
        [
            'id' => 'stat.craftItem.minecraft.tnt',
            'award' => 'Bad Intentions',
            'desc'  => 'TNT crafted',
            'icon'  => 'blocks/tnt_side.png',
        ],
        [
            'id' => 'stat.crouchOneCm',
            'award' => 'Sneaker',
            'desc'  => 'Distance crouched',
            'icon'  => 'gui/eye.png',
            'displayFunc' => 'cmToDistance',
        ],
        [
            'id' => 'stat.damageDealt',
            'award' => 'Berserker',
            'desc'  => 'Hearts of damage dealt',
            'icon'  => 'gui/sword_bloody.png',
        ],
        [
            'id' => 'stat.damageTaken',
            'award' => 'Masochist',
            'desc'  => 'Hearts of damage taken',
            'icon'  => 'gui/heart_black.png',
        ],
        [
            'id' => 'stat.deaths',
            'award' => 'Extra Life',
            'desc'  => 'Number of deaths',
            'icon'  => 'gui/heart.png',
        ],
        [
            'id' => 'stat.diveOneCm',
            'award' => 'Diver',
            'desc'  => 'Distance dived',
            'icon'  => 'gui/depth_strider.png',
            'displayFunc' => 'cmToDistance',
        ],
        [
            'id' => 'stat.drop',
            'award' => 'Begone!',
            'desc'  => 'Items dropped',
        ],
        [
            'id' => 'stat.fallOneCm',
            'award' => 'Basejumper',
            'desc'  => 'Distance fallen',
            'displayFunc' => 'cmToDistance',
        ],
        [
            'id' => 'stat.fishCaught',
            'award' => 'Fisherman',
            'desc'  => 'Fish caught',
            'icon'  => 'items/fish_cod_raw.png',
        ],
        [
            'id' => 'stat.horseOneCm',
            'award' => 'Rider',
            'desc'  => 'Distance ridden on horse',
            'icon'  => 'items/saddle.png',
            'displayFunc' => 'cmToDistance',
        ],
        [
            'id' => 'stat.jump',
            'award' => 'Bunnyhopper',
            'desc'  => 'Times jumped',
            'icon'  => 'gui/bunny.png',
        ],
        [
            'id' => 'stat.junkFished',
            'award' => 'Wannabe Fisherman',
            'desc'  => 'Junk items fished',
            'icon'  => 'items/bowl.png',
        ],
        [
            'id' => 'stat.killEntity.Bat',
            'award' => 'Badman',
            'desc'  => 'Bats killed',
            'icon'  => 'minecraft-wiki/BatFace.png',
        ],
        [
            'id' => 'stat.killEntity.Blaze',
            'award' => 'Nether Extinguisher',
            'desc'  => 'Blazes killed',
            'icon'  => 'minecraft-wiki/Blaze_Face.png',
        ],
        [
            'id' => 'stat.killEntity.Chicken',
            'award' => 'Kentucky Fried Chicken',
            'desc'  => 'Chickens killed',
            'icon'  => 'items/chicken_cooked.png',
        ],
        [
            'id' => 'stat.killEntity.Cow',
            'award' => 'Cow Tipper',
            'desc'  => 'Cows killed',
            'icon'  => 'items/leather.png',
        ],
        [
            'id' => 'stat.killEntity.Creeper',
            'award' => 'Creeper Creep',
            'desc'  => 'Creepers killed',
            'icon'  => 'minecraft-wiki/CreeperFace.png',
        ],
        [
            'id' => 'stat.killEntity.Enderman',
            'award' => 'Enderman Ender',
            'desc'  => 'Endermen killed',
            'icon'  => 'minecraft-wiki/EndermanFace.png',
        ],
        [
            'id' => 'stat.killEntity.Endermite',
            'award' => 'Endermite Ender',
            'desc'  => 'Endermites killed',
            'icon'  => 'minecraft-wiki/64px-EndermiteFace.png',
        ],
        [
            'id' => 'stat.killEntity.EntityHorse',
            'award' => 'Horse Hater',
            'desc'  => 'Horses killed',
            'icon'  => 'minecraft-wiki/HorseHead.png',
        ],
        [
            'id' => 'stat.killEntity.Ghast',
            'award' => 'Tear Drinker',
            'desc'  => 'Ghasts killed',
            'icon'  => 'items/ghast_tear.png',
        ],
        [
            'id' => 'stat.killEntity.Guardian',
            'award' => 'Underwater Raider',
            'desc'  => 'Guardians killed',
            'icon'  => 'minecraft-wiki/64px-GuardianFace.png',
        ],
        [
            'id' => 'stat.killEntity.LavaSlime',
            'award' => 'Magma Cream',
            'desc'  => 'Magma Cubes killed',
            'icon'  => 'items/magma_cream.png',
        ],
        [
            'id' => 'stat.killEntity.MushroomCow',
            'award' => 'I Killed a Mooshroom!',
            'desc'  => 'Mooshrooms killed',
            'icon'  => 'minecraft-wiki/MooshroomFace.png',
        ],
        [
            'id' => 'stat.killEntity.Ocelot',
            'award' => 'Bad Kitty!',
            'desc'  => 'Ocelots / cats killed',
            'icon'  => 'minecraft-wiki/OcelotFace.png',
        ],
        [
            'id' => 'stat.killEntity.Pig',
            'award' => 'Bacon Lover',
            'desc'  => 'Pigs killed',
            'icon'  => 'items/porkchop_raw.png',
        ],
        [
            'id' => 'stat.killEntity.PigZombie',
            'award' => 'Against the Nether',
            'desc'  => 'Zombie Pigmen killed',
            'icon'  => 'minecraft-wiki/ZombiePigmanFace.png',
        ],
        [
            'id' => 'stat.killEntity.Rabbit',
            'award' => 'Bunny Killer :(',
            'desc'  => 'Rabbits killed',
            'icon'  => 'minecraft-wiki/Rabbiticon.png',
        ],
        [
            'id' => 'stat.killEntity.Sheep',
            'award' => 'Antishepherd',
            'desc'  => 'Sheep killed',
            'icon'  => 'minecraft-wiki/SheepFace.png',
        ],
        [
            'id' => 'stat.killEntity.Silverfish',
            'award' => 'Nasty Little...',
            'desc'  => 'Silverfish killed',
            'icon'  => 'minecraft-wiki/SilverfishFace.png',
        ],
        [
            'id' => 'stat.killEntity.Skeleton',
            'award' => 'Bone Collector',
            'desc'  => 'Skeletons killed',
            'icon'  => 'minecraft-wiki/SkeletonFace.png',
        ],
        [
            'id' => 'stat.killEntity.Slime',
            'award' => 'Swamp Lurker',
            'desc'  => 'Slimes killed',
            'icon'  => 'minecraft-wiki/SlimeFace.png',
        ],
        [
            'id' => 'stat.killEntity.Spider',
            'award' => 'Arachnophobia',
            'desc'  => 'Spiders killed',
            'icon'  => 'minecraft-wiki/SpiderFace.png',
        ],
        [
            'id' => 'stat.killEntity.Squid',
            'award' => 'Pool Cleaner',
            'desc'  => 'Squids killed',
            'icon'  => 'minecraft-wiki/Squidface.png',
        ],
        [
            'id' => 'stat.killEntity.Villager',
            'award' => 'Bully',
            'desc'  => 'Villagers killed',
            'icon'  => 'minecraft-wiki/Villagerhead.png',
        ],
        [
            'id' => 'stat.killEntity.VillagerGolem',
            'award' => 'Down with the Defense!',
            'desc'  => 'Iron Golems killed',
            'icon'  => 'minecraft-wiki/Vg_face.png',
        ],
        [
            'id' => 'stat.killEntity.Witch',
            'award' => 'Burn the Witch!',
            'desc'  => 'Witches killed',
            'icon'  => 'minecraft-wiki/Witchface2.png',
        ],
        [
            'id' => 'stat.killEntity.Wolf',
            'award' => 'Bad Dog!',
            'desc'  => 'Wolves / dogs killed',
            'icon'  => 'minecraft-wiki/WolfFace.png',
        ],
        [
            'id' => 'stat.killEntity.Zombie',
            'award' => 'Zombie Grinder',
            'desc'  => 'Zombies killed',
            'icon'  => 'minecraft-wiki/ZombieFace.png',
        ],
        [
            'id' => 'stat.mineBlock.minecraft.coal_ore',
            'award' => 'Black Gold',
            'desc'  => 'Coal ore blocks mined',
            'icon'  => 'blocks/coal_ore.png',
        ],
        [
            'id' => 'stat.mineBlock.minecraft.diamond_ore',
            'award' => 'X-Ray',
            'desc'  => 'Diamond ore blocks mined',
            'icon'  => 'blocks/diamond_ore.png',
        ],
        [
            'id' => 'stat.mineBlock.minecraft.dirt',
            'award' => 'Excavator',
            'desc'  => 'Dirt "mined"',
            'icon'  => 'items/stone_shovel.png',
        ],
        [
            'id' => 'stat.mineBlock.minecraft.emerald_ore',
            'award' => 'Mountain Miner',
            'desc'  => 'Emerald ore blocks mined',
            'icon'  => 'blocks/emerald_ore.png',
        ],
        [
            'id' => 'stat.mineBlock.minecraft.gold_ore',
            'award' => 'Gold Rush',
            'desc'  => 'Gold ore blocks mined',
            'icon'  => 'blocks/gold_ore.png',
        ],
        [
            'id' => 'stat.mineBlock.minecraft.ice',
            'award' => 'Ice Breaker',
            'desc'  => 'Ice blocks destroyed',
            'icon'  => 'blocks/ice.png',
        ],
        [
            'id' => 'stat.mineBlock.minecraft.iron_ore',
            'award' => 'Heart of Iron',
            'desc'  => 'Iron ore blocks mined',
            'icon'  => 'blocks/iron_ore.png',
        ],
        [
            'id' => 'stat.mineBlock.minecraft.lapis_ore',
            'award' => 'Enchanter\'s Gopher',
            'desc'  => 'Lapis Lazuli ore blocks mined',
            'icon'  => 'blocks/lapis_ore.png',
        ],
        [
            'id' => 'stat.mineBlock.minecraft.obsidian',
            'award' => 'Obsidian Miner',
            'desc'  => 'Obsidian blocks mined',
            'icon'  => 'blocks/obsidian.png',
        ],
        [
            'id' => 'stat.mineBlock.minecraft.quartz_ore',
            'award' => 'Use the Quartz!',
            'desc'  => 'Nether Quartz ore blocks mined',
            'icon'  => 'blocks/quartz_ore.png',
        ],
        [
            'id' => 'stat.mineBlock.minecraft.redstone_ore',
            'award' => 'I Need This!',
            'desc'  => 'Redstone ore blocks mined',
            'icon'  => 'blocks/redstone_ore.png',
        ],
        [
            'id' => 'stat.mineBlock.minecraft.tallgrass',
            'award' => 'Lawnmower',
            'desc'  => 'Tall grass block destroyed',
            'icon'  => 'blocks/tallgrass.png',
        ],
        [
            'id' => 'stat.mineBlock.minecraft.torch',
            'award' => 'The Darkside',
            'desc'  => 'Torches destroyed',
            'icon'  => 'blocks/redstone_torch_off.png',
        ],
        [
            'id' => 'stat.mineBlock.minecraft.web',
            'award' => 'God...Damnit...!!',
            'desc'  => 'Cobweb removed',
            'icon'  => 'blocks/web.png',
        ],
        [
            'id' => 'stat.minecartOneCm',
            'award' => 'Rail Rider',
            'desc'  => 'Distance gone by minecart',
            'icon'  => 'items/minecart_normal.png',
            'displayFunc' => 'cmToDistance',
        ],
        [
            'id' => 'stat.mobKills',
            'award' => 'Killing Spree',
            'desc'  => 'Mobs killed',
        ],
        [
            'id' => 'stat.pigOneCm',
            'award' => 'Because I Can',
            'desc'  => 'Distance ridden on a pig',
            'icon'  => 'items/carrot_on_a_stick.png',
            'displayFunc' => 'cmToDistance',
        ],
        [
            'id' => 'stat.sprintOneCm',
            'award' => 'Marathon Runner',
            'desc'  => 'Distance sprinted',
            'displayFunc' => 'cmToDistance',
        ],
        [
            'id' => 'stat.swimOneCm',
            'award' => 'Swimmer',
            'desc'  => 'Distance swum',
            'icon'  => 'blocks/water_still.png',
            'displayFunc' => 'cmToDistance',
        ],
        [
            'id' => 'stat.talkedToVillager',
            'award' => 'Negotiator',
            'desc'  => 'Villagers talked to',
        ],
        [
            'id' => 'stat.tradedWithVillager',
            'award' => 'Trader',
            'desc'  => 'Villager trades completed',
            'icon'  => 'items/emerald.png',
        ],
        [
            'id' => 'stat.treasureFished',
            'award' => 'Treasure Hunter',
            'desc'  => 'Treasures fished',
            'icon'  => 'items/gold_ingot.png',
        ],
        [
            'id' => 'stat.useItem.minecraft.dirt',
            'award' => 'Dirtbag',
            'desc'  => 'Dirt placed',
            'icon'  => 'blocks/dirt.png',
        ],
        [
            'id' => 'stat.useItem.minecraft.fireworks',
            'award' => 'Happy New Year!',
            'desc'  => 'Fireworks launched',
            'icon'  => 'items/fireworks.png',
        ],
        [
            'id' => 'stat.useItem.minecraft.flint_and_steel',
            'award' => 'Pyromaniac',
            'desc'  => 'Fires started',
            'icon'  => 'blocks/fire.png',
        ],
        [
            'id' => 'stat.useItem.minecraft.flower_pot',
            'award' => 'Florist',
            'desc'  => 'Flower pots placed',
            'icon'  => 'blocks/flower_rose.png',
        ],
        [
            'id' => 'stat.useItem.minecraft.item_frame',
            'award' => 'Museum Owner',
            'desc'  => 'Item frames placed',
            'icon'  => 'items/item_frame.png',
        ],
        [
            'id' => 'stat.useItem.minecraft.jukebox',
            'award' => 'Disc Jockey',
            'desc'  => 'Jukeboxes placed',
            'icon'  => 'items/record_13.png',
        ],
        [
            'id' => 'stat.useItem.minecraft.lava_bucket',
            'award' => 'I\'m a Griefer!',
            'desc'  => 'Lava buckets emptied',
            'icon'  => 'items/bucket_lava.png',
        ],
        [
            'id' => 'stat.useItem.minecraft.noteblock',
            'award' => 'Musician',
            'desc'  => 'Note blocks placed',
            'icon'  => 'blocks/noteblock.png',
        ],
        [
            'id' => 'stat.useItem.minecraft.piston',
            'award' => 'Mechanic',
            'desc'  => 'Pistons placed',
            'icon'  => 'blocks/piston_side.png',
        ],
        [
            'id' => 'stat.useItem.minecraft.potion',
            'award' => 'Are you a Wizard',
            'desc'  => 'Potions used',
            'icon'  => 'items/potion_bottle_empty.png',
        ],
        [
            'id' => 'stat.useItem.minecraft.rail',
            'award' => 'Railway Company',
            'desc'  => 'Rails placed',
            'icon'  => 'blocks/rail_normal.png',
        ],
        [
            'id' => 'stat.useItem.minecraft.redstone',
            'award' => 'Electrician',
            'desc'  => 'Redstone wire placed',
            'icon'  => 'items/redstone_dust.png',
        ],
        [
            'id' => 'stat.useItem.minecraft.sign',
            'award' => 'readme.txt',
            'desc'  => 'Signs placed',
            'icon'  => 'items/sign.png',
        ],
        [
            'id' => 'stat.useItem.minecraft.torch',
            'award' => 'Enlightened',
            'desc'  => 'Torches placed',
            'icon'  => 'blocks/torch_on.png',
        ],
        [
            'id' => 'stat.walkOneCm',
            'award' => 'Traveler',
            'desc'  => 'Distance walked',
            'icon'  => 'items/iron_boots.png',
            'displayFunc' => 'cmToDistance',
        ],
    ];
?>
