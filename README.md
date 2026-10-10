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

## Optional shell integration

Enable hstr from its current directory and add the Ctrl-R widget to `~/.zshrc` with:

```sh
./hstr --install
```

Use another zsh key sequence with `--key`, for example:

```sh
./hstr --install --key '^T'
```

Remove the shell integration without deleting hstr files with:

```sh
./hstr --uninstall
```

```sh
./install.sh
```

Restart zsh (or run `source ~/.zshrc`). The installer places `hstr` in
`~/.local/bin` and adds the Ctrl-R widget to your zsh configuration.

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
