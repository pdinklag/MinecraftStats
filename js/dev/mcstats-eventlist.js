mcstats.showEventList = function() {
    var viewHTML = '';

    var generateList = function(keysByDate){
        var tbody = '';
        keysByDate.forEach(function(id){
            var e = mcstats.events[id];
            var award = mcstats.awards[e.link];

            var eventWidget = mcstats.eventWidget(id);
            if(e.active) {
                eventWidget += `<span class="text-success ms-2">[${mcstats.localize('page.eventList.live')}]</span>`;
            }

            var holder, info;
            if(e.best) {
                holder = mcstats.playerWidget(e.best.uuid);
                info = award.desc + ': ' + mcstats.formatValue(e.best.value, award.unit, true);
            } else {
                holder = mcstats.playerWidget(false);
                info = `<span class="text-muted">(${award.desc})</span>`;
            }

            var eventTime;
            if(e.active) {
                eventTime = `Going since ${formatDate(e.startTime)}`;
            } else {
                eventTime = `${formatDate(e.startTime)} - ${formatDate(e.stopTime)}`;
            }

            var eventStartTime = formatTime(e.startTime);
            var live = e.active
                ? `<span class="ps-2 text-success">[${mcstats.localize('page.eventList.live')}]</span>`
                : `<span class="ps-2 text-danger">[${mcstats.localize('page.eventList.finished')}]</span>`;

            tbody += `
                <div class="row">
                <div class="col-sm">
                    <div class="container p-1 mb-3 mcstats-entry">
                        <div class="p-1 mb-1 round-box text-center">
                            <div class="h4">
                                <img class="img-pixelated img-textsize align-baseline" src="img/award-icons/${e.link}.png" alt="${id}" title="${e.title}"/>
                                <a href="#event:${id}">${e.title}</a>
                                ${live}
                            </div>
                            <div class="text-muted">
                                ${eventTime}
                            </div>
                        </div>
                        <div class="p-1 round-box text-center">
                            <span class="rank-1">${e.active ? "${mcstats.localize('page.eventList.leading')}:" : "${mcstats.localize('page.eventList.winner')}:"}</span>
                            ${holder}
                            <br/>
                            ${info}
                        </div>
                    </div>
                </div>
                </div>
            `;
        });
        return tbody;
    };

    mcstats.viewContent.innerHTML = '';

    // ongoing events
    if(mcstats.liveEventKeysByDate.length > 0) {
        mcstats.viewContent.innerHTML += `
            <div class="text-center mb-2">
                <div class="h5 text-shadow">${mcstats.localize('page.eventList.ongoingEvents')}</div>
            </div>
            ${generateList(mcstats.liveEventKeysByDate)}
        `;
    }
    
    // finished events
    if(mcstats.finishedEventKeysByDate.length > 0) {
        mcstats.viewContent.innerHTML += `
            <div class="text-center mb-2 mt-4">
                <div class="h5 text-shadow">${mcstats.localize('page.eventList.finishedEvents')}</div>
            </div>
            ${generateList(mcstats.finishedEventKeysByDate)}
        `;
    }
    
    mcstats.showView(mcstats.localize('page.eventList.title'), false, false, false);
};
