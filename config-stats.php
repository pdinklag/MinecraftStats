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
            return number_format($cm / 100000, 1) . 'km';
        } else if($cm > 100) {
            return (int)($cm / 100) . 'm';
        } else {
            return $cm . 'cm';
        }
    }
    
    function ticksToTime($ticks) {
        $seconds = (int)($ticks / 20);
        
        $minutes = (int)($seconds / 60);
        $seconds %= 60;
        
        $hours = (int)($minutes / 60);
        $minutes %= 60;
        
        if($hours > 0) {
            return sprintf("%d:%02d h", $hours, $minutes);
        } else if($minutes > 0) {
            return sprintf("%d:%02d min", $minutes, $seconds);
        } else {
            return "$seconds s";
        }
    }
    
    function safeGet($key, $json, $def) {
        if(array_key_exists($key, $json)) {
            return $json[$key];
        } else {
            return $def;
        }
    }
    
    function breakToolProvider($json) {
        $sum =
            safeGet('stat.breakItem.minecraft.fishing_rod', $json, 0) +
            safeGet('stat.breakItem.minecraft.shears', $json, 0) +
            safeGet('stat.breakItem.minecraft.wooden_axe', $json, 0) +
            safeGet('stat.breakItem.minecraft.wooden_hoe', $json, 0) +
            safeGet('stat.breakItem.minecraft.wooden_pickaxe', $json, 0) +
            safeGet('stat.breakItem.minecraft.wooden_shovel', $json, 0) +
            safeGet('stat.breakItem.minecraft.stone_axe', $json, 0) +
            safeGet('stat.breakItem.minecraft.stone_hoe', $json, 0) +
            safeGet('stat.breakItem.minecraft.stone_pickaxe', $json, 0) +
            safeGet('stat.breakItem.minecraft.stone_shovel', $json, 0) +
            safeGet('stat.breakItem.minecraft.iron_axe', $json, 0) +
            safeGet('stat.breakItem.minecraft.iron_hoe', $json, 0) +
            safeGet('stat.breakItem.minecraft.iron_pickaxe', $json, 0) +
            safeGet('stat.breakItem.minecraft.iron_shovel', $json, 0) +
            safeGet('stat.breakItem.minecraft.golden_axe', $json, 0) +
            safeGet('stat.breakItem.minecraft.golden_hoe', $json, 0) +
            safeGet('stat.breakItem.minecraft.golden_pickaxe', $json, 0) +
            safeGet('stat.breakItem.minecraft.golden_shovel', $json, 0) +
            safeGet('stat.breakItem.minecraft.diamond_axe', $json, 0) +
            safeGet('stat.breakItem.minecraft.diamond_hoe', $json, 0) +
            safeGet('stat.breakItem.minecraft.diamond_pickaxe', $json, 0) +
            safeGet('stat.breakItem.minecraft.diamond_shovel', $json, 0);
            
        return ($sum > 0) ? $sum : FALSE;
    }
    
    function craftArmorProvider($json) {
        $sum =
            safeGet('stat.craftItem.minecraft.leather_helmet', $json, 0) +
            safeGet('stat.craftItem.minecraft.leather_chestplate', $json, 0) +
            safeGet('stat.craftItem.minecraft.leather_leggings', $json, 0) +
            safeGet('stat.craftItem.minecraft.leather_boots', $json, 0) +
            safeGet('stat.craftItem.minecraft.chainmail_helmet', $json, 0) +
            safeGet('stat.craftItem.minecraft.chainmail_chestplate', $json, 0) +
            safeGet('stat.craftItem.minecraft.chainmail_leggings', $json, 0) +
            safeGet('stat.craftItem.minecraft.chainmail_boots', $json, 0) +
            safeGet('stat.craftItem.minecraft.iron_helmet', $json, 0) +
            safeGet('stat.craftItem.minecraft.iron_chestplate', $json, 0) +
            safeGet('stat.craftItem.minecraft.iron_leggings', $json, 0) +
            safeGet('stat.craftItem.minecraft.iron_boots', $json, 0) +
            safeGet('stat.craftItem.minecraft.golden_helmet', $json, 0) +
            safeGet('stat.craftItem.minecraft.golden_chestplate', $json, 0) +
            safeGet('stat.craftItem.minecraft.golden_leggings', $json, 0) +
            safeGet('stat.craftItem.minecraft.golden_boots', $json, 0) +
            safeGet('stat.craftItem.minecraft.diamond_helmet', $json, 0) +
            safeGet('stat.craftItem.minecraft.diamond_chestplate', $json, 0) +
            safeGet('stat.craftItem.minecraft.diamond_leggings', $json, 0) +
            safeGet('stat.craftItem.minecraft.diamond_boots', $json, 0);
        
        return ($sum > 0) ? $sum : FALSE;
    }
    
    function eatMeatProvider($json) {
        $sum =
            safeGet('stat.useItem.minecraft.cooked_chicken', $json, 0) +
            safeGet('stat.useItem.minecraft.chicken', $json, 0) +
            safeGet('stat.useItem.minecraft.cooked_beef', $json, 0) +
            safeGet('stat.useItem.minecraft.beef', $json, 0) +
            safeGet('stat.useItem.minecraft.cooked_mutton', $json, 0) +
            safeGet('stat.useItem.minecraft.mutton', $json, 0) +
            safeGet('stat.useItem.minecraft.cooked_porkchop', $json, 0) +
            safeGet('stat.useItem.minecraft.porkchop', $json, 0) +
            safeGet('stat.useItem.minecraft.cooked_rabbit', $json, 0) +
            safeGet('stat.useItem.minecraft.rabbit', $json, 0) +
            safeGet('stat.useItem.minecraft.rabbit_stew', $json, 0);
            
        return ($sum > 0) ? $sum : FALSE;
    }
    
    function eatRawMeatProvider($json) {
        $sum =
            safeGet('stat.useItem.minecraft.chicken', $json, 0) +
            safeGet('stat.useItem.minecraft.beef', $json, 0) +
            safeGet('stat.useItem.minecraft.mutton', $json, 0) +
            safeGet('stat.useItem.minecraft.porkchop', $json, 0) +
            safeGet('stat.useItem.minecraft.rabbit', $json, 0) +
            safeGet('stat.useItem.minecraft.fish', $json, 0);
            
        return ($sum > 0) ? $sum : FALSE;
    }
    
    function eatVeggiesProvider($json) {
        $sum =
            safeGet('stat.useItem.minecraft.apple', $json, 0) +
            safeGet('stat.useItem.minecraft.baked_potato', $json, 0) +
            safeGet('stat.useItem.minecraft.break', $json, 0) +
            safeGet('stat.useItem.minecraft.beef', $json, 0) +
            safeGet('stat.useItem.minecraft.cake', $json, 0) +
            safeGet('stat.useItem.minecraft.carrot', $json, 0) +
            safeGet('stat.useItem.minecraft.cookie', $json, 0) +
            safeGet('stat.useItem.minecraft.golden_apple', $json, 0) +
            safeGet('stat.useItem.minecraft.golden_carrot', $json, 0) +
            safeGet('stat.useItem.minecraft.melon', $json, 0) +
            safeGet('stat.useItem.minecraft.mushroom_stew', $json, 0) +
            safeGet('stat.useItem.minecraft.potato', $json, 0) +
            safeGet('stat.useItem.minecraft.pumpkin_pie', $json, 0);
            
        return ($sum > 0) ? $sum : FALSE;
    }
    
    function eatFishProvider($json) {
        $sum =
            safeGet('stat.useItem.minecraft.cooked_fished', $json, 0) +
            safeGet('stat.useItem.minecraft.fish', $json, 0);
            
        return ($sum > 0) ? $sum : FALSE;
    }
    
    function eatStewProvider($json) {
        $sum =
            safeGet('stat.useItem.minecraft.mushroom_stew', $json, 0) +
            safeGet('stat.useItem.minecraft.rabbit_stew', $json, 0);
            
        return ($sum > 0) ? $sum : FALSE;
    }
    
    function eatCrapProvider($json) {
        $sum =
            safeGet('stat.useItem.minecraft.rotten_flesh', $json, 0) +
            safeGet('stat.useItem.minecraft.spider_eye', $json, 0) +
            safeGet('stat.useItem.minecraft.poisonous_potato', $json, 0);
            
        return ($sum > 0) ? $sum : FALSE;
    }
    
    function exploreBiomesProvider($json) {
        $sum = count($json['achievement.exploreAllBiomes']['progress']);
        return ($sum > 0) ? $sum : FALSE;
    }
    
    function placePlantProvider($json) {
        $sum =
            safeGet('stat.useItem.minecraft.sapling', $json, 0) +
            safeGet('stat.useItem.minecraft.yellow_flower', $json, 0) +
            safeGet('stat.useItem.minecraft.red_flower', $json, 0) +
            safeGet('stat.useItem.minecraft.double_plant', $json, 0);
        
        return ($sum > 0) ? $sum : FALSE;
    }
    
    function placeRedstoneProvider($json) {
        $sum =
            safeGet('stat.useItem.minecraft.redstone', $json, 0) +
            safeGet('stat.useItem.minecraft.stone_button', $json, 0) +
            safeGet('stat.useItem.minecraft.wooden_button', $json, 0) +
            safeGet('stat.useItem.minecraft.daylight_detector', $json, 0) +
            safeGet('stat.useItem.minecraft.daylight_detector_inverted', $json, 0) +
            safeGet('stat.useItem.minecraft.detector_rail', $json, 0) +
            safeGet('stat.useItem.minecraft.lever', $json, 0) +
            safeGet('stat.useItem.minecraft.stone_pressure_plate', $json, 0) +
            safeGet('stat.useItem.minecraft.wooden_pressure_plate', $json, 0) +
            safeGet('stat.useItem.minecraft.light_weighted_pressure_plate', $json, 0) +
            safeGet('stat.useItem.minecraft.heavy_weighted_pressure_plate', $json, 0) +
            safeGet('stat.useItem.minecraft.redstone_torch', $json, 0);
        
        return ($sum > 0) ? $sum : FALSE;
    }
    
    function placeTrapProvider($json) {
        $sum =
            safeGet('stat.useItem.minecraft.trapped_chest', $json, 0) +
            safeGet('stat.useItem.minecraft.tripwire_hook', $json, 0) +
            safeGet('stat.useItem.minecraft.tripwire', $json, 0);
        
        return ($sum > 0) ? $sum : FALSE;
    }

    $stats = [
        'achievement.buildSword' => [
            'award' => 'Blacksmith',
            'desc'  => 'Swords crafted',
            'icon'  => 'items/stone_sword.png',
        ],
        'achievement.diamonds' => [
            'award' => 'Capitalist',
            'desc'  => 'Diamonds acquired',
            'icon'  => 'blocks/diamond_block.png',
        ],
        'achievement.diamondsToYou' => [
            'award' => 'Communist',
            'desc'  => 'Diamonds tossed to others',
            'icon'  => 'items/diamond.png',
        ],
        'achievement.ghast' => [
            'award' => 'Minecraft Open',
            'desc'  => 'Ghasts killed with own fireball',
            'icon'  => 'items/fireball.png',
        ],
        'achievement.killEnemy' => [
            'award' => 'Hero',
            'desc'  => 'Enemies killed',
            'icon'  => 'items/diamond_sword.png',
        ],
        'achievement.mineWood' => [
            'award' => 'Woodcutter',
            'desc'  => 'Wood cut',
            'icon'  => 'blocks/log_oak_top.png',
        ],
        'achievement.openInventory' => [
            'award' => 'Where did I put...?',
            'desc'  => 'Times the inventory was opened',
            'icon'  => 'blocks/crafting_table_front.png',
        ],
        'achievement.portal' => [
            'award' => 'Multiworld',
            'desc'  => 'Number of portal uses',
            'icon'  => 'blocks/portal.png',
        ],
        'achievement.potion' => [
            'award' => 'Alchemist',
            'desc'  => 'Potions brewed',
            'icon'  => 'items/brewing_stand.png'
        ],
        'custom.breakTool' => [
            'award' => 'Wastrel',
            'desc'  => 'Tools broken',
            'icon'  => 'items/stick.png',
            'provider' => 'breakToolProvider',
        ],
        'custom.craftArmor' => [
            'award' => 'Armorer',
            'desc'  => 'Pieces of armor crafted',
            'icon'  => 'items/diamond_chestplate.png',
            'provider' => 'craftArmorProvider',
        ],
        'custom.eatMeat' => [
            'award' => 'Meat on the Table',
            'desc'  => 'Meat items eaten',
            'icon'  => 'items/beef_cooked.png',
            'provider' => 'eatMeatProvider',
        ],
        'custom.eatRawMeat' => [
            'award' => 'Raw Eater',
            'desc'  => 'Raw meat items eaten',
            'icon'  => 'items/beef_raw.png',
            'provider' => 'eatRawMeatProvider',
        ],
        'custom.eatStew' => [
            'award' => 'Soupy Kaspar',
            'desc'  => 'Stews eaten',
            'icon'  => 'items/mushroom_stew.png',
            'provider' => 'eatStewProvider',
        ],
        'custom.eatFish' => [
            'award' => 'Fish Gourmet',
            'desc'  => 'Fish eaten',
            'icon'  => 'items/fish_cod_cooked.png',
            'provider' => 'eatFishProvider',
        ],
        'custom.eatVeggies' => [
            'award' => 'Vegetarian',
            'desc'  => 'Veggie items eaten',
            'icon'  => 'items/apple.png',
            'provider' => 'eatVeggiesProvider',
        ],
        'custom.eatCrap' => [
            'award' => 'Bottom Feeder',
            'desc'  => 'Crap items eaten',
            'icon'  => 'items/rotten_flesh.png',
            'provider' => 'eatCrapProvider',
        ],
        'custom.exploreBiomes' => [
            'award' => 'Explorer',
            'desc'  => 'Different biomes explored',
            'icon'  => 'items/map_filled.png',
            'provider' => 'exploreBiomesProvider',
        ],
        'custom.placePlant' => [
            'award' => 'Green Thumb',
            'desc'  => 'Saplings and flowers planted',
            'icon'  => 'blocks/sapling_oak.png',
            'provider' => 'placePlantProvider',
        ],
        'custom.placeRedstone' => [
            'award' => 'Electrician',
            'desc'  => 'Redstone items placed',
            'icon'  => 'items/redstone_dust.png',
            'provider' => 'placeRedstoneProvider',
        ],
        'custom.placeTrap' => [
            'award' => 'Prankster',
            'desc'  => 'Trap items placed',
            'icon'  => 'blocks/trip_wire_source.png',
            'provider' => 'placeTrapProvider',
        ],
        'stat.animalsBred' => [
            'award' => 'Animal Lover',
            'desc'  => 'Animals bred',
            'icon'  => 'items/wheat.png',
        ],
        'stat.boatOneCm' => [
            'award' => 'Sailor',
            'desc'  => 'Distance gone by boat',
            'icon'  => 'items/boat.png',
            'displayFunc' => 'cmToDistance',
        ],
        'stat.climbOneCm' => [
            'award' => 'Climber',
            'desc'  => 'Distance climbed',
            'icon'  => 'blocks/ladder.png',
            'displayFunc' => 'cmToDistance',
        ],
        'stat.craftItem.minecraft.beacon' => [
            'award' => 'Ray of Light',
            'desc'  => 'Beacons crafted',
            'icon'  => 'blocks/beacon.png',
        ],
        'stat.craftItem.minecraft.clock' => [
            'award' => 'What time is it?',
            'desc'  => 'Clocks crafted',
            'icon'  => 'items/clock.png',
        ],
        'stat.craftItem.minecraft.compass' => [
            'award' => 'Where am I?',
            'desc'  => 'Compasses crafted',
            'icon'  => 'items/compass.png',
        ],
        'stat.craftItem.minecraft.cookie' => [
            'award' => 'Cookie Monster',
            'desc'  => 'Cookies made',
            'icon'  => 'items/cookie.png',
        ],
        'stat.craftItem.minecraft.ender_chest' => [
            'award' => 'Grief This!',
            'desc'  => 'Ender Chests crafted',
            'icon'  => 'blocks/ender_chest.png',
        ],
        'stat.craftItem.minecraft.ender_eye' => [
            'award' => 'Stronghold Radar',
            'desc'  => 'Ender Eyes crafted',
            'icon'  => 'items/ender_eye.png',
        ],
        'stat.craftItem.minecraft.lit_pumpkin' => [
            'award' => 'Trick or Treat!',
            'desc'  => 'Jack o\'Lanterns crafted',
            'icon'  => 'blocks/pumpkin_face_on.png',
        ],
        'stat.crouchOneCm' => [
            'award' => 'Sneaker',
            'desc'  => 'Distance crouched',
            'icon'  => 'gui/eye.png',
            'displayFunc' => 'cmToDistance',
        ],
        'stat.damageDealt' => [
            'award' => 'Berserker',
            'desc'  => 'Hearts of damage dealt',
            'icon'  => 'gui/sword_bloody.png',
        ],
        'stat.damageTaken' => [
            'award' => 'Masochist',
            'desc'  => 'Hearts of damage taken',
            'icon'  => 'gui/heart_black.png',
        ],
        'stat.deaths' => [
            'award' => 'Extra Life',
            'desc'  => 'Number of deaths',
            'icon'  => 'gui/heart.png',
        ],
        'stat.diveOneCm' => [
            'award' => 'Diver',
            'desc'  => 'Distance dived',
            'icon'  => 'gui/depth_strider.png',
            'displayFunc' => 'cmToDistance',
        ],
        'stat.drop' => [
            'award' => 'Begone!',
            'desc'  => 'Items dropped',
        ],
        'stat.fallOneCm' => [
            'award' => 'Basejumper',
            'desc'  => 'Distance fallen',
            'displayFunc' => 'cmToDistance',
        ],
        'stat.fishCaught' => [
            'award' => 'Fisherman',
            'desc'  => 'Fish caught',
            'icon'  => 'items/fish_cod_raw.png',
        ],
        'stat.horseOneCm' => [
            'award' => 'Rider',
            'desc'  => 'Distance ridden on horse',
            'icon'  => 'items/saddle.png',
            'displayFunc' => 'cmToDistance',
        ],
        'stat.jump' => [
            'award' => 'Bunnyhopper',
            'desc'  => 'Times jumped',
            'icon'  => 'gui/bunny.png',
        ],
        'stat.junkFished' => [
            'award' => 'Wannabe Fisherman',
            'desc'  => 'Junk items fished',
            'icon'  => 'items/bowl.png',
        ],
        'stat.killEntity.Bat' => [
            'award' => 'Badman',
            'desc'  => 'Bats killed',
            'icon'  => 'minecraft-wiki/mobs/BatFace.png',
        ],
        'stat.killEntity.Blaze' => [
            'award' => 'Nether Extinguisher',
            'desc'  => 'Blazes killed',
            'icon'  => 'minecraft-wiki/mobs/Blaze_Face.png',
        ],
        'stat.killEntity.Chicken' => [
            'award' => 'Kentucky Fried Chicken',
            'desc'  => 'Chickens killed',
            'icon'  => 'items/chicken_cooked.png',
        ],
        'stat.killEntity.Cow' => [
            'award' => 'Cow Tipper',
            'desc'  => 'Cows killed',
            'icon'  => 'items/leather.png',
        ],
        'stat.killEntity.Creeper' => [
            'award' => 'Creeper Creep',
            'desc'  => 'Creepers killed',
            'icon'  => 'minecraft-wiki/mobs/CreeperFace.png',
        ],
        'stat.killEntity.Enderman' => [
            'award' => 'Enderman Ender',
            'desc'  => 'Endermen killed',
            'icon'  => 'minecraft-wiki/mobs/EndermanFace.png',
        ],
        'stat.killEntity.Endermite' => [
            'award' => 'Endermite Ender',
            'desc'  => 'Endermites killed',
            'icon'  => 'minecraft-wiki/mobs/64px-EndermiteFace.png',
        ],
        'stat.killEntity.EntityHorse' => [
            'award' => 'Horse Hater',
            'desc'  => 'Horses killed',
            'icon'  => 'minecraft-wiki/mobs/HorseHead.png',
        ],
        'stat.killEntity.Ghast' => [
            'award' => 'Tear Drinker',
            'desc'  => 'Ghasts killed',
            'icon'  => 'items/ghast_tear.png',
        ],
        'stat.killEntity.Guardian' => [
            'award' => 'Underwater Raider',
            'desc'  => 'Guardians killed',
            'icon'  => 'minecraft-wiki/mobs/64px-GuardianFace.png',
        ],
        'stat.killEntity.LavaSlime' => [
            'award' => 'Magma Cream',
            'desc'  => 'Magma Cubes killed',
            'icon'  => 'items/magma_cream.png',
        ],
        'stat.killEntity.MushroomCow' => [
            'award' => 'I Killed a Mooshroom!',
            'desc'  => 'Mooshrooms killed',
            'icon'  => 'minecraft-wiki/mobs/MooshroomFace.png',
        ],
        'stat.killEntity.Ocelot' => [
            'award' => 'Bad Kitty!',
            'desc'  => 'Ocelots / cats killed',
            'icon'  => 'minecraft-wiki/mobs/OcelotFace.png',
        ],
        'stat.killEntity.Pig' => [
            'award' => 'Bacon Lover',
            'desc'  => 'Pigs killed',
            'icon'  => 'items/porkchop_raw.png',
        ],
        'stat.killEntity.PigZombie' => [
            'award' => 'Against the Nether',
            'desc'  => 'Zombie Pigmen killed',
            'icon'  => 'minecraft-wiki/mobs/ZombiePigmanFace.png',
        ],
        'stat.killEntity.Rabbit' => [
            'award' => 'Bunny Killer :(',
            'desc'  => 'Rabbits killed',
            'icon'  => 'minecraft-wiki/mobs/Rabbiticon.png',
        ],
        'stat.killEntity.Sheep' => [
            'award' => 'Antishepherd',
            'desc'  => 'Sheep killed',
            'icon'  => 'minecraft-wiki/mobs/SheepFace.png',
        ],
        'stat.killEntity.Silverfish' => [
            'award' => 'Nasty Little...',
            'desc'  => 'Silverfish killed',
            'icon'  => 'minecraft-wiki/mobs/SilverfishFace.png',
        ],
        'stat.killEntity.Skeleton' => [
            'award' => 'Bone Collector',
            'desc'  => 'Skeletons killed',
            'icon'  => 'minecraft-wiki/mobs/SkeletonFace.png',
        ],
        'stat.killEntity.Slime' => [
            'award' => 'Swamp Lurker',
            'desc'  => 'Slimes killed',
            'icon'  => 'minecraft-wiki/mobs/SlimeFace.png',
        ],
        'stat.killEntity.Spider' => [
            'award' => 'Arachnophobia',
            'desc'  => 'Spiders killed',
            'icon'  => 'minecraft-wiki/mobs/SpiderFace.png',
        ],
        'stat.killEntity.Squid' => [
            'award' => 'Pool Cleaner',
            'desc'  => 'Squids killed',
            'icon'  => 'minecraft-wiki/mobs/Squidface.png',
        ],
        'stat.killEntity.Villager' => [
            'award' => 'Bully',
            'desc'  => 'Villagers killed',
            'icon'  => 'minecraft-wiki/mobs/Villagerhead.png',
        ],
        'stat.killEntity.VillagerGolem' => [
            'award' => 'Down with the Defense!',
            'desc'  => 'Iron Golems killed',
            'icon'  => 'minecraft-wiki/mobs/Vg_face.png',
        ],
        'stat.killEntity.Witch' => [
            'award' => 'Burn the Witch!',
            'desc'  => 'Witches killed',
            'icon'  => 'minecraft-wiki/mobs/Witchface2.png',
        ],
        'stat.killEntity.Wolf' => [
            'award' => 'Bad Dog!',
            'desc'  => 'Wolves / dogs killed',
            'icon'  => 'minecraft-wiki/mobs/WolfFace.png',
        ],
        'stat.killEntity.Zombie' => [
            'award' => 'Zombie Grinder',
            'desc'  => 'Zombies killed',
            'icon'  => 'minecraft-wiki/mobs/ZombieFace.png',
        ],
        'stat.mineBlock.minecraft.coal_ore' => [
            'award' => 'Black Gold',
            'desc'  => 'Coal ore blocks mined',
            'icon'  => 'blocks/coal_ore.png',
        ],
        'stat.mineBlock.minecraft.diamond_ore' => [
            'award' => 'X-Ray',
            'desc'  => 'Diamond ore blocks mined',
            'icon'  => 'blocks/diamond_ore.png',
        ],
        'stat.mineBlock.minecraft.dirt' => [
            'award' => 'Excavator',
            'desc'  => 'Dirt "mined"',
            'icon'  => 'items/stone_shovel.png',
        ],
        'stat.mineBlock.minecraft.emerald_ore' => [
            'award' => 'Mountain Miner',
            'desc'  => 'Emerald ore blocks mined',
            'icon'  => 'blocks/emerald_ore.png',
        ],
        'stat.mineBlock.minecraft.gold_ore' => [
            'award' => 'Gold Rush',
            'desc'  => 'Gold ore blocks mined',
            'icon'  => 'blocks/gold_ore.png',
        ],
        'stat.mineBlock.minecraft.ice' => [
            'award' => 'Ice Breaker',
            'desc'  => 'Ice blocks destroyed',
            'icon'  => 'blocks/ice.png',
        ],
        'stat.mineBlock.minecraft.iron_ore' => [
            'award' => 'Heart of Iron',
            'desc'  => 'Iron ore blocks mined',
            'icon'  => 'blocks/iron_ore.png',
        ],
        'stat.mineBlock.minecraft.lapis_ore' => [
            'award' => 'Enchanter\'s Gopher',
            'desc'  => 'Lapis Lazuli ore blocks mined',
            'icon'  => 'blocks/lapis_ore.png',
        ],
        'stat.mineBlock.minecraft.netherrack' => [
            'award' => 'Terraformer',
            'desc'  => 'Netherrack mined',
            'icon'  => 'blocks/netherrack.png',
        ],
        'stat.mineBlock.minecraft.obsidian' => [
            'award' => 'Obsidian Miner',
            'desc'  => 'Obsidian blocks mined',
            'icon'  => 'blocks/obsidian.png',
        ],
        'stat.mineBlock.minecraft.quartz_ore' => [
            'award' => 'Use the Quartz!',
            'desc'  => 'Nether Quartz ore blocks mined',
            'icon'  => 'blocks/quartz_ore.png',
        ],
        'stat.mineBlock.minecraft.redstone_ore' => [
            'award' => 'I Need This!',
            'desc'  => 'Redstone ore blocks mined',
            'icon'  => 'blocks/redstone_ore.png',
        ],
        'stat.mineBlock.minecraft.tallgrass' => [
            'award' => 'Lawnmower',
            'desc'  => 'Tall grass block destroyed',
            'icon'  => 'blocks/tallgrass.png',
        ],
        'stat.mineBlock.minecraft.torch' => [
            'award' => 'The Darkside',
            'desc'  => 'Torches destroyed',
            'icon'  => 'blocks/redstone_torch_off.png',
        ],
        'stat.mineBlock.minecraft.web' => [
            'award' => 'God...Damnit...!!',
            'desc'  => 'Cobweb removed',
            'icon'  => 'blocks/web.png',
        ],
        'stat.minecartOneCm' => [
            'award' => 'Rail Rider',
            'desc'  => 'Distance gone by minecart',
            'icon'  => 'items/minecart_normal.png',
            'displayFunc' => 'cmToDistance',
        ],
        'stat.mobKills' => [
            'award' => 'Killing Spree',
            'desc'  => 'Mobs killed',
        ],
        'stat.pigOneCm' => [
            'award' => 'Because I Can',
            'desc'  => 'Distance ridden on a pig',
            'icon'  => 'items/carrot_on_a_stick.png',
            'displayFunc' => 'cmToDistance',
        ],
        'stat.playOneMinute' => [
            'award' => 'Addict',
            'desc'  => 'Time played on the server',
            'displayFunc' => 'ticksToTime',
        ],
        'stat.sprintOneCm' => [
            'award' => 'Marathon Runner',
            'desc'  => 'Distance sprinted',
            'displayFunc' => 'cmToDistance',
            'icon'  => 'gui/speed.png',
        ],
        'stat.swimOneCm' => [
            'award' => 'Swimmer',
            'desc'  => 'Distance swum',
            'icon'  => 'blocks/water_still.png',
            'displayFunc' => 'cmToDistance',
        ],
        'stat.talkedToVillager' => [
            'award' => 'Negotiator',
            'desc'  => 'Villagers talked to',
        ],
        'stat.timeSinceDeath' => [
            'award' => 'Survivor',
            'desc'  => 'Time since last death',
            'displayFunc' => 'ticksToTime',
        ],
        'stat.tradedWithVillager' => [
            'award' => 'Trader',
            'desc'  => 'Villager trades completed',
            'icon'  => 'items/emerald.png',
        ],
        'stat.treasureFished' => [
            'award' => 'Treasure Hunter',
            'desc'  => 'Treasures fished',
            'icon'  => 'items/gold_ingot.png',
        ],
        'stat.useItem.minecraft.banner' => [
            'award' => 'Propaganda',
            'desc'  => 'Banners placed',
            'icon'  => 'items/banner.png',
        ],
        'stat.useItem.minecraft.bow' => [
            'award' => 'Archer',
            'desc'  => 'Arrows shot',
            'icon'  => 'items/bow_standby.png',
        ],
        'stat.useItem.minecraft.dirt' => [
            'award' => 'Dirtbag',
            'desc'  => 'Dirt placed',
            'icon'  => 'blocks/dirt.png',
        ],
        'stat.useItem.minecraft.egg' => [
            'award' => 'Catch!',
            'desc'  => 'Eggs thrown',
            'icon'  => 'items/egg.png',
        ],
        'stat.useItem.minecraft.fireworks' => [
            'award' => 'Happy New Year!',
            'desc'  => 'Fireworks launched',
            'icon'  => 'items/fireworks.png',
        ],
        'stat.useItem.minecraft.flint_and_steel' => [
            'award' => 'Pyromaniac',
            'desc'  => 'Fires started',
            'icon'  => 'blocks/fire.png',
        ],
        'stat.useItem.minecraft.flower_pot' => [
            'award' => 'Florist',
            'desc'  => 'Flower pots placed',
            'icon'  => 'blocks/flower_rose.png',
        ],
        'stat.useItem.minecraft.item_frame' => [
            'award' => 'Museum Owner',
            'desc'  => 'Item frames placed',
            'icon'  => 'items/item_frame.png',
        ],
        'stat.useItem.minecraft.jukebox' => [
            'award' => 'Disc Jockey',
            'desc'  => 'Jukeboxes placed',
            'icon'  => 'items/record_13.png',
        ],
        'stat.useItem.minecraft.lava_bucket' => [
            'award' => 'I\'m a Griefer!',
            'desc'  => 'Lava buckets emptied',
            'icon'  => 'items/bucket_lava.png',
        ],
        'stat.useItem.minecraft.milk_bucket' => [
            'award' => 'Milksop',
            'desc'  => 'Milk buckets drunk',
            'icon'  => 'items/bucket_milk.png',
        ],
        'stat.useItem.minecraft.nether_wart' => [
            'award' => 'Nether Farmer',
            'desc'  => 'Nether Warts planted',
            'icon'  => 'blocks/nether_wart_stage_2.png',
        ],
        'stat.useItem.minecraft.noteblock' => [
            'award' => 'Musician',
            'desc'  => 'Note blocks placed',
            'icon'  => 'blocks/noteblock.png',
        ],
        'stat.useItem.minecraft.piston' => [
            'award' => 'Mechanic',
            'desc'  => 'Pistons placed',
            'icon'  => 'blocks/piston_side.png',
        ],
        'stat.useItem.minecraft.potion' => [
            'award' => 'Are you a Wizard',
            'desc'  => 'Potions used',
            'icon'  => 'items/potion_bottle_empty.png',
        ],
        'stat.useItem.minecraft.rail' => [
            'award' => 'Railway Company',
            'desc'  => 'Rails placed',
            'icon'  => 'blocks/rail_normal.png',
        ],
        'stat.useItem.minecraft.sign' => [
            'award' => 'Readme.txt',
            'desc'  => 'Signs placed',
            'icon'  => 'items/sign.png',
        ],
        'stat.useItem.minecraft.snowball' => [
            'award' => 'Snowball Fight!',
            'desc'  => 'Snowballs thrown',
            'icon'  => 'items/snowball.png',
        ],
        'stat.useItem.minecraft.torch' => [
            'award' => 'Enlightened',
            'desc'  => 'Torches placed',
            'icon'  => 'blocks/torch_on.png',
        ],
        'stat.useItem.minecraft.water_bucket' => [
            'award' => 'Spring',
            'desc'  => 'Water buckets emptied',
            'icon'  => 'items/bucket_water.png',
        ],
        'stat.useItem.minecraft.writable_book' => [
            'award' => 'Bestseller',
            'desc'  => 'Books written',
            'icon'  => 'items/book_writable.png',
        ],
        'stat.walkOneCm' => [
            'award' => 'Traveler',
            'desc'  => 'Distance walked',
            'icon'  => 'items/iron_boots.png',
            'displayFunc' => 'cmToDistance',
        ],
    ];
?>
