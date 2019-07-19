var loader = new Loader(function() {
    mcstats.init();
    window.onhashchange(); // navigate
});

loader.addRequest('data/summary.json.gz', function(summary) {
    // load db
    mcstats.info = summary.info;
    mcstats.players = summary.players;
    mcstats.awards = summary.awards;
    mcstats.hof = summary.hof;

    // fill server info
    serverName = JSON.parse('"' + mcstats.info.serverName + '"');
    serverNameNoFmt = mcstats.removeColorCodes(serverName);

    $('title').html(`${serverNameNoFmt} &ndash; Stats`);
    $('#server-name').html(mcstats.formatColorCode(serverName));
    $('#update-time').text(formatTime(mcstats.info.updateTime));

    if(!mcstats.info.hasIcon) {
        $('#info #server-icon').hide();
    } else {
        $('#info #server-icon').attr('title', serverNameNoFmt);
    }

    // sort award keys by award title
    for(var key in mcstats.awards) {
        mcstats.awardKeysByTitle.push(key);
    }

    mcstats.awardKeysByTitle.sort(function(a,b) {
        return mcstats.awards[a].title.localeCompare(
            mcstats.awards[b].title);
    });
}, true); // compressed!

// Start
mcstats.showLoader();

loader.start();
