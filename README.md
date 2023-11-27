# AmigoSecreto

Projeto criado só para evitar permissões desnecessárias em aplicativos esquisitos no fim do ano.

## Preparando o ambiente

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
    pip install -r requeriments.txt
```

criarArquivo ```.env``` na raiz do projeto:
preencher as seguintes propriedades:

```ENV
    SECRET_KEY=''
    OUTLOOKSERVERSMTP=''
    OUTLOOKSERVERSMTPPORTA=
    OUTLOOKMAIL=''
    OUTLOOKPASS=''
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


