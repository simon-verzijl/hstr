# hstr for macOS

A small, dependency-free interactive shell-history searcher for zsh. Press
Ctrl-R, type one or more words, move with the arrow keys, and press Enter to
put the selected command into the shell and execute it.

## Run manually

No installation is required. Start it directly from this directory:

```sh
./hstr
```

After selecting a command and pressing Enter, hstr executes it in zsh.
The complete selected command is printed immediately before execution, and
multiline history entries are preserved and can be searched and run.

To have a manually selected command immediately available with cursor-up,
load the temporary shell helper (this does not install anything):

```sh
eval "$(./hstr --bind-zsh)"
hstr-run
```

The `hstr-run` helper adds the selected command to the current zsh history
before executing it. Running `./hstr` directly still works, but a standalone
child process cannot update the parent shell's in-memory history.

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

Search terms are combined with AND semantics and matched case-insensitively.
Prefix a term with `^` to match it only at the beginning of the command.
Backspace only removes the last search character; Delete is used for deleting
history entries.
Press Right Arrow to insert the selected command into the prompt without
running it; press Enter to execute it after editing.
Esc exits without running anything. Ctrl-P/Ctrl-N also move through results.

## Test

```sh
python3 -m unittest -v
```
