// Only load previews that are visible in the chosen category.
(function () {
  var videos = Array.from(document.querySelectorAll('.publication-showcase video[data-src]'));
  var visible = new Set();
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  function update(video) {
    var active = visible.has(video) && !document.hidden && video.getClientRects().length > 0;
    if (active) {
      if (!video.hasAttribute('src')) {
        video.src = video.dataset.src;
        video.load();
      }
      if (reduced.matches) video.controls = true;
      else video.play().catch(function () {});
    } else {
      video.pause();
      if (video.hasAttribute('src')) {
        video.removeAttribute('src');
        video.load();
      }
    }
  }
  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) visible.add(entry.target);
        else visible.delete(entry.target);
        update(entry.target);
      });
    }, { rootMargin: '100px 0px' });
    videos.forEach(function (video) { observer.observe(video); });
  } else {
    videos.forEach(function (video) {
      video.controls = true;
      video.addEventListener('pointerdown', function () { visible.add(video); update(video); }, { once: true });
    });
  }
  document.addEventListener('visibilitychange', function () { videos.forEach(update); });
  reduced.addEventListener('change', function () {
    videos.forEach(function (video) { if (reduced.matches) video.pause(); else update(video); });
  });
})();
