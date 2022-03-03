// parse params
params = {
    'lang': null // null will use the server's default language
};

if(window.location.search.startsWith('?')) {
    paramDefs = window.location.search.substr(1).split('&');
    for(var i in paramDefs) {
        kv = paramDefs[i].split('=', 2);
        if(kv.length == 2) {
            params[kv[0]] = kv[1];
        }
    }
}

mcstats.start = function() {
    // maybe use default localization
    if(params.lang == null) {
        console.log(summary);
        params.lang = mcstats.defaultLanguage;
    }
    
    // localize awards
    for(var key in mcstats.awards) {
        var award = mcstats.awards[key];
        award.title = mcstats.localizeDefault('award.' + key + '.title', key);
        award.desc = mcstats.localizeDefault('award.' + key + '.desc', key);
    }

    // fill server info
    serverName = JSON.parse('"' + mcstats.info.serverName + '"');
    serverNameNoFmt = mcstats.removeColorCodes(serverName).replace('<br>', ' / ');

    document.title = `${serverNameNoFmt} \u2013 Stats`;
    document.getElementById('navigation').style.display = '';
    document.getElementById('server-name').innerHTML = mcstats.formatColorCode(serverName);
    document.getElementById('update-time').textContent = formatTime(mcstats.info.updateTime);
    
    var serverIcon = document.getElementById('server-icon');
    if(!mcstats.info.hasIcon) {
        serverIcon.style.display = 'none';
    } else {
        serverIcon.setAttribute('title', serverNameNoFmt);
    }

    // sort award keys by award title
    for(var key in mcstats.awards) {
        mcstats.awardKeysByTitle.push(key);
    }

    mcstats.awardKeysByTitle.sort(function(a,b) {
        return mcstats.awards[a].title.localeCompare(
            mcstats.awards[b].title);
    });

    // sort event keys by start time
    var numEvents = 0;    
    for(var key in mcstats.events) {
        if(mcstats.events[key].active) {
            mcstats.liveEventKeysByDate.push(key);
        } else {
            mcstats.finishedEventKeysByDate.push(key);
        }
        ++numEvents;
    }

    if(numEvents > 0) {
        mcstats.liveEventKeysByDate.sort(function(a,b) {
            return mcstats.events[b].startTime - mcstats.events[a].startTime;
        });
        mcstats.finishedEventKeysByDate.sort(function(a,b) {
            return mcstats.events[b].startTime - mcstats.events[a].startTime;
        });
        document.getElementById('tab-events').style.display = '';
    }
    
    // open the curtain!
    mcstats.infoBox.style.display = 'block';
    mcstats.content.style.display = 'block';
    
    // navigate to current page
    window.onhashchange();
}

// create localization loader
var localizationLoader = new Loader(function() {
    mcstats.start(); // once localization is loaded: start!
});

// create summary loader
summaryLoader = new Loader(function() {
    // only after loading the summary we definitely know the language
    localizationLoader.addRequest('localization/' + params.lang + '.json', function(localization) {
        mcstats.localization = localization;
        
        document.getElementById('loading-text').innerHTML = mcstats.localize('loading');
        mcstats.fillLangSelect();
    });
    
    // once summary is completely loaded, load localization
    localizationLoader.start();
});

summaryLoader.addRequest('data/summary.json.gz', function(summary) {
    // store summary data
    mcstats.info = summary.info;
    mcstats.players = summary.players;
    mcstats.awards = summary.awards;
    mcstats.events = summary.events;
    mcstats.hof = summary.hof;
    
    if(params.lang == null) {
        params.lang = mcstats.info.defaultLanguage;
    }
    if(params.lang === undefined) {
        params.lang = "en";
    }
}, true); // compressed!

// Start
mcstats.showLoader();
summaryLoader.start();
