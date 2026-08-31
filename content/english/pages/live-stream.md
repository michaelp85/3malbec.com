---
title: "Live Stream"
meta_title: "Live Stream"
description: "What a custom build in Murrumbateman actually costs - a running breakdown by trade, updated as each progress claim lands."
draft: false
---


<figure>
    <img id="cam" src="https://imagedelivery.net/OL_tkFq35_Yu641_Ab8jLA/latest/public" alt="Site camera" width="1440" height="804" decoding="async">
</figure>

**Note:** This image will automatically update every 2 minutes between 7am-7pm, and every 10 minutes outside that.

<script>
(() => {
  const el = document.getElementById('cam');
  const src = 'https://imagedelivery.net/OL_tkFq35_Yu641_Ab8jLA/latest/public';
  let busy = false;

  const refresh = () => {
    if (busy || document.hidden) return;
    busy = true;
    const next = new Image();
    next.onload  = () => { el.src = next.src; busy = false; };
    next.onerror = () => { busy = false; };
    next.src = `${src}?t=${Date.now()}`;
  };

  setInterval(refresh, 60000);
  document.addEventListener('visibilitychange', () => document.hidden || refresh());
  window.addEventListener('pageshow', e => e.persisted && refresh());
})();
</script>
