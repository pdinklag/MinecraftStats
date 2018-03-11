mcstats.showPlayerList = function() {
    var tbody = '';
    mcstats.playerIdsByName.forEach(function(uuid) {
        var player = mcstats.players[uuid];

        var rowClass = mcstats.isActive(player.last) ? '' : 'inactive';
        var widget = mcstats.playerWidget(uuid);
        var last = mcstats.lastOnlineWidget(player.last);

        tbody += `
            <tr class="${rowClass}">
                <td>${widget}</td>
                <td class="text-right">${last}</td>
            </tr>
        `;
    });

    mcstats.viewContent.html(`
        <div class="text-center mt-3">
            <input id="show-inactive" type="checkbox"/>
            <label for="show-inactive">Show inactive players</label>
        </div>
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

    // hide inactive by default
    $('.inactive').hide();

    // click event for checkbox
    $('#show-inactive').click(function() {
        $('.inactive').toggle(this.checked);
    });

    // show
    mcstats.showView(
        'Player List',
        false,
        `
            Players who have not been online for over ${mcstats.info.inactiveDays} days
            are considered inactive and are not eligible for any awards.
        `,
        false);
}
