# PyDeck — Instruções para Agentes de IA

## Visão Geral

PyDeck é um lançador de atalhos desktop estilo Stream Deck. O usuário gerencia uma grade de cards com emoji + título, cada um vinculado a uma ação (comando, programa, arquivo ou URL). Também possui um modo compacto flutuante com ícone transparente e arrastável.

---

## Stack

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Python | ≥ 3.12 | Linguagem |
| Flet | 0.85.0 | GUI (Flutter-based) |
| uv | — | Gerenciamento de dependências e execução |

**Importante**: O usuário usa **apenas uv** (sem pip). Comandos:

- `uv run pydeck` — executar o app
- `uv sync` — instalar/sincronizar dependências
- `uv run flet run main.py` — executar com hot reload do Flet
- `uv run python main.py` — executar diretamente

---

## Estrutura

```
pydeck/
├── pydeck/
│   ├── __init__.py       # Versão
│   ├── __main__.py       # Entry point: from .app import main; main()
│   ├── app.py            # Classe PyDeckApp — lógica principal
│   ├── ui.py             # Componentes Flet (builders)
│   ├── config.py         # ConfigManager — salva/carrega JSON
│   ├── models.py         # Shortcut + Config dataclasses
│   ├── actions.py        # Execução de ações (subprocess, startfile, webbrowser)
│   └── theme.py          # Cores, constantes de layout
├── assets/
│   └── pydeck_icon.png   # Ícone 680×680 (usado no modo compacto)
├── pyproject.toml
├── main.py               # Script alternativo
├── README.md
└── AGENTS.md
```

---

## Arquitetura e Padrões

### PyDeckApp (`app.py`)

- Classe única que recebe `ft.Page` no `__init__`
- Cria `main_col = ft.Column(expand=True, spacing=10)` e adiciona à página
- Métodos iniciados por `_` são privados
- **Fluxo**: `__init__` → `_setup_page()` → `_build_ui()`
- `_build_ui()` recalcula tamanho da janela e reconstrói `main_col.controls`
- Config toggle (`_toggle_config_mode`): alterna `self.config_mode`, chama `_build_ui()`
- Compact toggle (`_toggle_compact_mode`): **limpa `page.controls`** e adiciona compact view diretamente (bypassa `main_col`)

### Modo Compacto

- Usa `ft.WindowDragArea` (NÃO GestureDetector) para arrasto nativo de janela frameless
- `on_drag_end` → salva posição
- `Container.on_click` → restaura janela normal
- Janela: `width=COMPACT_SIZE, height=COMPACT_SIZE + COMPACT_EXTRA`
  - `COMPACT_EXTRA = 12` — compensa chrome invisível do Windows
- Fundo transparente: `page.window.bgcolor = "transparent"`, `page.bgcolor = "transparent"`
- `frameless = True`, `always_on_top = True`, `resizable = False`

### Redimensionamento da Janela

- `_build_ui` sempre define `page.window.resizable = True` ANTES de `page.window.height`
- Sem `min_height` — apenas altura calculada diretamente
- `window_height(tile, rows)` calcula altura total

### Componentes de UI (`ui.py`)

- Funções builder (NÃO classes): `build_top_bar`, `build_card`, `build_add_button`, `build_edit_form`, `build_delete_dialog`, `build_snackbar`, `build_compact_view`, `pick_file`
- Cada builder recebe callbacks como parâmetros (NÃO acopla ao PyDeckApp)

### Tema (`theme.py`)

- Paleta Dracula: `#282A36` (bg), `#BD93F9` (primary), `#FF79C6` (accent), `#44475A` (surface), `#F8F8F2` (light text)
- Grid: 4 colunas, spacing 12, padding 12
- `tile_size(width)` = `(width - padding*2 - spacing*(cols-1)) // cols`

### Configuração (`config.py`)

- JSON em `%APPDATA%/pydeck/config.json` (Windows) ou `~/.config/pydeck/config.json`
- Sempre tem .config (valida com existência do arquivo, não com tratamento de exceção)
- `ConfigManager.load()` + `ConfigManager.save()` gerenciam o arquivo

### Modelos (`models.py`)

- `Shortcut`: id (uuid8), title, icon (emoji string), action_type, action_value, color
- `Config`: grid_columns, button_size, always_on_top, compact_x, compact_y, shortcuts

---

## Convenções de Código

### Gerais

- **Sem comentários** no código — a não ser que o usuário peça explicitamente
- Nomes em inglês (código) / português (UI, README, mensagens de commit)
- Type hints em todas as funções
- Dataclasses para modelos de dados
- Sem classes de UI — builders são funções soltas

### Estilo Flet

- `expand=True` para preencher espaço disponível
- Controles com altura fixa (GridView com `height=grid_height`) em vez de expand
- `page.update()` chamado apenas uma vez por método, no final
- Event handlers podem ser async (Flet suporta nativamente)
- `page.overlay` para SnackBar, `page.show_dialog` para AlertDialog
- FilePicker adicionado via `page.services.append(file_picker)`

### Commits

- Mensagens em português
- Prefixos: "Corrige", "Adiciona", "Remove", "Atualiza"
- Foco no "porquê", não no "o quê"
- Exemplo: `Corrige redimensionamento da janela e widget cortado no modo compacto`

---

## Problemas Conhecidos e Soluções

### Janela não reduz ao alternar modo de edição

- **Causa**: Flet com `resizable=False` não permite redução programática da janela
- **Solução**: Sempre definir `page.window.resizable = True` antes de `page.window.height`
- Ver `_build_ui()` em `app.py:204-206`

### Ícone do modo compacto cortado na parte inferior

- **Causa**: Windows reserva ~12px de chrome invisível no rodapé de janelas frameless
- **Solução**: `window.height = COMPACT_SIZE + COMPACT_EXTRA` (112px)
- Ver `_toggle_compact_mode()` em `app.py:83-86`

### Atributo `_resize_task` inexistente causando AttributeError

- **Causa**: Resquício de implementação async removida
- **Solução**: Remover referências a `self._resize_task` em `_toggle_compact_mode`
- Ver `app.py:63-66` (já corrigido)

### `Container.image_src` / `Container.image_fit` não existem no Flet 0.85.0

- Usar `Image` widget como child do Container
- Ver `build_compact_view()` em `ui.py`

---

## Fluxos Comuns

### Adicionar atalho

1. Usuário ativa modo edição (Ctrl+E ou botão)
2. Clica no card "+"
3. `_add_shortcut()` → `_edit_shortcut(Shortcut(), is_new=True)`
4. Preenche formulário e salva → `_on_form_save()` → salva no config → `_build_ui()`

### Alternar modo compacto

1. Ctrl+Shift+C ou botão na top bar
2. `_toggle_compact_mode()` → salva estado atual → limpa page.controls → configura janela frameless → adiciona compact view
3. Arrasta: `WindowDragArea` nativo → `on_drag_end` → `_save_compact_pos()` → salva no config
4. Restaura: click → `_restore_from_compact()` → salva posição → recria `main_col` → `_build_ui()`

---

## Comandos úteis

```bash
uv run pydeck          # executar o app
uv sync                # instalar dependências
uv run flet run main.py  # modo dev com hot reload
```
