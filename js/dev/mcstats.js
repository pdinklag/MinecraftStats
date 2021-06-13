// Initialize
var mcstats = {
    loader: document.getElementById('loader'),

    infoBox: document.getElementById('info'),
    content: document.getElementById('content'),

    viewTitle: document.getElementById('view-title'),
    viewSubtitle: document.getElementById('view-subtitle'),
    viewDesc: document.getElementById('view-desc'),
    viewIcon: document.getElementById('view-icon'),
    viewContent: document.getElementById('view-content'),

    localization: {},
    info: {},
    awards: {},
    events: {},
    awardKeysByTitle: new Array(),
    liveEventKeysByDate: new Array(),
    finishedEventKeysByDate: new Array(),
    players: {},
};

// Initialize client
mcstats.init = function() {
    mcstats.infoBox.style.display = 'block';
    mcstats.content.style.display = 'block';
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
        }, false, true);
    }
}

// Show loader and nothing else
mcstats.showLoader = function() {
    mcstats.content.style.display = 'none';
    mcstats.loader.style.display = '';
}

// Show view - content shall be prepared before calling this
mcstats.showView = function(title, subtitle, desc, iconUrl) {
    mcstats.viewTitle.innerHTML = title;

    if(subtitle) {
        mcstats.viewSubtitle.innerHTML = subtitle;
        mcstats.viewSubtitle.style.display = '';
    } else {
        mcstats.viewSubtitle.style.display = 'none';
    }

    if(desc) {
        mcstats.viewDesc.innerHTML = desc;
        mcstats.viewDesc.style.display = '';
    } else {
        mcstats.viewDesc.style.display = 'none';
    }

    if(iconUrl) {
        mcstats.viewIcon.setAttribute('src', iconUrl);
        mcstats.viewIcon.style.display = '';
    } else {
        mcstats.viewIcon.style.display = 'none';
    }

    mcstats.localizePage();
    mcstats.loader.style.display = 'none';
    mcstats.content.style.display = 'block';
}

// Collapse navbar when an item is clicked
var navbarElement = document.getElementById('navbar-content');
var navbar = new bootstrap.Collapse(navbarElement, {toggle: false});

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
    } else if(hash.startsWith('#players')) {
        // go to player list, showing only active
        var page = 1;
        var x = hash.indexOf(':');
        if(x >= 0) {
            page = parseInt(hash.substring(x+1));
        }
        mcstats.showPlayerList(page, false);
    } else if(hash.startsWith('#allplayers')) {
        // go to player list, showing only active
        var page = 1;
        var x = hash.indexOf(':');
        if(x >= 0) {
            page = parseInt(hash.substring(x+1));
        }
        mcstats.showPlayerList(page, true);
    } else if(hash == '#hof') {
        // go to hall of fame
        mcstats.showHof();
    } else if(hash == '#events') {
        // go to event list
        mcstats.showEventList();
    } else if(hash.startsWith('#event:')) {
        // open event view
        var id = hash.substr(7);
        mcstats.showEvent(id);
    } else if(hash == '#loader') {
        // stick with loader - for debugging purposes
    } else {
        // go to awards list (default)
        mcstats.showAwardsList();
    }
    
    // collapse navbar
    navbar.hide();
};
