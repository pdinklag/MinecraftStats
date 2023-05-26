// Load a JSON file from an URL
loadJson = function(url, successFunc, compressed = false, allowCache = false) {
    // load zlib-compressed JSON as byte sequence, then decompress
    var req = new XMLHttpRequest();
    req.open('GET', url, true);

    if(!allowCache) {
        req.setRequestHeader("Cache-Control", "no-cache, no-store, must-revalidate");
    }

    if(compressed) {
        req.responseType = 'arraybuffer';
    }

    req.onload = function(e) {
        var data;
        if(compressed) {
            // decompress JSON
            var compressedData = new Uint8Array(req.response);
            data = JSON.parse(pako.inflate(compressedData, {to: 'string'}));
        } else {
            data = JSON.parse(req.response);
        }

        // call success handler
        successFunc(data);
    };
    req.send();
};

class Loader {
    constructor(completeFunc) {
        this.oncomplete = completeFunc;
        this.requests = [];
        this.numLoaded = 0;
    }

    addRequest(url, successFunc, compressed = false) {
        this.requests.push({
            url: url,
            successFunc: successFunc,
            compressed: compressed,
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
            }, req.compressed);
        });
    }
}
