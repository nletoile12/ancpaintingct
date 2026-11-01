/* ANC Painting — quote form + mobile Text/Call/Quote bar */
(function () {
  'use strict';

  var PHONE = '+14016606025';

  // ── Mobile action bar (Text / Call / Quote) ─────────────────────────
  function addMobileBar() {
    if (document.querySelector('.mobile-bar')) return;
    var target = document.getElementById('quoteFormWrap') ? '#quoteFormWrap' : '/#quoteFormWrap';
    var bar = document.createElement('div');
    bar.className = 'mobile-bar';
    bar.innerHTML =
      '<a href="sms:' + PHONE + '" class="mobile-bar-btn">Text</a>' +
      '<a href="tel:' + PHONE + '" class="mobile-bar-btn">Call</a>' +
      '<a href="' + target + '" class="mobile-bar-btn mobile-bar-quote">Free Quote</a>';
    document.body.appendChild(bar);
    document.body.classList.add('has-mobile-bar');
  }
  if (document.body) addMobileBar();
  else document.addEventListener('DOMContentLoaded', addMobileBar);

  // ── Quote form ───────────────────────────────────────────────────
  var form = document.getElementById('quoteForm');
  if (!form) return;

  var nameInput    = document.getElementById('name');
  var phoneInput   = document.getElementById('phone');
  var emailInput   = document.getElementById('email');
  var consentInput = document.getElementById('consent');
  var submitBtn    = document.getElementById('submitQuote');
  var contactHint  = form.querySelector('.contact-hint');
  var formError    = document.getElementById('formError');
  var defaultHint  = contactHint ? contactHint.textContent : '';
  var submitted    = false;
  var submitLabel  = submitBtn ? submitBtn.textContent : '';

  // If someone taps Back after submitting, phones restore the old page with the
  // button still saying "Sending…". Reset it so they can use the form again.
  window.addEventListener('pageshow', function () {
    if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = submitLabel; }
    submitted = false;
  });

  function digits(v) { return (v || '').replace(/\D/g, ''); }
  function nameOk(v) { return (v || '').trim().length >= 2; }
  function phoneOk(v) {
    var d = digits(v);
    if (d.length === 11 && d.charAt(0) === '1') d = d.slice(1);
    return d.length === 10;
  }
  function emailOk(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test((v || '').trim()); }

  function setFieldError(input, msg) {
    if (!input) return;
    var err = input.parentElement.querySelector('.field-error');
    if (!err && msg) {
      err = document.createElement('span');
      err.className = 'field-error';
      err.style.cssText = 'display:block;margin-top:4px;font-size:13px;color:#B42318;font-weight:600;';
      input.parentElement.appendChild(err);
    }
    if (err) err.textContent = msg || '';
    input.style.borderColor = msg ? '#B42318' : '';
  }

  function setContactError(msg) {
    if (contactHint) {
      contactHint.textContent = msg || defaultHint;
      contactHint.style.color = msg ? '#B42318' : '';
    }
    if (phoneInput) phoneInput.style.borderColor = msg ? '#B42318' : '';
    if (emailInput) emailInput.style.borderColor = msg ? '#B42318' : '';
  }

  function checkName() {
    var ok = nameOk(nameInput && nameInput.value);
    setFieldError(nameInput, ok ? '' : 'Please enter your name.');
    return ok;
  }

  function checkContact() {
    var p = phoneInput ? phoneInput.value.trim() : '';
    var e = emailInput ? emailInput.value.trim() : '';
    if ((p && phoneOk(p)) || (e && emailOk(e))) { setContactError(''); return true; }
    var msg;
    if (!p && !e)      msg = 'Enter a phone number or email so we can reach you.';
    else if (p)        msg = 'That phone number looks short. 10 digits, please.';
    else               msg = 'That email address doesn\'t look right.';
    setContactError(msg);
    return false;
  }

  function checkConsent() {
    return !consentInput || consentInput.checked;
  }

  function showFormError(msg) {
    if (!formError) return;
    formError.textContent = msg || '';
    formError.classList.toggle('hidden', !msg);
  }

  // Only scold after someone has typed something or tried to submit.
  if (nameInput) {
    nameInput.addEventListener('blur', function () {
      if (submitted || nameInput.value.trim()) checkName();
    });
    nameInput.addEventListener('input', function () {
      if (submitted || nameOk(nameInput.value)) checkName();
    });
  }
  [phoneInput, emailInput].forEach(function (el) {
    if (!el) return;
    el.addEventListener('blur', function () {
      if (submitted || el.value.trim()) checkContact();
    });
    el.addEventListener('input', function () {
      var p = phoneInput ? phoneInput.value : '';
      var e = emailInput ? emailInput.value : '';
      if (submitted || phoneOk(p) || emailOk(e)) checkContact();
    });
  });
  if (consentInput) {
    consentInput.addEventListener('change', function () {
      if (consentInput.checked) showFormError('');
    });
  }

  form.addEventListener('submit', function (e) {
    submitted = true;
    var okName    = checkName();
    var okContact = checkContact();
    var okConsent = checkConsent();

    if (!(okName && okContact && okConsent)) {
      e.preventDefault();
      if (!okConsent && okName && okContact) {
        showFormError('Please check the box above so we\'re allowed to contact you.');
      } else {
        showFormError('Almost there. Fix the highlighted field above.');
      }
      var first = !okName ? nameInput : (!okContact ? (phoneInput || emailInput) : consentInput);
      if (first && first.scrollIntoView) first.scrollIntoView({ behavior: 'smooth', block: 'center' });
      return;
    }

    showFormError('');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending…';
    }
  });
})();

// Tap a photo to see it full screen; swipe or use arrows to browse
(function () {
  var imgs = Array.prototype.slice.call(document.querySelectorAll('main img'));
  if (!imgs.length) return;
  var box = document.createElement('div');
  box.className = 'lb';
  box.setAttribute('role', 'dialog');
  box.setAttribute('aria-label', 'Photo viewer');
  box.innerHTML = '<button class="lb-close" aria-label="Close">&times;</button>' +
    '<button class="lb-prev" aria-label="Previous photo">&#8249;</button>' +
    '<img class="lb-img" alt="">' +
    '<button class="lb-next" aria-label="Next photo">&#8250;</button>' +
    '<p class="lb-cap"></p>';
  document.body.appendChild(box);
  var big = box.querySelector('.lb-img'), cap = box.querySelector('.lb-cap'), i = 0;
  function show(n) {
    i = (n + imgs.length) % imgs.length;
    big.src = imgs[i].currentSrc || imgs[i].src;
    big.alt = imgs[i].alt || '';
    var fig = imgs[i].closest('figure');
    var fc = fig && fig.querySelector('figcaption');
    cap.textContent = fc ? fc.textContent : '';
  }
  function open(n) { show(n); box.classList.add('open'); document.body.style.overflow = 'hidden'; }
  function close() { box.classList.remove('open'); document.body.style.overflow = ''; }
  imgs.forEach(function (im, n) {
    im.classList.add('zoomable');
    im.addEventListener('click', function () { open(n); });
  });
  box.querySelector('.lb-close').addEventListener('click', close);
  box.querySelector('.lb-prev').addEventListener('click', function (e) { e.stopPropagation(); show(i - 1); });
  box.querySelector('.lb-next').addEventListener('click', function (e) { e.stopPropagation(); show(i + 1); });
  box.addEventListener('click', function (e) { if (e.target === box) close(); });
  document.addEventListener('keydown', function (e) {
    if (!box.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') show(i - 1);
    if (e.key === 'ArrowRight') show(i + 1);
  });
  var x0 = null;
  box.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  box.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 50) show(dx < 0 ? i + 1 : i - 1);
  });
})();
