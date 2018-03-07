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

    return `<span class="award-value">${value}</span>`;
};

// Create a widget showing a player's last online time and activity
mcstats.lastOnlineWidget = function(last) {
    var fmt = formatTime(last);

    var daysSinceLast = (mcstats.info.updateTime - last) / 86400;
    if(daysSinceLast <= mcstats.info.inactiveDays) {
        return `<span class="online-date">${fmt}</span>`;
    } else {
        return `
            <span class="online-date inactive">${fmt}</span>
        `;
    }
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
        return `<span class="disabled">(nobody)</span>`;
    }
};
