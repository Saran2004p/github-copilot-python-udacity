import { describe, it, expect, beforeEach } from 'vitest';
import { createBoard, getBoardState } from '../board.js';

let container;
beforeEach(() => {
  // reset DOM container
  document.body.innerHTML = '';
  container = document.createElement('div');
  container.id = 'test-board';
  document.body.appendChild(container);
});

describe('board module', () => {
  it('creates a 9x9 grid of inputs with block classes', () => {
    createBoard(container);
    const inputs = container.querySelectorAll('input.sudoku-cell');
    expect(inputs.length).toBe(81);
    // check block parity: (0,0) should be block-even, (0,3) block-odd
    const first = inputs[0];
    const fourth = inputs[3];
    expect(first.classList.contains('block-even')).toBe(true);
    expect(fourth.classList.contains('block-odd')).toBe(true);
  });

  it('getBoardState returns 9x9 zeros for empty board', () => {
    createBoard(container);
    const board = getBoardState(container);
    expect(board.length).toBe(9);
    expect(board.every(row => row.length === 9)).toBe(true);
    expect(board.flat().every(v => v === 0)).toBe(true);
  });
});
