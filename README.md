# 🧠 .NET Easy Starter CLI

Um gerador universal de projetos **.NET**, feito para que você possa iniciar novos repositórios de forma **instantânea, padronizada e escalável** — com tudo configurado: arquitetura, ORM, banco de dados, Docker, CI/CD e estrutura de pastas.

-----

## 🚀 O que é?

O **.NET Easy Starter CLI** é uma ferramenta interativa em **Python**, compatível com **Windows, Linux e macOS**, que permite criar rapidamente qualquer tipo de projeto .NET com apenas alguns cliques — basta rodar, escolher o tipo de arquitetura, banco(s), nome do projeto e o diretório onde deseja gerar.

Tudo será criado automaticamente:

  - Estrutura limpa e escalável (Clean Architecture base);
  - Configurações de ORM (Entity Framework Core, MongoDB Driver);
  - Suporte a múltiplos bancos (SQL Server, PostgreSQL, MySQL, MongoDB);
  - Geração de `Dockerfile` e `docker-compose.yml`;
  - CI/CD automático via **GitHub Actions**;
  - Injeção de variáveis de ambiente via `.env`;
  - Estrutura completa de pastas (`Controllers`, `Services`, `Commands`, `Queries`, `Migrations`, `DTOs`, etc);
  - E claro: tudo 100% funcional — é só rodar `dotnet run`.

-----

## 🧩 Tecnologias e recursos incluídos

| Categoria | Recursos |
|------------|-----------|
| **.NET SDK** | Compatível com **.NET 7 e .NET 8** |
| **Arquiteturas** | API REST (Limpa e Simples), Worker Service, Webhook Manager, **gRPC** |
| **ORMs** | Entity Framework Core, MongoDB Driver |
| **Bancos de dados** | SQL Server, PostgreSQL, MySQL, MongoDB |
| **Infraestrutura** | Docker + Docker Compose gerados automaticamente |
| **CI/CD** | GitHub Actions pré-configurado |
| **Padrão de pastas** | `src/Domain`, `src/Application`, `src/Infra`, `src/Api` (ou `Worker`), `tests`, `Utils`, `Controllers`, `Services`, `Commands`, `Queries`, `Migrations`, `DTOs` |

-----

## ⚙️ Instalação

### Pré-requisitos

  - **Python 3.7+**
  - **.NET SDK 7.0 ou superior**
  - (Opcional) **Docker** e **Docker Compose**
  - (Opcional) **Git** (para versionamento automático)

### Instalação

Clone este repositório e execute o script principal:

```bash
git clone https://github.com/seuusuario/dotnet-easy.git
cd dotnet-easy
python dotnet_easy_full_v2.py
```

-----

## 🧭 Como usar

Após executar o script, o CLI fará perguntas interativas.

```bash
python dotnet_easy_full_v2.py
```

### 🧱 Exemplo de uso 1: Clean Architecture WebAPI

Este é o fluxo de prompt para criar uma API completa com SQL Server e MongoDB:

```plaintext
🚀 .NET Easy Starter CLI
========================

Presets disponíveis:
  1) clean-webapi-efcore - Clean Architecture WebAPI (Api/Domain/Infra/Application/Tests)
  2) worker-service - Worker Service (BackgroundService + infra/domain/tests)
  3) simple-webapi - Simple WebAPI (single API project + Tests)
  4) webhook-manager - Webhook Manager (API + Processor + Domain/Infra/Tests)
  5) grpc-clean - gRPC Clean (GrpcService + Domain/Infra/Application/Tests)
Escolha o número do preset: 1

Nome da solução/projeto (ex: Company.Product): MyCompany.MyAwesomeApi
Caminho onde gerar (ENTER para pasta atual): ./Projects

Targets disponíveis:
  1) net8.0
  2) net7.0
Escolha target framework (ENTER para net8.0): 1

Escolha bancos (pode selecionar múltiplos separando por espaço). Opções:
  1) sqlserver
  2) postgres
  3) mysql
  4) mongo
  5) none
Ex: 1 4  (ENTER para 'none'): 1 4
```

### 🧱 Exemplo de uso 2: Worker Service

Este é o fluxo para um Worker Service com PostgreSQL:

```plaintext
Escolha o número do preset: 2

Nome da solução/projeto (ex: Company.Product): MyCompany.MyWorker
Caminho onde gerar (ENTER para pasta atual): ./Projects
Escolha target framework (ENTER para net8.0): 1
Escolha bancos (pode selecionar múltiplos separando por espaço)...
Ex: 1 4  (ENTER para 'none'): 2
```

-----

## 🏗️ Resultado e Estrutura

O script gera uma estrutura de solução completa, nomeando cada projeto de acordo.

### Caso de Uso 1: WebAPI (do Exemplo 1)

O resultado para `MyCompany.MyAwesomeApi` será:

```
Projects/MyCompany.MyAwesomeApi/
├── src/
│   ├── MyCompany.MyAwesomeApi.Api/
│   │   ├── Controllers/
│   │   ├── DTOs/
│   │   ├── Utils/
│   │   └── Program.cs
│   ├── MyCompany.MyAwesomeApi.Application/
│   │   ├── Commands/
│   │   ├── Queries/
│   │   ├── Services/
│   │   └── Utils/
│   ├── MyCompany.MyAwesomeApi.Domain/
│   │   ├── Utils/
│   │   └── TodoEntity.cs
│   └── MyCompany.MyAwesomeApi.Infra/
│       ├── Migrations/
│       ├── Utils/
│       ├── AppDbContext.cs
│       └── MongoContext.cs
├── tests/
│   └── MyCompany.MyAwesomeApi.Tests/
│       └── SmokeTests.cs
├── .github/
│   └── workflows/
│       └── ci.yml
├── .env
├── .gitignore
├── appsettings.json
├── docker-compose.yml
├── Dockerfile
└── MyCompany.MyAwesomeApi.sln
```

**Como rodar (WebAPI):**

```bash
cd Projects/MyCompany.MyAwesomeApi
dotnet run --project src/MyCompany.MyAwesomeApi.Api
```

### Caso de Uso 2: Worker Service (do Exemplo 2)

O resultado para `MyCompany.MyWorker` será:

```
Projects/MyCompany.MyWorker/
├── src/
│   ├── MyCompany.MyWorker.Worker/
│   │   ├── Utils/
│   │   ├── Program.cs
│   │   └── Worker.cs
│   ├── MyCompany.MyWorker.Domain/
│   │   └── TodoEntity.cs
│   └── MyCompany.MyWorker.Infra/
│       ├── Migrations/
│       └── AppDbContext.cs
├── tests/
│   └── MyCompany.MyWorker.Tests/
├── .github/
...
└── MyCompany.MyWorker.sln
```

**Como rodar (Worker):**

```bash
cd Projects/MyCompany.MyWorker
dotnet run --project src/MyCompany.MyWorker.Worker
```

-----

## 🐳 Docker

Cada projeto gerado já inclui um `Dockerfile` e `docker-compose.yml` configurados com os bancos selecionados.

### Rodar localmente com Docker:

Basta estar na raiz do projeto (ex: `Projects/MyCompany.MyAwesomeApi/`) e rodar:

```bash
docker-compose up --build
```

-----

## ⚙️ CI/CD com GitHub Actions

O workflow é gerado automaticamente em `.github/workflows/ci.yml` e executa as seguintes etapas:

1.  **Checkout do código**
2.  **Setup do .NET SDK**
3.  **Restore de dependências**
4.  **Build**
5.  **Testes**
6.  **Publicação (publish)**

-----

## 🧠 Variáveis de ambiente padrão

O script também gera um arquivo `.env` com base nos bancos de dados selecionados, pronto para ser usado pelo `docker-compose` e pelo `Program.cs`:

```ini
# Exemplo .env para MyCompany.MyAwesomeApi com SQLServer e Mongo
ASPNETCORE_ENVIRONMENT=Development
ConnectionStrings__SqlServer=Server=db;Database=MyCompany.MyAwesomeApi;User Id=sa;Password=Your_password123;
MONGO__CONN=mongodb://mongo:27017
MONGO__DB=mycompany.myawesomeapi
```

```ini
# Exemplo .env para MyCompany.MyWorker com Postgres
ASPNETCORE_ENVIRONMENT=Development
ConnectionStrings__Postgres=Host=postgres;Database=MyCompany.MyWorker;Username=postgres;Password=Your_password123
```

-----

## 🤝 Contribuindo

Sinta-se à vontade para contribuir com novos presets, templates e melhorias\!

1.  Faça um fork do repositório
2.  Crie sua branch (`git checkout -b feature/nova-feature`)
3.  Commit suas alterações (`git commit -m 'feat: nova feature'`)
4.  Envie sua branch (`git push origin feature/nova-feature`)
5.  Abra um **Pull Request**

-----

## 📜 Licença

Distribuído sob a licença **MIT**. Veja `LICENSE` para mais informações.

-----

## ✨ Autor

**Eduardo Caversan**
Desenvolvedor Fullstack • Líder técnico na Adven.Tech
[GitHub](https://github.com/EduardoCaversan) | [LinkedIn](https://linkedin.com/in/deveduardocaversan)

-----

## 💡 Inspiração

> “Padronizar e automatizar é multiplicar produtividade.
> Um CLI como esse transforma horas de setup em segundos.”

-----

### ⭐ Dê uma estrela

Se este projeto te ajudou, **deixe uma ⭐ no repositório\!**
Isso ajuda o projeto a crescer e alcançar mais desenvolvedores.