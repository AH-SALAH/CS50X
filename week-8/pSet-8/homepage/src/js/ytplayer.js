/**
 * @author AH.SALAH
 * @email https://github.com/AH-SALAH
 * @create date 2021-06-02 04:48:02
 * @modify date 2021-06-02 05:38:17
 * @desc [ytplayer]
 */

// scope ytplayer module
const Ytplayer = function ({ elementID = 'player', videoUrl = "", playerVars = {}, onReady = () => { }, onPause = () => { }, onStateChange = () => { } }) {
    this.videoUrl = videoUrl;
    this.playerVars = playerVars;
    this.onPause = onPause;
    this.onReady = onReady;
    this.onStateChange = onStateChange;
    this.elementID = elementID;
};
// 2. This code loads the IFrame Player API code asynchronously.
let tag = document.createElement('script');

tag.src = "//www.youtube.com/player_api";
tag.id = "ytapi";
let firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
// document.body.append(tag);

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
let playerDefaults = {
    autoplay: 1,
    autohide: 1,
    modestbranding: 0,
    rel: 0,
    showinfo: 0,
    controls: 0,
    disablekb: 1,
    enablejsapi: 0,
    iv_load_policy: 3,
    // origin: window?.location.protocol + '//' + window?.location.host
};

let player;
Ytplayer.prototype.onYouTubeIframeAPIReady = function () {
    player = new YT.Player(this.elementID, {
        height: '100%',
        // height: '390',
        width: '100%',
        // width: '640',
        videoId: this.videoUrl?.split('v=')[1] || 'd2O16mYojm0',
        suggestedQuality: "large",
        playerVars: {
            ...playerDefaults,
            ...this.playerVars
        },
        events: {
            'onReady': this.onPlayerReady.bind(this),
            'onStateChange': this.onPlayerStateChange.bind(this)
        }
    });
}

let currentPlayer = player;
// 4. The API will call this function when the video player is ready.
Ytplayer.prototype.onPlayerReady = function (event) {
    event.target.playVideo();
    this.onReady(event.target);
    currentPlayer = event.target;
}

// 5. The API calls this function when the player's state changes.
//    The function indicates that when playing a video (state=1),
//    the player should play for six seconds and then stop.
// let done = false;
Ytplayer.prototype.onPlayerStateChange = function (event) {
    let playerStatus = event.data;
    this.onStateChange(playerStatus, currentPlayer);
};

// Ytplayer.prototype.stopVideo = () => {
//     player.stopVideo();
// };