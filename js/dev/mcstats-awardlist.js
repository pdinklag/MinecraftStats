mcstats.showAwardsList = function() {
    viewHTML = '';

    var numPerRow = 3;
    var counter = 0;
    var currentRow = '';

    mcstats.awardKeysByTitle.forEach(function(id) {
        var award = mcstats.awards[id];
        var holder, info;

        if(award.best) {
            holder = mcstats.playerWidget(award.best.uuid);
            info = award.desc + ': ' + mcstats.formatValue(award.best.value, award.unit, true);
        } else {
            holder = mcstats.playerWidget(false);
            info = `<span class="text-muted">(${award.desc})</span>`;
        }

        currentRow += `
            <div class="col-sm">
                <div class="container p-1 mb-3 mcstats-entry">
                    <div class="h4 p-1 mb-1 round-box text-center">
                        <img class="img-pixelated img-textsize align-baseline" src="img/award-icons/${id}.png" alt="${id}" title="${award.title}"/>
                        <a href="#award:${id}">${award.title}</a>
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
            viewHTML += `<div class="row">${currentRow}</div>`;
            currentRow = '';
            counter = 0;
        }
    });

    if(counter > 0) {
        for(var i = counter; i < numPerRow; i++) {
            currentRow += `<div class="col-sm"></div>`;
        }
        viewHTML += `<div class="row">${currentRow}</div>`;
    }

    // show
    mcstats.viewContent.innerHTML = viewHTML;
    mcstats.showView(mcstats.localize('page.awardList.title'), false, false, false);
};
