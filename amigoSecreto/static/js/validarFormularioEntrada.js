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


function validarNomeUsuario(input) {
  // Obtenha o valor do campo
  var valor = input.value;

  // Use uma expressão regular para verificar se o valor contém apenas letras, números e traços
  var regex = /^[a-zA-Z0-9-]+$/;

  // Verifique se o valor atende à expressão regular
  if (!regex.test(valor)) {
    // Se não atender, remova os caracteres inválidos
    input.value = valor.replace(/[^a-zA-Z0-9-]/g, '');
  }
}


