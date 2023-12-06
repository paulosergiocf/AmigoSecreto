import smtplib
import unittest
from unittest.mock import patch
from amigoSecreto.usecases.enviar_email import ServidorEmail, Email

class TestServidorEmail(unittest.TestCase):

    @patch('smtplib.SMTP')
    def test_enviar_email_com_sucesso(self, mock_smtp):
        servidor_email = ServidorEmail()
        email = Email(destinatario='destinatario@example.com', corpo='Corpo do email', assunto='Assunto do email')

        servidor_email.enviarEmail(email)

        mock_smtp.return_value.starttls.assert_called_once()
        mock_smtp.return_value.login.assert_called_once_with(servidor_email._ServidorEmail__remetente, servidor_email._ServidorEmail__pass)
        mock_smtp.return_value.sendmail.assert_called_once_with(servidor_email._ServidorEmail__remetente,
                                                                email.destinatario,
                                                                servidor_email.formatarEmail(email).as_string())
        mock_smtp.return_value.quit.assert_called_once()

    @patch('smtplib.SMTP')
    def test_enviar_email_com_falha_autenticacao(self, mock_smtp):
        mock_smtp.return_value.login.side_effect = smtplib.SMTPAuthenticationError(535, 'Authentication failed')

        servidor_email = ServidorEmail()
        email = Email(destinatario='destinatario@example.com', corpo='Corpo do email', assunto='Assunto do email')

        with self.assertRaises(smtplib.SMTPAuthenticationError):
            servidor_email.enviarEmail(email)


if __name__ == '__main__':
    unittest.main()

