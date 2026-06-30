import { createBoard, renderPuzzle, getBoardState, markIncorrect } from './board.js';
import { initThemeToggle } from './theme.js';

const BOARD_ID = 'sudoku-board';
const NEW_BTN = 'new-game';
const CHECK_BTN = 'check-solution';
const MESSAGE_ID = 'message';

function _el(id) { return document.getElementById(id); }

export function initUI() {
  const boardContainer = _el(BOARD_ID);
  if (!boardContainer) throw new Error('Board container not found');
  createBoard(boardContainer);

  initThemeToggle();

  const newBtn = _el(NEW_BTN);
  const checkBtn = _el(CHECK_BTN);
  const msg = _el(MESSAGE_ID);

  if (newBtn) newBtn.addEventListener('click', async () => {
    try {
      const res = await fetch('/new');
      const data = await res.json();
      renderPuzzle(boardContainer, data.puzzle);
      if (msg) { msg.innerText = ''; msg.style.color = ''; }
    } catch (err) {
      if (msg) { msg.innerText = 'Error starting new game'; msg.style.color = '#d32f2f'; }
    }
  });

  if (checkBtn) checkBtn.addEventListener('click', async () => {
    const board = getBoardState(boardContainer);
    try {
      const res = await fetch('/check', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ board })
      });
      const data = await res.json();
      if (data.error) {
        if (msg) { msg.style.color = '#d32f2f'; msg.innerText = data.error; }
        return;
      }
      markIncorrect(boardContainer, data.incorrect || []);
      if (data.incorrect && data.incorrect.length === 0) {
        if (msg) { msg.style.color = '#388e3c'; msg.innerText = 'Congratulations! You solved it!'; }
      } else {
        if (msg) { msg.style.color = '#d32f2f'; msg.innerText = 'Some cells are incorrect.'; }
      }
    } catch (err) {
      if (msg) { msg.style.color = '#d32f2f'; msg.innerText = 'Error checking solution'; }
    }
  });

  // initialize: click new game programmatically
  if (newBtn) newBtn.click();
}
