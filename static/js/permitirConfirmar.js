function toggleSubmit() {
    // Obtém o estado do checkbox
    var checkbox = document.getElementById("exampleCheck1");
    // Obtém o botão de envio
    var submitButton = document.getElementById("submitButton");

    // Habilita ou desabilita o botão de envio com base no estado do checkbox
    submitButton.disabled = !checkbox.checked;
}