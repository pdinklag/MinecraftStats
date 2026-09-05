// Award overview as a table, one row per award
mcstats.renderAwardTable = function() {
    var tbody = '';

    mcstats.awardKeysByTitle.forEach(function(id) {
        var award = mcstats.awards[id];
        var holder, value;

        if(award.best) {
            holder = mcstats.playerWidget(award.best.uuid);
            value = mcstats.formatValue(award.best.value, award.unit, true);
        } else {
            holder = mcstats.playerWidget(false);
            value = '';
        }

        tbody += `
            <tr>
                <td>
                    <img class="img-pixelated img-textsize-1_5 align-baseline me-1" src="img/award-icons/${id}.png" alt="${id}" title="${award.title}"/>
                    <a href="#award:${id}">${award.title}</a>
                    <br/>
                    <small class="text-muted">${award.desc}</small>
                </td>
                <td>${holder}</td>
                <td class="text-data text-end">${value}</td>
            </tr>
        `;
    });

    return `
        <div class="mcstats-entry p-1">
        <div class="round-box p-1">
            <table class="table table-responsive-xs table-hover table-sm">
            <thead>
                <th scope="col" class="text-shadow">${mcstats.localize('stat.award')}</th>
                <th scope="col" class="text-shadow">${mcstats.localize('stat.player')}</th>
                <th scope="col" class="text-end text-shadow">${mcstats.localize('page.awardList.value')}</th>
            </thead>
            <tbody>${tbody}</tbody>
            </table>
        </div>
        </div>
    `;
};
