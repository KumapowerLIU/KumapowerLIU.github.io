---
layout: page
title: OPSD-V
description: On-policy self-distillation for post-training few-step autoregressive video generators, improving long-horizon quality and motion dynamics while preserving the original sampler.
img: assets/img/project/opsdv-poster.jpg
video: assets/video/project/opsdv-preview.mp4
redirect: https://meigen-ai.github.io/OPSD-V/
importance: -1
category: work
---

<video class="project-detail-video" src="{{ 'assets/video/project/opsdv-preview.mp4' | relative_url }}" poster="{{ 'assets/img/project/opsdv-poster.jpg' | relative_url }}" autoplay muted loop playsinline controls preload="metadata"></video>

OPSD-V is an on-policy self-distillation framework for post-training few-step autoregressive video generators. It continues training the student on its inference-time rollout states while using a cleaner teacher context to reduce long-horizon degradation and strengthen motion dynamics.

The project targets long autoregressive video generation after few-step distillation, preserving the original sampler while improving visual stability and sustained motion.

Links: [Project page](https://meigen-ai.github.io/OPSD-V/) · [arXiv](https://arxiv.org/abs/2607.08766) · [GitHub](https://github.com/MeiGen-AI/OPSD-V)
