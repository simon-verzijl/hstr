import importlib.util
import pathlib
import unittest
from importlib.machinery import SourceFileLoader

module_path = pathlib.Path(__file__).with_name("hstr")
module_spec = importlib.util.spec_from_loader("hstr_module", SourceFileLoader("hstr_module", str(module_path)))
assert module_spec and module_spec.loader
hstr_module = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(hstr_module)
matching = hstr_module.matching
parse_history = hstr_module.parse_history
display_command = hstr_module.display_command
command_for_execution = hstr_module.command_for_execution


class HistoryTests(unittest.TestCase):
    def test_zsh_history_is_newest_first_and_multiline(self):
        lines = [": 1:0;git status\n", ": 2:0;docker compose up\n", "docker compose logs\n"]
        self.assertEqual(parse_history(lines), ["git status", "docker compose up\ndocker compose logs"])
        self.assertEqual(parse_history([": 1700000000:0;git status\n"])[0].timestamp, "2023-11-14 23:13")

    def test_zsh_doubled_continuation_backslash_is_preserved_for_execution(self):
        lines = [": 1:0;ls -l ;\\\\\n", "echo hoihoi;\\\\\n", "ls -l\n"]
        self.assertEqual(parse_history(lines), ["ls -l ;\\\\\necho hoihoi;\\\\\nls -l"])

    def test_zsh_encoded_newlines_split_entries_and_restore_multiline_commands(self):
        lines = [r": 1:0;gcloud alpha sql instances patch \n  --project=qbuzz-accept \n  --storage-auto-increase-limit=2000\n: 2:0;echo next" + "\n"]
        self.assertEqual(parse_history(lines), ["gcloud alpha sql instances patch \\\n  --project=qbuzz-accept \\\n  --storage-auto-increase-limit=2000", "echo next"])

    def test_numbered_fc_history(self):
        self.assertEqual(parse_history(["  12  git status\n", "  11  git log\n"]), ["git status", "git log"])

    def test_file_history_is_reversed_to_newest_first(self):
        path = pathlib.Path(self.id().replace(".", "_") + ".history")
        try:
            path.write_text(": 1:0;old\n: 2:0;new\n", encoding="utf-8")
            self.assertEqual(hstr_module.history_from_file(path), ["new", "old"])
        finally:
            path.unlink(missing_ok=True)

    def test_multiple_terms_are_and_matched_case_insensitively(self):
        commands = ["git commit -am fix", "git status", "GIT COMMIT --amend"]
        self.assertEqual(matching(commands, "git commit"), ["git commit -am fix", "GIT COMMIT --amend"])

    def test_caret_anchors_a_term_to_the_beginning(self):
        self.assertEqual(matching(["git status", "echo git status", "GIT commit"], "^git"), ["git status", "GIT commit"])

    def test_prefix_matches_are_ranked_before_mentions(self):
        commands = ["echo nc status", "nc -zv host 443", "nc", "watch nc -zv host 443"]
        self.assertEqual(matching(commands, "nc")[:3], ["nc", "nc -zv host 443", "echo nc status"])

    def test_duplicate_commands_are_shown_once(self):
        self.assertEqual(matching(["nc -zv host 443", "nc  -zv host 443", "echo nc"], "nc"), ["nc -zv host 443", "echo nc"])

    def test_multiline_commands_remain_searchable_as_one_entry(self):
        command = "for file in *.txt; do\n  echo $file\ndone"
        self.assertEqual(matching([command, "echo done"], "echo file"), [command])

    def test_display_hides_line_continuation_backslashes(self):
        command = "ls -l ;\\\\\necho hoihoi;\\\\\nls -l"
        self.assertEqual(display_command(command), "ls -l ; ↵ echo hoihoi; ↵ ls -l")

    def test_execution_normalizes_zsh_multiline_history_escaping(self):
        command = "PROJECT=qbuzz-devops\\\\\n\\\\\ngcloud compute snapshots list \\\\\n  --project \"$PROJECT\" \\\\\n  --limit=20"
        expected = "PROJECT=qbuzz-devops\ngcloud compute snapshots list \\\n  --project \"$PROJECT\" \\\n  --limit=20"
        self.assertEqual(command_for_execution(command), expected)

    def test_assignment_continuation_becomes_command_boundary(self):
        command = "PROJECT=qbuzz-devops\\\\\ngcloud compute snapshots list \\\n  --project \"$PROJECT\""
        expected = "PROJECT=qbuzz-devops\ngcloud compute snapshots list \\\n  --project \"$PROJECT\""
        self.assertEqual(command_for_execution(command), expected)


if __name__ == "__main__":
    unittest.main()
