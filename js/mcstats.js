// Initialize
var mcstats = {
    loader: $('#loader'),

    infoBox: $('#info'),
    content: $('#content'),
    footer: $('#footer'),

    view: $('#view'),
    viewTitle: $('#view-title'),
    viewSubtitle: $('#view-subtitle'),
    viewDesc: $('#view-desc'),
    viewIcon: $('#view-icon'),
    viewContent: $('#view-content'),

    info: {},
    awards: {},
    awardKeysByTitle: new Array(),
    players: {},
};

// Initialize client
mcstats.init = function() {
    mcstats.infoBox.css('display', 'block');
    mcstats.content.css('display', 'block');
}

// Make sure a certain player is cached
mcstats.cachePlayer = function(uuid, successFunc) {
    if(uuid in mcstats.players) {
        // already cached, call success right away
        successFunc();
    } else {
        // load from server
        var key = uuid.substring(0, mcstats.info.cacheQ);
        loadJson('data/playercache/' + key + '.json', function(cache) {
            cache.forEach(function(entry) {
                mcstats.players[entry['uuid']] = {
                    'name': entry['name'],
                    'skin': entry['skin'],
                    'last': entry['last']
                };
            });

            // cached now, call success func
            successFunc();
        });
    }
}

// Show loader and nothing else
mcstats.showLoader = function() {
    mcstats.content.hide();
    mcstats.loader.show();
}

// Show view - content shall be prepared before calling this
mcstats.showView = function(title, subtitle, desc, iconUrl) {
    mcstats.viewTitle.html(title);

    if(subtitle) {
        mcstats.viewSubtitle.html(subtitle);
        mcstats.viewSubtitle.show();
    } else {
        mcstats.viewSubtitle.hide();
    }

    if(desc) {
        mcstats.viewDesc.html(desc);
        mcstats.viewDesc.show();
    } else {
        mcstats.viewDesc.hide();
    }

    if(iconUrl) {
        mcstats.viewIcon.attr('src', iconUrl);
        mcstats.viewIcon.show();
    } else {
        mcstats.viewIcon.hide();
    }

    mcstats.loader.hide();
    mcstats.content.show();
}

// Collapse navbar when an item is clicked
$('.nav-link').on('click', function() {
    $('.collapse').collapse('hide');
});

// Register navigation event handler
window.onhashchange = function() {
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
    } else if(hash == '#players') {
        // go to player list
        mcstats.showPlayerList();
    } else if(hash == '#hof') {
        // go to hall of fame
        mcstats.showHof();
    } else if(hash == '#loader') {
        // stick with loader - for debugging purposes
    } else {
        // go to awards list (default)
        mcstats.showAwardsList();
    }
};


