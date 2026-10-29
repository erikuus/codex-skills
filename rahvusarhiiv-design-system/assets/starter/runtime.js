/* Shell/navigation enhancement only. No business endpoints or third-party runtime. */
(() => {
  const triggers = [...document.querySelectorAll('[data-open-dialog]')];
  let returnFocus = null;
  let previousOverflow = '';
  function closeDialog(dialog) { if (dialog.open) dialog.close(); }
  for (const trigger of triggers) {
    trigger.addEventListener('click', () => {
      const dialog = document.getElementById(trigger.dataset.openDialog);
      if (!dialog || dialog.open) return;
      document.querySelectorAll('dialog[open]').forEach(closeDialog);
      returnFocus = trigger;
      previousOverflow = document.body.style.overflow;
      document.body.style.overflow = 'hidden';
      trigger.setAttribute('aria-expanded', 'true');
      dialog.showModal();
    });
  }
  for (const dialog of document.querySelectorAll('dialog')) {
    dialog.querySelectorAll('[data-close-dialog]').forEach(button => button.addEventListener('click', () => closeDialog(dialog)));
    dialog.addEventListener('click', event => {
      const r = dialog.getBoundingClientRect();
      if (event.target === dialog && (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom)) closeDialog(dialog);
    });
    dialog.querySelectorAll('a[href]').forEach(link => link.addEventListener('click', event => {
      // TOC links own their anchor/focus handling below. Local section links must
      // also move focus after close, rather than letting focus return undo scroll.
      const destination = new URL(link.href);
      const sameDocument = destination.origin === location.origin && destination.pathname === location.pathname && destination.search === location.search;
      const target = sameDocument && destination.hash ? document.getElementById(decodeURIComponent(destination.hash.slice(1))) : null;
      if (target && !link.closest('[data-toc]')) {
        event.preventDefault();
        dialog.addEventListener('close', () => {
          history.pushState(null, '', destination.hash);
          target.setAttribute('tabindex', '-1');
          target.scrollIntoView({behavior:'instant',block:'start'});
          target.focus({preventScroll:true});
        }, {once:true});
      }
      closeDialog(dialog);
    }));
    dialog.addEventListener('close', () => {
      document.body.style.overflow = previousOverflow;
      triggers.filter(t => t.dataset.openDialog === dialog.id).forEach(t => t.setAttribute('aria-expanded', 'false'));
      const visible = returnFocus && returnFocus.getClientRects().length;
      if (visible) returnFocus.focus();
      else document.getElementById('main-content')?.focus({preventScroll:true});
    });
    if (dialog.dataset.closeAt) {
      const media = matchMedia(`(min-width: ${dialog.dataset.closeAt}px)`);
      media.addEventListener('change', () => { if (media.matches) closeDialog(dialog); });
    }
  }
  for (const link of document.querySelectorAll('[data-feedback]')) {
    const target = new URL(link.href);
    target.searchParams.set('url', location.href);
    link.href = target.href;
    link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      const popup = window.open('', 'rahvusarhiiv-feedback', 'top=100,left=100,width=800,height=600,resizable=yes,scrollbars=yes');
      if (popup) {
        event.preventDefault();
        popup.opener = null;
        popup.location.href = link.href;
      }
    });
  }
  const article = document.querySelector('[data-article]');
  if (!article) return;
  const headings = [...article.querySelectorAll('h2[id]')];
  const links = [...document.querySelectorAll('[data-toc] a')];
  const mark = id => links.forEach(link => {
    if (decodeURIComponent(link.hash.slice(1)) === id) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
  let queued = false;
  const update = () => {
    queued = false;
    let current = headings[0];
    for (const h of headings) { if (h.getBoundingClientRect().top <= 200) current = h; }
    if (current) mark(current.id);
  };
  document.addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(update); } }, {passive:true});
  for (const link of links) link.addEventListener('click', event => {
    const id = decodeURIComponent(link.hash.slice(1));
    const heading = document.getElementById(id);
    if (!heading) return;
    event.preventDefault();
    document.querySelectorAll('dialog[open]').forEach(closeDialog);
    // Native anchor-equivalent navigation: stable URL, target focus, no timing race with scroll spy.
    history.pushState(null, '', link.hash);
    heading.setAttribute('tabindex', '-1');
    requestAnimationFrame(() => { heading.scrollIntoView({behavior:'instant',block:'start'}); heading.focus({preventScroll:true}); mark(id); });
  });
  window.addEventListener('hashchange', update);
  update();
})();
