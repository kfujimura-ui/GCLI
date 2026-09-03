/* Consent controls for optional Google Analytics on GCLI public pages. */
(function () {
  var KEY = 'gcli_cookie_preferences_v1';
  var choice = read();
  function read() { try { return JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { return null; } }
  function save(analytics) {
    choice = { analytics: !!analytics, updatedAt: new Date().toISOString(), version: 1 };
    try { localStorage.setItem(KEY, JSON.stringify(choice)); } catch (e) {}
    window.dispatchEvent(new CustomEvent('gcli:cookie-consent', { detail: choice }));
  }
  function close() { var banner = document.getElementById('gcli-cookie-banner'); if (banner) banner.remove(); }
  function show() {
    close();
    var banner = document.createElement('section');
    banner.id = 'gcli-cookie-banner'; banner.setAttribute('role', 'dialog'); banner.setAttribute('aria-label', 'Cookie choices');
    banner.innerHTML = '<style>#gcli-cookie-banner{position:fixed;z-index:9999;right:18px;bottom:18px;width:min(460px,calc(100% - 36px));padding:22px;border:1px solid #31505a;background:#103f4a;color:#fff;box-shadow:0 14px 42px rgba(16,63,74,.28);font:15px/1.55 Figtree,Arial,sans-serif}#gcli-cookie-banner h2{margin:0 0 8px;font-size:20px}#gcli-cookie-banner p{margin:0 0 15px;color:#dfe8e7}#gcli-cookie-banner a{color:#fff;text-decoration:underline}#gcli-cookie-actions{display:flex;flex-wrap:wrap;gap:9px}#gcli-cookie-actions button{min-height:40px;padding:8px 13px;border:1px solid #fff;background:transparent;color:#fff;font:inherit;font-weight:750;cursor:pointer}#gcli-cookie-actions button:first-child{background:#d6614f;border-color:#d6614f}#gcli-cookie-actions button:hover,#gcli-cookie-actions button:focus-visible{outline:2px solid #fff;outline-offset:2px}</style><h2>Your privacy choices</h2><p>GCLI uses essential storage to remember this choice. With your permission, we use Google Analytics to understand how the public site is used. You can change your choice at any time.</p><p><a href="/privacy/">Read Privacy &amp; Cookies</a></p><div id="gcli-cookie-actions"><button type="button" data-choice="accept">Accept analytics</button><button type="button" data-choice="reject">Reject analytics</button></div>';
    document.body.appendChild(banner);
    banner.addEventListener('click', function (event) { var button = event.target.closest('button[data-choice]'); if (button) { save(button.dataset.choice === 'accept'); close(); } });
  }
  window.GcliCookieConsent = { analyticsAllowed: function () { return !!(choice && choice.analytics); }, open: show };
  document.addEventListener('click', function (event) { var trigger = event.target.closest('[data-gcli-cookie-settings]'); if (trigger) { event.preventDefault(); show(); } });
  if (!choice) show();
}());
