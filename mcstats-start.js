var loader = new Loader(function() {
    mcstats.init();
    window.onhashchange(); // navigate
});

loader.addRequest('data/awards.json', function(result) {
    mcstats.awards = result;

    // sort award keys by award title
    for(var key in mcstats.awards) {
        mcstats.awardKeysByTitle.push(key);
    }

    mcstats.awardKeysByTitle.sort(function(a,b) {
        return mcstats.awards[a].title.localeCompare(
            mcstats.awards[b].title);
    });
});

loader.addRequest('data/hof.json', function(result) {
    mcstats.hof = result;
});

loader.addRequest('data/players.json', function(result) {
    mcstats.players = result;

    // sort player UUIDs by player name
    for(var uuid in mcstats.players) {
        mcstats.playerIdsByName.push(uuid);
    }

    mcstats.playerIdsByName.sort(function(a,b) {
        return mcstats.players[a].name.localeCompare(
            mcstats.players[b].name);
    });
});

loader.addRequest('data/info.json', function(result) {
    mcstats.info = result;

    $('title').html(`${result.serverName} &ndash; Stats`);
    $('#server-name').text(result.serverName);
    $('#update-time').text(formatTime(result.updateTime));

    if(!result.hasIcon) {
        $('#info #server-icon').hide();
    } else {
        $('#info #server-icon').attr('title', result.serverName);
    }
});

// Start
mcstats.showLoader();

loader.start();
