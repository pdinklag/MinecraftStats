// Number formatter
intlFormat = new Intl.NumberFormat('en');

formatFloat = function(value) {
    return (value != parseInt(value)) ? value.toFixed(1) : value;
};

formatTime = function(unixTime) {
    var date = new Date();
    date.setTime(unixTime * 1000);

    return date.toLocaleDateString('en-US', {day: 'numeric', month: 'short', year: 'numeric'}) +
        ' - ' +
        date.toLocaleTimeString('en-US', {hour: '2-digit', minute: '2-digit', hour12: false});

};

// Format an award value
mcstats.formatValue = function(value, unit) {
    switch(unit) {
        case 'cm':
            if(value >= 100000) {
                value /= 100000;
                unit = 'km';
            } else if(value >= 100) {
                value /= 100;
                unit = 'm';
            }

            value = formatFloat(value) + unit;
            break;

        case 'ticks':
            seconds = value / 20; // ticks per second
            value = '';
            var higher = false;

            if(seconds > 86400) {
                value += Math.floor(seconds / 86400) + 'd ';
                seconds %= 86400;
                higher = true;
            }

            if(higher || seconds > 3600) {
                value += Math.floor(seconds / 3600) + 'h ';
                seconds %= 3600;
                higher = true;
            }

            if(higher || seconds > 60) {
                value += Math.floor(seconds / 60) + 'min ';
                seconds %= 60;
            }

            value += Math.floor(seconds) + 's';
            break;

        case 'int':
            value = intlFormat.format(parseInt(value));
            break;

        default:
            value = '' + value + ' ' + unit;
            break;
    }

    return `<span class="text-data">${value}</span>`;
};

// Create a rank widget
mcstats.rankWidget = function(rank) {
    if(rank) {
        var widget = `<span class="rank rank-${rank}">#${rank}</span>`;
        var medal, medalTitle;
        switch(rank) {
            case 1:
                // gold
                medal = 'gold';
                medalTitle = 'Gold Medal';
                break;

            case 2:
                // silver
                medal = 'silver';
                medalTitle = 'Silver Medal';
                break;

            case 3:
                // bronze
                medal = 'bronze';
                medalTitle = 'Bronze Medal';
                break;

            default:
                medal = false;
        }

        if(medal) {
            widget = `
                <img class="img-textsize-1_5 mr-1 align-top" title="${medalTitle}" src="img/fatcow/medal_award_${medal}.png"/>
            ` + widget;
        }
    } else {
        widget = `<span class="rank">-</span>`;
    }
    return widget;
};

// Create a widget showing a player's last online time and activity
mcstats.lastOnlineWidget = function(last) {
    var fmt = formatTime(last);

    var daysSinceLast = (mcstats.info.updateTime - last) / 86400;
    if(daysSinceLast <= mcstats.info.inactiveDays) {
        return `<span class="text-success">${fmt}</span>`;
    } else {
        return `
            <span class="text-danger">${fmt}</span>
        `;
    }
};

// Create an award widget
mcstats.awardWidget = function(id) {
    var award = mcstats.awards[id];
    return `
        <img class="img-pixelated img-textsize mr-1 align-baseline" src="img/award-icons/${id}.png" alt="${id}" title="${award.title}"/>
        <a href="#award:${id}">${award.title}</a>
    `;
}

// Create a player widget
mcstats.playerWidget = function(uuid) {
    if(uuid) {
        var p = mcstats.players[uuid];
        return `
            <!-- TODO: face -->
            <a href="#player:${uuid}">${p.name}</a>

        `;
    } else {
        return `<span class="text-muted">(nobody)</span>`;
    }
};
