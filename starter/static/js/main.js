import { initUI } from './ui.js';

window.addEventListener('DOMContentLoaded', () => {
  try { initUI(); } catch (err) { console.error('UI init failed', err); }
});
