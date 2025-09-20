// Password Toggle Functionality
function initializePasswordToggle() {
    const passwordFields = document.querySelectorAll('input[type="password"]');
    passwordFields.forEach(field => {
        const container = document.createElement('div');
        container.className = 'password-input-container';
        field.parentNode.insertBefore(container, field);
        container.appendChild(field);

        const toggleButton = document.createElement('button');
        toggleButton.type = 'button';
        toggleButton.className = 'password-toggle-btn';
        // Create eye icon safely using DOM methods
        const eyeIcon = document.createElement('i');
        eyeIcon.className = 'fas fa-eye';
        toggleButton.appendChild(eyeIcon);
        toggleButton.setAttribute('aria-label', 'Toggle password visibility');
        container.appendChild(toggleButton);

        toggleButton.addEventListener('click', function() {
            const type = field.getAttribute('type') === 'password' ? 'text' : 'password';
            field.setAttribute('type', type);
            this.querySelector('i').className = type === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash';
        });
    });
}

// Password Generation
function getRandomPassword() {
    fetch("/accounts/password-gen")
        .then(response => response.json())
        .then(data => {
            const passwordFields = document.getElementsByName("password1");
            const confirmPasswordFields = document.getElementsByName("password2");
            if (passwordFields.length > 0) {
                passwordFields[0].value = data.data;
                if (confirmPasswordFields.length > 0) {
                    confirmPasswordFields[0].value = data.data;
                }
            }
        });
}

// Email Validation
function validateEmail(emailField, emailErrorMessage, emailIcon) {
    const emailValue = emailField.value.trim();
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    if (emailPattern.test(emailValue)) {
        emailErrorMessage.textContent = "";
        emailField.classList.remove("is-invalid");
        emailField.classList.add("is-valid");
        emailIcon.classList.remove("fa-envelope");
        emailIcon.classList.add("fa-check-circle");
        emailIcon.style.color = "green";
    } else {
        emailErrorMessage.textContent = "Please enter a valid email address";
        emailField.classList.remove("is-valid");
        emailField.classList.add("is-invalid");
        emailIcon.classList.remove("fa-check-circle");
        emailIcon.classList.add("fa-envelope");
        emailIcon.style.color = "red";
    }
}

// Password Validation
function validatePassword(passwordField, confirmPasswordField, confirmIcon) {
    const passwordValue = passwordField.value;
    const confirmPasswordValue = confirmPasswordField.value;

    if (confirmPasswordValue === passwordValue) {
        confirmPasswordField.classList.remove("is-invalid");
        confirmPasswordField.classList.add("is-valid");
        confirmIcon.classList.remove("fa-unlock-alt");
        confirmIcon.classList.add("fa-check-circle");
        confirmIcon.style.color = "green";
        document.getElementById("confirm-password-error").textContent = "";
    } else {
        confirmPasswordField.classList.remove("is-valid");
        confirmPasswordField.classList.add("is-invalid");
        confirmIcon.classList.remove("fa-check-circle");
        confirmIcon.classList.add("fa-unlock-alt");
        confirmIcon.style.color = "red";
        document.getElementById("confirm-password-error").textContent = "Passwords do not match.";
    }
}

// Password Requirements Check
function checkPasswordRequirements(passwordValue) {
    const requirements = {
        length: passwordValue.length >= 8,
        lowercase: /[a-z]/.test(passwordValue),
        uppercase: /[A-Z]/.test(passwordValue),
        number: /\d/.test(passwordValue),
        symbol: /[@$!%*?&]/.test(passwordValue)
    };

    Object.keys(requirements).forEach(req => {
        const checkElement = document.getElementById(`${req}-check`);
        if (checkElement) {
            if (requirements[req]) {
                checkElement.classList.remove("text-danger");
                checkElement.classList.add("text-success");
                // Create elements safely
                checkElement.textContent = '';
                const checkIcon = document.createElement('i');
                checkIcon.className = 'fas fa-check';
                const reqText = document.createTextNode(' ' + getRequirementText(req));
                checkElement.appendChild(checkIcon);
                checkElement.appendChild(reqText);
            } else {
                checkElement.classList.remove("text-success");
                checkElement.classList.add("text-danger");
                // Create elements safely
                checkElement.textContent = '';
                const timesIcon = document.createElement('i');
                timesIcon.className = 'fas fa-times';
                const reqText = document.createTextNode(' ' + getRequirementText(req));
                checkElement.appendChild(timesIcon);
                checkElement.appendChild(reqText);
            }
        }
    });
}

function getRequirementText(req) {
    const texts = {
        length: "At least 8 characters",
        lowercase: "At least one lowercase letter",
        uppercase: "At least one uppercase letter",
        number: "At least one number",
        symbol: "At least one special symbol (@, $, !, %, *, ?, &)"
    };
    return texts[req];
}

// Initialize all authentication functionality
document.addEventListener("DOMContentLoaded", function() {
    initializePasswordToggle();

    // Email validation
    const emailField = document.getElementById("id_email");
    if (emailField) {
        const emailErrorMessage = document.getElementById("email-error");
        const emailIcon = document.querySelector("#basic-addon3 .fa-envelope");
        if (emailField && emailErrorMessage && emailIcon) {
            emailField.addEventListener("input", () => validateEmail(emailField, emailErrorMessage, emailIcon));
        }
    }

    // Password validation
    const passwordField = document.getElementById("id_password1");
    const confirmPasswordField = document.getElementById("id_password2");
    if (passwordField && confirmPasswordField) {
        const confirmIcon = document.querySelector("#confirm-addon .fa-unlock-alt");
        if (confirmIcon) {
            passwordField.addEventListener("input", () => {
                validatePassword(passwordField, confirmPasswordField, confirmIcon);
                checkPasswordRequirements(passwordField.value);
            });
            confirmPasswordField.addEventListener("input", () => validatePassword(passwordField, confirmPasswordField, confirmIcon));
        }
    }
}); 