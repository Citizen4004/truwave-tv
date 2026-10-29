// 4K Dream — minimal progressive-enhancement JS (no framework, no build step)

document.addEventListener('DOMContentLoaded', function () {
  // Mobile nav toggle
  var toggle = document.querySelector('.menu-toggle');
  var links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var isOpen = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
    links.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { links.classList.remove('open'); });
    });
  }

  // FAQ accordion (content stays in the DOM/HTML at all times — nothing hidden from crawlers,
  // only the open/closed visual state is toggled)
  document.querySelectorAll('.faq-item').forEach(function (item) {
    var btn = item.querySelector('.faq-q');
    btn.addEventListener('click', function () {
      var wasOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(function (openItem) {
        if (openItem !== item) openItem.classList.remove('open');
      });
      item.classList.toggle('open', !wasOpen);
      btn.setAttribute('aria-expanded', !wasOpen ? 'true' : 'false');
    });
  });

  // Multi-device pricing selector
  var devicePricing = {
    '1':  { 1: 16.99, 2: 29.99,  3: 40.99,  4: 49.99,  5: 58.99  },
    '3':  { 1: 34.99, 2: 61.99,  3: 84.99,  4: 104.99, 5: 122.99 },
    '6':  { 1: 54.99, 2: 96.99,  3: 131.99, 4: 162.99, 5: 189.99 },
    '12': { 1: 79.99, 2: 139.99, 3: 191.99, 4: 235.99, 5: 275.99 }
  };

  document.querySelectorAll('.price-card[data-plan]').forEach(function (card) {
    var plan = card.getAttribute('data-plan');
    var planLabel = card.getAttribute('data-plan-label');
    var priceEl = card.querySelector('.price-amount');
    var cta = card.querySelector('.whatsapp-cta');
    var pills = card.querySelectorAll('.device-pill');

    pills.forEach(function (pill) {
      pill.addEventListener('click', function () {
        var devices = pill.getAttribute('data-devices');
        var price = devicePricing[plan][devices];

        pills.forEach(function (p) { p.classList.remove('active'); });
        pill.classList.add('active');

        if (priceEl) priceEl.textContent = price.toFixed(2);

        if (cta) {
          var deviceWord = devices === '1' ? 'device' : 'devices';
          var message = "Hi! I'd like to get started with the TruWave TV " + planLabel +
            ' plan (' + devices + ' ' + deviceWord + ', $' + price.toFixed(2) +
            "). Can you help me set it up?";
          cta.href = 'https://wa.me/12057092376?text=' + encodeURIComponent(message);
        }
      });
    });
  });
});
