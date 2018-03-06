mcstats.showAward = function(id) {
    load('rankings/' + id + '.json', function(ranking) {
        $('h1', mcstats.awardView).text(mcstats.awards[id].title);
        var content = $('.content', mcstats.awardView);
        content.empty();

        var rank = 1;
        ranking.forEach(function(entry) {
            pw = mcstats.playerWidget(entry.uuid);

            content.append(`<div>${rank}: ${pw}</div>`);
            rank++;
        });

        mcstats.hideLoader();
        mcstats.awardView.show();
    });
};
