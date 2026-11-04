---
title: "Live Stream"
meta_title: "Live Stream"
description: "Live site cameras from our custom home build in Murrumbateman - snapshots update every 2 minutes during the day and every 10 minutes overnight."
draft: false
---

<figure>
    <img class="livecam" src="https://webcam.3malbec.com/cam1.jpg" alt="Site camera 1" width="1440" height="804" decoding="async">
</figure>

<figure>
    <img class="livecam" src="https://webcam.3malbec.com/cam2.jpg" alt="Site camera 2" width="1440" height="804" decoding="async">
</figure>

**Note:** These images automatically update every 2 minutes between 6am-7pm, and every 10 minutes outside that.

<script>
(() => {
  const cams = [...document.querySelectorAll('img.livecam')].map(el => ({
    el,
    src: el.src.split('?')[0],
    busy: false,
  }));

  const refreshOne = cam => {
    if (cam.busy) return;
    cam.busy = true;
    const next = new Image();
    next.onload  = () => { cam.el.src = next.src; cam.busy = false; };
    next.onerror = () => { cam.busy = false; };
    next.src = `${cam.src}?t=${Date.now()}`;
  };

  const refresh = () => { if (!document.hidden) cams.forEach(refreshOne); };

  setInterval(refresh, 60000);
  document.addEventListener('visibilitychange', () => document.hidden || refresh());
  window.addEventListener('pageshow', e => e.persisted && refresh());
})();
</script>
