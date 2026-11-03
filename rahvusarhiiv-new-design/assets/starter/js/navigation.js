/* Optional native-dialog drawer. Keep an existing equivalent implementation instead of binding twice. */
(() => {
  for (const dialog of document.querySelectorAll('dialog[data-ra-drawer]')) {
    if (dialog.dataset.raBound || typeof dialog.showModal !== 'function') continue;
    dialog.dataset.raBound = 'true';
    const openers = [...document.querySelectorAll('[data-ra-open]')].filter(button => button.dataset.raOpen === dialog.id);
    let opener;
    let previousOverflow;
    const desktop = window.matchMedia('(min-width: 1024px)');
    const close = () => { if (dialog.open) dialog.close(); };
    for (const button of openers) {
      button.hidden = false;
      button.addEventListener('click', () => {
        if (desktop.matches || dialog.open) return;
        opener = button;
        previousOverflow = document.documentElement.style.overflow;
        dialog.showModal();
        document.documentElement.style.overflow = 'hidden';
        openers.forEach(item => item.setAttribute('aria-expanded', 'true'));
      });
    }
    dialog.addEventListener('close', () => {
      if (previousOverflow !== undefined) document.documentElement.style.overflow = previousOverflow;
      previousOverflow = undefined;
      openers.forEach(item => item.setAttribute('aria-expanded', 'false'));
      if (opener?.getClientRects().length) opener.focus();
    });
    dialog.addEventListener('click', event => {
      if (event.target.closest('[data-ra-close], nav a')) close();
      if (event.target === dialog) {
        const rect = dialog.getBoundingClientRect();
        if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) close();
      }
    });
    desktop.addEventListener('change', () => { if (desktop.matches) close(); });
  }
})();
