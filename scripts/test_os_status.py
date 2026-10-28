"""Minimal tests for os_status.py over a temporary vault.

Run from the vault root: python -m unittest scripts/test_os_status.py
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import os_status  # noqa: E402

FILES = {
    "review/queue.md": (
        "# Queue\n\nsession: 3\n\n"
        "## Card: a\n- box: 1\n- due: 2\n- misses: 2\n\n"
        "## Card: b\n- box: 3\n- due: 9\n\n"
        "## Card: c\n- box: 1\n- due: 4\n"
    ),
    "areas/estudos/trilhas/rag.md": (
        "---\ntype: trilha\nstatus: ativa\nscope: standard\n---\n# Trilha\n\n## Sessões\n"
        "Formato:\nPróximo passo: \n"  # empty template line must not swallow the next one
        "### 2026-10-20 · teoria\nPróximo passo: ler bm25\n"
        "### 2026-10-24 · aplicada\nPróximo passo: montar eval\n\n## Artefato\n"
    ),
    "areas/estudos/trilhas/old.md": "---\ntype: trilha\nstatus: concluida\nscope: quick\n---\n",
    "areas/publico/posts/2026-10-20-x.md": (
        "---\ntype: post\nkind: post\nstatus: publicado\nplatform: x\npublished: 2026-10-20\nthesis: evals\n---\n"
    ),
    "areas/publico/posts/2026-10-21-art.md": (
        "---\ntype: post\nkind: artigo\nstatus: publicado\nplatform: medium\npublished: 2026-09-30\n---\n"
    ),
    "areas/publico/posts/2026-10-05-sub.md": (
        "---\ntype: post\nkind: artigo\nstatus: publicado\nplatform: substack\npublished: 2026-10-05\n---\n"
    ),
    "areas/publico/posts/2026-10-25-d.md": (
        "---\ntype: post\nstatus: rascunho\nplatform: linkedin\ndate: 2026-10-25\n---\n"
    ),
    "areas/teses/_index.md": "---\ntype: indice\n---\n",
    "areas/teses/evals.md": "---\ntype: tese\nstatus: sustentada\nupdated: 2026-10-22\n---\n",
    "areas/projetos/_index.md": "---\ntype: indice\n---\n",
    "areas/projetos/bench.md": (
        "---\ntype: projeto\nstatus: em-andamento\nthesis: evals\n---\n"
        "## Log\n### 2026-10-23\nPróximo passo: rodar baseline\n\n## Divulgação\n"
    ),
    "areas/projetos/done.md": "---\ntype: projeto\nstatus: publicado\npublished: 2026-10-01\n---\n",
    "journal/2026-10-25.md": "---\ntype: diario\n---\n",
    "journal/semanas/2026-W43.md": "---\ntype: semana\n---\n",
    "raw/inbox.md": (
        "@post uma ideia\n# Inbox\n\nAppend on top.\nLines starting with # are ignored.\n\n---\n"
        "segundo item\n# comentário\n"
    ),
}


class OsStatusTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.vault = Path(cls.tmp.name)
        for rel, content in FILES.items():
            p = cls.vault / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
        cls.s = os_status.collect(cls.vault, today="2026-10-26")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_keys_and_json(self):
        for k in ("today", "week", "review", "tracks", "posts", "teses", "projetos",
                  "producao_publica", "journal", "inbox_items"):
            self.assertIn(k, self.s)
        json.dumps(self.s)
        self.assertEqual(self.s["week"], "2026-W44")

    def test_review(self):
        r = self.s["review"]
        self.assertEqual((r["session"], r["total_cards"], r["due_now"]), (3, 3, 2))
        self.assertEqual(r["box_distribution"], {"1": 2, "3": 1})
        self.assertEqual(r["stuck_box1"], ["a"])

    def test_tracks(self):
        self.assertEqual([t["sessions_7d"] for t in self.s["tracks"] if t["slug"] == "rag"], [2])
        t = {x["slug"]: x for x in self.s["tracks"]}
        self.assertEqual(t["rag"]["last_session"], "2026-10-24")
        self.assertEqual(t["rag"]["next_step"], "montar eval")
        self.assertEqual(t["old"]["status"], "concluida")

    def test_posts_teses_projetos(self):
        self.assertEqual(self.s["posts"]["by_status"], {"publicado": 3, "rascunho": 1})
        self.assertEqual(self.s["posts"]["open"][0]["platform"], "linkedin")
        self.assertEqual(self.s["teses"]["sustentadas"][0]["cited_by"], 2)
        pj = self.s["projetos"]["em_andamento"][0]
        self.assertEqual((pj["next_step"], pj["last_log"]), ("rodar baseline", "2026-10-23"))

    def test_producao_publica(self):
        pp = self.s["producao_publica"]
        self.assertEqual(pp["2026-10"], {"projetos": 1, "artigos": 1, "posts": 1})
        self.assertEqual(pp["2026-09"], {"projetos": 0, "artigos": 1, "posts": 0})

    def test_journal_inbox(self):
        self.assertEqual(self.s["journal"], {"last_day": "2026-10-25", "last_week": "2026-W43"})
        self.assertEqual(self.s["inbox_items"], 2)

    def test_empty_vault(self):
        with tempfile.TemporaryDirectory() as d:
            s = os_status.collect(Path(d), today="2026-01-05")
            self.assertEqual(s["review"]["total_cards"], 0)
            self.assertIn("2025-12", s["producao_publica"])
            os_status.human(s)


if __name__ == "__main__":
    unittest.main()
