# Patch 1.0.0

## Bugfixes and Improvements
1. Added favicon and changed the title of the page.
2. Fixed the issue when logging in with a new user, the page was not redirecting to the home page.
3. Redesigned the profile page.
4. Centered the icon in the nav, remove the home icon.
5. Added log out button in the profile.
6. Removed the ability to bet in the Dice Game, since the value is preset.


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