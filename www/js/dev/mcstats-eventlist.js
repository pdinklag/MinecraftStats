mcstats.showEventList = function () {
  var viewHTML = "";

  var generateList = function (keysByDate) {
    var tbody = "";
    var promises = keysByDate.map(function (id) {
      return new Promise(function (resolve) {
        loadJson("data/events/" + id + ".json", function (eventData) {
          var e = mcstats.events[id];
          var award = mcstats.awards[e.link];

          var eventWidget = mcstats.eventWidget(id);

          if (e.active) {
            eventWidget += `<span class="text-success ms-2">[${mcstats.localize("page.eventList.live")}]</span>`;
          }

          if (eventData.ranking.length > 0) {
            var holder = mcstats.playerWidget(eventData.ranking[0].uuid);
            var info = `<span class="text-muted">(${award.desc})</span>`;
          } else {
            var holder = mcstats.playerWidget(false);
            var info = `<span class="text-muted">${award.desc})</span>`;
          }

          var eventTime;
          if (e.active) {
            eventTime = `${mcstats.localize("page.eventList.ongoingSince")} ${formatDate(e.startTime)}! <br /> ${mcstats.localize("page.eventList.endsAt")} ${formatDate(e.stopTime)}.`;
          } else {
            eventTime = `${formatDate(e.startTime)} - ${formatDate(e.stopTime)}`;
          }

          var eventStartTime = formatTime(e.startTime);
          var live = e.active
            ? `<span class="ps-2 text-success">[${mcstats.localize("page.eventList.live")}]</span>`
            : `<span class="ps-2 text-danger">[${mcstats.localize("page.eventList.finished")}]</span>`;

          tbody = `
              <div class="row">
              <div class="col-sm">
                  <div class="container p-1 mb-3 mcstats-entry">
                    <div class="p-1 mb-1 round-box text-center align-middle">
                      <div class="h4">
                        <img class="img-pixelated img-textsize align-baseline" src="img/award-icons/${e.link}.png" alt="${id}" title="${e.title}"/>
                          <a href="#event:${id}">${e.title}</a>
                          ${live}
                        </div>
                        <div class="text-muted">
                            ${eventTime}
                        </div>
                      </div>
                      <div class="p-1 round-box text-center">
                          <span class="rank-1">${mcstats.localize(e.active? "page.eventList.leading": "page.eventList.winner")}:</span>
                          ${holder}
                          <br/>
                          ${info}
                      </div>
                  </div>
              </div>
              </div>
          `;
          resolve(tbody);
        });
      });
    });

    return Promise.all(promises).then(function (html) {
      return html.join("");
    });
  };

  mcstats.viewContent.innerHTML = "";

  // ongoing events
  if (mcstats.liveEventKeysByDate.length > 0) {
    generateList(mcstats.liveEventKeysByDate).then(function (ongoingEvents) {
      mcstats.viewContent.innerHTML += `
          <div class="text-center mb-2">
              <div class="h5 text-shadow">${mcstats.localize("page.eventList.ongoingEvents")}</div>
          </div>
              ${ongoingEvents}
      `;
    });
  }

  // finished events
  if (mcstats.finishedEventKeysByDate.length > 0) {
    generateList(mcstats.finishedEventKeysByDate).then(function (finishedEvents) {
      mcstats.viewContent.innerHTML += `
          <div class="text-center mb-2 mt-4">
              <div class="h5 text-shadow">${mcstats.localize("page.eventList.finishedEvents")}</div>
          </div>
              ${finishedEvents}
          `;
    });
  }

  mcstats.showView(mcstats.localize("page.eventList.title"), false, false, false);
};
