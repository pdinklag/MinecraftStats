mcstats.showPlayer = function(uuid) {
    load('data/playerdata/' + uuid + '.json', function(stats) {
        var player = mcstats.players[uuid];

        mcstats.viewContent.empty();

        // list statistics
        mcstats.awardKeysByTitle.forEach(function(id) {
            var award = mcstats.awards[id];
            var stat = stats[id];
            if(stat) {
                var value = mcstats.formatValue(stat.value, award.unit);
                var rank;
                if(stat.rank) {
                    rank = `<span class="rank rank-${stat.rank}">#${stat.rank}</span>`;
                    var medal, medalTitle;
                    switch(stat.rank) {
                        case 1:
                            // gold
                            medal = 'gold';
                            medalTitle = 'Gold Medal';
                            break;

                        case 2:
                            // silver
                            medal = 'silver';
                            medalTitle = 'Silver Medal';
                            break;

                        case 3:
                            // bronze
                            medal = 'bronze';
                            medalTitle = 'Bronze Medal';
                            break;

                        default:
                            medal = false;
                    }

                    if(medal) {
                        rank = `
                            <img class="sz-1_5" title="${medalTitle}" src="img/fatcow/medal_award_${medal}.png"/>&nbsp;
                        ` + rank;
                    }
                } else {
                    rank = `<span class="rank">-</span>`;
                }

                mcstats.viewContent.append(`
                    <div class="row p-1 mb-1 mcstats-entry">
                        <div class="col-sm mr-1 p-1 round-box">
                            <div class="d-flex">
                                <div>
                                <img class="pixelated sz-1_5 vb mr-1" src="img/award-icons/${id}.png" alt="${id}" title="${award.title}"/>
                                <a class="h6" href="#award:${id}">${award.title}</a>
                                </div>
                                <div class="ml-auto">
                                ${rank}
                                </div>
                            </div>
                        </div>
                        <div class="col-sm mr-1 py-1 pl-2 round-box">
                            ${award.desc}: ${value}
                        </div>
                    </div>
                `);
            }
        });

        // show
        mcstats.showView(
            player.name,
            'Player Statistics',
            'Last played: ' + mcstats.lastOnlineWidget(player.last),
            false);
    });
};
