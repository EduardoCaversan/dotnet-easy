# 🧠 .NET Easy Starter CLI

Um gerador universal de projetos **.NET**, feito para que você possa iniciar novos repositórios de forma **instantânea, padronizada e escalável** — com tudo configurado: arquitetura, ORM, banco de dados, Docker, CI/CD e estrutura de pastas.

---

## 🚀 O que é?

O **.NET Easy Starter CLI** é uma ferramenta interativa em **Python**, compatível com **Windows, Linux e macOS**, que permite criar rapidamente qualquer tipo de projeto .NET com apenas alguns cliques — basta rodar, escolher o tipo de arquitetura, banco(s), ORM(s), nome do projeto e o diretório onde deseja gerar.

Tudo será criado automaticamente:
- Estrutura limpa e escalável (Clean Architecture base);
- Configurações de ORM (Entity Framework Core, Dapper, MongoDB, etc);
- Suporte a múltiplos bancos (SQL Server, PostgreSQL, MySQL, MongoDB);
- Geração de `Dockerfile` e `docker-compose.yml`;
- CI/CD automático via **GitHub Actions**;
- Injeção de variáveis de ambiente;
- Estrutura completa de pastas (`Controllers`, `Services`, `Commands`, `Queries`, `Utils`, etc);
- E claro: tudo 100% funcional — é só rodar `dotnet run`.

---

## 🧩 Tecnologias e recursos incluídos

| Categoria | Recursos |
|------------|-----------|
| **.NET SDK** | Compatível com .NET 6, .NET 7 e .NET 8 |
| **Arquiteturas** | API REST, Worker Service, Webhook Manager, Service Bus Listener |
| **ORMs** | Entity Framework Core, Dapper, MongoDB Driver |
| **Bancos de dados** | SQL Server, PostgreSQL, MySQL, MongoDB |
| **Infraestrutura** | Docker + Docker Compose gerados automaticamente |
| **CI/CD** | GitHub Actions pré-configurado |
| **Padrão de pastas** | `src/Core`, `src/Application`, `src/Infrastructure`, `src/WebAPI`, `tests`, `Utils`, `Controllers`, `Services`, `Commands`, `Queries`, `Entities` |

---

## ⚙️ Instalação

### Pré-requisitos

- **Python 3.8+**
- **.NET SDK 6.0 ou superior**
- (Opcional) **Docker** e **Docker Compose**
- (Opcional) **Git** (para versionamento automático)

### Instalação

Clone este repositório e execute o script principal:

git clone https://github.com/seuusuario/dotnet-easystarter-cli.git
cd dotnet-easystarter-cli
python dotnet_easy_full_v2.py

---

## 🧭 Como usar

Após executar o script, o CLI fará perguntas interativas:

python dotnet_easy_full_v2.py

### 🧱 Exemplo de uso:

🚀 .NET Easy Starter CLI
========================

1. api - API REST com Swagger, EF Core e arquitetura limpa
2. worker - Worker Service com logs e background tasks
3. webhook-manager - Gerenciador de Webhooks (Listener + Processor)
4. servicebus-listener - Listener Azure Service Bus (com Dapper)

Selecione o tipo de projeto: 1
Digite o nome do projeto: MyAwesomeAPI
Selecione o Target Framework (6.0 / 7.0 / 8.0): 8.0
Selecione os bancos de dados (SQLServer, PostgreSQL, MySQL, MongoDB) [separe por vírgula ou deixe em branco]: SQLServer,MongoDB
Selecione os ORMs (EFCore, Dapper, Mongo) [separe por vírgula ou deixe em branco]: EFCore
Caminho onde deseja criar o projeto (deixe em branco para atual): ./Projects

### 🏗️ Resultado

📦 Criando projeto MyAwesomeAPI...
├── src/
│   ├── Core/
│   ├── Application/
│   ├── Infrastructure/
│   ├── WebAPI/
│   └── Utils/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── .github/workflows/ci.yml
└── MyAwesomeAPI.sln

Após a criação:


cd Projects/MyAwesomeAPI
dotnet run

🎉 Pronto! Sua API está rodando e pronta para desenvolvimento.

---

## 🧱 Estrutura de diretórios gerada

MyAwesomeAPI/
├── src/
│   ├── Core/
│   │   ├── Entities/
│   │   ├── Interfaces/
│   │   └── DTOs/
│   ├── Application/
│   │   ├── Commands/
│   │   ├── Queries/
│   │   └── Handlers/
│   ├── Infrastructure/
│   │   ├── Contexts/
│   │   ├── Repositories/
│   │   └── Migrations/
│   ├── WebAPI/
│   │   ├── Controllers/
│   │   ├── Services/
│   │   └── Program.cs
│   └── Utils/
├── tests/
├── Dockerfile
├── docker-compose.yml
└── .github/
    └── workflows/
        └── ci.yml

---

## 🐳 Docker

Cada projeto gerado já inclui um `Dockerfile` e `docker-compose.yml` configurados com o banco selecionado.

### Rodar localmente com Docker:


docker-compose up --build

---

## ⚙️ CI/CD com GitHub Actions

O workflow é gerado automaticamente em `.github/workflows/ci.yml` e executa as seguintes etapas:

1. **Checkout do código**
2. **Setup do .NET SDK**
3. **Restore de dependências**
4. **Build**
5. **Testes**
6. **Publicação (publish)**

---

## 🧠 Variáveis de ambiente padrão

O script também gera um arquivo `.env` (se aplicável), com variáveis como:

ASPNETCORE_ENVIRONMENT=Development
ConnectionStrings__DefaultConnection=Server=db;Database=MyAwesomeAPI;User Id=sa;Password=Your_password123;
Mongo__Connection=mongodb://mongo:27017
Mongo__Database=MyAwesomeAPI

---

## 🤝 Contribuindo

Sinta-se à vontade para contribuir com novos presets, templates e melhorias!

1. Faça um fork do repositório
2. Crie sua branch (`git checkout -b feature/nova-feature`)
3. Commit suas alterações (`git commit -m 'feat: nova feature'`)
4. Envie sua branch (`git push origin feature/nova-feature`)
5. Abra um **Pull Request**

---

## 📜 Licença

Distribuído sob a licença **MIT**. Veja `LICENSE` para mais informações.

---

## ✨ Autor

**Eduardo Caversan**
Desenvolvedor Fullstack • Líder técnico na Adven.Tech
[GitHub](https://github.com/EduardoCaversan) | [LinkedIn](https://linkedin.com/in/deveduardocaversan)

---

## 💡 Inspiração

> “Padronizar e automatizar é multiplicar produtividade.
> Um CLI como esse transforma horas de setup em segundos.”

---

### ⭐ Dê uma estrela

Se este projeto te ajudou, **deixe uma ⭐ no repositório!**
Isso ajuda o projeto a crescer e alcançar mais desenvolvedores.