# Execução
Para iniciar o projeto execute o seguinte comando no diretório raiz do projeto:
```sh
python server.py
```

O servidor irá subir na porta 8081.

Para testar faça um arequisição POST utilizando o Postman no endpoint `/client/dialog` com o a estrutura abaixo no body alterando os parâmetros conforme necessidade:

```json
{ "request": {"session": "sess00", "transcription":"ola", "confidence":0.7 } }
```

# Ambiente

## Dependências
- Python
- git
- pip
    - pip install --upgrade "watson-developer-cloud>=1.5.0"
    - pip install flask

## Cloud

## Desenho de arquitetura
![AWS CloudFormation](https://innersource.accenture.com//projects/PAV-OI/repos/pav-oi/raw/resource/img/pavoi.png)

 
O projeto está hospedado em um servidor AWS.

- **Host:** *54.153.32.247*
- **Usuário:** *ec2-user*
- **Diretório raiz:** *~/pav-oi/*

As chaves para conexão ssh com o servidor estão disponíveis no Teams. Crie um diretório *settings/keys/* e baixe as chaves para dentro dele, o git está configurado para não sincronizar esse diretório

No Windows pode ser utilizado o Putty para fazer a conexão, a chave no formato reconhecido pelo Putty é *pa-virtual-oi.ppk*.

Também está no diretório a chave *pa-virtual-oi.pem* para sistemas base UNIX, a conexão nesse caso pode ser realizada com o comando:
```sh
ssh -i settings/keys/pa-virtual-oi.pem user@host
```
Substituindo *user* e *host* pelos dados fornecidos anteriormente.

## Local - Dev
Para criar um ambiente localmente, primeiro deve-se instalar as dependências acima.

- Instale o SonarQube: https://docs.sonarqube.org/display/PLUG/SonarPython
- Dependências do Sonar para cobertura de testes:
    - pip install coverage
    - pip install nose
- Instale o Pylint:
    - pip install pylint

### Executando o SonarQube
- Execute o servidor do sonar: `<install-dir>/bin/macosx-universal-64/sonar.sh console`
- Execute no diretório do projeto: `sonar-scanner`
