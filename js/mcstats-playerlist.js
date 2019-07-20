mcstats.showPlayerList = function(page=1,inactive=false) {
    loadJson('data/playerlist/' + (inactive ? 'all' : 'active') + page + '.json.gz', function(list) {
        // add players to cache
        list.forEach(function(p){
            mcstats.players[p.uuid] = {
                'name': p.name,
                'skin': p.skin,
                'last': p.last
            }
        });

        // build page
        var tbody = '';

        var viewName = inactive ? 'allplayers' : 'players';

        var numPlayers = mcstats.info.numPlayers;
        var numActive = mcstats.info.numActive;
        var numInactive = numPlayers - numActive;
        var numPerPage = mcstats.info.playersPerPage;

        var numPages = Math.ceil((inactive ? numPlayers : numActive) / numPerPage);

        list.forEach(function(player) {
            var widget = mcstats.playerWidget(player.uuid);
            var last = mcstats.lastOnlineWidget(player.last);

            tbody += `
                <tr>
                    <td>${widget}</td>
                    <td class="text-right">${last}</td>
                </tr>
            `;
        });

        var paginator = '';

        if(page > 1) {
            paginator += `
                <li class="page-item">
                    <a class="page-link" href="#${viewName}:${page-1}">&lt;</a>
                </li>`;
        } else {
            paginator += `
                <li class="page-item disabled">
                    <div class="page-link">&lt;</div>
                </li>`;
        }

        for(var i = 1; i <= numPages; i++) {
            if(page == i) {
                paginator += `
                    <li class="page-item active">
                        <div class="page-link">${i}</div>
                    </li>`;
            } else {
                paginator += `
                    <li class="page-item">
                        <a class="page-link" href="#${viewName}:${i}">${i}</a>
                    </li>`;
            }
        }

        if(page < numPages) {
            paginator += `
                <li class="page-item">
                    <a class="page-link" href="#${viewName}:${page+1}">&gt;</a>
                </li>`;
        } else {
            paginator += `
                <li class="page-item disabled">
                    <div class="page-link">&gt;</div>
                </li>`;
        }

        mcstats.viewContent.html(`
            <div class="text-center mt-3">
                <input id="show-inactive" type="checkbox" ${inactive ? 'checked' : ''}/>
                <label for="show-inactive">Show inactive players</label>
            </div>
            <div class="text-center mt-3">
                <ul class="pagination justify-content-center">${paginator}</ul>
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
            <div class="text-center mt-3">
                <ul class="pagination justify-content-center">${paginator}</ul>
            </div>
        `);

        // hide inactive by default
        //$('.inactive').hide();

        // click event for checkbox
        $('#show-inactive').click(function() {
            window.location.hash = (inactive ? '#players' : '#allplayers');
        });

        // show
        mcstats.showView(
            'Player List',
            `
                    <span class="text-data">${numPlayers}</span>
                    players total
                    ( <span class="text-success">${numActive}</span> active,
                    <span class="text-danger">${numInactive}</span> inactive).
            `,
            `
                Showing ${numPerPage} players per page.<br/>
                Players who have not been online for over ${mcstats.info.inactiveDays} days
                are considered inactive and are not eligible for any awards.
            `,
            false);
    }, true);
}
