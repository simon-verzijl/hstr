# hstr for macOS

A small, dependency-free interactive shell-history searcher for zsh. Press
Ctrl-R, type one or more words, move with the arrow keys, and press Enter to
put the selected command into the shell and execute it.

## Install

Clone the repository and run the installer:

```sh
git clone https://github.com/simon-verzijl/hstr.git
cd hstr
./hstr --install
```

The installer shows the exact `.zshrc` block it will add and asks for
confirmation. It leaves the executable in the repository and adds that
directory to `PATH`; it does not copy or move files. Reload the current shell
after installation:

```sh
source ~/.zshrc
```

By default, hstr is bound to Ctrl-R. To use another zsh key sequence, pass
`--key` during installation:

```sh
./hstr --install --key '^T'
```

To remove the hstr shell integration from `~/.zshrc`, without deleting the
repository or executable, run:

```sh
./hstr --uninstall
```

The uninstaller also previews the exact lines it will remove and asks for
confirmation. Reload the shell afterward with `source ~/.zshrc`.

## Use

Press Ctrl-R in an interactive zsh shell, then type one or more search terms.
Search terms use case-insensitive AND matching. Prefix a term with `^` to
match it at the beginning of the command.

- Enter: execute the selected command.
- Right Arrow: insert the selected command into the prompt without executing it.
- Up/Down: navigate results.
- Page Up/Page Down: navigate by screen.
- Home/End or Ctrl-A/Ctrl-E: jump to the first/last result.
- Delete: select history entries for deletion; press Enter or `Y` to confirm.
- Escape or Ctrl-C: exit.

The selected command is printed before execution, and multiline history
entries are preserved.

## Test

```sh
python3 -m unittest -v
```
