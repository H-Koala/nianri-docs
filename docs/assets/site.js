"use strict";
const menu = document.querySelector(".language");
document.addEventListener("click", event => { if (menu && !menu.contains(event.target)) menu.open = false; });
document.addEventListener("keydown", event => { if (event.key === "Escape" && menu?.open) { menu.open = false; menu.querySelector("summary").focus(); } });
const copy = document.querySelector("[data-copy]");
if (copy) {
  copy.hidden = false;
  copy.addEventListener("click", async () => {
    const status = document.querySelector(".live-status");
    try { await navigator.clipboard.writeText(copy.dataset.copy); status.textContent = copy.dataset.success; }
    catch { status.textContent = copy.dataset.failure; }
  });
}
const sections = document.querySelectorAll(".policy-section");
if ("IntersectionObserver" in window && sections.length) {
  const observer = new IntersectionObserver(entries => {
    const entry = entries.find(item => item.isIntersecting);
    if (!entry) return;
    document.querySelectorAll(".toc a").forEach(link => {
      const active = link.getAttribute("href") === "#" + entry.target.id;
      link.classList.toggle("active", active);
      if (active) link.setAttribute("aria-current", "location"); else link.removeAttribute("aria-current");
    });
  }, {rootMargin: "-12% 0px -70% 0px", threshold: 0});
  sections.forEach(section => observer.observe(section));
}
