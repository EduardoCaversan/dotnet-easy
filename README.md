### 1. Tabela de Tecnologias e Recursos

| Categoria | Recursos |
|------------|-----------|
| **.NET SDK** | Compatível com **.NET 7 e .NET 8** |
| **Arquiteturas** | API REST (Limpa e Simples), Worker Service, Webhook Manager, **gRPC** |
| **ORMs** | Entity Framework Core, MongoDB Driver |
| **Padrão de pastas** | `src/Domain`, `src/Application`, `src/Infra`, `src/Api` (ou `Worker`), `tests`, `Utils`, `Controllers`, `Services`, `Commands`, `Queries`, `Migrations`, `DTOs` |

### 2. Instalação

O script suporta Python 3.7+ e foca no .NET 7+.
> - **Python 3.7+**
> - **.NET SDK 7.0 ou superior**

### 3. Uso
> 🚀 .NET Easy Starter CLI
> ========================
>
> Presets disponíveis:
> 1) clean-webapi-efcore - Clean Architecture WebAPI (Api/Domain/Infra/Application/Tests)
> 2) worker-service - Worker Service (BackgroundService + infra/domain/tests)
> 3) simple-webapi - Simple WebAPI (single API project + Tests)
> 4) webhook-manager - Webhook Manager (API + Processor + Domain/Infra/Tests)
> 5) grpc-clean - gRPC Clean (GrpcService + Domain/Infra/Application/Tests)
>
> Escolha o número do preset: **1**
>
> Nome da solução/projeto (ex: Company.Product): **.MyCompanyMyAwesomeAPI**
> Caminho onde gerar (ENTER para pasta atual): **./Projects**
>
> Targets disponíveis:
> 1) net8.0
> 2) net7.0
> Escolha target framework (ENTER para net8.0): **1**
>
> Escolha bancos (pode selecionar múltiplos separando por espaço). Opções:
> 1) sqlserver
> 2) postgres
> 3) mysql
> 4) mongo
> 5) none
> Ex: 1 4 (ENTER para 'none'): **1 4**

### 4. Resultado

O script gera os projetos com o nome completo (ex: `MyAwesomeAPI.Api`) e o comando `dotnet run` precisa do `--project`.

> 📦 Criando projeto MyAwesomeAPI...
> ├── src/
> │   ├── **MyAwesomeAPI.Api/**
> │   ├── **MyAwesomeAPI.Domain/**
> │   ├── **MyAwesomeAPI.Application/**
> │   └── **MyAwesomeAPI.Infra/**
> ├── tests/
> │   └── **MyAwesomeAPI.Tests/**
> ├── Dockerfile
> ├── docker-compose.yml
> ├── .github/workflows/ci.yml
> └── MyAwesomeAPI.sln
>
> Após a criação:
>
>
> cd Projects/MyAwesomeAPI
> dotnet run --project src/MyAwesomeAPI.Api

### 5. Estrutura de diretórios gerada
> MyAwesomeAPI/
> ├── src/
> │   ├── **MyAwesomeAPI.Api/**
> │   │   ├── Controllers/
> │   │   ├── DTOs/
> │   │   ├── Utils/
> │   │   └── Program.cs
> │   ├── **MyAwesomeAPI.Application/**
> │   │   ├── Commands/
> │   │   ├── Queries/
> │   │   ├── Services/
> │   │   ├── DTOs/
> │   │   └── Utils/
> │   ├── **MyAwesomeAPI.Domain/**
> │   │   ├── Utils/
> │   │   └── TodoEntity.cs
> │   └── **MyAwesomeAPI.Infra/**
> │       ├── Migrations/
> │       ├── Services/
> │       ├── Utils/
> │       ├── AppDbContext.cs
> │       └── MongoContext.cs
> ├── tests/
> │   └── **MyAwesomeAPI.Tests/**
> │       └── SmokeTests.cs
> ├── Dockerfile
> ├── docker-compose.yml
> └── .github/
>     └── workflows/
>         └── ci.yml

### 6. Variáveis de ambiente padrão
> ASPNETCORE_ENVIRONMENT=Development
> ConnectionStrings__SqlServer=Server=db;Database=MyAwesomeAPI;User Id=sa;Password=Your_password123;
> MONGO__CONN=mongodb://mongo:27017
> MONGO__DB=myawesomeapi