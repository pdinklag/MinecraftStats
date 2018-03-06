mcstats.showAward = function(id) {
    load('rankings/' + id + '.json', function(ranking) {
        var content = $('.content', mcstats.awardView);
        content.empty();

        var award = mcstats.awards[id];
        $('.h1', mcstats.awardView).text(award.title);
        $('img', mcstats.awardView).attr('src', 'img/award-icons/' + id + '.png');

        content.append(`
            <div class="mb-2 text-center award-desc">
                ${award.desc}
            </div>
        `
        );

        var rank = 1;
        ranking.forEach(function(entry) {
            playerWidget = mcstats.playerWidget(entry.uuid);
            value = mcstats.formatValue(entry.value, award.unit);

            content.append(`
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

        mcstats.hideLoader();
        mcstats.awardView.show();
    });
};
