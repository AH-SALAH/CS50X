/**
 * @author AH.SALAH
 * @email https://github.com/AH-SALAH
 * @create date 2021-06-02 04:47:38
 * @modify date 2021-06-02 05:34:37
 * @desc [App.js]
 */

// scope App module
const App = function () { };

// initialize vars
App.prototype.initVars = function () {
    this.footerDateEl = $('footer .footer-date');
    this.mainEl = $('.main-container');
    this.videoHeaderEl = $('.main-container #player');
    this.videoHeaderElVideoUrl = this.videoHeaderEl?.data("video");
    this.videoCtls = this.mainEl?.find(".controls");
    this.videoCtlsPlPa = this.videoCtls?.find(".play-pause");
    this.videoCtlsRe = this.videoCtls?.find(".repeat");
    this.headerIntroTxt = this.mainEl?.find(".header-intro-text");
    this.loaded = false;
    this.mouseCoords = {};
    this.navbarNav = $('.navbar-nav');
    this.mainOverlay = this.mainEl.find('.overlay, .circle-clip');
    this.circleClip = $('.circle-clip');
    this.circleClipLeft = this.circleClip.css('left');
    this.circleClipTop = this.circleClip.css('top');
    this.headerMapImg = this.headerIntroTxt.find(' > foreignObject img');
};

// chk device
App.prototype.device = () => window.innerWidth < 600 ? "mobile" : "desktop";

// handle init & play of the bg video
App.prototype.playYt = function () {
    // get the player element but not from cache because its already changed dynamically to iframe
    this.videoHeaderEl = $('.main-container #player');

    // this.headerIntroTxt.addClass("slideinLeft-anime")
    // .on('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend',
    // function () {
    //     $(this).removeClass("slideinLeft-anime");
    // });

    // this.headerIntroTxt.css("left", 0);

    // if its mobile or the custom yt object not fount, return to default & don't init the YTPLayer module
    if (this.device() == "mobile" || !Ytplayer) {
        this.videoHeaderEl?.replaceWith('<div id="player"></div>');
        // hide video controlers 
        this.videoCtls.css("right", "-100%");
        // show header txt
        this.headerIntroTxt.css("left", 0);

        // $('#ytapi, #www-widgetapi-script')?.remove();
        this.loaded = true;
        return;
    }

    // set in global scope as it's called/seeked globaly from yt api loaded script
    onYouTubeIframeAPIReady = () => {
        let yt = new Ytplayer({
            videoUrl: this.videoHeaderElVideoUrl,
            onReady: this.onVideoPlayerReady.bind(this),
            onStateChange: this.onStateChange.bind(this)
        });
        yt.onYouTubeIframeAPIReady();
        // set loaded to true as the first time to load flag
        this.loaded = true;
        return;
    };
    // if its loaded before reinit
    if (this.loaded) onYouTubeIframeAPIReady();
};

// handle video on ready
App.prototype.onVideoPlayerReady = function (evTrgt) {
    // some animation
    this.mainEl?.find('.overlay').addClass('fadeout-anime');
    this.mainEl?.find('.videoWrapper .circle-clip').addClass('scaledown-anime');
    // show video controlers 
    this.videoCtls.css("right", "2%");
    // hide header txt
    this.headerIntroTxt.css("left", -100 + '%');
};

// handle on video on state change
App.prototype.onStateChange = function (playerStatus, player) {
    if (playerStatus == 0) {
        this.mainEl?.find('.overlay').removeClass('fadeout-anime');
        this.headerIntroTxt.css("left", 0);
    }
    if (playerStatus == 2) {
        this.mainEl?.find('.overlay').addClass('fadeout-anime');
        // this.headerIntroTxt.css("left", -100 + '%');
    }
    this.handleVideoControllers(playerStatus, player);
};

App.prototype.handleVideoControllers = function (playerStatus, player) {
    let self = this;
    // remove disabled class if found
    this.videoCtlsPlPa.removeClass('disabled');

    this.videoCtlsPlPa.on('click', function () {
        let icon = $(this).find('>.icon');

        switch (playerStatus) {
            case 1: // paused
                player.pauseVideo();
                icon.attr({ 'title': 'Play' })
                    .html('&opar;')
                    .addClass('text-danger paused')
                    .removeClass('text-success playing');
                self.headerIntroTxt.css("left", 0);
                break;
            case 2: // playing
                player.playVideo();
                icon.attr({ 'title': 'Pause' })
                    .html('&ogt;')
                    .addClass('text-success playing')
                    .removeClass('text-danger paused');
                self.headerIntroTxt.css("left", -100 + '%');
                break;
            case 3: // buffering
                $(this).addClass('disabled');
                break;
            case 0: // ended
                player.playVideo();
                icon.attr({ 'title': 'Pause' })
                    .html('&ogt;')
                    .addClass('text-success playing')
                    .removeClass('text-danger paused');
                self.headerIntroTxt.css("left", 0);
                break;

            default:
                $(this).removeClass('disabled');
                break;
        }

        // update this tooltip title
        // [https://stackoverflow.com/questions/34540990/cant-change-bootstrap-tooltip-title/58479276]
        icon.tooltip('_fixTitle');
    });

    this.videoCtlsRe.on('click', function () {
        $(this).find('>.icon')
            .addClass("rotate-anime")
            .on('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend',
                function () {
                    $(this).removeClass("rotate-anime");
                });
        player.seekTo(0);
        player.playVideo();
        self.mainEl?.find('.overlay').addClass('fadeout-anime');
        self.headerIntroTxt.css("left", -100 + '%');
    });
};

// add current year to footer
App.prototype.addFooterDate = function () {
    this.footerDateEl?.text(new Date(Date.now()).getFullYear());
};

// handle on mouse circle clip el animation
App.prototype.onmouseCircleClipAnimation = function () {
    let trgt = this.circleClip,
        orgLeft = this.circleClipLeft,
        orgTop = this.circleClipTop;

    this.mainOverlay.on('mousemove', (ev) => {
        let x = this.mouseCoords?.x - (trgt.width() / 2);
        let y = this.mouseCoords?.y - (trgt.height() / 3.6);

        trgt.css({ left: x, top: y, opacity: 0.1 });
    });

    this.mainOverlay.on('mouseout', (ev) => {
        // return to default
        trgt.css({ left: orgLeft, top: orgTop, opacity: 0 });
    });

    // if ($(this.mouseCoords?.target).hasClass('overlay') || $(this.mouseCoords?.target).hasClass('circle-clip')) {
    //     let x = this.mouseCoords?.x - (trgt.width() / 2);
    //     let y = this.mouseCoords?.y - (trgt.height() / 3.5);
    //     // let translate = 'translate('+x+'px, '+y+'px)';
    //     // let translateY = 'translateY('+y+'px)';
    //     trgt.css({ left: x, top: y, opacity: 0.1 });
    //     // trgt.css({"transform": translate});
    // }
    // else {
    //     // return to default
    //     trgt.css({ left: orgLeft, top: orgTop, opacity: 0 });
    // }
};

// handle on mouse navbar ele animation
App.prototype.onmouseNavBarAnimation = function () {
    // let span = '<span class="anchor d-block" style="width: 50px;height: 35px;position: absolute;z-index: -1;transition: all 0.2s ease;border-top: 20px solid transparent;border-left: 60px solid crimson;border-bottom: 20px solid transparent;"></span>';
    let span = '<span class="anchor d-block" style="border-radius: 50%;background: crimson;width: 50px;height: 35px;position: absolute;z-index: -1;transition: all 0.2s cubic-bezier(0.93, -0.07, 0, 0.99) 0s;"></span>';
    let active = this.navbarNav.find('.nav-item .nav-link.active');

    // if anchor not exist, append it
    if (!this.navbarNav.find('.anchor').length) {
        this.navbarNav.append(span);
    }
    // set default status
    this.navbarNav.find('.anchor').css({
        left: active.offset().left,
        top: active.offset().top,
        width: 10,
        height: 10
    });

    this.navbarNav.on('mousemove', function (ev) {
        // if ($(ev.target).hasClass('nav-item') || $(ev.target).hasClass('nav-link')) {
        let x = $(ev.target).offset().left;
        let y = $(ev.target).offset().top;
        $(this).parent().find('.anchor').css({
            left: x + ($(ev.target).innerWidth() - $(ev.target).width()) / 2, // offset + (innerWidth - width) / 2 [to negate padding]
            top: y + $(ev.target).innerHeight(),
            width: $(ev.target).width(),
            // height: $(ev.target).innerHeight(),
            height: 5,
            borderRadius: 4,
            transitionDuration: 0.2 + 's'
        });
        // }
    });

    this.navbarNav.on('mouseout', function (ev) {
        $(this).find('.anchor').css({
            left: active.offset().left,
            top: active.offset().top,
            width: 10,
            height: 10,
            borderRadius: 50 + '%',
            transitionDuration: 0.8 + 's'
        });
    });
};

App.prototype.imgMagnify = function (img) {
    if (!img) return;
    let self = this;
    // prepare container
    // let style = 'background:#fff;border-radius: 6px;z-index:100;padding: 0.5em;width:' + $(img).innerWidth() * 2 + 'px;height:' + $(img).innerHeight() * 2 + 'px;position: absolute;top:' + Math.round($(img).offset().top + $(img).innerHeight() / 2) + 'px;left:' + Math.round($(img).offset().left + $(img).innerWidth()) + 'px;';
    let style = 'background:#fff;border-radius: 6px;z-index:100;padding: 0.5em;width:' + $(window).innerWidth() / (self.device() == "mobile" ? 2 : 4) + 'px;height:auto;position: absolute;top:' + Math.round($(window).innerHeight() / 2) + 'px;left:' + Math.round($(img).offset().left + $(img).innerWidth()) + 'px;overflow:hidden;';
    let virtCont = '<div class="magnifier" style="' + style + '"></div>';
    // create random unique id
    let id = Math.random() * Math.pow(10, ('' + Math.random()).length);
    // clone img & assign the id
    let clone = $(img).clone().attr('id', id);

    // handle on mousemove
    $(img).on('mousemove', function (ev) {
        // handle left & top move
        let left = self.device() == "mobile" ? $(window).innerWidth() / 4 : Math.round($(this).offset().left + ($(this).innerWidth() + ev.clientX / 4));
        let top = self.device() == "mobile" ? $(window).innerHeight() / 4 : Math.round(($(window).innerHeight() / 2) - ev.clientY);
        // let x = ev.clientX - $(this).offset().left;
        // let y = ev.clientY - $(this).offset().top;
        let magnifier = $('.magnifier');
        let cloneId = magnifier.find('#' + id);

        // if magnifier not exist yet in the dom, create it
        if (!magnifier.length) { $('body').append($(virtCont).css({ left, top })); }
        else {
            // handle some edge cases
            top = top <= 0 ? 0 :
                top + magnifier?.innerHeight() > $(window).innerHeight() ?
                    Math.round(top - ((top + magnifier?.innerHeight()) - $(window).innerHeight())) :
                    top;
            left = left + magnifier?.innerWidth() > $(window).innerWidth() ?
                Math.round($(this).offset().left - ($(this).innerWidth() + ev.clientX / 4)) :
                left;

            // if same id found just change magnif [left,top] else change magnif coords and append the new img
            if (cloneId.length) {
                magnifier.css({ left, top });
                // cloneId.css({ left: magnifier.offset().left - (x * 4) + ev.clientX, top: magnifier.offset().top - (y * 4) + ev.clientY, transform: 'scale(' + 2 + ')' });
            }
            else {
                magnifier
                    .css({ left, top })
                    .html(
                        $(clone).attr('style', null)
                            .css({ "width": "100%", "height": "100%", "position": "relative" })
                    )
                    .show();
            }
        }
    });
    // handle mouseleave, hide & empty the html content
    $(img).on('mouseleave', function () {
        $('.magnifier').hide();
        $('.magnifier').empty();
    });

};

// get mouse Coords
App.prototype.getMouseXY = function () {
    window.onmousemove = ev => {
        this.mouseCoords = { x: ev.clientX, y: ev.clientY, target: ev.target };
    };
};

// init bootstrap optionated js
App.prototype.initBs = function () {
    // init bs tooltip
    let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
};

// init App
App.prototype.init = function () {
    this.initVars();
    this.addFooterDate();
    this.initBs();
    this.getMouseXY();
    this.onmouseNavBarAnimation();

    if (location.pathname.includes("index.html")) {
        this.headerIntroTxt?.css("left", 0);
        this.playYt();
        this.onmouseCircleClipAnimation();
        this.imgMagnify(this.headerMapImg);
    }
};

// check for jq as dependancy if exist then init
(function () {
    if (typeof jQuery == 'undefined' || !window.jQuery || !$) {
        console.log("jquery is needed!");
        return;
    }
    // init App
    let app = new App();
    app.init();
    // on resize re-evaluate device [hide video on mobile, show on desktop]
    if (location.pathname.includes("index.html")) {
        window.onresize = () => {
            // simple debounce for window resize
            let tOut = setTimeout(() => {
                app.playYt();
                clearTimeout(tOut);
                return false;
            }, 500);
        };
    };
})();