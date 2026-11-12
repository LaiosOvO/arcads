
/* Meta ads land on this site, the app is a different origin, and these params
   are the only thing that tells app.arcads.ai which ad paid for the visit. */
(function () {
  var CARRY = /^(utm_|ref$|fbclid$|fbc_id$|h_ad_id$|gclid$|gbraid$|wbraid$|msclkid$|ttclid$|twclid$|li_fat_id$|rdt_cid$|ko_click_id$|lj_click_id$)/;
  var STORE = 'arcads_attribution';

  /* Kept for the whole visit rather than read off each link's page: the ad drops
     someone on the home page and they read three more before clicking Start, and
     none of those internal links carry the query either. Session-scoped, so a
     Meta click today cannot be credited with an organic visit next week. */
  function attribution() {
    var landed = new URLSearchParams(window.location.search);
    var carry = new URLSearchParams();
    landed.forEach(function (value, key) {
      if (CARRY.test(key) && value) {
        carry.append(key, value);
      }
    });
    var carried = carry.toString();

    try {
      // First touch wins, matching the `initial_*` attribution everything
      // downstream reports on.
      var stored = sessionStorage.getItem(STORE);
      if (stored) {
        return stored;
      }
      if (carried) {
        sessionStorage.setItem(STORE, carried);
      }
    } catch (e) {
      /* Private mode, or storage full — the landing URL still works. */
    }
    return carried;
  }

  var carried = attribution();
  if (!carried) {
    return;
  }

  /* Every arcads.ai host except this one. sessionStorage does not cross origins,
     so each hop out of this site needs the params on the link — app.arcads.ai and
     get.arcads.ai both. Same-host links need nothing: storage covers them. */
  var ARCADS_HOST = /(^|\.)arcads\.ai$/;

  function leavesThisSite(hostname) {
    return hostname !== window.location.hostname && ARCADS_HOST.test(hostname);
  }

  function decorate(link) {
    var href = link.getAttribute('href');
    if (!href) {
      return;
    }

    var url;
    try {
      url = new URL(href, window.location.href);
    } catch (e) {
      return;
    }
    if (!leavesThisSite(url.hostname)) {
      return;
    }

    // The link's own query wins: a CTA that names its own `ref` is saying where
    // in the page it sits, which the ad does not know.
    new URLSearchParams(carried).forEach(function (value, key) {
      if (!url.searchParams.has(key)) {
        url.searchParams.append(key, value);
      }
    });
    link.setAttribute('href', url.toString());
  }

  /* Delegated, and rewritten at click time: Webflow builds part of the page after
     load, and the browser reads href after the listeners have run. */
  document.addEventListener(
    'click',
    function (event) {
      var target = event.target;
      var link = target && target.closest ? target.closest('a[href]') : null;
      if (link) {
        decorate(link);
      }
    },
    true,
  );
})();
