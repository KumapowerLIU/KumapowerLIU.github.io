---
layout: default
permalink: /memories/
title: Memories
nav: true
nav_order: 4
---

<div class="post memories-page">

{% assign memories = site.data.memories | sort: "date" | reverse %}
{% assign featured_memories = site.data.memories | where: "featured", true %}

  <div class="header-bar memories-header">
    <h1>{{ site.blog_name }}</h1>
    <h2>{{ site.blog_description }}</h2>
  </div>
  <div class="memories-intro">
    <p>A lighter page for fishing, travel, and the small moments worth keeping.</p>
  </div>
  <div class="memories-stats">
    <div class="memory-stat">
      <span class="memory-stat-value">{{ memories.size }}</span>
      <span class="memory-stat-label">Albums</span>
    </div>
    <div class="memory-stat">
      <span class="memory-stat-value">{{ featured_memories.size }}</span>
      <span class="memory-stat-label">Featured</span>
    </div>
    <div class="memory-stat">
      <span class="memory-stat-value">{{ memories | map: "date" | first | date: "%Y" }}</span>
      <span class="memory-stat-label">Latest Year</span>
    </div>
  </div>

  <section class="memory-gallery" aria-label="Memories gallery">
    {% for album in memories %}
      {% assign preview_images = album.preview_images %}
      <article class="memory-card{% if album.featured %} memory-card-featured{% endif %}">
        <a
          class="memory-card-button"
          href="{{ album.album_url }}"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Open {{ album.title }} album"
        >
          <div class="memory-card-media">
            <div class="memory-card-collage">
              {% for gallery_image in preview_images limit: 4 %}
                <div class="memory-card-collage-tile memory-card-collage-tile-{{ forloop.index }}">
                  <img class="memory-card-image" src="{{ gallery_image }}" alt="{{ album.title }}">
                </div>
              {% endfor %}
            </div>
            <div class="memory-card-overlay">
              <span class="memory-card-badge">{% if album.featured %}Featured Album{% else %}Memory Album{% endif %}</span>
              <div class="memory-card-overlay-copy">
                <div class="memory-card-meta">
                  <span>{{ album.date | date: '%b %d, %Y' }}</span>
                  <span>{{ album.source | default: 'Album' }}</span>
                </div>
                <h3 class="memory-card-title">{{ album.title }}</h3>
                <p class="memory-card-description">{{ album.description }}</p>
              </div>
            </div>
          </div>
        </a>
      </article>
    {% endfor %}
  </section>

</div>
