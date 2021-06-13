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
            var lastOnlineColumn = mcstats.info.showLastOnline ? `<td class="text-end">${mcstats.lastOnlineWidget(player.last)}</td>` : '';

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
        
        // next page button
        paginator += generatePageLink(page+1, '&gt', page < numPages);

        // build
        var lastOnlineHeader = mcstats.info.showLastOnline ? `<th scope="col" class="text-end text-shadow">${mcstats.localize('page.playerList.lastOnline')}</th>` : '';
        
        mcstats.viewContent.innerHTML = `
            <div class="text-center mt-3">
                <input id="show-inactive" type="checkbox" ${inactive ? 'checked' : ''}/>
                <label for="show-inactive">${mcstats.localize('page.playerList.showInactive')}</label>
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
                ${mcstats.localize('page.playerList.activityInfo', [mcstats.info.minPlayTime, mcstats.info.inactiveDays])}
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
            mcstats.localize('page.playerList.title'),
            mcstats.localize('page.playerList.count', [numPlayers, numActive, numInactive]),
            mcstats.localize('page.playerList.paginationInfo', [numPerPage]) + '<br/>',
            false);
    }, true);
}
