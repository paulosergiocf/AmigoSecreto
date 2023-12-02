import unittest
from unittest.mock import patch
from amigoSecreto.usecases.sortear import AmigoSecreto

class TestAmigoSecreto(unittest.TestCase):

    def test_sortear_com_sucesso(self):
        amigo_secreto = AmigoSecreto(max_tentativas=100)
        participantes = ["Alice", "Bob", "Charlie", "David"]

        with patch.object(amigo_secreto, "_AmigoSecreto__executar") as mock_executar:
            mock_executar.return_value = {"Alice": "Bob", "Bob": "Alice", "Charlie": "David", "David": "Charlie"}
            resultado = amigo_secreto.sortear(participantes)

        self.assertCountEqual(resultado.keys(), participantes)
        self.assertCountEqual(resultado.values(), participantes)
        self.assertNotEqual(resultado, {p: p for p in participantes})

    def test_sortear_com_excecao(self):
        amigo_secreto = AmigoSecreto(max_tentativas=0)  # Forçar exceção imediata
        participantes = ["Alice", "Bob"]

        with self.assertRaises(ValueError) as context:
            amigo_secreto.sortear(participantes)

        self.assertEqual(str(context.exception), 'deu ruim')

    # Adicione mais testes conforme necessário

if __name__ == '__main__':
    unittest.main()
