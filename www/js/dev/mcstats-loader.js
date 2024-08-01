// Load a JSON file from an URL
loadJson = function(url, successFunc, allowCache = false) {
    var req = new XMLHttpRequest();
    req.open('GET', url, true);

    if(!allowCache) {
        req.setRequestHeader("Cache-Control", "no-cache, no-store, must-revalidate");
    }

    req.onload = function(e) {
        successFunc(JSON.parse(req.response));
    };
    req.send();
};

class Loader {
    constructor(completeFunc) {
        this.oncomplete = completeFunc;
        this.requests = [];
        this.numLoaded = 0;
    }

    addRequest(url, successFunc) {
        this.requests.push({
            url: url,
            successFunc: successFunc,
        });
    }

    start() {
        var loader = this;
        this.requests.forEach(function(req) {
            loadJson(req.url, function(result) {
                req.successFunc(result);

                ++loader.numLoaded;
                if(loader.numLoaded >= loader.requests.length) {
                    loader.oncomplete();
                }
            });
        });
    }
}
