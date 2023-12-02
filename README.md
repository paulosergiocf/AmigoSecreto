# AmigoSecreto

Projeto criado só para evitar permissões desnecessárias em aplicativos esquisitos no fim do ano.

[![Deploy on Railway](https://railway.app/button.svg)](https://amigosecreto-production.up.railway.app/)

## Preparando o ambiente

[![Python 3.11.5](https://img.shields.io/badge/python-3.11.5-red.svg)](https://www.python.org/downloads/release/python-360/)

Para utilizar o projeto crie um ambiente virtual.

```sh
    python -m venv .venv
```

Em seguida ative o ambiente em sua maquina.
```sh
    source .venv/bin/activate
```
Agora instale os dependencias nescessárias:

```sh
    pip install -r requeriments
```

criarArquivo ```.env``` na raiz do projeto:
preencher as seguintes propriedades:

```ENV
    SECRET_KEY=''
    OUTLOOKSERVERSMTP=''
    OUTLOOKSERVERSMTPPORTA=
    OUTLOOKMAIL=''
    OUTLOOKPASS=''
    PGDATABASE=''
    PGUSER=''
    PGPASSWORD=''
    PGHOST=''
    PGPORT=
```

## configurando o django

Faça o migração do banco de dados.
```sh
    python manage.py makemigrations
    python manage.py migration
```
Em seguida defina uma senha de superusuario.

```sh
    python manage.py createsuperuser
```

Agora para iniciar a aplicação utilize o comando.

```sh
    python manage.py runserver
```
> se tiver problemas com os arquivos estaticos rode da seguinte forma: foi nescessário ajustar o settings para ler os arquivos estaticos no servidor usando o gunucorn
```sh
    python manage.py migrate && python manage.py collectstatic --noinput && gunicorn setup.wsgi
```

```sh

    gunicorn setup.wsgi:application --log-file=- --log-level=debug


```

## Todo

lista de implementações que ainda precisam ser feitas.

- [ ] criar script para rodar de maneira agendada, com frequencia de 5 vezes ao dia, lendo todos os parametros agendados, se faltar menos de 5 horas para o sorteio então bloquear a participação de usuarios na sala.
- [ ] metodo para sortear de maneira agendada com base no parametro estabelecido.
- [ ] permitir que qualquer pessoa possa criar e gerenciar uma sala.



