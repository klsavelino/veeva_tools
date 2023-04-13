# veeva_tools (srv)

  

Este módulo é especificamente projetado para web scraping de dados do site Veeva. Ele foi criado a fim de automatizar uma série de tarefas manuais e trabalhosas e, até o momento, pode somente baixar _reports_. O projeto está aberto para sugestões de funcionalidades.

  
  

## Classe: `Session`

  

Esta classe é usada para criar uma sessão do Veeva para coletar dados do site. É necessário fornecer as informações de login e outras configurações para criar uma sessão.

  

Session(**kr_usr**: str, _[**kr_addr**: str]_, _[**driver_path**: str]_, _[**download_path**: str]_)

  

#### Parâmetros de inicialização

  

-  **kr_usr**: Se trata do nome do usuário armazenado no Keyring.

-  **kr_addr**  _(opcional)_: Se trata do endereço das credenciais no Keyring. Por padrão, é definido como "https://login.salesforce.com/".

-  **driver_path**  _(opcional)_: O caminho onde o ==chromedriver.exe== está localizado. Por padrão, é definido como "P:\ChromeDriver\chromedriver.exe".

-  **download_path**  _(opcional)_: O caminho onde o relatório deve ser baixado. Por padrão, é definido como “C:\Users\\<USER\>\AppData\Local\Temp\TEMPDIR”

  

#### Exemplo de uso

##### Uso comum

```

veeva_tools.Session(kr_usr = "usuario@email.com", kr_addr = "Usuário Veeva 1", driver_path = "C:\ChromeDriver\chromedriver.exe", download_path = "C:\Users\<Usuário>\Documentos\Projeto1")

```

##### Uso direto

Veja mais sobre o [uso direto](##Uso-direto)

```

veeva_tools -u "usuario@email.com" -a "Usuário Veeva 1" -c "C:\ChromeDriver\chromedriver.exe" -d "C:\Users\<Usuário>\Documentos\Projeto1")

```

  

### Método: `get_report`

  

Este método é usado para baixar um relatório específico da plataforma. Ele baixa o relatório diretamente para o caminho de download especificado durante a inicialização da sessão. O usuário precisa possuir uma sessão (`Session`) ativa para acessar a página de download do relatório.

  

Session(...).get_report(**report**: str)

  

#### Parâmetros

-  **report**: Nome exato do _report_ a ser baixado.

  

#### Parâmetros diretos

Para mais informações veja Uso Direto.

  

Após os argumentos da inicialização da classe:

-  `get_report`: Especifica a ferramenta que será utilizada, no caso, a ferramenta `get_report`.

-  `-r` ou `--report`: **report**

  

#### Retorno

Este método retorna o caminho absoluto do _report_ baixado.

  

#### Exemplo de uso

##### Uso comum:

```

veeva_tools.Session(...).get_report("Report1")

```

##### Uso direto

Veja mais sobre o [uso direto](README.md##Uso-direto)

```

veeva_tools ... get_report -r Report1

```

  

## Uso direto

  

É possível utilizar o módulo diretamente da linha de comando conforme o seguinte:

  

**cmd.exe**


```veeva_tools <script.py> -u [-a ou --kr_addr] [-c ou --driver_path] [-d ou --download_path]```

  

Substitua o <script.py>  pelo  script  cli.py  no  caminho ...\veeva_tools\tools\cli.py.

  

-  `-u` ou `--kr_usr`: **kr_usr**

-  `-a` ou `--kr_addr`  _(opcional)_: **kr_addr**

-  `-c` ou `--driver_path` _(opcional)_: **driver_path**

-  `-d` ou `--download_path`  _(opcional)_: **download_path**