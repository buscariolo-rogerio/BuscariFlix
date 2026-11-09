# Relatório - Pipeline CI/CD do BuscariFlix

## Projeto

- Repositório: https://github.com/buscariolo-rogerio/BuscariFlix
- Aplicação: catálogo web estático de filmes e séries
- Pipeline: `.github/workflows/ci-cd.yml`
- Estratégia de deployment: GitHub Pages

O GitHub Pages foi escolhido porque o BuscariFlix utiliza apenas HTML, CSS e JavaScript no navegador, sem backend ou banco de dados. Assim, o serviço é compatível com a tecnologia do projeto, fornece uma URL pública e permite publicação automática pelo GitHub Actions sem infraestrutura adicional.

## Prompts utilizados e evolução

### Prompt 1

**Prompt:** "Analise meu site BuscariFlix em HTML e CSS e crie uma pipeline de CI/CD no GitHub Actions. Ela deve rodar em push e pull request para a main e publicar no GitHub Pages somente depois que a validação passar."

**Resultado:** Foi sugerido separar a pipeline em dois jobs: `ci`, responsável por validar e montar o site, e `deploy`, dependente da CI.

**Problema encontrado:** O projeto não tinha testes nem processo de build, então não existia uma verificação real para executar na CI.

**Alteração realizada:** Foi criado um validador em Python, sem bibliotecas externas, para verificar os HTMLs, os textos alternativos e a existência de todos os arquivos locais referenciados.

### Prompt 2

**Prompt:** "Crie um teste simples em Python que encontre imagens, CSS, JavaScript e links locais quebrados nos meus arquivos HTML, sem instalar dependências."

**Resultado:** O script `tests/validate_site.py` passou a analisar todas as páginas com `html.parser` e retornar erro quando encontra um problema.

**Problema encontrado:** A página de San Andreas apontava para um caminho absoluto inexistente e as páginas de detalhes recarregavam automaticamente a cada dois segundos.

**Alteração realizada:** O caminho da imagem foi corrigido e as tags `meta refresh` foram removidas.

### Prompt 3

**Prompt:** "Deixe o BuscariFlix moderno, responsivo e com identidade visual em roxo escuro. Adicione hover elegante em todos os filmes e preserve os pôsteres existentes."

**Resultado:** Foi criada uma interface com fundo roxo quase preto, tipografia destacada, hero, grid responsivo, cards com brilho, zoom suave e botão revelado no hover.

**Problema encontrado:** O CSS anterior usava larguras fixas e o efeito hover existia apenas no pôster de Avatar, o que prejudicava telas menores e tornava o comportamento inconsistente.

**Alteração realizada:** O layout passou a usar CSS Grid, medidas fluidas, breakpoints para tablet/celular e o efeito foi aplicado à classe de todos os cards.

### Prompt 4

**Prompt:** "Faça a barra de pesquisa funcionar de verdade. Ela deve filtrar enquanto digito por nome ou ano, ignorar acentos e mostrar uma mensagem quando não houver resultados."

**Resultado:** Foi criado o `app.js`, que filtra os dez títulos em tempo real, atualiza a contagem de resultados, oculta seções vazias e oferece um botão para limpar a busca.

**Problema encontrado:** O formulário original não tinha ação, recarregava a página e não apresentava retorno ao usuário.

**Alteração realizada:** O envio padrão foi bloqueado e a busca foi implementada no navegador com JavaScript e região `aria-live` para acessibilidade.

### Prompt 5

**Prompt:** "Revise a pipeline para garantir que o deploy use exatamente os arquivos aprovados na CI e que nunca publique em pull requests."

**Resultado:** A CI passou a gerar um artefato chamado `site-build`. O job de deployment baixa esse mesmo artefato e só é executado quando o evento é um push na branch `main`.

**Problema encontrado:** Montar o site novamente no job de deploy poderia publicar arquivos diferentes dos testados.

**Alteração realizada:** O artefato validado foi compartilhado entre os jobs com `upload-artifact` e `download-artifact`, e o CD recebeu uma condição explícita de evento e branch.

### Prompt 6

**Prompt:** "Explique como validar e ativar o GitHub Pages para essa pipeline e quais evidências devo registrar para o relatório."

**Resultado:** Foram definidos os passos de configuração do Pages e as evidências necessárias: execução verde dos dois jobs, URL do ambiente `github-pages` e site publicado aberto no navegador.

**Problema encontrado:** A configuração inicial do repositório pode estar com Pages desativado ou usando publicação por branch.

**Alteração realizada:** A orientação final é selecionar **GitHub Actions** como fonte em **Settings > Pages** antes do primeiro deployment.

## Análise final do processo

Foram necessários **6 prompts** para chegar à versão final. Os principais problemas encontrados foram a ausência de uma validação automatizada, um caminho de imagem quebrado, recarregamentos automáticos, layout não responsivo, hover restrito a um único filme e barra de pesquisa sem comportamento.

As alterações manuais foram a revisão dos textos e títulos, a conferência visual dos pôsteres e o ajuste da seleção de filmes. A IA auxiliou na estrutura da pipeline, no código do validador, no JavaScript da pesquisa, no CSS responsivo e na identificação de riscos do deployment.

A pipeline foi verificada localmente executando `python tests/validate_site.py`. No GitHub, a comprovação final deve incluir uma execução bem-sucedida dos jobs **Validar e preparar site** e **Publicar no GitHub Pages**, seguida da abertura da URL informada pelo ambiente `github-pages`.

## Evidências a anexar ao PDF final

1. Captura da aba **Actions** com a execução do workflow em estado verde.
2. Captura dos detalhes do job de CI mostrando a etapa de validação concluída.
3. Captura dos detalhes do job de deploy mostrando a URL gerada.
4. Captura do BuscariFlix publicado no GitHub Pages.

Essas evidências somente existirão depois que os arquivos forem enviados para a branch `main` e o workflow terminar. Elas devem ser adicionadas antes de exportar este relatório para o PDF de entrega.
