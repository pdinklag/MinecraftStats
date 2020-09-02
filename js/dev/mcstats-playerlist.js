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
        var numPagesAroundCurrent = 3; // yep, this is hardcoded

        var numPages = Math.ceil((inactive ? numPlayers : numActive) / numPerPage);

        list.forEach(function(player) {
            var widget = mcstats.playerWidget(player.uuid);
            var lastOnlineColumn = mcstats.info.showLastOnline ? `<td class="text-right">${mcstats.lastOnlineWidget(player.last)}</td>` : '';

            tbody += `
                <tr>
                    <td>${widget}</td>
                    ${lastOnlineColumn}
                </tr>
            `;
        });

        var paginator = '';
        
        var generatePageLink = function(i, caption = null, enabled = true) {
            if(caption === null) caption = i.toString();
            if(enabled) {
                return `
                    <li class="page-item">
                        <a class="page-link" href="#${viewName}:${i}">${caption}</a>
                    </li>`; 
            } else {
                return `
                <li class="page-item disabled">
                    <div class="page-link">${caption}</div>
                </li>`;
            }
        };
        
        var generatePageActive = function() {
            return `
                <li class="page-item active">
                    <div class="page-link">${page}</div>
                </li>`;
        };
        
        var generatePageDots = function() {
            return `<li class="page-dots">...</li>`;
        };

        // previous page button
        paginator += generatePageLink(page-1, '&lt', page > 1);

        // first page
        if(page > 1) {
            paginator += generatePageLink(1);
        }

        // pages between first and neighbourhood
        if(page - 2 > numPagesAroundCurrent) {
            paginator += generatePageDots();
        }
        
        // left neighbourhood
        for(var i = Math.max(2, page - numPagesAroundCurrent); i < page; i++) {
            paginator += generatePageLink(i);
        }
        
        // current
        paginator += generatePageActive();
        
        // right neighbourhood
        for(var i = page + 1; i <= Math.min(page + numPagesAroundCurrent, numPages - 1); i++) {
            paginator += generatePageLink(i);
        }
        
        // pages between neighbourhood and last
        if(numPages - page - 1 > numPagesAroundCurrent) {
            paginator += generatePageDots();
        }
        
        // last page
        if(page < numPages) {
            paginator += generatePageLink(numPages);
        }
        
        /*
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
        */

        // next page button
        paginator += generatePageLink(page+1, '&gt', page < numPages);

        // build
        var lastOnlineHeader = mcstats.info.showLastOnline ? `<th scope="col" class="text-right text-shadow">Last online</th>` : '';
        
        mcstats.viewContent.innerHTML = `
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
                    ${lastOnlineHeader}
                </thead>
                <tbody>${tbody}</tbody>
                </table>
            </div>
            </div>
            <div class="mt-2 text-muted text-center text-shadow">
                Players need to have played at least ${mcstats.info.minPlayTime} minutes
                in order to appear in the statistics.<br/>
                Players who have not been online for over ${mcstats.info.inactiveDays} days
                are considered inactive and are not eligible for any awards.
            </div>
            <div class="text-center mt-3">
                <ul class="pagination justify-content-center">${paginator}</ul>
            </div>
        `;

        // click event for checkbox
        document.getElementById('show-inactive').onclick = function() {
            window.location.hash = (inactive ? '#players' : '#allplayers');
        };

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
            `,
            false);
    }, true);
}
