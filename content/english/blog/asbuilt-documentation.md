---
title: "As Built Documentation & Drone Surveys"
slug: 'asbuilt-documentation'
meta_title: "As-Built Documentation for an Owner-Build"
description: "What I'm recording as we build — as-built 3D model, survey data, and photos — plus what I learned about surveying accuracy the hard way."
date: 2026-08-18T12:00:00Z
image: "images/documentation/Framing-Overview.jpg"
categories: ["documentation", "survey", "technology"]
author: "Michael"
tags: ["documentation"]
summary: "What level of documentation I currently have, and some lessons with surveying."
draft: false
toc: false
headerImage: false
---

I designed and modelled the house in 3D in SketchUp, right down to individual elements like framing members and waffle pods. As it goes up, I survey the site myself and feed the photogrammetry back into the model - so what's on screen matches what's actually been built, not just what was drawn.

## My 3D Model

Here is my current model with anticipated framing members and trusses, we're not quite at framing stage yet - but once we are then I can easily adjust this. Once structual steel, electrical, plumbing and other details go in I'll also add these into the model.

{{< image src="images/documentation/Framing-Overview.jpg" caption="My 3D model showing framing and trusses" position="center" command="fill" option="q75" class="img-fluid" title="3D framing model" webp="false" >}}

## My Surveying Setup

* DJI Mavic 2 with RTK module, using CORSnet-NSW via the free NTRIP broadcaster service from [Geoscience Australia](https://gnss.ga.gov.au/stream)
* 6x 3D Printed GCPs that have been professionally targeted by a surveyor
* Pix4DMatic for Processing, with dialed in settings for my specific site.
* Flying a nadir path using DroneDeploy, 25m height, 80% front overlap, 75% side overlap.

I am flying under ideal conditions, wind, and time of day and it's taken me a little bit of effort and trial and error to really dial-in my Pix4DMatic settings for my site.

*Note*: For any survey requirements for council, construction drawings, etc, I've used a qualified surveyor. These surveys I am doing is only for my as-built documentation.

## Accuracy

Throughout every survey I fly and model, I've been taking real-life measurements and comparing them to my 3D models. Vertical "z" accuracy is the hardest to dial in, but everywhere important that I've checked I've managed to get it to around +/- 6mm accuracy, and some unimportant places 20-30mm.

There's even better accuracy on the x,y plane which is the dimension that matters for locating hydronic pipes for example. Measuring the pipes from various locations in real-life and comparing to my models, it's hard to even spot the margin of error. If I ever need to pinpoint something in the slab, I am confident I can hit it to within 5mm in any x,y or z plane.

{{< image src="images/documentation/3D-vs-Reallife.jpg" caption="My 3D model accuracy vs Real-life, both measured at the same position" position="center" command="fill" option="q75" class="img-fluid" title="3D model accuracy" webp="false" >}}

## Ground Control Points (GCPs)

I've got 6 permanent GCPs on the property and had a qualified surveyor target them for me, plus all the fence posts.

{{< image src="images/documentation/GCPs.jpg" caption="One of the Ground Control Points (GCP) on the property as show in the 3D model" position="center" command="fill" option="q75" class="img-fluid" title="GCP" webp="false" >}}