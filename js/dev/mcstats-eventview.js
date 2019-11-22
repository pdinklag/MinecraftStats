mcstats.showEvent = function(id) {
    loadJson('data/events/' + id + '.json', function(eventData) {
        console.log(eventData);

        var e = mcstats.events[id];
        var awardId = e.link;
        var award = mcstats.awards[awardId];
        var tbody = '';
        var rank = 1;
        eventData.ranking.forEach(function(entry) {
            var rankWidget = mcstats.rankWidget(rank++);
            var playerWidget = mcstats.playerWidget(entry.uuid);
            var value = mcstats.formatValue(entry.value, award.unit);

            tbody += `
                <tr>
                    <td class="text-right">${rankWidget}</th>
                    <td>${playerWidget}</td>
                    <td class="text-data text-right">${value}</td>
                </tr>
            `;
        });

        mcstats.viewContent.innerHTML = `
            <div class="mcstats-entry p-1">
            <div class="round-box p-1">
                <table class="table table-responsive-xs table-hover table-sm">
                <thead>
                    <th scope="col" class="text-right text-shadow">Rank</th>
                    <th scope="col" class="text-shadow">Player</th>
                    <th scope="col" class="text-right text-shadow">${award.desc}</th>
                </thead>
                <tbody>${tbody}</tbody>
                </table>
            </div>
            </div>
        `;

        // show
        mcstats.showView(
            e.title,
            'Event Ranking',
            false,
            'img/award-icons/' + awardId + '.png');
    });
};
