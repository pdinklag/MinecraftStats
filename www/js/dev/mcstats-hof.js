mcstats.showHof = function() {
    var tbody = '';

    var rank = 1;
    mcstats.hof.forEach(function(entry) {
        var rankWidget = mcstats.rankWidget(rank++, 'crown');
        var playerWidget = mcstats.playerWidget(entry.uuid);
        var value = entry.value;

        tbody += `
            <tr>
                <td class="text-end">${rankWidget}</th>
                <td>${playerWidget}</td>
                <td class="text-data text-center">${value[1]}</td>
                <td class="text-data text-center">${value[2]}</td>
                <td class="text-data text-center">${value[3]}</td>
                <td class="text-data text-end">${value[0]}</td>
            </tr>
        `;
    });

    mcstats.viewContent.innerHTML = `
        <div class="mcstats-entry p-1">
        <div class="round-box p-1">
            <table class="table table-responsive-xs table-hover table-sm">
            <thead>
                <th scope="col" class="text-end text-shadow">${mcstats.localize('stat.rank')}</th>
                <th scope="col" class="text-shadow">${mcstats.localize('stat.player')}</th>
                <th scope="col" class="text-center"><img class="img-textsize-2" title="${mcstats.localize('stat.unit.medals.gold')}" src="img/fatcow/medal_award_gold.png"/></th>
                <th scope="col" class="text-center"><img class="img-textsize-2" title="${mcstats.localize('stat.unit.medals.silver')}" src="img/fatcow/medal_award_silver.png"/></th>
                <th scope="col" class="text-center"><img class="img-textsize-2" title="${mcstats.localize('stat.unit.medals.bronze')}" src="img/fatcow/medal_award_bronze.png"/></th>
                <th scope="col" class="text-end text-shadow">${mcstats.localize('stat.score')}</th>
            </thead>
            <tbody>${tbody}</tbody>
            </table>
        </div>
        </div>
    `;

    var crown = mcstats.info.crown;
    var formatCrown = function(x) {
        return x + ' ' + mcstats.localize(x > 1 ? 'stat.unit.points' : 'stat.unit.point');
    };

    // show
    mcstats.showView(
        mcstats.localize('page.hof.title'),
        mcstats.localize('page.hof.subtitle'),
        mcstats.localize('page.hof.description', [formatCrown(crown[0]), formatCrown(crown[1]), formatCrown(crown[2])]),
        false);
}
