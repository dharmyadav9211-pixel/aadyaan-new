(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
    });
  }
  document.querySelectorAll('.sub-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var li = btn.parentElement;
      var open = li.classList.toggle('open');
      btn.setAttribute('aria-expanded', open);
    });
  });

  // Quote form: compose the enquiry and hand it to WhatsApp or email.
  var form = document.getElementById('quote-form');
  if (!form) return;
  var via = 'wa';
  form.querySelectorAll('button[type=submit]').forEach(function (b) {
    b.addEventListener('click', function () { via = b.value; });
  });
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var f = form.elements;
    var err = form.querySelector('.form-error');
    if (!f.name.value.trim() || !f.phone.value.trim()) { err.hidden = false; return; }
    err.hidden = true;
    var lines = [
      'Quote request - Reliable Steel Weld website',
      'Name: ' + f.name.value,
      f.company.value && 'Company: ' + f.company.value,
      'Phone: ' + f.phone.value,
      'Service: ' + f.service.value,
      'Material: ' + f.material.value,
      f.thickness.value && 'Thickness/size: ' + f.thickness.value,
      f.qty.value && 'Quantity: ' + f.qty.value,
      f.msg.value && 'Details: ' + f.msg.value
    ].filter(Boolean).join('\n');
    if (via === 'email') {
      location.href = 'mailto:' + form.dataset.email + '?subject=' +
        encodeURIComponent('Quote request: ' + f.service.value) + '&body=' + encodeURIComponent(lines);
    } else {
      window.open('https://wa.me/' + form.dataset.wa + '?text=' + encodeURIComponent(lines), '_blank', 'noopener');
    }
  });
})();
