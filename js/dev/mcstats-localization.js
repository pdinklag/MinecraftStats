mcstats.languages = [
    { 'code': 'de', 'display': 'Deutsch' },
    { 'code': 'en', 'display': 'English' },
    { 'code': 'es', 'display': 'Español' },
    { 'code': 'fr', 'display': 'Français' },
    { 'code': 'ja', 'display': '日本語'},
    { 'code': 'pl', 'display': 'Polski'},
    { 'code': 'ru', 'display': 'Русский' },
    { 'code': 'zh-hans', 'display': '简体中文' },
    { 'code': 'zh-hant', 'display': '繁體中文' }
];

mcstats.getLangURL = function(code) {
    return `?lang=${code}${window.location.hash}`;
}

mcstats.fillLangSelect = function() {
    langSelect = '';
    mcstats.languages.sort(function(a, b) {
        return a.display.localeCompare(b.display);
    });
    
    for(var i in mcstats.languages) {
        var lang = mcstats.languages[i];
        langSelect += `<li><a id="lang-${lang.code}" class="dropdown-item language" href="${mcstats.getLangURL(lang.code)}">${lang.display}</a></li>`;
    }
    
    document.getElementById('lang-select').innerHTML = langSelect;
}

mcstats.updateLangSelect = function() {
    for(var i in mcstats.languages) {
        var lang = mcstats.languages[i];
        var x = document.getElementById(`lang-${lang.code}`);
        x.setAttribute('href', mcstats.getLangURL(lang.code));
    }
}

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
