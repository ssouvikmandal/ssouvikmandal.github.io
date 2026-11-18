/* MathJax settings for this site. MathJax itself is in assets/mathjax/ (version 4.1.3,
   with its New Computer Modern math font in assets/mathjax/fonts/), so no outside
   service is used. Write inline formulas as $...$ or \(...\), displayed ones as
   $$...$$ or \[...\]; write \$ for a literal dollar sign. */
window.MathJax = {
  loader: {
    paths: { fonts: '[mathjax]/fonts' }   // the local font copy, not the default CDN
  },
  tex: {
    inlineMath: { '[+]': [['$', '$']] },
    processEscapes: true
  },
  output: { displayOverflow: 'scroll' }   // wide formulas and diagrams scroll sideways on phones
};
