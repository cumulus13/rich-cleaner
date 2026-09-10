# Rich Cleaner

**Rich Cleaner** is a zero-dependency, production-ready Python library and command-line interface (CLI) for stripping [Rich](https://github.com/Textualize/rich) markup formatting from text, strings, and files.

If you have logs or strings polluted with `[bold red]`, `[link=...]`, or `[:smile:]` and need pure, unformatted text without actually installing the heavy `rich` library, this tool handles it natively using a highly accurate state-machine parser.

## Features

* **Zero Dependencies:** Built entirely on Python's standard library. Doesn't require `rich` to be installed.
* **100% Native Parsing:** Accurately strips color codes, style tags, links, and emojis while safely preserving escaped brackets (`[[ ]]`).
* **Robust CLI:** Clean files in-place or traverse directories recursively to scrub entire log folders.
* **Dry-Run Mode:** Preview which files would be modified before touching anything.
* **Safe:** Automatically skips binary files or files with non-UTF-8 encodings.

## Installation

Install directly via pip:

```bash
pip install rich-cleaner

```

Or, if installing from the source repository:

```bash
git clone https://github.com/cumulus13/rich-cleaner.git
cd rich-cleaner
pip install -e .

# or 

pip install git+https://github.com/cumulus13/rich-cleaner.git

```

## Command-Line Usage (CLI)

Installing the package automatically registers the `rich-cleaner` command globally.

```bash
# Clean a single file in-place
rich-cleaner application.log

# See what would change in a directory without actually modifying files
rich-cleaner /var/logs/my_app --dry-run

# Recursively clean all .log files in a directory
rich-cleaner /var/logs/my_app --recursive --ext .log

# Quiet mode (only output errors)
rich-cleaner application.log --quiet

```

### CLI Arguments

| Argument | Short | Description |
| --- | --- | --- |
| `target` |  | **Required.** The target file or directory path to clean. |
| `--recursive` | `-r` | Process directories recursively. |
| `--dry-run` | `-d` | Show what files would be modified without actually changing them. |
| `--ext` | `-e` | Only process files with this extension (e.g., `.log`, `.txt`). |
| `--quiet` | `-q` | Suppress standard output, only print errors. |
| `--help` | `-h` | Show the help message and exit. |

## Library Usage (Python API)

You can easily use the core parser inside your own Python projects.

### Clean a Simple String

```python
from rich_cleaner import RichCleaner

cleaner = RichCleaner()

dirty_text = "✓ github [bold #00FFFF]Forking[/] [bold #FFAA00]repo[/] [bold #00FFFF]Successfully[/]"
clean_text = cleaner.clean_text(dirty_text)

print(clean_text)
# Output: ✓ github Forking repo Successfully

```

### Clean a File Programmatically

```python
from pathlib import Path
from rich_cleaner import RichCleaner

cleaner = RichCleaner()
target_file = Path("app_output.txt")

# Cleans the file in-place. Returns True if modifications were made.
was_modified = cleaner.clean_file(target_file)

```

## Edge Cases Handled

The parser behaves exactly like Rich's internal syntax engine. It correctly parses and handles:

* Single tags: `[bold]`, `[red]`
* Multi-word tags: `[bold red on black]`
* Hex & RGB codes: `[#00FFFF]`, `[rgb(255,0,0)]`
* Closing tags: `[/]`, `[/bold]`
* Hyperlinks: `[link=https://example.com]Click Here[/link]`
* Emojis: `[:smile:]`
* Escaped brackets (leaves them intact): `[[Not a tag]]` -> `[Not a tag]`

## 👤 Author & License

**Author:** Hadi Cahyadi ([cumulus13@gmail.com](https://www.google.com/search?q=mailto%3Acumulus13%40gmail.com))

**Source:** [github.com/cumulus13/rich-cleaner](https://www.google.com/url?sa=E&source=gmail&q=https://github.com/cumulus13/rich-cleaner)

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/cumulus13)

[![Donate via Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cumulus13)
 
[Support me on Patreon](https://www.patreon.com/cumulus13)