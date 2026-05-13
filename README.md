<!-- markdownlint-disable MD033 MD060 MD040 -->

# PyDeck

Um lançador de atalhos inspirado no Stream Deck para **Windows e Linux**, construído com Python e **Flet 0.85.0**. Gerencie comandos, programas, arquivos e URLs em uma grade visual com tema escuro estilo Dracula.

<div align="center"><img src="assets/pydeck_icon.png" width="100" height="100" alt="PyDeck"></div>

## Funcionalidades

### Grade de Atalhos

- Exibe até **20 atalhos** (5 linhas × 4 colunas) em cards com ícone emoji e título
- Cores personalizáveis por atalho com preview visual e paleta de cores
- Clique para executar a ação associada
- Rolagem automática quando necessário

### Modo de Edição (Ctrl+E)

- Adicionar novos atalhos com título, ícone emoji, cor e ação
- **Seletor de cor**: preview visual ao lado do campo hex + botão de paleta com 20 cores predefinidas
- Editar ou excluir atalhos existentes
- Botão de editar e deletar sobrepostos em cada card
- Botão de reset para restaurar configurações padrão

### Modo Compacto (Ctrl+Shift+C) — Windows

- Ícone flutuante de 100×100 que fica sobre as janelas
- **Arrastável**: clique e arraste para reposicionar na tela
- Posição salva automaticamente ao arrastar
- Fundo transparente com moldura removida
- Toque no ícone para restaurar a janela completa
- **Disponível apenas no Windows** (limitação do Flet no Linux)

### Tipos de Ação

| Tipo | Windows | Linux |
|------|---------|-------|
| `Comando` | `shutdown /s` | `gnome-terminal` |
| `Programa` | `notepad.exe`, `calc.exe` | Usa `xdg-open` |
| `Arquivo` | `C:\documento.pdf` | Usa `xdg-open` |
| `URL` | Navegador padrão | Usa `xdg-open` |

### Atalhos de Teclado

| Tecla | Ação |
|-------|------|
| `Ctrl + E` | Alterna modo de edição |
| `Ctrl + Shift + C` | Alterna modo compacto (apenas Windows) |

## Tecnologias

| Tecnologia | Versão | Finalidade |
|------------|--------|------------|
| Python | ≥ 3.12 | Linguagem principal |
| **Flet** | 0.85.0 | Framework GUI (Flutter-based) |
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
│   ├── actions.py       # Execução de ações
│   ├── os_utils.py       # Utilitários de detecção de SO
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

Na primeira execução, os atalhos padrão são adaptados ao SO:

- **Windows**: Bloco de Notas, Calculadora, Terminal (cmd.exe), Google
- **Linux**: Navegador, Terminal (gnome-terminal), Calculadora (gnome-calculator), Google

## Como Rodar

```bash
uv run pydeck
```

Ou, para desenvolvimento com recarregamento automático:

```bash
uv run flet run main.py
```

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

## Licença

Distribuído sob a licença MIT.
