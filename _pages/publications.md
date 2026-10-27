---
layout: page
permalink: /publications/
title: Publications
description:
hide_title: true
nav: true
nav_order: 2
---

<!-- _pages/publications.md -->

<div class="publication-showcase">
  <header class="publication-hero">
    <p class="publication-kicker">Research Output</p>
    <h1>Publications</h1>
    <p class="publication-intro">World models, digital humans, and visual generation.</p>
    <div class="publication-meta">
      <div class="publication-note">

        <p><code>*</code> denotes equal contribution; <code>†</code> denotes project leader or corresponding author.</p>
      </div>
      <a
        class="publication-action"
        href="https://scholar.google.com/citations?user=bLRjUzAAAAAJ&hl=zh-CN"
        target="_blank"
        rel="noopener noreferrer"
      >
        Google Scholar ↗
      </a>
    </div>
  </header>

  <section class="publication-search-panel">
    <label class="search-panel-label" for="bibsearch">Find a paper</label>

    <div class="search-panel-input">
      {% include bib_search.liquid %}
    </div>
  </section>

  <section class="publication-categories-nav" aria-label="Publication categories">
    <button type="button" class="publication-category-chip" data-target="full">Full</button>
    <button type="button" class="publication-category-chip is-active" data-target="selected">Selected</button>
    <button type="button" class="publication-category-chip" data-target="2d">Image Generation &amp; Editing</button>
    <button type="button" class="publication-category-chip" data-target="3d">Human-Centered Spatial Intelligence</button>
    <button type="button" class="publication-category-chip" data-target="4d">Video Generation &amp; World Models</button>
  </section>

  <script>
    // Set the filter buttons as soon as they exist, before the long bibliography parses.
    document.querySelectorAll('.publication-category-chip').forEach(function (chip) {
      var active = chip.dataset.target === document.documentElement.dataset.publicationCategory;
      chip.classList.toggle('is-active', active);
      chip.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
  </script>

  <div class="publications publications-collection" data-category="full">
    <h2 class="bibliography">Full</h2>
    {% bibliography --group_by year --query @* %}
  </div>

  <div class="publications publications-collection is-active" data-category="selected">
    <h2 class="bibliography">Selected</h2>
    {% bibliography --group_by year --query @*[selected=true]* %}
  </div>

  <div class="publications publications-collection" data-category="2d">
    <h2 class="bibliography">Image Generation &amp; Editing</h2>
    {% bibliography --group_by year --query @*[dimension=2d]* %}
  </div>

  <div class="publications publications-collection" data-category="3d">
    <h2 class="bibliography">Human-Centered Spatial Intelligence</h2>
    {% bibliography --group_by year --query @*[dimension=3d]* %}
  </div>

  <div class="publications publications-collection" data-category="4d">
    <h2 class="bibliography">Video Generation &amp; World Models</h2>
    {% bibliography --group_by year --query @*[dimension=4d]* %}
  </div>

</div>

<script>
  (function () {
    const chips = document.querySelectorAll(".publication-category-chip");
    const collections = document.querySelectorAll(".publications-collection");

    const validCategories = new Set(Array.from(chips, (chip) => chip.dataset.target));

    const setActiveCategory = (target, updateUrl = false) => {
      const category = validCategories.has(target) ? target : "selected";

      document.documentElement.dataset.publicationCategory = category;

      chips.forEach((chip) => {
        chip.classList.toggle("is-active", chip.dataset.target === category);
        chip.setAttribute("aria-pressed", chip.dataset.target === category ? "true" : "false");
      });

      const activeChip = document.querySelector('.publication-category-chip.is-active');
      const nav = activeChip.parentElement;
      if (nav.scrollWidth > nav.clientWidth) {
        nav.scrollLeft += activeChip.getBoundingClientRect().left - nav.getBoundingClientRect().left - (nav.clientWidth - activeChip.offsetWidth) / 2;
      }

      collections.forEach((section) => {
        section.classList.toggle("is-active", section.dataset.category === category);
      });

      if (updateUrl) {
        const url = new URL(window.location.href);
        if (category === "selected") {
          url.searchParams.delete("category");
        } else {
          url.searchParams.set("category", category);
        }
        window.history.replaceState({}, "", url);
      }
    };

    chips.forEach((chip) => {
      chip.addEventListener("click", function () {
        setActiveCategory(chip.dataset.target, true);
      });
    });

    const restoreCategory = () => setActiveCategory(new URLSearchParams(window.location.search).get("category") || "selected");
    restoreCategory();
    window.addEventListener("popstate", restoreCategory);
    window.addEventListener("pageshow", restoreCategory);
  })();
</script>

<script src="{{ '/assets/js/publication-media.js' | relative_url | bust_file_cache }}" defer></script>
