---
layout: page
permalink: /publications/
title: Publications
description: 
nav: true
nav_order: 2
---

<!-- _pages/publications.md -->

<div class="publication-showcase">
  <header class="publication-hero">
    <p class="publication-kicker">Research Output</p>
    <h1>Publications</h1>
    <p class="publication-intro">
      A curated record of recent work across computer vision, multimedia understanding, and efficient AI systems.
      Use the search box to filter by topic, venue, or collaborator.
    </p>
    <div class="publication-meta">
      <div class="publication-note">
        <span class="label">Contribution note</span>
        <p><code>*</code> denotes equal contribution; <code>†</code> denotes project leader or corresponding author.</p>
      </div>
      <a
        class="publication-action"
        href="https://scholar.google.com/citations?user=bLRjUzAAAAAJ&hl=zh-CN"
        target="_blank"
        rel="noopener noreferrer"
      >
        View Full Google Scholar List
      </a>
    </div>
  </header>

  <section class="publication-search-panel">
    <div class="search-panel-copy">
      <span class="search-panel-label">Quick Filter</span>
      <p>Search by title, author, venue, year, or keyword to jump directly to relevant papers.</p>
    </div>

    <div class="search-panel-input">
      {% include bib_search.liquid %}
    </div>
  </section>

  <section class="publication-categories-nav" aria-label="Publication categories">
    <button type="button" class="publication-category-chip" data-target="full">Full</button>
    <button type="button" class="publication-category-chip is-active" data-target="selected">Selected</button>
    <button type="button" class="publication-category-chip" data-target="2d">2D Reconstruction & Editing</button>
    <button type="button" class="publication-category-chip" data-target="3d">3D Static Generation</button>
    <button type="button" class="publication-category-chip" data-target="4d">4D Dynamic Avatarization</button>
  </section>

  <div class="publications publications-collection" data-category="full">
    <h2 class="bibliography">Full</h2>
    {% bibliography --group_by year --query @* %}
  </div>

  <div class="publications publications-collection is-active" data-category="selected">
    <h2 class="bibliography">Selected</h2>
    {% bibliography --group_by year --query @*[selected=true]* %}
  </div>

  <div class="publications publications-collection" data-category="2d">
    <h2 class="bibliography">2D Reconstruction & Editing</h2>
    {% bibliography --group_by year --query @*[dimension=2d]* %}
  </div>

  <div class="publications publications-collection" data-category="3d">
    <h2 class="bibliography">3D Static Generation</h2>
    {% bibliography --group_by year --query @*[dimension=3d]* %}
  </div>

  <div class="publications publications-collection" data-category="4d">
    <h2 class="bibliography">4D Dynamic Avatarization</h2>
    {% bibliography --group_by year --query @*[dimension=4d]* %}
  </div>

</div>

<script>
  document.addEventListener("DOMContentLoaded", function () {
    const chips = document.querySelectorAll(".publication-category-chip");
    const collections = document.querySelectorAll(".publications-collection");

    const setActiveCategory = (target) => {
      chips.forEach((chip) => {
        chip.classList.toggle("is-active", chip.dataset.target === target);
      });

      collections.forEach((section) => {
        section.classList.toggle("is-active", section.dataset.category === target);
      });
    };

    chips.forEach((chip) => {
      chip.addEventListener("click", function () {
        setActiveCategory(chip.dataset.target);
      });
    });

    setActiveCategory("selected");
  });
</script>
