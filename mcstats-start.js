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

// Start
mcstats.hideAll();
mcstats.init();
mcstats.showLoader();

loader.start();
