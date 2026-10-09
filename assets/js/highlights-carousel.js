(() => {
  document.querySelectorAll('[data-highlights-carousel]').forEach(root => {
    const stage = root.querySelector('.home-report-grid');
    const cards = [...stage.querySelectorAll('.home-report-card')];
    if (cards.length < 2) return;
    const videos = cards.map(card => card.querySelector('video'));
    const reduce = matchMedia('(prefers-reduced-motion: reduce)');
    const motion = root.querySelector('[data-carousel-motion]');
    const sound = root.querySelector('[data-carousel-sound]');
    let muted = true;
    let index = 0, paused = reduce.matches, visible = false, gesture = null, suppressClickUntil = 0;
    const dots = cards.map((card, i) => {
      const dot = document.createElement('button');
      dot.type = 'button'; dot.className = 'highlight-dot';
      dot.setAttribute('aria-label', 'Show ' + card.querySelector('h3').textContent);
      dot.addEventListener('click', () => select(i));
      root.querySelector('.highlight-dots').append(dot);
      card.setAttribute('aria-label', `${i + 1} of ${cards.length}: ${card.querySelector('h3').textContent}`);
      return dot;
    });
    function playback() {
      videos.forEach((video, i) => {
        if (!video) return;
        video.muted = muted || i !== index;
        if (i === index && visible && !paused && !document.hidden) video.play().catch(() => {});
        else video.pause();
      });
      motion.setAttribute('aria-pressed', String(paused));
      motion.setAttribute('aria-label', paused ? 'Play video preview' : 'Pause video preview');
      motion.querySelector('svg').innerHTML = paused ? '<path d="m9 5 10 7-10 7Z"/>' : '<path d="M9 6v12m6-12v12"/>';
      if (sound) {
        sound.setAttribute('aria-pressed', String(!muted));
        sound.setAttribute('aria-label', muted ? 'Unmute video preview' : 'Mute video preview');
        sound.querySelector('svg').innerHTML = '<path d="M10 5 5 9H2v6h3l5 4Z"/>' + (muted ? '<path d="M15 9l6 6m0-6-6 6"/>' : '<path d="M14 8a6 6 0 0 1 0 8m3-11a10 10 0 0 1 0 14"/>');
      }
    }
    function size() { stage.style.height = Math.ceil(Math.max(...cards.map(card => card.offsetHeight)) + 52) + 'px'; }
    function select(next, announce = true) {
      index = (next + cards.length) % cards.length;
      cards.forEach((card, i) => {
        const offset = (i - index + cards.length) % cards.length;
        const position = offset === 0 ? 'center' : offset === 1 ? 'right' : offset === cards.length - 1 ? 'left' : 'hidden';
        card.dataset.position = position;
        card.inert = position === 'hidden';
        card.setAttribute('aria-hidden', String(position === 'hidden'));
        dots[i].setAttribute('aria-current', String(i === index));
      });
      if (announce) root.querySelector('.highlight-status').textContent = `${index + 1} of ${cards.length}: ${cards[index].querySelector('h3').textContent}`;
      playback(); size();
    }
    root.classList.add('is-enhanced');
    root.querySelector('.highlight-controls').hidden = false;
    root.querySelector('[data-carousel-prev]').addEventListener('click', () => select(index - 1));
    root.querySelector('[data-carousel-next]').addEventListener('click', () => select(index + 1));
    motion.addEventListener('click', () => { paused = !paused; playback(); });
    if (sound) sound.addEventListener('click', () => { muted = !muted; playback(); });
    cards.forEach((card, i) => {
      card.addEventListener('click', event => {
        if (performance.now() < suppressClickUntil) { event.preventDefault(); return; }
        if (event.target.closest('a')) return;
        if (i !== index) { event.preventDefault(); select(i); }
      });
      card.addEventListener('focus', () => { if (i !== index && card.matches(':focus-visible')) select(i); });
      card.addEventListener('dragstart', event => event.preventDefault());
    });
    root.addEventListener('keydown', event => {
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault(); select(index + (event.key === 'ArrowRight' ? 1 : -1));
      }
    });
    stage.addEventListener('pointerdown', event => {
      if (event.button !== 0) return;
      gesture = { x: event.clientX, y: event.clientY, id: event.pointerId, dragging: false };
    });
    stage.addEventListener('pointermove', event => {
      if (!gesture || gesture.id !== event.pointerId) return;
      const dx = event.clientX - gesture.x, dy = event.clientY - gesture.y;
      if (Math.abs(dx) > 12 && Math.abs(dx) > Math.abs(dy) * 1.3) {
        gesture.dragging = true; stage.setPointerCapture(event.pointerId);
      }
    });
    stage.addEventListener('pointerup', event => {
      if (!gesture || gesture.id !== event.pointerId) return;
      const dx = event.clientX - gesture.x;
      if (gesture.dragging) {
        suppressClickUntil = performance.now() + 400;
        if (Math.abs(dx) > 40) select(index + (dx < 0 ? 1 : -1));
      }
      gesture = null;
    });
    stage.addEventListener('pointercancel', () => { gesture = null; });
    new ResizeObserver(size).observe(stage);
    cards.forEach(card => new ResizeObserver(size).observe(card));
    new IntersectionObserver(entries => { visible = entries[0].isIntersecting; playback(); }, { threshold: .15 }).observe(root);
    document.addEventListener('visibilitychange', playback);
    reduce.addEventListener('change', () => { paused = reduce.matches; playback(); });
    select(0, false);
  });
})();
