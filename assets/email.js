/* Email links. Each link with a data-mail attribute becomes a mailto: link when the page
   loads. The attribute holds the address backwards, with every character moved one place
   on (so "@" becomes "A"); build.py writes it from site.toml. The address therefore never
   appears whole in the HTML, where programs that collect addresses for spam would find
   it. Without JavaScript the links lead to the Contact page instead. */
(function () {
  var links = document.querySelectorAll('a[data-mail]');
  for (var i = 0; i < links.length; i++) {
    var s = links[i].getAttribute('data-mail'), address = '';
    for (var j = s.length - 1; j >= 0; j--) address += String.fromCharCode(s.charCodeAt(j) - 1);
    links[i].href = 'mailto:' + address;
  }
})();
