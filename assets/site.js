(() => {
  'use strict';
  const root = document.documentElement;
  const themeButton = document.querySelector('.theme-toggle');
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  let preferredTheme;
  try { preferredTheme = localStorage.getItem('portfolio-theme'); } catch { /* Storage is optional. */ }
  function setTheme(theme) {
    root.dataset.theme = theme;
    themeButton.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`);
    themeButton.title = themeButton.getAttribute('aria-label');
    document.querySelector('meta[name="theme-color"]').content = theme === 'dark' ? '#151b25' : '#ffffff';
  }
  setTheme(preferredTheme === 'light' || preferredTheme === 'dark' ? preferredTheme : systemTheme.matches ? 'dark' : 'light');
  themeButton.hidden = false;
  themeButton.addEventListener('click', () => {
    preferredTheme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    setTheme(preferredTheme);
    try { localStorage.setItem('portfolio-theme', preferredTheme); } catch { /* The theme still works. */ }
  });
  systemTheme.addEventListener('change', event => { if (!preferredTheme) setTheme(event.matches ? 'dark' : 'light'); });

  const filters = document.querySelector('.filters');
  if (filters) {
    const buttons = [...filters.querySelectorAll('button')];
    const cards = [...document.querySelectorAll('.project-card')];
    filters.hidden = false;
    buttons.forEach(button => button.addEventListener('click', () => {
      const category = button.dataset.filter;
      buttons.forEach(other => other.setAttribute('aria-pressed', String(other === button)));
      cards.forEach(card => { card.hidden = category !== 'all' && card.dataset.category !== category; });
      const count = cards.filter(card => !card.hidden).length;
      document.getElementById('filter-status').textContent = `${count} ${category === 'mentored' ? 'mentored ' : ''}projects shown.`;
    }));
  }

  const dialog = document.getElementById('figure-dialog');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const dialogImage = document.getElementById('dialog-image');
  let figureTrigger;
  document.querySelectorAll('.figure-link').forEach(link => {
    link.setAttribute('aria-haspopup', 'dialog');
    link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      figureTrigger = link;
      document.getElementById('figure-dialog-title').textContent = link.dataset.figureTitle;
      dialogImage.src = link.getAttribute('href');
      dialogImage.alt = link.querySelector('img').alt;
      document.getElementById('dialog-credit').textContent = link.dataset.credit;
      document.getElementById('dialog-source').href = link.dataset.source;
      dialog.showModal();
    });
  });
  dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => { if (figureTrigger) figureTrigger.focus(); });
})();
