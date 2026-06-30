// Theme helpers: toggle and persist theme preference
const STORAGE_KEY = 'sudoku-contrast';

export function setTheme(lowContrast) {
  document.body.classList.toggle('contrast-low', !!lowContrast);
  const btn = document.getElementById('contrast-toggle');
  if (btn) {
    btn.setAttribute('aria-pressed', String(!!lowContrast));
    btn.textContent = !!lowContrast ? 'Low contrast' : 'High contrast';
  }
}

export function loadTheme() {
  const saved = localStorage.getItem(STORAGE_KEY);
  return saved === 'low';
}

export function persistTheme(lowContrast) {
  localStorage.setItem(STORAGE_KEY, lowContrast ? 'low' : 'high');
}

export function initThemeToggle() {
  const btn = document.getElementById('contrast-toggle');
  if (!btn) return;
  const initial = loadTheme();
  setTheme(initial);
  btn.addEventListener('click', () => {
    const nowLow = !document.body.classList.contains('contrast-low');
    setTheme(nowLow);
    persistTheme(nowLow);
  });
}
