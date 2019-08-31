mcstats.showHof = function() {
    var tbody = '';

    var rank = 1;
    mcstats.hof.forEach(function(entry) {
        var rankWidget = mcstats.rankWidget(rank++, 'crown');
        var playerWidget = mcstats.playerWidget(entry.uuid);
        var value = entry.value;

        tbody += `
            <tr>
                <td class="text-right">${rankWidget}</th>
                <td>${playerWidget}</td>
                <td class="text-data text-center">${value[1]}</td>
                <td class="text-data text-center">${value[2]}</td>
                <td class="text-data text-center">${value[3]}</td>
                <td class="text-data text-right">${value[0]}</td>
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
                <th scope="col" class="text-center"><img class="img-textsize-2" title="Gold Medals" src="img/fatcow/medal_award_gold.png"/></th>
                <th scope="col" class="text-center"><img class="img-textsize-2" title="Silver Medals" src="img/fatcow/medal_award_silver.png"/></th>
                <th scope="col" class="text-center"><img class="img-textsize-2" title="Bronze Medals" src="img/fatcow/medal_award_bronze.png"/></th>
                <th scope="col" class="text-right text-shadow">Score</th>
            </thead>
            <tbody>${tbody}</tbody>
            </table>
        </div>
        </div>
    `;

    var crown = mcstats.info.crown;
    var formatCrown = function(x) {
        return wordSmallInt(x) + ' point' + ((x > 1) ? 's' : '');
    };

    // show
    mcstats.showView(
        'Hall of Fame',
        'Crown Score Ranking',
        `
            The crown score is calculated by the amount of medals a player
            holds.<br/>
            A gold medal is worth <span class="rank-1">${formatCrown(crown[0])}</span>,
            a silver medal is worth <span class="rank-2">${formatCrown(crown[1])}</span> and
            a bronze medal is worth <span class="rank-3">${formatCrown(crown[2])}</span>.
        `,
        false);
}
