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

## Refactoring Techniques Used

### 1. **Extract Method**: Moved duplicate or complex inline logic into a separate, named function to improve code readability, reusability, and maintainability.

Before:

```javascript
{diceType1 === 'd6' ? diceD6(diceValue1) : diceType1 === 'd8' ? diceD8(diceValue1) : diceD12(diceValue1)}
...
{diceType2 === 'd6' ? diceD6(6) : diceType2 === 'd8' ? diceD8(8) : diceD12(12)}

```
After:
```javascript
{getDiceComponent(diceType1, diceValue1)}
...
{getInitDiceComponent(diceType2)}
```
Functions Extracted:
```javascript
const getDiceComponent = (diceType, diceValue) => {
    switch (diceType) {
        case 'd6': return diceD6(diceValue);
        case 'd8': return diceD8(diceValue);
        case 'd12': return diceD12(diceValue);
    default: return null;
}
};

const getInitDiceComponent = (diceType) => {
    switch (diceType) {
      case 'd6': return diceD6(6);
      case 'd8': return diceD8(8);
      case 'd12': return diceD12(12);
    default: return null;
}
};
```
### 2. **Replace Magic Number with Symbolic Constant**: replaced hard-coded values with named constants to improve code clarity and maintainability.

Before:
```javascript
const generateReels = () => {
    return Array(5).fill().map(() =>
        Array(3).fill().map(() => SYMBOLS[getRandomReels(SYMBOLS.length)])
    );
}
```
After:
```javascript
const NUM_COLUMNS = 5;
const NUM_ROWS = 3;

const generateReels = () => {
    return Array(NUM_COLUMNS).fill().map(() =>
        Array(NUM_COLUMNS).fill().map(() => SYMBOLS[getRandomReels(SYMBOLS.length)])
    );
}
```
### 3. **Encapsulate Collection**: access collection logic through functions/methods.

Before: 
```javascript
setReels(Array(5).fill().map(() => Array(3).fill().map(() => SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)])));
```
After:
```javascript
export const getRandomReels = (max) => {
    const array = new Uint32Array(1);
    window.crypto.getRandomValues(array);
    return array[0] % max;
};

setReels(generateReels());
```

### 4. **Extract Class**: encapsulate deck logic in a dedicated class.

Before:
```javascript
function createDeck() {
    return suitsArray.flatMap(suit => values.map(({ name, value }) => ({ suit, name, value })));
}

function shuffleDeck(deck) {
    const array = [...deck];
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(window.crypto.getRandomValues(new Uint32Array(1))[0] / (0xFFFFFFFF + 1) * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function drawCard() {
    if (deck.length === 0) setDeck(shuffleDeck(createDeck()));
    return deck.pop();
}
```

After (gameApi.jsx):
```javascript
export class Deck {
    constructor() {
        this.reset();
    }

    reset() {
        this.cards = suitsArray.flatMap(suit =>
            values.map(({ name, value }) => ({ suit, name, value }))
        );
        this.shuffle();
    }

    shuffle() {
        for (let i = this.cards.length - 1; i > 0; i--) {
            const j = Math.floor(
                window.crypto.getRandomValues(new Uint32Array(1))[0] /
                (0xFFFFFFFF + 1) * (i + 1)
            );
            [this.cards[i], this.cards[j]] = [this.cards[j], this.cards[i]];
        }
    }

    drawCard() {
        if (this.cards.length === 0) {
            this.reset();
        }
        return this.cards.pop();
    }

    getCount() {
        return this.cards.length;
    }

```

Usage in component:
```javascript
const [deck, setDeck] = useState(new Deck());
...
const card = deck.draw();
```

### 5. **Remove Dead Code**: eliminate redundant or unused code.

Removed Code:
```javascript
{error && <div className="text-red-500">{error}</div>}
```
Since I am displaying error messages using `react-toastify`, this line was unnecessary and cluttered the UI.

### 6. **Replace Temp with Query**: remove intermediate variables and directly query calculations when needed.
   
Before:
```javascript
const playerValue = calculateHandValue(playerHand);
...
if (playerValue > 21) {
    ...
}
```
After:
```javascript
if (calculateHandValue(playerHand) > 21) {
...
}
```
### 7. **Rename Variable**: improved variable names for clarity and understanding.

Before:
```javascript
const res = await fetchUser();
const data = await res.json();
```
After:
```javascript
const response = await fetchUser();
const updatedUser = await response.json();
```
### 8. **Separate Query from Modifier**: separate data retrieval and modification logic for better clarity and maintainability.

Before:
```javascript
const handleEdit = async (e) => {
   e.preventDefault();

   try {
      const response = await fetch(`${apiUrl}/user/update/`, {
         method: 'PUT',
         headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
         },
         body: JSON.stringify(user)
      });

      if (!response.ok) throw new Error('Failed to update user profile');

      const updatedUser = await response.json();
      setUser(updatedUser);
      setIsEditing(false);
   } catch (err) {
      console.log(err.message);
   }
}
```
### 9. **Consolidate Conditional Expressions**: simplified complex conditional expressions for better readability and maintainability.

Before:
```javascript
{isSignUp && (
    <>
       <label htmlFor="confirmPassword" className="text-sm my-3">Confirm Password:</label>        
       <input
               id="confirmPassword" 
               name="confirmPassword"
               type="password"
               required
               value={confirmPassword}
               onChange={(e) => setConfirmPassword(e.target.value)}
               className="w-full bg-gray-700 rounded p-2 text-white"
               data-testid="confirm-password-input"
       />
       </>
   )}
```
After:
```javascript
const ConfirmPasswordField = () => (
    <>
        <label htmlFor="confirmPassword" className="text-sm my-3">Confirm Password:</label>
        <input
            id="confirmPassword"
            name="confirmPassword"
            type="password"
            required
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="w-full bg-gray-700 rounded p-2 text-white"
            data-testid="confirm-password-input"
        />
    </>
);

{isSignUp && <ConfirmPasswordField />}
```
### 10. **Replace Conditional with Polymorphism**: used polymorphism to render dice.

Before:
```javascript
const diceSVG = (diceValue, points) => (
  <svg width="75" height="75" viewBox="0 0 100 100">
    <polygon points={points} fill="#fcc800" />
    <text x="50" y="60" textAnchor="middle" fill="black" fontSize="36">
      {diceValue}
    </text>
  </svg>
);

const diceD6  = (v) => diceSVG(v, "10,10 90,10 90,90 10,90");
const diceD8  = (v) => diceSVG(v, "50,10 90,50 50,90 10,50");
const diceD12 = (v) => diceSVG(v, "50,10 90,30 90,70 50,90 10,70 10,30");

<motion.div
  variants={diceVariants}
  initial="initial"
  animate={rolling ? "animate" : "initial"}
>
{diceType1 === 'd6' ? diceD6(diceValue1) : diceType1 === 'd8' ? diceD8(diceValue1) : diceD12(diceValue1)}
</motion.div>
<motion.div
  variants={diceVariants}
  initial="initial"
  animate={rolling ? "animate" : "initial"}
>
{diceType2 === 'd6' ? diceD6(diceValue2) : diceType2 === 'd8' ? diceD8(diceValue2) : diceD12(diceValue2)}
</motion.div>
```

After:
```javascript
const DICE_SHAPES = {
  d6:  "10,10 90,10 90,90 10,90",
  d8:  "50,10 90,50 50,90 10,50",
  d12: "50,10 90,30 90,70 50,90 10,70 10,30",
};

const renderDice = (type, value) => {
  const points = DICE_SHAPES[type] || DICE_SHAPES.d6;
  return (
      <svg width="75" height="75" viewBox="0 0 100 100">
          <polygon points={points} fill="#fcc800" />
          <text
              x="50"
              y="60"
              textAnchor="middle"
              fill="black"
              fontSize="36"
          >
              {value}
          </text>
      </svg>
  );
};
    
<motion.div
   variants={diceVariants}
   initial="initial"
   animate={rolling ? "animate" : "initial"}
>
   {renderDice(diceType1, diceValue1)}
</motion.div>
<motion.div
   variants={diceVariants}
   initial="initial"
   animate={rolling ? "animate" : "initial"}
>
   {renderDice(diceType2, diceValue2)}
</motion.div>
```

---

## Sonarqube Report

| Category              | Metric                 | Value              | Rating | Notes                                                |
|-----------------------|------------------------|--------------------|--------|------------------------------------------------------|
| **Security**          | Open issues            | 0                  | A      | No issues above info severity impacting security     |
| **Reliability**       | Open issues            | 7                  | C      | At least one issue with medium impact on reliability |
| **Coverage**          | Lines covered          | 85.0% of 837 lines | —      |                                                      |
| **Duplications**      | Code duplication       | 2.6% on 1.2k lines | —      |                                                      |
| **Security Hotspots** | Issues needing review  | 0                  | A      | 100% of Security Hotspots reviewed                   |
