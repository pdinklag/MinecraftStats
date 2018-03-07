// Initialize
var mcstats = {
    loaded: 0,
    awardsListLoaded: false,

    content: $('#content'),

    loader: $('#loader'),
    info: $('#info'),
    footer: $('#footer'),
    awardsContainer: $('#awards'),
    awardView: $('#award-view'),
    playerView: $('#player-view'),

    awards: {},
    awardKeys: new Array(),
    players: {},
};

// Initialize contents
mcstats.init = function() {
    mcstats.content.css('display', 'block');
    mcstats.info.css('display', 'block');
}

// Hide all containers
mcstats.hideAll = function() {
    mcstats.awardsContainer.hide();

    mcstats.loader.hide();
    mcstats.awardView.hide();
    mcstats.playerView.hide();
};

// Show loader
mcstats.showLoader = function() {
    mcstats.footer.hide();
    mcstats.loader.show();
}

// Hide loader
mcstats.hideLoader = function() {
    mcstats.loader.hide();
    mcstats.footer.show();
}

// Register navigation event handler
window.onhashchange = function() {
    mcstats.hideAll();
    window.scrollTo(0, 0);
    mcstats.showLoader();

    var hash = window.location.hash;
    if(hash.startsWith('#award:')) {
        // open award view
        var id = hash.substr(7);
        mcstats.showAward(id);
    } else if(hash.startsWith('#player:')) {
        // open player view
        var uuid = hash.substr(8);
        mcstats.showPlayer(uuid);
    } else {
        // go to awards list
        mcstats.showAwardsList();
    }
};


