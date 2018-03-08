mcstats.showPlayerList = function() {
    var tbody = '';
    mcstats.playerIdsByName.forEach(function(uuid) {
        var player = mcstats.players[uuid];

        var widget = mcstats.playerWidget(uuid);
        var last = mcstats.lastOnlineWidget(player.last);

        tbody += `
            <tr>
                <td>${widget}</td>
                <td class="text-right">${last}</td>
            </tr>
        `;
    });

    mcstats.viewContent.html(`
        <div class="mcstats-entry p-1">
        <div class="round-box p-1">
            <table class="table table-responsive-xs table-hover table-sm">
            <thead>
                <th scope="col" class="text-shadow">Player</th>
                <th scope="col" class="text-right text-shadow">Last online</th>
            </thead>
            <tbody>${tbody}</tbody>
            </table>
        </div>
        </div>
    `);

    // show
    mcstats.showView(
        'Player List',
        false,
        `
            Players inactive for over ${mcstats.info.inactiveDays} days
            are considered inactive and are not eligible for any awards.
        `,
        false);
}
