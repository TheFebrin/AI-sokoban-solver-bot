// ==UserScript==
// @author       Dawid dieu
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Script to download the map
// @match        https://www.sokobanonline.com/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    window.get_canvas = function get_canvas(){
        const result = document.querySelectorAll("canvas")
        const dataUrl = result[0].toDataURL('image/png').replace("image/png", "image/octet-stream");
        window.location.href = dataUrl;
    }
})();
