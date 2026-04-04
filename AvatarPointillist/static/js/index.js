$(document).ready(function() {
  $('.navbar-burger').on('click', function() {
    const target = $(this).data('target');
    $(this).toggleClass('is-active');
    $('#' + target).toggleClass('is-active');
  });

  const teaser = document.getElementById('hero-teaser-video');
  if (teaser) {
    const loopEnd = 14;
    teaser.addEventListener('timeupdate', function() {
      if (teaser.currentTime >= loopEnd) {
        teaser.currentTime = 0;
        const playPromise = teaser.play();
        if (playPromise && typeof playPromise.catch === 'function') {
          playPromise.catch(() => {});
        }
      }
    });
  }

  const rotator = document.getElementById('gallery-rotator');
  if (rotator) {
    const slides = Array.from(rotator.querySelectorAll('.gallery-slide'));
    const prevButton = rotator.querySelector('.gallery-prev');
    const nextButton = rotator.querySelector('.gallery-next');
    let activeIndex = 0;

    function resetVideo(video) {
      video.pause();
      video.currentTime = 0;
    }

    function playSlide(index) {
      slides.forEach((slide, slideIndex) => {
        const isActive = slideIndex === index;
        slide.classList.toggle('is-active', isActive);
        if (!isActive) {
          slide.querySelectorAll('.gallery-video').forEach(resetVideo);
        }
      });

      const activeSlide = slides[index];
      const video = activeSlide.querySelector('.gallery-video');
      if (!video) {
        return;
      }

      video.onended = () => {
        activeIndex = (activeIndex + 1) % slides.length;
        playSlide(activeIndex);
      };
      video.currentTime = 0;
      const playPromise = video.play();
      if (playPromise && typeof playPromise.catch === 'function') {
        playPromise.catch(() => {});
      }
    }

    if (prevButton) {
      prevButton.addEventListener('click', function() {
        activeIndex = (activeIndex - 1 + slides.length) % slides.length;
        playSlide(activeIndex);
      });
    }

    if (nextButton) {
      nextButton.addEventListener('click', function() {
        activeIndex = (activeIndex + 1) % slides.length;
        playSlide(activeIndex);
      });
    }

    playSlide(activeIndex);
  }

  const comparisonPagesRoot = document.getElementById('comparison-pages');
  if (comparisonPagesRoot) {
    const pages = Array.from(comparisonPagesRoot.querySelectorAll('.comparison-page'));
    const dots = Array.from(document.querySelectorAll('.comparison-dot'));
    const prev = document.querySelector('.comparison-prev');
    const next = document.querySelector('.comparison-next');
    let activePage = 0;

    function syncComparisonVideos(page, shouldPlay) {
      const videos = page.querySelectorAll('.comparison-clip-video');
      videos.forEach((video) => {
        if (shouldPlay) {
          const startPlayback = () => {
            if (video.currentTime < 0.04) {
              try {
                video.currentTime = 0.04;
              } catch (e) {}
            }
            const playPromise = video.play();
            if (playPromise && typeof playPromise.catch === 'function') {
              playPromise.catch(() => {});
            }
          };

          if (video.readyState >= 2) {
            startPlayback();
          } else {
            video.onloadeddata = startPlayback;
          }
        } else {
          video.pause();
          video.currentTime = 0;
          video.onloadeddata = null;
        }
      });
    }

    function showComparisonPage(index) {
      activePage = (index + pages.length) % pages.length;
      pages.forEach((page, pageIndex) => {
        const isActive = pageIndex === activePage;
        page.classList.toggle('is-active', isActive);
        syncComparisonVideos(page, isActive);
      });
      dots.forEach((dot, dotIndex) => {
        dot.classList.toggle('is-active', dotIndex === activePage);
      });
    }

    if (prev) {
      prev.addEventListener('click', function() {
        showComparisonPage(activePage - 1);
      });
    }

    if (next) {
      next.addEventListener('click', function() {
        showComparisonPage(activePage + 1);
      });
    }

    dots.forEach((dot) => {
      dot.addEventListener('click', function() {
        showComparisonPage(Number(dot.dataset.page));
      });
    });

    showComparisonPage(0);
  }
});
