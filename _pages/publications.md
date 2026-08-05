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
    <p class="publication-intro">
      A research record spanning image generation and editing, human-centered multimodal spatial intelligence,
      and video generation with generative world models. Search by topic, venue, year, or collaborator.
    </p>
    <div class="publication-pathway" aria-label="Research themes across image generation, spatial intelligence, and video generation">
      <span>Image Generation &amp; Editing</span>
      <i aria-hidden="true">→</i>
      <span>Human-Centered Spatial Intelligence</span>
      <i aria-hidden="true">→</i>
      <span>Video Generation &amp; World Models</span>
    </div>
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
    <button type="button" class="publication-category-chip" data-target="2d">Image Generation &amp; Editing</button>
    <button type="button" class="publication-category-chip" data-target="3d">Human-Centered Spatial Intelligence</button>
    <button type="button" class="publication-category-chip" data-target="4d">Video Generation &amp; World Models</button>
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
  document.addEventListener("DOMContentLoaded", function () {
    const chips = document.querySelectorAll(".publication-category-chip");
    const collections = document.querySelectorAll(".publications-collection");

    const validCategories = new Set(Array.from(chips, (chip) => chip.dataset.target));

    const setActiveCategory = (target, updateUrl = false) => {
      const category = validCategories.has(target) ? target : "selected";

      chips.forEach((chip) => {
        chip.classList.toggle("is-active", chip.dataset.target === category);
      });

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

    const requestedCategory = new URLSearchParams(window.location.search).get("category");
    setActiveCategory(requestedCategory || "selected");
  });
</script>
