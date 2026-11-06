---
title: "I (Crazily) Built a Full-Sheet CNC to Make Some Doors"
meta_title: ""
description: "A completely reasonable and proportionate response to needing a few kitchen doors."
date: 2026-11-02T09:00:00+11:00
image: "/images/cnc/IMG_2640.JPEG"
categories: ["joinery"]
author: "Michael"
tags: ["CNC", "LowRider", "V1 Engineering", "kitchen", "overkill"]
draft: false
toc: false
headerImage: false
---

Most people who need kitchen doors ring a joinery shop and get a quote.

I built a robot.

{{< image src="images/cnc/IMG_2640.JPEG" caption="My LowRider CNC I built" position="center" command="fill" option="q75" class="img-fluid" title="LowRider V4 CNC" webp="false" >}}

**Honestly, why?**

The honest reason is to save a lot of cost, the cabinetry quote is high-very-very-high. And the materials quoted aren't all that great. I want best of the best, without paying insane prices. So I did the math and for around $8k in material costs, $2k for a home-built CNC and an insane amount of my own time and sanity - I can do roughly $100k of joinery for less than $15k myself.

And the result will be high end materials, and flexibility to do whatever I want. I've already build a test cabinet carcess and shaker door and it's turned out great.


## The problem

We need shaker doors for the kitchen. A dozen or so rectangles with a groove around the edge.

A sensible person would look at that and think, "I'll buy those."

My brain looked at it and thought, *"What if I built a 2.4 metre gantry robot that can do anything, ever?"*

## The solution (allegedly)

Meet the **LowRider v4** from V1 Engineering. It's a CNC router, built using metal pipe and 3D printed parts that rides on rails and cuts a full **2.4 m × 1.2 m** sheet in one go, which is great if you ever need to machine an entire sheet of plywood in one sitting. Something I have needed exactly zero times so far.

The specs, for people who enjoy this sort of thing:

- **Working area:** a full sheet. Every last square millimetre. My doors are about 400 mm wide.
- **Brain:** a Jackpot3 board running FluidNC. More processing power than the Apollo guidance computer, to carve a groove around a rectangle.
- **Muscle:** a Makita RT0700CX trim router. It spins at speeds that make the dog leave the room.
- **Rails:** 31.75 mm stainless tube. Yes, I researched seamless versus welded stainless for a hobby machine. Yes, there was a spreadsheet. No, I won't take questions.

## The software stack

You can't just *tell* a CNC to cut a door. That would be too easy.

First you design the cabinet in **Mozaik**. Then Mozaik needs a post processor to turn the design into G-code the LowRider understands. That post processor doesn't exist, so I had to reverse engineer and code up my own CNC post-processor. Easy!

## The cost-benefit analysis

Before you say anything: I did one. And the robot wins. Making the doors myself works out way, way, way cheaper than paying a joinery shop.

Is that the main reason I built a CNC? Absolutely not. Is it a very handy number to show anyone who asks why there's a 2.4 metre robot in the shed? Absolutely yes.

And the doors will be mine, each one cut to tolerances that the timber will completely ignore the first time the humidity changes.

## Where it's at

The machine is built and now in **fully functional**. Woohoo! I've also already done a job for someone. I didn't build this to engrave signs for wedding, but turns out it can do that too - who knew!

{{< image src="images/cnc/IMG_2527.JPEG" caption="CNC doing some engraving for a friend's wedding" position="center" command="fill" option="q75" class="img-fluid" title="CNC doing some engraving for a friend's wedding" webp="false" >}}

If you've ever looked at a simple job and thought "I could build a machine for that", welcome. You're among friends. Bring your own stainless tube.
