mcstats.localizeDefault = function(key, def) {
    if(key in mcstats.localization) {
        return mcstats.localization[key];
    } else {
        console.warn('unlocalized key: ' + key);
        return def;
    }
}

mcstats.localize = function(key, params) {
    if(key in mcstats.localization) {
        var s = mcstats.localization[key];
        if(Array.isArray(params)) {
            return s.replace(/{(\d+)}/g, function(m, i) { 
                return typeof params[i] != 'undefined' ? params[i] : m;
            });
        } else {
            return s;
        }
    } else {
        console.warn('unlocalized key: ' + key);
        return key;
    }
}

mcstats.localizePage = function() {
    var els = Array.from(document.getElementsByClassName('localize'));
    els.forEach(function(e) {
        e.innerHTML = mcstats.localize(e.innerHTML);
        e.classList.remove('localize');
    });
}
