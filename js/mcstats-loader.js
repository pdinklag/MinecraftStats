// Load a JSON file from an URL
loadJson = function(url, successFunc, compressed = false) {
    if(compressed) {
        // load zlib-compressed JSON as byte sequence, then decompress
        var req = new XMLHttpRequest();
        req.open('GET', url, true);
        req.responseType = 'arraybuffer';
        req.onload = function(e) {
            // decompress JSON
            var compressedData = new Uint8Array(req.response);
            data = JSON.parse(pako.inflate(compressedData, {to: 'string'}));

            // call success handler
            successFunc(data);
        };
        req.send();
    } else {
        // simple AJAX request
        $.ajax({url: url, success: successFunc});
    }
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
