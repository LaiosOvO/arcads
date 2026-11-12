
(function () {
  var COOKIE = 'arcads_web_ab';
  var EXCLUDED = 'off';
  var last = null, current = {}, shown = {}, ampReady = false;

  /* Rolled here rather than by Amplitude: the plan allows one web experiment and
     meta-paid-funnel is using it. `rollout` is the share entering the test at
     all; the rest are held out and recorded nowhere. */
  var TESTS = {};

  /* Tests that have ended. Their arm is dropped from the cookie, so a visitor
     assigned while one ran stops carrying it into the app. */
  var RETIRED = ['agent-landing'];

  function held() {
    var out = {};
    var parts = document.cookie ? document.cookie.split('; ') : [];
    var raw = null;
    for (var i = 0; i < parts.length; i++) {
      if (parts[i].indexOf(COOKIE + '=') === 0) {
        raw = parts[i].slice(COOKIE.length + 1);
      }
    }
    if (!raw) {
      return out;
    }
    try {
      raw = decodeURIComponent(raw);
    } catch (e) {
      return out;
    }
    raw.split('|').forEach(function (entry) {
      var sep = entry.indexOf(':');
      if (sep > 0 && RETIRED.indexOf(entry.slice(0, sep)) === -1) {
        out[entry.slice(0, sep)] = entry.slice(sep + 1);
      }
    });
    return out;
  }

  /* null is "not yet": nothing is stored, and a later page may roll. */
  function roll(key) {
    var cfg = TESTS[key];
    if (cfg.excluded && cfg.excluded()) {
      return EXCLUDED;
    }
    if (cfg.rollsOn && !cfg.rollsOn()) {
      return null;
    }
    if (Math.random() >= cfg.rollout) {
      return EXCLUDED;
    }
    return cfg.arms[Math.floor(Math.random() * cfg.arms.length)];
  }

  function forced() {
    var params = new URLSearchParams(window.location.search);
    var out = {};
    if (params.get('PREVIEW') !== 'true') {
      return out;
    }
    for (var key in TESTS) {
      var arm = params.get(key);
      if (arm) {
        out[key] = arm;
      }
    }
    return out;
  }

  function amplitudeArms() {
    var we = window.webExperiment;
    if (!we) {
      return {};
    }
    var out = {};
    var client = we.experimentClient;
    if (client && client.all) {
      var all = client.all();
      for (var key in all) {
        var variant = all[key];
        if (variant && variant.key && variant.key !== EXCLUDED) {
          out[key] = variant.key;
          ampReady = true;
        }
      }
    }
    if (we.isPreviewMode && we.previewFlags) {
      for (var previewed in we.previewFlags) {
        out[previewed] = we.previewFlags[previewed];
        ampReady = true;
      }
    }
    return out;
  }

  /* The stored arms are the base, holdouts included: re-rolling an excluded
     visitor on each page view would walk them into the test, and dropping an
     Amplitude arm the tag has not re-read yet would lose it from the cookie. */
  function assignments() {
    var out = held();
    for (var key in TESTS) {
      if (TESTS[key].rollout > 0 && !out[key]) {
        var rolled = roll(key);
        if (rolled) {
          out[key] = rolled;
        }
      }
    }
    var remote = amplitudeArms();
    for (var assigned in remote) {
      out[assigned] = remote[assigned];
    }
    var preview = forced();
    for (var previewed in preview) {
      out[previewed] = preview[previewed];
    }
    return out;
  }

  function serialise(out) {
    return Object.keys(out)
      .sort()
      .map(function (key) {
        return key + ':' + out[key];
      })
      .join('|');
  }

  /* Same bundle as the experiment tag, so these carry the device id the rest of
     the funnel is recorded against and join to it without extra identity. */
  function track(name, key) {
    if (!name || !window.amplitude || !window.amplitude.track) {
      return;
    }
    window.amplitude.track(name, { variant: current[key], src: 'landing' });
  }

  /* The whole budget an event may spend on its way off the page. */
  var EXIT_BUDGET_MS = 1500;

  /* The tag in the head is a stub: it queues whatever is called on it and
     fetches the SDK over two further scripts, and the SDK then holds the
     events it is handed until init has added the plugin that uploads them.
     Each stage passes the next one's promise back, so the promise `track`
     returns settles when the event has reached the uploader — which a device
     id does not say, since init mints one long before it gets that far. The
     queue keeps its order, so the transport and the flush travel with it.
     `done` runs on the first of that promise and the budget. */
  function trackOnExit(name, key, done) {
    var settled = false;
    function finish() {
      if (!settled) {
        settled = true;
        done();
      }
    }
    setTimeout(finish, EXIT_BUDGET_MS);
    var amp = window.amplitude;
    if (!name || !amp || !amp.track) {
      finish();
      return;
    }
    try {
      amp.setTransport('beacon');
      var tracked = amp.track(name, { variant: current[key], src: 'landing' });
      amp.flush();
      if (tracked && tracked.promise && tracked.promise.then) {
        tracked.promise.then(finish, finish);
      } else {
        finish();
      }
    } catch (e) {
      finish();
    }
  }

  /* Whether this click takes the page with it. A link opening a new tab, or one
     opened with a modifier, leaves this page standing, so its event goes out on
     the transport the page already uses. `setTransport` is a setting on the
     client with no getter to restore from, so reaching for the exit path here
     would put every later event on the page, autocapture included, on a
     transport that is never retried and answers nothing. */
  function takesThePage(event, node) {
    var link = node.closest('a[href]');
    if (!link || (link.target && link.target !== '_self')) {
      return false;
    }
    return !(event.metaKey || event.ctrlKey || event.shiftKey || event.altKey);
  }

  var REDIRECTING = 'arcads-ab-redirecting';
  var redirecting = false;

  (function () {
    var style = document.createElement('style');
    style.textContent = 'html.' + REDIRECTING + ' body { visibility: hidden; }';
    document.head.appendChild(style);
  })();

  /* Both arms log their exposure here, on the page they were split on, so a
     visitor lost during the hop still counts in the arm that sent them. The
     page stays hidden while the event goes out, never longer than the budget. */
  function leaveFor(key, target) {
    redirecting = true;
    document.documentElement.classList.add(REDIRECTING);
    var cfg = TESTS[key];
    var url = new URL(target);
    new URLSearchParams(window.location.search).forEach(function (value, name) {
      if (!url.searchParams.has(name)) {
        url.searchParams.set(name, value);
      }
    });
    if (cfg.armParam) {
      url.searchParams.set(cfg.armParam, 'test');
    }
    trackOnExit(cfg.shown, key, function () {
      window.location.replace(url.toString());
    });
  }

  function apply(out) {
    for (var key in TESTS) {
      var cfg = TESTS[key];
      var arm = out[key];
      if (!arm || arm === EXCLUDED) {
        continue;
      }
      var className = (cfg.classes || {})[arm];
      if (className) {
        document.documentElement.classList.add(className);
      }
      current[key] = arm;
      var onItsPage = !cfg.rollsOn || cfg.rollsOn();
      /* A visit the test holds out is not in the test, whichever arm the
         visitor was given on an earlier one: it neither leaves the page nor
         counts. Held out on the way in AND on the way out, because the arm
         outlives the visit that set it — someone rolled into the test on an
         organic visit is still in it when they come back on a Meta ad, and
         counting that visit as a treatment exposure would credit the arm with
         someone who stayed here and read the marketing page. */
      var heldOut = Boolean(cfg.excluded && cfg.excluded());
      var target = (cfg.redirect || {})[arm];
      if (target && onItsPage && !heldOut) {
        if (!redirecting) {
          shown[key] = true;
          leaveFor(key, target);
        }
        continue;
      }
      if (!shown[key] && onItsPage && !heldOut) {
        shown[key] = true;
        track(cfg.shown, key);
      }
    }
  }

  function write() {
    var out = assignments();
    apply(out);
    var value = serialise(out);
    if (value === last) {
      return;
    }
    document.cookie =
      COOKIE + '=' + encodeURIComponent(value) +
      '; domain=.arcads.ai; path=/; max-age=' + (value ? 2592000 : 0) +
      '; SameSite=Lax; Secure';
    last = value;
  }

  var tries = 0;
  var timer = setInterval(function () {
    write();
    if (ampReady || ++tries > 100) {
      clearInterval(timer);
    }
  }, 50);

  window.addEventListener('pagehide', write);
  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'hidden') {
      write();
    }
  });

  document.addEventListener(
    'click',
    function (event) {
      var target = event.target;
      if (!target || !target.closest) {
        return;
      }
      var leaving = takesThePage(event, target);
      for (var key in TESTS) {
        var cfg = TESTS[key];
        if (current[key] && cfg.selector && target.closest(cfg.selector)) {
          if (leaving) {
            trackOnExit(cfg.clicked, key, function () {});
          } else {
            track(cfg.clicked, key);
          }
        }
      }
    },
    true,
  );

  write();
})();
