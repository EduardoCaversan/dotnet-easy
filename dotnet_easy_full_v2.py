#!/usr/bin/env python3
"""
dotnet_easy_full_v2.py
GERADOR COMPLETO .NET — cross-platform, standalone (Python 3.7+)
Gera presets, multiple DB support (sqlserver, postgres, mysql, mongo), target framework selection,
pastas comuns (Utils, Controllers, Commands, Queries, Services, DTOs, Migrations), Docker, docker-compose,
CI (GitHub Actions), .env, appsettings.json, Serilog wiring, sample DbContext/Mongo wiring, tests, git init.
Rode: python dotnet_easy_full_v2.py
"""

import os
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

# -----------------------
# Presets
# -----------------------
PRESETS = {
    "clean-webapi-efcore": {
        "label": "Clean Architecture WebAPI (Api/Domain/Infra/Application/Tests)",
        "projects": ["Api", "Domain", "Infra", "Application", "Tests"],
        "is_web": True
    },
    "worker-service": {
        "label": "Worker Service (BackgroundService + infra/domain/tests)",
        "projects": ["Worker", "Domain", "Infra", "Tests"],
        "is_web": False
    },
    "simple-webapi": {
        "label": "Simple WebAPI (single API project + Tests)",
        "projects": ["Api", "Tests"],
        "is_web": True
    },
    "webhook-manager": {
        "label": "Webhook Manager (API + Processor + Domain/Infra/Tests)",
        "projects": ["Api", "Processor", "Domain", "Infra", "Tests"],
        "is_web": True
    },
    "grpc-clean": {
        "label": "gRPC Clean (GrpcService + Domain/Infra/Application/Tests)",
        "projects": ["GrpcService", "Domain", "Infra", "Application", "Tests"],
        "is_web": False
    }
}

# -----------------------
# NuGet packages mapping
# -----------------------
NUGET = {
    "serilog": ["Serilog.AspNetCore", "Serilog.Sinks.Console"],
    "swashbuckle": ["Swashbuckle.AspNetCore"],
    "mediatr": ["MediatR.Extensions.Microsoft.DependencyInjection"],
    "autofac": ["Autofac.Extensions.DependencyInjection"],
    "polly": ["Polly"],
    "healthchecks": ["AspNetCore.HealthChecks.UI.Client"],
    # EF Core base packages (we'll add provider specific)
    "efcore_base": ["Microsoft.EntityFrameworkCore", "Microsoft.EntityFrameworkCore.Design"],
    # Providers
    "sqlserver": ["Microsoft.EntityFrameworkCore.SqlServer"],
    "postgres": ["Npgsql.EntityFrameworkCore.PostgreSQL"],
    "mysql": ["Pomelo.EntityFrameworkCore.MySql"],
    # Mongo
    "mongo": ["MongoDB.Driver"]
}

# -----------------------
# Helpers
# -----------------------
def run(cmd, cwd=None, check=True):
    print(f"> {cmd}")
    res = subprocess.run(cmd, shell=True, cwd=cwd)
    if check and res.returncode != 0:
        print(f"Erro ({res.returncode}) executando: {cmd}")
        sys.exit(res.returncode)
    return res.returncode

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content), encoding="utf-8")

def safe_mkdir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def confirm(prompt: str) -> bool:
    r = input(f"{prompt} (y/N): ").strip().lower()
    return r == "y"

# -----------------------
# Templates / file snippets
# -----------------------

GITIGNORE = """
bin/
obj/
.vs/
.env
publish/
*.db
*.sqlite
"""

README_MD = """# {project}
Scaffold gerado pelo dotnet_easy_full_v2.py

Preset: {preset}
Target Framework: {tf}
Databases: {dbs}

Como começar:
1. Ajuste `.env` com suas credenciais
2. `cd {root}`
3. `dotnet restore`
4. `dotnet build`
5. `dotnet run --project src/{project_api}` (ou o projeto worker)
"""

APPSETTINGS_TEMPLATE = """{{
  "Logging": {{
    "LogLevel": {{
      "Default": "Information",
      "Microsoft": "Warning",
      "Microsoft.Hosting.Lifetime": "Information"
    }}
  }},
  "AllowedHosts": "*",
  "ConnectionStrings": {{
    {conn_strings}
  }},
  "MongoSettings": {{
    "ConnectionString": "{mongo_conn}",
    "Database": "{mongo_db}"
  }}
}}
"""

ENV_EXAMPLE_TEMPLATE = """# Exemplo .env
ASPNETCORE_ENVIRONMENT=Development
{env_conn_vars}
"""

DOCKERFILE_TEMPLATE = """FROM mcr.microsoft.com/dotnet/aspnet:{tf} AS base
WORKDIR /app
EXPOSE 80

FROM mcr.microsoft.com/dotnet/sdk:{tf} AS build
WORKDIR /src
COPY . .
RUN dotnet restore
RUN dotnet publish -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "{dll_name}.dll"]
"""

DOCKER_COMPOSE_TEMPLATE = """version: '3.8'
services:
  app:
    build: .
    ports:
      - "5000:80"
    env_file:
      - .env
    depends_on:
{depends}
{db_services}
"""

DOCKER_SERVICE_MSSQL = """
  db:
    image: mcr.microsoft.com/mssql/server:2022-latest
    environment:
      SA_PASSWORD: "Your_password123"
      ACCEPT_EULA: "Y"
    ports:
      - "1433:1433"
"""

DOCKER_SERVICE_POSTGRES = """
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: "Your_password123"
    ports:
      - "5432:5432"
"""

DOCKER_SERVICE_MYSQL = """
  mysql:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: "Your_password123"
    ports:
      - "3306:3306"
"""

DOCKER_SERVICE_MONGO = """
  mongo:
    image: mongo:6
    ports:
      - "27017:27017"
"""

GITHUB_CI = """name: .NET Build & Test

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '{tf_version}'
      - name: Restore
        run: dotnet restore
      - name: Build
        run: dotnet build --no-restore --configuration Release
      - name: Test
        run: dotnet test --no-build --verbosity normal
      - name: Publish
        run: dotnet publish -c Release -o publish
"""

PROGRAM_MINIMAL_WEBAPI = """using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Configuration;
using Serilog;
{ef_usings}
{mongo_usings}

var builder = WebApplication.CreateBuilder(args);

// Serilog
builder.Host.UseSerilog((ctx, cfg) => cfg.WriteTo.Console());

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

{db_registrations}

var app = builder.Build();

if (app.Environment.IsDevelopment())
{{
    app.UseSwagger();
    app.UseSwaggerUI();
}}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();
"""

# CORREÇÃO: Adicionado 'using {ns};' para encontrar a classe Worker
PROGRAM_MINIMAL_WORKER = """using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Serilog;
using {ns};
{ef_usings}
{mongo_usings}

Host.CreateDefaultBuilder(args)
    .UseSerilog((ctx, cfg) => cfg.WriteTo.Console())
    .ConfigureServices((hostContext, services) =>
    {{
        services.AddHostedService<Worker>();
        {db_registrations}
    }})
    .Build()
    .Run();
"""

DBCONTEXT_CS = """using Microsoft.EntityFrameworkCore;

namespace {ns}.Infra
{{
    public class AppDbContext : DbContext
    {{
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) {{ }}

        public DbSet<{ns}.Domain.TodoEntity> Todos {{ get; set; }}
    }}
}}
"""

MONGO_SERVICE_CS = """using MongoDB.Driver;
namespace {ns}.Infra
{{
    public class MongoContext
    {{
        public IMongoDatabase Database {{ get; }}
        public MongoContext(string connString, string dbName)
        {{
            var client = new MongoClient(connString);
            Database = client.GetDatabase(dbName);
        }}
    }}
}}
"""

TODO_ENTITY_CS = """namespace {ns}.Domain
{{
    public class TodoEntity
    {{
        public int Id {{ get; set; }}
        public string Title {{ get; set; }} = string.Empty;
        public bool Done {{ get; set; }}
    }}
}}
"""

SAMPLE_CONTROLLER_CS = """using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace {ns}.Controllers
{{
    [ApiController]
    [Route("api/[controller]")]
    public class HealthController : ControllerBase
    {{
        [HttpGet]
        public IActionResult Get() => Ok(new {{ status = "ok" }});
    }}
}}
"""

SAMPLE_WORKER_CS = """using System;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace {ns}
{{
    public class Worker : BackgroundService
    {{
        private readonly ILogger<Worker> _logger;
        public Worker(ILogger<Worker> logger) => _logger = logger;

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {{
            _logger.LogInformation("Worker running.");
            while (!stoppingToken.IsCancellationRequested)
            {{
                _logger.LogInformation("Worker heartbeat: {{time}}", DateTimeOffset.Now);
                await Task.Delay(5000, stoppingToken);
            }}
        }}
    }}
}}
"""

SAMPLE_TEST_CS = """using Xunit;

namespace {ns}.Tests
{{
    public class SmokeTests
    {{
        [Fact]
        public void TrueIsTrue() => Assert.True(true);
    }}
}}
"""

# -----------------------
# Helper logic for DB wiring
# -----------------------
def build_conn_strings(selected_dbs, project):
    conn_strings = []
    env_vars = []
    mongo_conn = ""
    mongo_db = ""
    for db in selected_dbs:
        if db == "sqlserver":
            conn_strings.append(f'"SqlServer": "Server=db;Database={project};User Id=sa;Password=Your_password123;"')
            env_vars.append(f'ConnectionStrings__SqlServer=Server=db;Database={project};User Id=sa;Password=Your_password123;')
        if db == "postgres":
            conn_strings.append(f'"Postgres": "Host=postgres;Database={project};Username=postgres;Password=Your_password123"')
            env_vars.append(f'ConnectionStrings__Postgres=Host=postgres;Database={project};Username=postgres;Password=Your_password123')
        if db == "mysql":
            conn_strings.append(f'"MySql": "Server=mysql;Database={project};User=root;Password=Your_password123;"')
            env_vars.append(f'ConnectionStrings__MySql=Server=mysql;Database={project};User=root;Password=Your_password123;')
        if db == "mongo":
            mongo_conn = "mongodb://mongo:27017"
            mongo_db = project.lower()
            env_vars.append(f'MONGO__CONN={mongo_conn}')
            env_vars.append(f'MONGO__DB={mongo_db}')
    return ",\n    ".join(conn_strings), "\n".join(env_vars), mongo_conn, mongo_db

def build_db_registrations(selected_dbs, ns, config_source, services_source):
    registrations = []
    ef_usings = set()
    mongo_usings = ""
    for db in selected_dbs:
        if db in ("sqlserver", "postgres", "mysql"):
            ef_usings.add("using Microsoft.EntityFrameworkCore;")
            if db == "sqlserver":
                registrations.append(f'{services_source}.AddDbContext<{ns}.Infra.AppDbContext>(opt => opt.UseSqlServer({config_source}.GetConnectionString("SqlServer")));')
            elif db == "postgres":
                registrations.append(f'{services_source}.AddDbContext<{ns}.Infra.AppDbContext>(opt => opt.UseNpgsql({config_source}.GetConnectionString("Postgres")));')
            elif db == "mysql":
                registrations.append(f'// NOTE: adjust ServerVersion for MySQL provider\n{services_source}.AddDbContext<{ns}.Infra.AppDbContext>(opt => opt.UseMySql({config_source}.GetConnectionString("MySql"), Microsoft.EntityFrameworkCore.ServerVersion.AutoDetect({config_source}.GetConnectionString("MySql"))));')
        if db == "mongo":
            mongo_usings = "using MongoDB.Driver;"
            registrations.append(f'{services_source}.AddSingleton(new {ns}.Infra.MongoContext({config_source}["MongoSettings:ConnectionString"]!, {config_source}["MongoSettings:Database"]!));')
    ef_usings_str = "\n".join(sorted(ef_usings))
    return ef_usings_str, mongo_usings, "\n".join(registrations)

# -----------------------
# Main flow
# -----------------------
def choose_preset():
    print("Presets disponíveis:")
    for i, (k, v) in enumerate(PRESETS.items(), 1):
        print(f"  {i}) {k} - {v['label']}")
    s = input("Escolha o número do preset: ").strip()
    if not s:
        print("Nenhum preset escolhido. Saindo.")
        sys.exit(1)
    try:
        idx = int(s) - 1
        key = list(PRESETS.keys())[idx]
        return key
    except Exception:
        print("Entrada inválida.")
        sys.exit(1)

def choose_target_framework():
    print("\nTargets disponíveis:")
    options = ["net8.0", "net7.0"]
    for i, t in enumerate(options, 1):
        print(f"  {i}) {t}")
    s = input("Escolha target framework (ENTER para net8.0): ").strip() or "1"
    try:
        return options[int(s)-1]
    except Exception:
        return "net8.0"

def choose_dbs():
    print("\nEscolha bancos (pode selecionar múltiplos separando por espaço). Opções:")
    dbs = ["sqlserver", "postgres", "mysql", "mongo", "none"]
    for i, d in enumerate(dbs, 1):
        print(f"  {i}) {d}")
    s = input("Ex: 1 4  (ENTER para 'none'): ").strip()
    if not s:
        return []
    parts = s.split()
    chosen = []
    for p in parts:
        try:
            idx = int(p) - 1
            if dbs[idx] != "none":
                chosen.append(dbs[idx])
        except:
            continue
    # remove duplicates
    return list(dict.fromkeys(chosen))

def run_generation():
    key = choose_preset()
    preset = PRESETS[key]
    project_root_name = input("\nNome da solução/projeto (ex: Company.Product): ").strip()
    if not project_root_name:
        print("Nome inválido.")
        sys.exit(1)
    target_input = input("Caminho onde gerar (ENTER para pasta atual): ").strip() or "."
    dest_root = Path(target_input).resolve() / project_root_name
    if dest_root.exists():
        print(f"O diretório {dest_root} já existe.")
        if not confirm("Deseja sobrescrever/sobrescrever conteúdo?"):
            print("Cancelado.")
            sys.exit(0)
    dest_root.mkdir(parents=True, exist_ok=True)

    tf = choose_target_framework()
    db_choices = choose_dbs()
    print(f"\nGerando preset '{key}' em {dest_root} com target {tf} e DBs {db_choices}\n")

    # -----------------------------
    # Criar solution
    # -----------------------------
    os.chdir(dest_root)
    run(f"dotnet new sln -n {project_root_name}")

    # -----------------------------
    # Criar pastas principais
    # -----------------------------
    src = dest_root / "src"
    tests = dest_root / "tests"
    safe_mkdir(src)
    safe_mkdir(tests)

    # -----------------------------
    # Criar projetos
    # -----------------------------
    created = []  # tuples: (proj_name, proj_folder, kind)
    for p in preset["projects"]:
        proj_name = f"{project_root_name}.{p}"
        
        # Coloca projetos de teste na pasta 'tests'
        if p.lower() in ("tests",) or p.lower().endswith("tests"):
            test_proj_name = f"{project_root_name}.Tests"
            test_folder = tests / test_proj_name
             # Evita criar a pasta 'tests' duas vezes se "Tests" estiver no preset
            if not any(t[0] == test_proj_name for t in created):
                run(f"dotnet new xunit -n {test_proj_name} -f {tf} -o \"{test_folder}\"")
                created.append((test_proj_name, test_folder, "test"))
            continue

        # Outros projetos vão para 'src'
        proj_folder = src / proj_name

        # decide template type
        if p.lower() in ("api", "grpcservice", "grpc"):
            if "grpc" in p.lower():
                run(f"dotnet new grpc -n {proj_name} -f {tf} -o \"{proj_folder}\"")
                created.append((proj_name, proj_folder, "grpc"))
            else:
                run(f"dotnet new webapi -n {proj_name} -f {tf} -o \"{proj_folder}\"")
                created.append((proj_name, proj_folder, "webapi"))
        elif p.lower() in ("worker", "processor"):
            run(f"dotnet new worker -n {proj_name} -f {tf} -o \"{proj_folder}\"")
            created.append((proj_name, proj_folder, "worker"))
        else:
            # classlib genérica (Domain, Application, Infra)
            run(f"dotnet new classlib -n {proj_name} -f {tf} -o \"{proj_folder}\"")
            created.append((proj_name, proj_folder, "classlib"))

    # -----------------------------
    # Função auxiliar para encontrar csproj
    # -----------------------------
    def find_csproj(suffix):
        # Procura pelo sufixo do nome do projeto (ex: .Domain)
        proj = next(((name, folder) for name, folder, k in created if name.endswith(f".{suffix}")), None)
        return (proj[1] / f"{proj[0]}.csproj") if proj else None

    core_csproj = find_csproj("Domain")
    app_csproj = find_csproj("Application")
    infra_csproj = find_csproj("Infra")
    
    # Para web_csproj, precisamos encontrar por 'kind' ou 'suffix'
    web_proj_tuple = next(((name, folder) for name, folder, k in created if k in ("webapi", "grpc") or name.endswith(".Api")), None)
    web_csproj = (web_proj_tuple[1] / f"{web_proj_tuple[0]}.csproj") if web_proj_tuple else None
    
    # CORREÇÃO: Encontra o worker_csproj
    worker_proj_tuple = next(((name, folder) for name, folder, k in created if k in ("worker", "processor")), None)
    worker_csproj = (worker_proj_tuple[1] / f"{worker_proj_tuple[0]}.csproj") if worker_proj_tuple else None

    # -----------------------------
    # Adicionar referências entre projetos (sem criar ciclos)
    # -----------------------------
    if app_csproj and core_csproj and app_csproj != core_csproj:
        run(f"dotnet add \"{app_csproj}\" reference \"{core_csproj}\"")

    if infra_csproj and core_csproj and infra_csproj != core_csproj:
        run(f"dotnet add \"{infra_csproj}\" reference \"{core_csproj}\"")
    
    # Referência de Application para Infra (ex: para IRepository)
    if app_csproj and infra_csproj:
         # Application depende de Infra (para implementações)
         run(f"dotnet add \"{app_csproj}\" reference \"{infra_csproj}\"")

    if web_csproj:
        if app_csproj:
            run(f"dotnet add \"{web_csproj}\" reference \"{app_csproj}\"")
        if infra_csproj:
            run(f"dotnet add \"{web_csproj}\" reference \"{infra_csproj}\"")
        if core_csproj and not app_csproj: # Para presets simples sem Application
            run(f"dotnet add \"{web_csproj}\" reference \"{core_csproj}\"")

    # CORREÇÃO: Adiciona referências para o Worker
    if worker_csproj:
        if app_csproj:
            run(f"dotnet add \"{worker_csproj}\" reference \"{app_csproj}\"")
        if infra_csproj:
            run(f"dotnet add \"{worker_csproj}\" reference \"{infra_csproj}\"")
        if core_csproj and not app_csproj: # Para presets simples
            run(f"dotnet add \"{worker_csproj}\" reference \"{core_csproj}\"")

    # -----------------------------
    # Adicionar todos os projetos na solution
    # -----------------------------
    for name, folder, kind in created:
        csproj_files = list(folder.glob("*.csproj"))
        if csproj_files:
            for csproj in csproj_files:
                run(f"dotnet sln add \"{csproj}\"")
        else:
            print(f"⚠️ csproj não encontrado em {folder}")


    # create common folders inside each project
    for name, folder, kind in created:
        if kind == "webapi" or kind == "grpc":
            safe_mkdir(folder / "Controllers")
            safe_mkdir(folder / "DTOs")
        if kind == "classlib" and "Application" in name:
            safe_mkdir(folder / "Commands")
            safe_mkdir(folder / "Queries")
            safe_mkdir(folder / "Services")
            safe_mkdir(folder / "DTOs")
        if kind == "classlib" and "Infra" in name:
            safe_mkdir(folder / "Services")
            safe_mkdir(folder / "Migrations")
        
        safe_mkdir(folder / "Utils")


    # generate files for API / worker
    api_proj = next((n for n,f,k in created if k in ("webapi","grpc")), None)
    api_folder = None
    if api_proj:
        api_entry = next((t for t in created if t[0]==api_proj), None)
        if api_entry:
            api_folder = api_entry[1]
    
    # produce connection strings etc
    conn_strings, env_vars, mongo_conn, mongo_db = build_conn_strings(db_choices, project_root_name)
    conn_strings_block = conn_strings if conn_strings else ""
    env_conn_block = env_vars if env_vars else ""

    # Write Program.cs replacement for webapi/worker projects
    for name, folder, kind in created:
        ns = name  # use full project name as namespace
        if kind == "webapi":
            ef_usings, mongo_usings, db_registrations = build_db_registrations(db_choices, project_root_name, "builder.Configuration", "builder.Services")
            
            prog = PROGRAM_MINIMAL_WEBAPI.format(ef_usings=ef_usings, mongo_usings=mongo_usings,
                                                 db_registrations=db_registrations)
            write(folder / "Program.cs", prog)
            write(folder / "Controllers" / "HealthController.cs", SAMPLE_CONTROLLER_CS.format(ns=ns))
            # appsettings / .env in root
            write(dest_root / "appsettings.json", APPSETTINGS_TEMPLATE.format(conn_strings=conn_strings_block or '"Default": ""', mongo_conn=mongo_conn or "", mongo_db=mongo_db or ""))
            write(dest_root / ".env", ENV_EXAMPLE_TEMPLATE.format(env_conn_vars=env_conn_block))
        
        if kind == "worker":
            ef_usings, mongo_usings, db_registrations = build_db_registrations(db_choices, project_root_name, "hostContext.Configuration", "services")

            # CORREÇÃO: Adiciona 'ns=ns' ao formatar o Program.cs do worker
            prog = PROGRAM_MINIMAL_WORKER.format(ef_usings=ef_usings, mongo_usings=mongo_usings,
                                                 db_registrations=db_registrations, ns=ns)
            write(folder / "Program.cs", prog)
            
            # Sobrescreve Worker.cs com namespace
            write(folder / "Worker.cs", SAMPLE_WORKER_CS.format(ns=ns)) 
            
            write(dest_root / ".env", ENV_EXAMPLE_TEMPLATE.format(env_conn_vars=env_conn_block))
        
        if kind == "grpc":
            pass # Manter o padrão por enquanto
        
        if kind == "classlib":
            # remove o 'Class1.cs' padrão
            class1 = folder / "Class1.cs"
            if class1.exists():
                class1.unlink()
        
        if kind == "test":
             # remove o 'UnitTest1.cs' padrão
            unittest1 = folder / "UnitTest1.cs"
            if unittest1.exists():
                unittest1.unlink()
            write(folder / "SmokeTests.cs", SAMPLE_TEST_CS.format(ns=project_root_name))

    # For infra project: add DbContext / Mongo context and sample entity & repository
    infra_entries = [t for t in created if t[0].endswith(".Infra")]
    for name, folder, kind in infra_entries:
        # add DbContext if EF chosen
        if any(db in ("sqlserver","postgres","mysql") for db in db_choices):
            write(folder / "AppDbContext.cs", DBCONTEXT_CS.format(ns=project_root_name))
            # add sample repository
            write(folder / "TodoRepository.cs", dedent(f"""using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
namespace {project_root_name}.Infra
{{
    public class TodoRepository
    {{
        private readonly AppDbContext _ctx;
        public TodoRepository(AppDbContext ctx) => _ctx = ctx;
        public async Task<List<{project_root_name}.Domain.TodoEntity>> GetAllAsync() => await _ctx.Todos.ToListAsync();
    }}
}}
"""))
        # add mongo context if selected
        if "mongo" in db_choices:
            write(folder / "MongoContext.cs", MONGO_SERVICE_CS.format(ns=project_root_name))
        
    # Add sample entity under Domain (find Domain project)
    domain_proj_entry = next((t for t in created if t[0].endswith(".Domain")), None)
    if domain_proj_entry:
        domain_folder = domain_proj_entry[1]
        write(domain_folder / "TodoEntity.cs", TODO_ENTITY_CS.format(ns=project_root_name))


    # -----------------------------
    # Adicionar pacotes NuGet
    # -----------------------------
    print("\nAdicionando pacotes NuGet conforme escolhas...")

    for name, folder, kind in created:
        csproj_files = list(folder.glob("*.csproj"))
        if not csproj_files:
            continue
        csproj = csproj_files[0]

        # Serilog (WebAPI, Worker, Application)
        if kind in ("webapi", "worker", "grpc") or "Application" in name:
            for pkg in NUGET.get("serilog", []):
                run(f"dotnet add \"{csproj}\" package {pkg}")

        # Swashbuckle (WebAPI)
        if kind == "webapi":
            for pkg in NUGET.get("swashbuckle", []):
                run(f"dotnet add \"{csproj}\" package {pkg}")

        # EF Core (Infra E Api/Worker)
        if (kind in ("webapi", "worker", "grpc") or "Infra" in name) and any(db in ("sqlserver","postgres","mysql") for db in db_choices):
            for pkg in NUGET.get("efcore_base", []):
                run(f"dotnet add \"{csproj}\" package {pkg}")
            if "sqlserver" in db_choices:
                for pkg in NUGET.get("sqlserver", []):
                    run(f"dotnet add \"{csproj}\" package {pkg}")
            if "postgres" in db_choices:
                for pkg in NUGET.get("postgres", []):
                    run(f"dotnet add \"{csproj}\" package {pkg}")
            if "mysql" in db_choices:
                for pkg in NUGET.get("mysql", []):
                    run(f"dotnet add \"{csproj}\" package {pkg}")

        # Mongo (Infra E Api/Worker)
        if (kind in ("webapi", "worker", "grpc") or "Infra" in name) and "mongo" in db_choices:
            for pkg in NUGET.get("mongo", []):
                run(f"dotnet add \"{csproj}\" package {pkg}")

        # Mediatr / Autofac (Application / Api)
        if kind in ("webapi", "grpc") or "Application" in name:
            for pkg in NUGET.get("mediatr", []):
                run(f"dotnet add \"{csproj}\" package {pkg}")
            for pkg in NUGET.get("autofac", []):
                run(f"dotnet add \"{csproj}\" package {pkg}")

        # Polly (Webhook-manager preset)
        if "webhook" in key and (kind == "worker" or "Processor" in name): # 'key' é o nome do preset
            for pkg in NUGET.get("polly", []):
                run(f"dotnet add \"{csproj}\" package {pkg}")

        # HealthChecks (Worker preset)
        if "worker" in kind or "processor" in kind:
            for pkg in NUGET.get("healthchecks", []):
                run(f"dotnet add \"{csproj}\" package {pkg}")

    # Generate Dockerfile + docker-compose
    if db_choices or preset["is_web"] or "worker" in key:
        print("\nGerando Dockerfile e docker-compose...")
        dll_like = next((n for n,f,k in created if k in ("webapi","worker","grpc")), None)
        dll_name = dll_like or f"{project_root_name}.Api"
        write(dest_root / "Dockerfile", DOCKERFILE_TEMPLATE.format(tf=tf, dll_name=dll_name))
        
        deps = []
        db_services = ""
        if "sqlserver" in db_choices:
            deps.append("      - db")
            db_services += DOCKER_SERVICE_MSSQL
        if "postgres" in db_choices:
            deps.append("      - postgres")
            db_services += DOCKER_SERVICE_POSTGRES
        if "mysql" in db_choices:
            deps.append("      - mysql")
            db_services += DOCKER_SERVICE_MYSQL
        if "mongo" in db_choices:
            deps.append("      - mongo")
            db_services += DOCKER_SERVICE_MONGO
        
        depends_lines = "\n".join(deps) if deps else ""
        write(dest_root / "docker-compose.yml", DOCKER_COMPOSE_TEMPLATE.format(depends=depends_lines, db_services=db_services))

    # Write README, .gitignore and CI
    conn_strings_block = conn_strings if conn_strings else '"Default": ""'
    
    api_proj_name = next((n for n,f,k in created if k == "webapi"), None)
    if not api_proj_name:
        api_proj_name = next((n for n,f,k in created if k in ("worker", "grpc")), project_root_name)


    write(dest_root / ".gitignore", GITIGNORE)
    write(dest_root / "README.md", README_MD.format(project=project_root_name, preset=key, tf=tf, dbs=",".join(db_choices) or "none", root=dest_root, project_api=(api_proj_name or "")))
    
    # appsettings.json
    if not (dest_root / "appsettings.json").exists():
        write(dest_root / "appsettings.json", APPSETTINGS_TEMPLATE.format(conn_strings=conn_strings_block, mongo_conn=mongo_conn or "", mongo_db=mongo_db or ""))
    # .env
    if not (dest_root / ".env").exists():
        write(dest_root / ".env", ENV_EXAMPLE_TEMPLATE.format(env_conn_vars=env_conn_block))
    # CI
    write(dest_root / ".github/workflows/ci.yml", GITHUB_CI.format(tf_version=tf))

    # Initialize git
    print("\nInicializando git (opcional)...")
    try:
        run("git --version", check=False)
        run("git init", cwd=str(dest_root))
        run("git add .", cwd=str(dest_root))
        run('git commit -m "chore: scaffold generated by dotnet_easy_full_v2"', cwd=str(dest_root))
    except Exception as e:
        print("git não está disponível ou commit falhou:", e)

    # Restore / build / test
    print("\nExecutando dotnet restore / build / test (se dotnet estiverível)...")
    try:
        run("dotnet restore", cwd=str(dest_root))
        run("dotnet build --configuration Release", cwd=str(dest_root))
        # run tests if present
        if any(kind=="test" for (_,_,kind) in created):
            run("dotnet test", cwd=str(dest_root))
    except Exception as e:
        print("dotnet comandos falharam (talvez SDK não instalado). Scaffold criado; rode manualmente 'dotnet restore' e 'dotnet build'.")
        print("Erro:", e)
        # Se o build falhou, saímos com o código de erro para o usuário ver
        if isinstance(e, SystemExit):
            sys.exit(e.code)
        else:
            sys.exit(1)


    print("\n✅ Scaffold completo criado em:", dest_root)
    print("Próximos passos recomendados:")
    if api_proj_name:
        print(f" - cd \"{dest_root}\"")
        print(f" - dotnet run --project src/{api_proj_name}")
    else:
        first = created[0][1] if created else dest_root
        print(f" - cd \"{first}\" && dotnet run")
    print(" - Ajuste appsettings.json e .env; preencha ServerVersion para MySQL se necessário; configure secrets no CI para deploy/push de imagem.")
    print("\nBoa codificação! 🚀")


# -----------------------
# Entrypoint
# -----------------------
if __name__ == "__main__":
    try:
        run_generation()
    except KeyboardInterrupt:
        print("\nCancelado pelo usuário.")
        sys.exit(0)
    except SystemExit as e:
        # Captura saídas de 'sys.exit' para não imprimir traceback
        if e.code != 0:
            print(f"\nScript interrompido com erro (código: {e.code}).")
        sys.exit(e.code)
    except Exception as e:
        print(f"\nOcorreu um erro inesperado no script: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)