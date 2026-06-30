# GitHub Copilot Instructions

## Project Overview
This project is a Python Flask Sudoku application. Refactor the legacy code into a clean, modular, maintainable application while preserving existing functionality.

## Coding Standards
- Follow PEP 8 style guidelines.
- Use meaningful variable, function, and class names.
- Keep functions short, reusable, and focused on a single responsibility.
- Avoid duplicate code.
- Add docstrings to public functions and classes.
- Handle errors gracefully and consistently.

## Project Structure
- Separate Flask routes from Sudoku game logic.
- Organize code into reusable modules where appropriate.
- Keep HTML, CSS, JavaScript, and Python responsibilities separate.
- Maintain a clean and readable folder structure.

## Testing
- Use pytest for testing.
- Ensure existing tests pass before making changes.
- Run tests after each major feature or refactoring.
- Add new tests for new functionality when practical.

## Sudoku Requirements
- Generate Sudoku puzzles with exactly one unique solution.
- Support Easy, Medium, and Hard difficulty levels.
- Lock prefilled cells so they cannot be edited.
- Highlight invalid user entries.
- Display a congratulatory message when the puzzle is solved.
- Implement a Hint button that fills one correct cell and locks it.
- Implement a Check Puzzle button to highlight incorrect entries.
- Maintain a Top 10 leaderboard with player name, completion time, difficulty, and hints used.
- Persist leaderboard data between browser sessions.

## User Interface
- Build a responsive layout for desktop and mobile devices.
- Support both light and dark mode.
- Use alternating colors for each 3×3 Sudoku block.
- Keep fonts, buttons, and controls consistent and readable.
- Minimize layout shifts and maintain a clean interface.

## General Guidance
- Prefer readability over overly complex solutions.
- Preserve existing functionality while refactoring.
- Explain complex logic with concise comments when needed.
- Suggest simpler alternatives when multiple valid implementations exist.
- Write maintainable and production-quality code.