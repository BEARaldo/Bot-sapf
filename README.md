# Bot para Sistema SAPF

Projeto de automação de cadastro de cidadãos no sistema de apoio a partidos em formação, utilizando o CPF como dado básico.

## Características

- Utiliza endpoints privados para automatizar o processo de busca e tratamento de dados.
- Produz fichas pré-preenchidas de maneira personalizada.

## Módulos

Os módulos até o momento são:

- `cpfAPI_connect.py`: Conecta com a API de dados do cidadão para capturar informações baseadas no CPF.
- `sapf_connect.py`: Gerencia sessões e interações com o sistema SAPF.
- `main.py`: Script principal que executa a aplicação.
- `manage.py`: Script de linha de comando para o projeto Django.

## Contribuição

A colaboração entre as equipes de back-end e front-end é crucial. O projeto visa a integração completa entre as duas áreas. Lembrem-se de adicionar as dependências dos seus projetos nos arquivos `requirements.txt` nas suas branches de desenvolvimento.

Para gerar o `requirements.txt`:

```bash
pip freeze > requirements.txt
