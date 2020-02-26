function anchorScroll(fragment) {
    "use strict";
    let amount, ttarget;
    amount = $('#nav-header').height();
    ttarget = $('#' + fragment);
    if (ttarget.offset()) {
        //$('html,body').animate({ scrollTop: ttarget.offset().top - amount }, 250);
        //$(ttarget).animate({ scrollTop: ttarget.offset().top - amount }, 250);
        $('html,body').scrollTop(ttarget.offset().top - amount);
    }
    return false;
}

function scrollToWindowHash() {
    "use strict";
    let fragment;
    if (window.location.hash) {
        fragment = window.location.hash.substring(1);
        anchorScroll(fragment);
    }
}

$(window)
    .on("load", scrollToWindowHash)
    .on('hashchange', scrollToWindowHash);
