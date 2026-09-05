mcstats.showAwardsList = function(view = 'cards') {
    var cards = (view != 'table');

    // view switcher, styled like the pagination controls
    var switcherItem = function(caption, hash, active) {
        if(active) {
            return `<li class="page-item active"><div class="page-link">${caption}</div></li>`;
        } else {
            return `<li class="page-item"><a class="page-link" href="${hash}">${caption}</a></li>`;
        }
    };

    var switcher = `
        <div class="text-center mt-3">
            <ul class="pagination justify-content-center">
                ${switcherItem(mcstats.localize('page.awardList.viewCards'), '#awards:cards', cards)}
                ${switcherItem(mcstats.localize('page.awardList.viewTable'), '#awards:table', !cards)}
            </ul>
        </div>
    `;

    // show
    mcstats.viewContent.innerHTML = switcher + (cards ? mcstats.renderAwardCards() : mcstats.renderAwardTable());
    mcstats.showView(mcstats.localize('page.awardList.title'), false, false, false);
};
