function checkSenha(input) {
    var senha = document.getElementById('senha');
    var confirmarSenha = input;

    if (senha.value !== confirmarSenha.value) {
      input.setCustomValidity('As senhas não coincidem');
    } else {
      input.setCustomValidity('');
    }
  }

function validateEmail(input) {
    const email = input.value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(email)) {
      input.setCustomValidity('Digite um endereço de e-mail válido');
    } else {
      input.setCustomValidity('');
    }
  }