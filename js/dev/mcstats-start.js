var loader = new Loader(function() {
    mcstats.init();
    window.onhashchange(); // navigate
});

loader.addRequest('data/summary.json.gz', function(summary) {
    // load db
    mcstats.info = summary.info;
    mcstats.players = summary.players;
    mcstats.awards = summary.awards;
    mcstats.events = summary.events;
    mcstats.hof = summary.hof;

    // fill server info
    serverName = JSON.parse('"' + mcstats.info.serverName + '"');
    serverNameNoFmt = mcstats.removeColorCodes(serverName).replace('<br>', ' / ');

    document.title = `${serverNameNoFmt} \u2013 Stats`;
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
    for(var key in mcstats.events) {
        if(mcstats.events[key].active) {
            mcstats.liveEventKeysByDate.push(key);
        } else {
            mcstats.finishedEventKeysByDate.push(key);
        }
    }

    mcstats.liveEventKeysByDate.sort(function(a,b) {
        return mcstats.events[b].startTime - mcstats.events[a].startTime;
    });
    mcstats.finishedEventKeysByDate.sort(function(a,b) {
        return mcstats.events[b].startTime - mcstats.events[a].startTime;
    });

}, true); // compressed!

// Start
mcstats.showLoader();

loader.start();
