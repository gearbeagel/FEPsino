# Patch 1.0.0

## Bugfixes and Improvements
1. Added favicon and changed the title of the page.
2. Fixed the issue when logging in with a new user, the page was not redirecting to the home page.
3. Redesigned the profile page.
4. Centered the icon in the nav, removed the home icon.
5. Added log out button in the profile.


## Refactoring Changes

1. **Removed Unused Imports**:
   - Removed the unused import of `RotateCcw` to clean up the codebase and improve maintainability.

2. **Reduced Cognitive Complexity**:
   - Refactored the `spin` function by breaking it into smaller, reusable helper functions, making the logic easier to understand and test.

3. **Removed Useless Assignment**: 
   - Removed unused variables and assignments to streamline the code and enhance performance.
   - Eliminated the unnecessary assignment to the variable `setBet`, optimizing the code and reducing redundancy.

4. **Extracted Nested Ternary Operations**:
   - Simplified deeply nested ternary operations by breaking them into independent statements, improving readability and reducing potential errors.

5. **Added `PropTypes`**:
   - Implemented `prop-types` for all components to enforce type checking and improve code reliability.

6. **Associated Form Labels with Controls**:
   - Ensured that form labels are explicitly associated with their respective input controls using the `htmlFor` attribute, enhancing accessibility for assistive technologies.

7. **Improved Testing Practices**:
   - Utilized `@testing-library/react` and `vitest` for writing unit tests, ensuring robust test coverage for components like `SignUpIn` and `Profile`.
   - Mocked `axios` and `react-router-dom` to isolate component behavior during testing.

8. **Enhanced Error Handling**:
   - Improved error handling in the `SignUpIn` component by displaying user-friendly error messages using `react-toastify`.

9. **Used Modern Animations**:
   - Incorporated `framer-motion` for smooth animations in the `SignUpIn` component, enhancing the user experience.

10. **Environment Variable Management**:
   - Used `import.meta.env` to manage API URLs dynamically, ensuring flexibility across different environments.

11. **Improved State Management**:
    - Leveraged React's `useState` hook for managing form states and toggling between sign-up and sign-in modes.

12. **Optimized API Requests**:
    - Used `axios` for making API requests with proper headers and error handling, ensuring secure and efficient communication with the backend.

---

# Patch 1.0.1

## Bugfixes and Improvements
1. Fixed an issue in the Blackjack game where returning to the page and starting a new game would fetch the last game session instead of creating a new one.
   - Added cleanup function to reset game state when component unmounts
   - Modified the `fetchGameState` function to properly handle game state reset
   - Updated the `startGame` function to reset player and dealer hands, game result, and game state flags before starting a new game

2. Implemented proper balance fetching in the Dice game and enhanced the UI
   - Added balance fetching from user context or API if not available in context
   - Improved error handling for balance fetching with toast notifications
   - Enhanced dice rendering with SVG shapes for different dice types (d6, d8, d12)
   - Added tooltips with game instructions for better user experience

3. Fixed the issue with the games being accessible without logging in
   - Implemented route protection to ensure users are redirected to the login page if not authenticated
   - Added a context provider to manage user authentication state
   - Updated the routing logic to check for authentication before rendering game components