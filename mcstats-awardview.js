mcstats.showAward = function(id) {
    load('data/rankings/' + id + '.json', function(ranking) {
        var award = mcstats.awards[id];

        mcstats.viewContent.empty();

        var rank = 1;
        ranking.forEach(function(entry) {
            playerWidget = mcstats.playerWidget(entry.uuid);
            value = mcstats.formatValue(entry.value, award.unit);

            mcstats.viewContent.append(`
                <div class="p-1 mb-1 mcstats-entry">
                    <div class="d-flex p-1 round-box">
                        <div>
                            <span class="rank rank-${rank} mr-2">#${rank}</span>
                            ${playerWidget}
                        </div>
                        <div class="ml-auto">
                            <span class="award-value">${value}</span>
                        </div>
                    </div>
                </div>
            `);
            rank++;
        });

        // show
        mcstats.showView(
            award.title,
            'Award Ranking',
            award.desc,
            'img/award-icons/' + id + '.png');
    });
};
