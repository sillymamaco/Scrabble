# FP2526P2 - ist1117890

Este repositório deverá conter a solução do seu projecto de FP. 
A solução deve estar toda ela num único *script* ou programa Python: `FP2526P2.py`. 
O repositório não deve conter mais nenhum outro programa Python (ficheiro `.py`) ou ficheiro. 

## O que devem fazer?
- Fazer **clone** do repositório remoto para o seu computador habitual de trabalho:
    - Antes de poder clonar o repositório, precisa acrescentar uma chave SSH no seu [perfil de utilizador do GitLab](https://gitlab.rnl.tecnico.ulisboa.pt/-/profile/keys). 
    - Também precisa instalar o cliente Git na sua máquina de trabalho.
    - Pode encontrar instruções para gerar um par de chaves SSH [aqui](https://docs.gitlab.com/ee/user/ssh.html#generate-an-ssh-key-pair), para instalação do Git [aqui](https://git-scm.com/downloads) ou na [página da disciplina](https://fenix.tecnico.ulisboa.pt/disciplinas/FProg3112/2025-2026/1-semestre/ambiente-de-desenvolvimento).
- Trabalhar normalmente na sua solução.
- Podem fazer commit das suas alterações para atualizar o repositório local tantas vezes como desejem.
- Submeter os seu projecto no repositório remoto (atenção ao limite de submissões sem desconto).
- (opcional) Se trabalham em mais de um computador, devem de sincronizar com o repositório remoto fazendo um **pull** antes de começar a trabalhar.

## Como fazer uma submissão?
- Para submeter o projeto é preciso fazer um **push** do conteúdo do repositório local para o repositório remoto.
- A cada submissão (ou push) é desencadeiado o processo de avaliação automática do projeto. 
- Os resultados dos testes automáticos (públicos e privados) são enviados por e-mail e podem ser consultados em 
[http://fp.rnl.tecnico.ulisboa.pt/fp/fp25p2/reports/ist1117890/](http://fp.rnl.tecnico.ulisboa.pt/fp/fp25p2/reports/ist1117890/)


## O que **NÃO** devem fazer
- Acrescentar ficheiros, apagar ficheiros, *forks*, novas *branches*, ou qualquer outra operação que altere a estrutura do repositório.

## Qual é a forma mais simples (recomendada) de fazer tudo o anterior?
- Instalar o cliente Git e o Visual Studio Code no seu computador. 
- Ir a "Project Overview" do seu repositório de projeto no GitLab e escolher "Clone" > "Visual Studio Code (SSH)". Isto lançará o VS code. 
- Escolher a pasta onde queremos manter a cópia local do projeto e o VS Code realizará o **clone** nesta pasta.
- Configurar o nome e o e-mail com os que ficarão registradas as alterações no Git. Execute os seguintes comandos num Terminal:
    - `git config --global user.name "John Doe"`: configura o  nome que aparecerá no registro de alterações, quando as realize.
    - `git config --global user.email johndoe@example.com:` configura o email que aparecerá no registro de alterações, quando as realize.
- Trabalhar localmente no projeto utilizando o editor do VS Code. O VS Code nos facilita realizar commits (isto é, atualizações da cópia local do repositório) e pushes (isto é, atualizações do repositório remoto) através do IDE, sem necessidade de comandos no terminal. 

## Qual é a forma ainda mais simples (não recomendada) de fazer tudo o anterior?
- A interface web do GitLab incorpora um IDE Web. Assim que é possível:
    - Abrir no browser o ficheiro com a solução do projeto.
    - Selecionar a opção Edit > Open in Web IDE. Isto lançará um IDE muito parecido com o VS code no nosso browser.
    - Realizar as alterações do nosso projeto neste editor web e fazer commit das alterações antes de fechar/sair.
- ATENÇÃO: Como estarão a trabalhar diretamente  no repositório remoto, sempre que façam um commit (registro de alterações), estarão a realizar uma submissão do projeto.

## Contatos:

LEIC-A/LEGM: [fp-alameda@tecnico.ulisboa.pt](mailto:fp-alameda@tecnico.ulisboa.pt) 

LEIC-T/LETI: [fp-tagus@tecnico.ulisboa.pt](mailto:fp-tagus@tecnico.ulisboa.pt)
