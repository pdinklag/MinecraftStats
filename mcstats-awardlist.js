mcstats.showAwardsList = function() {
    if(!mcstats.awardsListLoaded) {
        var numPerRow = 3;
        var counter = 0;
        var currentRow = '';

        mcstats.awardKeys.forEach(function(id) {
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
                    <div class="container mb-3 mcstats-entry">
                        <div class="row">
                            <div class="col p-1 m-1 round-box text-center">
                                <img class="pixelated sz-1_5 vt" src="img/award-icons/${id}.png" alt="${id}" title="${award.title}"/>
                                <span class="h4 ml-1">
                                    <a href="#award:${id}">${award.title}</a>
                                </span>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col p-1 mx-1 mb-1 round-box text-center">
                                ${holder}
                                <br/>
                                ${info}
                            </div>
                        </div>
                    </div>
                </div>
            `;

            if(++counter >= numPerRow) {
                mcstats.awardsContainer.append(`<div class="row">${currentRow}</div>`);
                currentRow = '';
                counter = 0;
            }
        });

        if(counter > 0) {
            for(var i = counter; i < numPerRow; i++) {
                currentRow += `<div class="col-sm"></div>`;
            }
            mcstats.awardsContainer.append(`<div class="row">${currentRow}</div>`);
        }

        mcstats.awardsListLoaded = true;
    }

    mcstats.hideLoader();
    mcstats.awardsContainer.show();
};
