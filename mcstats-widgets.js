// Number formatter
intlFormat = new Intl.NumberFormat('en');

formatFloat = function(value) {
    return (value != parseInt(value)) ? value.toFixed(1) : value;
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

    return `<span class="award-value">${value}</span>`;
};

// Create a player widget
mcstats.playerWidget = function(uuid) {
    if(uuid) {
        var p = mcstats.players[uuid];
        return `
            <!-- face -->
            <a href="#player:${uuid}">
                <span class="player-name">${p.name}</span>
            </a>
        `;
    } else {
        return `<span class="disabled">(nobody)</span>`;
    }
};
