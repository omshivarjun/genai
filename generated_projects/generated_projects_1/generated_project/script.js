document.addEventListener('DOMContentLoaded', () => {
  const currentInput = document.getElementById('currentInput');
  const historyDisplay = document.getElementById('history');
  const buttons = document.querySelector('.buttons');

  let currentExpression = '';
  let history = [];

  function add(a, b) {
    return a + b;
  }

  function subtract(a, b) {
    return a - b;
  }

  function multiply(a, b) {
    return a * b;
  }

  function divide(a, b) {
    if (b === 0) {
      return 'Error: Division by zero';
    }
    return a / b;
  }

  function clear() {
    currentExpression = '';
    updateDisplay();
  }

  function allClear() {
    currentExpression = '';
    history = [];
    updateDisplay();
  }

  function calculate() {
    try {
      currentExpression = currentExpression.replace(/\s+/g, '');

      const tokens = tokenize(currentExpression);
      const result = evaluate(tokens);

      if (isNaN(result) || !isFinite(result)) {
        throw new Error('Invalid result');
      }

      history.unshift(`${currentExpression} = ${result}`);
      if (history.length > 3) {
        history.pop();
      }
      currentExpression = result.toString();
      updateDisplay();
    } catch (error) {
      currentExpression = error.message;
      updateDisplay();
    }
  }

  function tokenize(expression) {
    const tokens = [];
    let number = '';
    for (const char of expression) {
      if (/[0-9.]/.test(char)) {
        number += char;
      } else if (/[+\-*/]/.test(char)) {
        if (number !== '') {
          tokens.push(number);
          number = '';
        }
        tokens.push(char);
      } else {
        throw new Error('Invalid character: ' + char);
      }
    }
    if (number !== '') {
      tokens.push(number);
    }
    return tokens;
  }

  function evaluate(tokens) {
    const precedence = {
      '*': 2,
      '/': 2,
      '+': 1,
      '-': 1,
    };

    function applyOp(op, b, a) {
      a = parseFloat(a);
      b = parseFloat(b);
      switch (op) {
        case '+':
          return add(a, b);
        case '-':
          return subtract(a, b);
        case '*':
          return multiply(a, b);
        case '/':
          if (b === 0) throw new Error('Division by zero');
          return divide(a, b);
      }
    }

    const values = [];
    const ops = [];

    for (const token of tokens) {
      if (!isNaN(parseFloat(token)) && isFinite(token)) {
        values.push(token);
      } else if (precedence[token]) {
        while (
          ops.length > 0 &&
          precedence[token] <= precedence[ops[ops.length - 1]]
        ) {
          const op = ops.pop();
          const val2 = values.pop();
          const val1 = values.pop();
          values.push(applyOp(op, val2, val1));
        }
        ops.push(token);
      } else {
        throw new Error('Invalid token: ' + token);
      }
    }

    while (ops.length > 0) {
      const op = ops.pop();
      const val2 = values.pop();
      const val1 = values.pop();
      values.push(applyOp(op, val2, val1));
    }

    return parseFloat(values[0]);
  }

  function handleNumberInput(number) {
    currentExpression += number;
    updateDisplay();
  }

  function handleOperatorInput(operator) {
    if (currentExpression === '' && operator === '-') {
      currentExpression += operator;
    } else if (currentExpression !== '') {
      if (!/[+\-*/.]$/.test(currentExpression)) {
        currentExpression += operator;
      }
    }
    updateDisplay();
  }

  function handleDecimalInput() {
    if (!currentExpression.includes('.')) {
      currentExpression += '.';
      updateDisplay();
    }
  }

  function handleBackspace() {
    currentExpression = currentExpression.slice(0, -1);
    updateDisplay();
  }

  function updateDisplay() {
    currentInput.textContent = currentExpression || '0';
    historyDisplay.textContent = history.join('\n');
  }

  buttons.addEventListener('click', (event) => {
    const target = event.target;
    if (target.matches('button')) {
      const value = target.value;
      const action = target.dataset.action;

      if (!action) {
        handleNumberInput(value);
      } else if (action === 'operator') {
        handleOperatorInput(value);
      } else if (action === 'decimal') {
        handleDecimalInput();
      } else if (action === 'clear') {
        clear();
      } else if (action === 'all-clear') {
        allClear();
      } else if (action === 'calculate') {
        calculate();
      } else if (action === 'backspace') {
        handleBackspace();
      }
    }
  });

  document.addEventListener('keydown', (event) => {
    const key = event.key;
    if (/[0-9]/.test(key)) {
      handleNumberInput(key);
    } else if (/[+\-*/]/.test(key)) {
      handleOperatorInput(key);
    } else if (key === '.') {
      handleDecimalInput();
    } else if (key === 'Enter') {
      calculate();
    } else if (key === 'Backspace') {
      handleBackspace();
    } else if (key === 'Escape') {
      clear();
    }
  });

  updateDisplay();
});
