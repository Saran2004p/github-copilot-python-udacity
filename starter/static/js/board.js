// Board module: responsible for DOM creation and simple board operations
const SIZE = 9;

export function createBoard(container) {
  container.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      const blockRow = Math.floor(i / 3);
      const blockCol = Math.floor(j / 3);
      const isEvenBlock = ((blockRow + blockCol) % 2) === 0;
      input.classList.add('sudoku-cell');
      input.classList.add(isEvenBlock ? 'block-even' : 'block-odd');
      input.dataset.row = i;
      input.dataset.col = j;
      input.setAttribute('aria-label', `Row ${i+1} Column ${j+1}`);
      input.addEventListener('input', (e) => {
        e.target.value = e.target.value.replace(/[^1-9]/g, '');
      });
      rowDiv.appendChild(input);
    }
    container.appendChild(rowDiv);
  }
}

function _ensureBoard(container) {
  if (!container.querySelector('.sudoku-row')) createBoard(container);
}

export function renderPuzzle(container, puzzle) {
  _ensureBoard(container);
  const inputs = container.querySelectorAll('input.sudoku-cell');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      inp.classList.remove('incorrect');
      inp.classList.remove('prefilled');
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.classList.add('prefilled');
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}

export function getBoardState(container) {
  _ensureBoard(container);
  const inputs = container.querySelectorAll('input.sudoku-cell');
  const board = Array.from({ length: SIZE }, () => Array(SIZE).fill(0));
  inputs.forEach((inp, idx) => {
    const r = Math.floor(idx / SIZE);
    const c = idx % SIZE;
    board[r][c] = inp.value ? parseInt(inp.value, 10) : 0;
  });
  return board;
}

export function markIncorrect(container, incorrectCells) {
  _ensureBoard(container);
  const inputs = container.querySelectorAll('input.sudoku-cell');
  inputs.forEach(inp => inp.classList.remove('incorrect'));
  incorrectCells.forEach(([r, c]) => {
    const idx = r * SIZE + c;
    const inp = inputs[idx];
    if (inp && !inp.disabled) inp.classList.add('incorrect');
  });
}

export function reset(container) {
  _ensureBoard(container);
  const inputs = container.querySelectorAll('input.sudoku-cell');
  inputs.forEach(inp => {
    inp.value = '';
    inp.disabled = false;
    inp.classList.remove('prefilled', 'incorrect');
  });
}
