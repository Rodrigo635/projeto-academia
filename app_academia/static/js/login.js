// const email = document.getElementById('email');
// const password = document.getElementById('mainPassword');
// const confirmPassword = document.getElementById('confirmPassword');
// const loginEmail = document.getElementById('loginEmail');
// const errorMessage = document.getElementById('errorMessage');

// const btnCadastro = document.getElementById('btn-cadastro');
// const btnGoogle = document.getElementById('btn-google');
// const btnEntrar = document.getElementById('btn-entrar');

// const controlCadastrar = document.getElementById('auth-toggle-cadastrar');
// const controlEntrar = document.getElementById('auth-toggle-entrar');

// const invalidInput = 'invalid-input';

// let boolEmail = false,
//   boolPassword = false,
//   boolConfirmPassword = false;

// function togglePassword(inputId, iconId) {
//   const passwordInput = document.getElementById(inputId);
//   const eyeIcon = document.getElementById(iconId);
//   const iconPath = '../static/svgs/';
//   if (passwordInput.type === 'password') {
//     passwordInput.type = 'text';
//     eyeIcon.querySelector('img').src = `${iconPath}eye-slash-solid.svg`;
//   } else {
//     passwordInput.type = 'password';
//     eyeIcon.querySelector('img').src = `${iconPath}eye-solid.svg`;
//   }
// }

// function toggleEnter(inputId) {
//   if (inputId === 'form-cadastro') {
//     document.getElementById('form-login').style.display = 'none';
//     document.getElementById('form-cadastro').style.display = 'flex';
//     controlCadastrar.style.backgroundColor = 'var(--cor-bg)';
//     controlEntrar.style.backgroundColor = 'var(--cor-bgEscuro)';
//   } else {
//     document.getElementById('form-cadastro').style.display = 'none';
//     document.getElementById('form-login').style.display = 'flex';
//     controlEntrar.style.backgroundColor = 'var(--cor-bg)';
//     controlCadastrar.style.backgroundColor = 'var(--cor-bgEscuro)';
//   }
// }

// // Desabilita o botão de cadastro se algum campo estiver vazio
// function toggleCadastrar() {
//   console.log(boolEmail, boolPassword, boolConfirmPassword);
//   btnCadastro.disabled = !(boolEmail && boolPassword && boolConfirmPassword);
// }

// // Função comum para validar campos de input e desabilitar o botão de cadastro se algum campo estiver vazio
// function validarCampo(input, condition, boolVar) {
//   const isEmpty = input.value === '';
//   const isValid = !isEmpty && condition;

//   // Atualiza visual
//   input.classList.toggle(invalidInput, !isEmpty && !isValid);

//   // Atualiza variável booleana correspondente
//   switch (boolVar) {
//     case 'boolEmail':
//       boolEmail = isValid;
//       break;
//     case 'boolPassword':
//       boolPassword = isValid;
//       break;
//     case 'boolConfirmPassword':
//       boolConfirmPassword = isValid;
//       break;
//   }

//   toggleCadastrar();
//   return isValid;
// }

// // Funções de validação de Email
// function validarEmail(input, type) {
//   const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
//   validarCampo(input, regex.test(input.value), 'boolEmail');
// }

// // Funções de validação de Senha
// function validarPassword(input, type) {
//   const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
//   validarCampo(input, regex.test(input.value), 'boolPassword');
//   if (type === 'blur' && !boolPassword) {
//     errorMessage.innerText = "Senha deve conter pelo menos 8 caracteres, uma letra maiúscula, uma letra minúscula, um número e um caractere especial.";
//   } else {
//     errorMessage.innerText = '';
//   }
//   validarConfirmPassword();
// }

// // Funções de validação de Confirmar Senha
// function validarConfirmPassword() {
//   const saoIguais = password.value === confirmPassword.value;
//   const estaVazio = confirmPassword.value === '';

//   confirmPassword.classList.toggle(invalidInput, !estaVazio && !saoIguais);
//   boolConfirmPassword = saoIguais;
//   toggleCadastrar();
// }

// // Funções para iniciar a validação
// function setupValidation(input, validationFn) {
//   input.addEventListener('input', () => validationFn(input), 'input');
//   input.addEventListener('blur', () => validationFn(input, 'blur'));
// }

// // Função para inicializar as validações quando a pagina carregar
// function inicializarValidacoes() {
//   setupValidation(email, validarEmail);
//   setupValidation(password, validarPassword);

//   confirmPassword.addEventListener('input', validarConfirmPassword);
//   confirmPassword.addEventListener('blur', validarConfirmPassword);

//   [email, password, confirmPassword].forEach(input => {
//     if (input.value) {
//       if (input === confirmPassword) {
//         validarConfirmPassword();
//       } else if (input === email) {
//         validarEmail(input);
//       } else if (input === password) {
//         validarPassword(input);
//       }
//     }
//   });
//   toggleCadastrar();
// }

// document.addEventListener('DOMContentLoaded', inicializarValidacoes);

