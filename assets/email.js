/* Email links. Each link with a data-mail attribute is turned into a working email link
   when the page loads:

   - On phones and tablets it becomes a mailto: link, which opens the email app (for
     example the Gmail app) with a new message to the address.
   - On computers it opens Gmail's "new message" window in a new browser tab, with the
     address already filled in. (A mailto: link on a computer only works when an email
     program is set up there, which is often not the case.) Visitors who do not use Gmail
     can copy the address from the Contact page.

   The attribute holds the address backwards, with every character moved one place on (so
   "@" becomes "A"); build.py writes it from site.toml. The address therefore never appears
   whole in the HTML, where programs that collect addresses for spam would find it. Without
   JavaScript the links lead to the Contact page, where the address can be read and copied. */
(function () {
  var ua = navigator.userAgent || '';
  var phone = /Android|iPhone|iPad|iPod|Mobile|Silk|Kindle|BlackBerry|IEMobile|Opera Mini/i.test(ua) ||
              (navigator.userAgentData && navigator.userAgentData.mobile === true) ||
              (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);   // iPads present themselves as Macs
  var links = document.querySelectorAll('a[data-mail]');
  for (var i = 0; i < links.length; i++) {
    var a = links[i], s = a.getAttribute('data-mail'), address = '';
    for (var j = s.length - 1; j >= 0; j--) address += String.fromCharCode(s.charCodeAt(j) - 1);
    if (phone) {
      a.href = 'mailto:' + address;
    } else {
      a.href = 'https://mail.google.com/mail/?view=cm&fs=1&to=' + encodeURIComponent(address);
      a.target = '_blank';
      a.rel = 'noopener';
      var label = a.getAttribute('aria-label');
      if (label) a.setAttribute('aria-label', label + ' (opens Gmail in a new tab)');
      a.title = a.title ? a.title + ' (opens Gmail in a new tab)' : 'Opens Gmail in a new tab';
    }
  }
})();
