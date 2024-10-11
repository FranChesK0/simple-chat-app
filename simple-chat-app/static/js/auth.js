const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
})

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
})

const validateForm = fields => fields.every(field => field.trim() !== '');

const sendRequest = async (url, data) => {
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            alert(result.message || 'Operation successful');
            return result;
        } else {
            alert(result.message || 'Request error');
            return null;
        }
    } catch (error) {
        console.error("Error:", error);
        alert('Internal server error');
    }
};

const handleFormSubmit = async (formType, url, fields) => {
    if (!validateForm(fields)) {
        alert("Please, enter all fields");
        return;
    }

    const data = await sendRequest(url, formType === 'login'
        ? {email: fields[0], password: fields[1]}
        : {email: fields[0], name: fields[1], password: fields[2], password_check: fields[3]}
    );
    if (data && formType === 'login') {
        window.location.href = '/chat';
    }
};

document.getElementById('login-button').addEventListener('click', async (event) => {
    event.preventDefault();

    const email = document.querySelector('#login-form input[type="email"').value;
    const password = document.querySelector('#login-form input[type="password"').value;

    await handleFormSubmit('login', 'login/', [email, password]);
});

document.getElementById('register-button').addEventListener('click', async (event) => {
    event.preventDefault();

    const email = document.querySelector('#register-form input[type="email"]').value;
    const name = document.querySelector('#register-form input[type="text"]').value;
    const password = document.querySelectorAll('#register-form input[type="password"]')[0].value;
    const password_check = document.querySelectorAll('#register-form input[type="password"]')[1].value;

    if (password !== password_check) {
        alert('Passwords mismatched');
        return;
    }

    await handleFormSubmit('register', 'register/', [email, name, password, password_check]);
});
