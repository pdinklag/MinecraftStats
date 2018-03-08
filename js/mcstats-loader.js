// Loader
load = function(filename, success_func) {
    $.ajax({url: filename, success: success_func});
};

class Loader {
    constructor(complete_func) {
        this.oncomplete = complete_func;
        this.requests = [];
        this.numLoaded = 0;
    }

    addRequest(filename, success_func) {
        this.requests.push({filename: filename, success_func: success_func});
    }

    start() {
        var loader = this;
        this.requests.forEach(function(req) {
            $.ajax({url: req.filename, success: function(result) {
                req.success_func(result);

                ++loader.numLoaded;
                if(loader.numLoaded >= loader.requests.length) {
                    loader.oncomplete();
                }
            }});
        });
    }
}
