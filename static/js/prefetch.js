const cache = new Map();

document.addEventListener("mouseover", e => {
  const link = e.target.closest("a[data-prefetch]");
  if (!link) return;

  const url = link.href;
  if (cache.has(url)) return;

  fetch(url)
    .then(res => res.text())
    .then(html => cache.set(url, html));
});

document.addEventListener("click", e => {
  const link = e.target.closest("a[data-prefetch]");
  if (!link) return;

  const url = link.href;
  if (!cache.has(url)) return;

  e.preventDefault();
  document.open();
  document.write(cache.get(url));
  document.close();
});
