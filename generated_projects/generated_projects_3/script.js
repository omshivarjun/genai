let displayValue = '';
let currentInput = '';
let currentOperator = '';
let result = null;

function updateDisplay() {
    document.getElementById('display').value = displayValue;
}

function appendNumber(number) {
    currentInput += number;
    displayValue += number;
    updateDisplay();
}

function appendOperator(operator) {
    if (currentInput === '' && result === null) return;

    if (currentInput !== '') {
        calculate();
    }

    currentOperator = operator;
    displayValue += operator;
    currentInput = '';
    updateDisplay();
}

function calculate() {
    if (currentInput === '') return;

    let num1 = result === null ? parseFloat(displayValue) : result;
    let num2 = parseFloat(currentInput);

    switch (currentOperator) {
        case '+':
            result = add(num1, num2);
            break;
        case '-':
            result = subtract(num1, num2);
            break;
        case '*' :
            result = multiply(num1, num2);
            break;
        case '/':
            if (num2 === 0) {
                alert("Division by zero is not allowed!");
                clearDisplay();
                return;
            }
            result = divide(num1, num2);
            break;
        default:
            result = num2;
    }

    displayValue = result.toString();
    currentInput = '';
    currentOperator = '';
    updateDisplay();
}

function clearDisplay() {
    displayValue = '';
    currentInput = '';
    currentOperator = '';
    result = null;
    updateDisplay();
}

function add(x, y) {
    return x + y;
}

function subtract(x, y) {
    return x - y;
}

function multiply(x, y) {
    return x * y;
}

function divide(x, y) {
    if (y === 0) {
        alert("Division by zero is not allowed!");
        clearDisplay();
        return NaN; 
    }
    return x / y;
}


document.querySelectorAll('.number').forEach(button => {
    button.addEventListener('click', () => {
        appendNumber(button.textContent);
    });
});

document.querySelectorAll('.operator').forEach(button => {
    button.addEventListener('click', () => {
        appendOperator(button.textContent);
    });
});

document.getElementById('equals').addEventListener('click', () => {
    calculate();
});

document.getElementById('clear').addEventListener('click', () => {
    clearDisplay();
});

document.addEventListener('keydown', function(event) {
    const key = event.key;
    if (/[0-9]/.test(key)) {
        appendNumber(key);
    } else if (['+', '-', '*', '/'].includes(key)) {
        appendOperator(key);
    } else if (key === '=' || key === 'Enter') {
        calculate();
    } else if (key === 'Escape' || key === 'c' || key === 'C') {
        clearDisplay();
    }
});