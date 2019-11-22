mcstats.showEventList = function() {
    var viewHTML = '';
    var tbody = '';

    mcstats.eventKeysByDate.forEach(function(id){
        var e = mcstats.events[id];
        var award = mcstats.awards[e.link];

        var eventWidget = mcstats.eventWidget(id);
        if(e.active) {
            eventWidget += `<span class="text-success ml-2">[LIVE]</span>`;
        }

        var eventWinner;

        if(e.best) {
            var holder = mcstats.playerWidget(e.best.uuid);
            var info = award.desc + ': ' + mcstats.formatValue(e.best.value, award.unit, true);
            eventWinner = holder + ' (' + info + ')';
        } else {
            var holder = mcstats.playerWidget(false);
            var info = `<span class="text-muted">(${award.desc})</span>`;
            eventWinner = holder + ' ' + info;
        }

        var eventTime = formatTime(e.startTime);

        tbody += `
            <tr>
                <td>${eventWidget}</td>
                <td>${eventTime}</td>
                <td>${eventWinner}</td>
            </tr>
        `;
    });

    // show
    mcstats.viewContent.innerHTML = `
        <div class="mcstats-entry p-1">
        <div class="round-box p-1">
            <table class="table table-responsive-xs table-hover table-sm">
            <thead>
                <th scope="col" class="text-shadow">Event</th>
                <th scope="col" class="text-shadow">Time</th>
                <th scope="col" class="text-shadow">Winner</th>
            </thead>
            <tbody>${tbody}</tbody>
            </table>
        </div>
        </div>
    `;
    mcstats.showView('Events', false, false, false);
};
