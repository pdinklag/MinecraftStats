var loader = new Loader(function() {
    mcstats.init();
    window.onhashchange(); // navigate
});

loader.addRequest('data/db.json.gz', function(db) {
    // load db
    mcstats.info = db.info;
    mcstats.players = db.players;
    mcstats.awards = db.awards;
    mcstats.hof = db.hof;

    // fill server info
    $('title').html(`${mcstats.info.serverName} &ndash; Stats`);
    $('#server-name').text(mcstats.info.serverName);
    $('#update-time').text(formatTime(mcstats.info.updateTime));

    if(!mcstats.info.hasIcon) {
        $('#info #server-icon').hide();
    } else {
        $('#info #server-icon').attr('title', mcstats.info.serverName);
    }

    // sort award keys by award title
    for(var key in mcstats.awards) {
        mcstats.awardKeysByTitle.push(key);
    }

    mcstats.awardKeysByTitle.sort(function(a,b) {
        return mcstats.awards[a].title.localeCompare(
            mcstats.awards[b].title);
    });

    // sort player UUIDs by player name
    for(var uuid in mcstats.players) {
        mcstats.playerIdsByName.push(uuid);
    }

    mcstats.playerIdsByName.sort(function(a,b) {
        return mcstats.players[a].name.localeCompare(
            mcstats.players[b].name);
    });
}, true); // compressed!

// Start
mcstats.showLoader();

loader.start();
