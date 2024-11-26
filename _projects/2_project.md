---
layout: page
title: Consumer Digital Human.
description:  Given a single image(T pose), we can create an avatar and drive this avatar with target motion.
img: assets/img/project/digital.gif
redirect: https://github.com/xthan/smplreg/tree/main
importance: 2
category: work
---


A Pytorch3D-based registration method between a reconstructed point cloud (e.g., the output of PIFuHD, scan data, or synthetic data like CLOTH4D) and an estimated SMPL mesh (e.g., HMR, ProHMR, or PyMAF). 

Please our code: [**SMPL Registration**](https://github.com/xthan/smplreg/tree/main) 


## Registration


<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/project/before_registration.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/project/after_registration.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/project/after_smpld_registration.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    On the left. Visualization of PIFu point clouds and SMPL point clouds.
Middle.Visualization of point clouds after SMPL registration.
Right.Visualization of point clouds  after SMPL+D registration.
</div>

 
 
