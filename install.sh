#!/bin/sh
set -eu

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
install_dir="${HOME}/.local/bin"
mkdir -p "$install_dir"
cp "$project_dir/hstr" "$install_dir/hstr"
chmod 755 "$install_dir/hstr"

block='# hstr shell integration
eval "$(hstr --bind-zsh)"'
zshrc="${ZDOTDIR:-$HOME}/.zshrc"
if grep -Fq '# hstr shell integration' "$zshrc" 2>/dev/null; then
  tmp_zshrc="$(mktemp -t hstr-zshrc.XXXXXXXX)"
  awk '
    /^# hstr shell integration$/ { skip=1; next }
    skip && /^eval "\$\(hstr --bind-zsh\)"$/ { skip=0; next }
    !skip { print }
  ' "$zshrc" >| "$tmp_zshrc"
  mv "$tmp_zshrc" "$zshrc"
fi
if ! grep -Fq '# hstr shell integration' "$zshrc" 2>/dev/null; then
  {
    printf '\n%s\n' "$block"
  } >> "$zshrc"
fi

case ":${PATH}:" in
  *":${install_dir}:"*) ;;
  *)
    path_line="export PATH=\"${install_dir}:\$PATH\""
    if ! grep -Fq "$path_line" "$zshrc" 2>/dev/null; then
      printf '\n%s\n' "$path_line" >> "$zshrc"
    fi
    ;;
esac
printf 'Installed hstr to %s and configured Ctrl-R in %s.\n' "$install_dir" "$zshrc"
