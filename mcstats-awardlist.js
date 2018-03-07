mcstats.showAwardsList = function() {
    mcstats.viewContent.empty();

    var numPerRow = 3;
    var counter = 0;
    var currentRow = '';

    mcstats.awardKeysByTitle.forEach(function(id) {
        var award = mcstats.awards[id];
        var holder, info;

        if(award.best) {
            holder = mcstats.playerWidget(award.best.uuid);
            info = award.desc + ': ' + mcstats.formatValue(award.best.value, award.unit);
        } else {
            holder = mcstats.playerWidget(false);
            info = `<span class="disabled">(${award.desc})</span>`;
        }

        currentRow += `
            <div class="col-sm">
                <div class="container p-1 mb-3 mcstats-entry">
                    <div class="p-1 mb-1 round-box text-center">
                        <img class="pixelated sz-1_5 vt" src="img/award-icons/${id}.png" alt="${id}" title="${award.title}"/>
                        <span class="h4 ml-1">
                            <a href="#award:${id}">${award.title}</a>
                        </span>
                    </div>
                    <div class="p-1 round-box text-center">
                        ${holder}
                        <br/>
                        ${info}
                    </div>
                </div>
            </div>
        `;

        if(++counter >= numPerRow) {
            mcstats.viewContent.append(`<div class="row">${currentRow}</div>`);
            currentRow = '';
            counter = 0;
        }
    });

    if(counter > 0) {
        for(var i = counter; i < numPerRow; i++) {
            currentRow += `<div class="col-sm"></div>`;
        }
        mcstats.viewContent.append(`<div class="row">${currentRow}</div>`);
    }

    // show
    mcstats.showView('Award Overview', false, false, false);
};
