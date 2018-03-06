// Loader synchronizer
mcstats.onLoaded = function() {
    ++mcstats.loaded;
    if(mcstats.loaded >= 2) {
        window.onhashchange();
    }
};

// Show loader
mcstats.hideAll();
mcstats.init();
mcstats.showLoader();

// Load awards
load('awards.json', function(result) {
    mcstats.awards = result;

    // sort award keys by award title
    for(var key in mcstats.awards) {
        mcstats.awardKeys.push(key);
    }

    mcstats.awardKeys.sort(function(a,b) {
        return mcstats.awards[a].title.localeCompare(
            mcstats.awards[b].title);
    });

    mcstats.onLoaded();
});

// Load players
load('players.json', function(result) {
    mcstats.players = result;
    mcstats.onLoaded();
});
