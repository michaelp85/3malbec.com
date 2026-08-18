---
title: "Subscribe"
meta_title: "Subscribe to receive email notifications"
description: "Subscribe to receive email notifications."
draft: false
---

Subscribe by email to receive notifications for any new blog posts. I won't use your email for anything else.

<script>
(() => {
  const el = document.getElementById('cam');
  const src = 'https://3malbec.b-cdn.net/latest.jpg';
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


<form action="https://buttondown.com/api/emails/embed-subscribe/mpasqualone" method="post" class="embeddable-buttondown-form">
    <div class="mb-6">
        <label for="bd-email" class="form-label">Enter your email <span class="text-red-500">*</span></label>
        <input id="bd-email" name="email" class="form-input" type="text">
    </div>
    <button type="submit" class="btn btn-primary" value="Subscribe">Subscribe</button>
</form>