mcstats.showPlayer = function(uuid) {
    load('playerdata/' + uuid + '.json', function(data) {
        $('h1', mcstats.playerView).text(mcstats.players[uuid].name);
        var content = $('.content', mcstats.playerView);
        content.empty();

        mcstats.awardKeys.forEach(function(key) {
            var award = mcstats.awards[key];
            var stat = data.stats[key];
            if(stat) {
                content.append(`<div>${award.title}: ${stat.value}</div>`);
            }
        });

        mcstats.hideLoader();
        mcstats.playerView.show();
    });
};
