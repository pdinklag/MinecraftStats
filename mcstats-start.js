var loader = new Loader(function() {
    // navigate when loading is complete
    window.onhashchange();
});

loader.addRequest('data/awards.json', function(result) {
    mcstats.awards = result;

    // sort award keys by award title
    for(var key in mcstats.awards) {
        mcstats.awardKeys.push(key);
    }

    mcstats.awardKeys.sort(function(a,b) {
        return mcstats.awards[a].title.localeCompare(
            mcstats.awards[b].title);
    });
});

loader.addRequest('data/players.json', function(result) {
    mcstats.players = result;
});

loader.addRequest('data/info.json', function(result) {
    mcstats.info = result;

    $('#info #server-name').text(result.serverName);
    $('#info #update-time').text(formatTime(result.updateTime));

    if(result.hasIcon) {
        $('#info #server-icon').attr('src', 'data/server-icon.png');
    } else {
        $('#info #server-icon').hide();
    }
});

// Start
mcstats.hideAll();
mcstats.init();
mcstats.showLoader();

loader.start();
