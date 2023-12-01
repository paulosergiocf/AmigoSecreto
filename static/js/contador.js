// contador.js

function formatarNumero(numero) {
    return numero < 10 ? '0' + numero : numero;
}

function obterDataFutura() {
    // Obter a data futura do elemento HTML com id="dataFutura"
    var elementoDataFutura = document.getElementById('dataFutura');
    var dataFuturaHTML = elementoDataFutura.innerText;
    document.getElementById('dataFuturaDefinida').innerHTML = dataFuturaHTML;
    // Certificar-se de que o elemento existe
    if (elementoDataFutura) {
        return new Date(elementoDataFutura.innerText + 'T23:59:59');
    } else {
        // Caso o elemento não exista ou não tenha um valor válido, use uma data padrão
        return new Date('2023-12-15T23:59:59');
    }

    
    
}

function atualizarContador() {
    // Obter a data futura
    var dataFutura = obterDataFutura();

    // Obter a data e hora atuais
    var agora = new Date();

    // Calcular a diferença em milissegundos entre a data futura e a data atual
    var diferenca = dataFutura - agora;

    // Calcular horas, minutos e segundos a partir da diferença
    var horas = Math.floor(diferenca / (1000 * 60 * 60));
    var minutos = Math.floor((diferenca % (1000 * 60 * 60)) / (1000 * 60));
    var segundos = Math.floor((diferenca % (1000 * 60)) / 1000);

    // Formatar os números
    horas = formatarNumero(horas);
    minutos = formatarNumero(minutos);
    segundos = formatarNumero(segundos);

    // Atualizar o contador no HTML
    var contadorHTML = horas + ':' + minutos + ':' + segundos;    
    document.getElementById('contador').innerHTML = contadorHTML;
   
}

// Atualizar o contador a cada segundo
setInterval(atualizarContador, 1000);

// Chamar a função pela primeira vez para evitar um atraso de 1 segundo
atualizarContador();
