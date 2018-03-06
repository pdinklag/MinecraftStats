mcstats.showAwardsList = function() {
    if(!mcstats.awardsListLoaded) {
        var numPerRow = 2;
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
                    <div class="container award mb-3">
                        <div class="row">
                            <div class="p-2 m-1 icon">
                                <img class="award-icon" src="img/award-icons/${id}.png" alt="${id}" title="${award.title}"/>
                            </div>
                            <div class="col pt-2 pl-2 mt-1 mr-1 title">
                                <h4 class="m-0">
                                    <a href="#award:${id}">${award.title}</a>
                                </h4>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col py-2 mx-1 mb-1 text-center holder">
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
