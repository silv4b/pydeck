# PyDeck

Um lançador de atalhos inspirado no Stream Deck para Windows, construído com Python e **Flet 0.85.0**. Gerencie comandos, programas, arquivos e URLs em uma grade visual com tema escuro estilo Dracula.

![PyDeck](assets/pydeck_icon.png)

---

## Funcionalidades

### Grade de Atalhos

- Exibe até **20 atalhos** (5 linhas × 4 colunas) em cards com ícone emoji e título
- Cores personalizáveis por atalho
- Clique para executar a ação associada
- Rolagem automática quando necessário

### Modo de Edição (Ctrl+E)

- Adicionar novos atalhos com título, ícone emoji, cor e ação
- Editar ou excluir atalhos existentes
- Botão de editar e deletar sobrepostos em cada card
- Botão de reset para restaurar configurações padrão

### Modo Compacto (Ctrl+Shift+C)

- Ícone flutuante de 100×100 que fica sobre as janelas
- **Arrastável**: clique e arraste para reposicionar na tela
- Posição salva automaticamente ao arrastar
- Fundo transparente com moldura removida
- Toque no ícone para restaurar a janela completa

### Tipos de Ação

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| `Comando` | Executa um comando no shell | `shutdown /s /t 0` |
| `Programa` | Abre um aplicativo | `notepad.exe`, `calc.exe` |
| `Arquivo` | Abre um arquivo ou pasta | `C:\documento.pdf` |
| `URL` | Abre no navegador padrão | `https://google.com` |

### Atalhos de Teclado

| Tecla | Ação |
|-------|------|
| `Ctrl + E` | Alterna modo de edição |
| `Ctrl + Shift + C` | Alterna modo compacto flutuante |

---

## Tecnologias

| Tecnologia | Versão | Finalidade |
|------------|--------|------------|
| Python | ≥ 3.12 | Linguagem principal |
| **Flet** | 0.85.0 | Framework GUI (Flutter-based) |
| setuptools | ≥ 75.0 | Build system |
| **uv** | — | Gerenciamento de dependências e execução |

### Estrutura do Projeto

```
pydeck/
├── pydeck/
│   ├── __init__.py      # Versão do pacote
│   ├── __main__.py      # Ponto de entrada
│   ├── app.py           # Lógica principal da aplicação
│   ├── ui.py            # Componentes de interface
│   ├── config.py        # Gerenciamento de configuração (JSON)
│   ├── models.py        # Modelos de dados (Shortcut, Config)
│   ├── actions.py       # Execução de ações (subprocess, startfile, webbrowser)
│   └── theme.py         # Tema, cores e constantes de layout
├── assets/
│   └── pydeck_icon.png  # Ícone do aplicativo
├── pyproject.toml       # Configuração do projeto
├── main.py              # Script de entrada alternativo
└── README.md
```

### Configuração

As configurações e atalhos são salvos em formato JSON em:

- **Windows**: `%APPDATA%\pydeck\config.json`
- **Linux**: `~/.config/pydeck/config.json`

---

## Como Rodar

```bash
uv run pydeck
```

Ou, para desenvolvimento com recarregamento automático:

```bash
uv run flet run main.py
```

### Atalhos Padrão

Ao iniciar pela primeira vez, o PyDeck cria automaticamente 4 atalhos de exemplo:

- **Bloco de Notas** — `notepad.exe`
- **Calculadora** — `calc.exe`
- **Terminal** — `cmd.exe`
- **Google** — `https://google.com`

---

## Desenvolvimento

```bash
# Clonar o repositório
git clone https://github.com/seuuser/pydeck.git
cd pydeck

# Sincronizar dependências (cria .venv automaticamente)
uv sync

# Executar em modo desenvolvimento
uv run python main.py

# Ou com recarregamento automático do Flet
uv run flet run main.py
```

---

## Licença

Distribuído sob a licença MIT.
