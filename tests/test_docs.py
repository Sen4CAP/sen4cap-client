import ast
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import Mock
from urllib.parse import unquote, urlsplit

import pytest
from cuiman.api import Client
from gavicore.models import JobInfo
from mkdocs.commands.build import build
from mkdocs.config import load_config

ROOT = Path(__file__).resolve().parents[1]


class PageLinks(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.targets = []
        self.ids = set()
        self.python_blocks = []
        self._languages = []
        self._code = None
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "div":
            self._languages.append("language-python" in attrs.get("class", ""))
        elif tag == "pre" and any(self._languages):
            self._code = []
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for name in ("href", "src"):
            if attrs.get(name):
                self.targets.append(attrs[name])

    def handle_data(self, data):
        if self._code is not None:
            self._code.append(data)

    def handle_endtag(self, tag):
        if tag == "pre" and self._code is not None:
            self.python_blocks.append("".join(self._code))
            self._code = None
        elif tag == "div" and self._languages:
            self._languages.pop()


@pytest.fixture(scope="module")
def built_site(tmp_path_factory):
    site = tmp_path_factory.mktemp("docs") / "site"
    config = load_config(str(ROOT / "mkdocs.yml"), site_dir=str(site), strict=True)
    build(config)
    return site


def test_built_docs_have_valid_local_links_and_assets(built_site):
    site = built_site

    # Old notebook copies and local credentials must never enter the built site.
    assert not (site / "notebooks").exists()
    pages = {
        path.resolve(): PageLinks(path.read_text(encoding="utf-8"))
        for path in site.rglob("*.html")
    }
    failures = []
    for path, page in pages.items():
        for target in page.targets:
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            if url.path.startswith("/"):
                destination = (site / unquote(url.path).lstrip("/")).resolve()
            else:
                destination = (
                    (path.parent / unquote(url.path)).resolve() if url.path else path
                )
            if destination.is_dir():
                destination /= "index.html"
            if not destination.is_file():
                failures.append(f"{path.relative_to(site)}: missing {target}")
            elif url.fragment and destination in pages:
                if unquote(url.fragment) not in pages[destination].ids:
                    failures.append(
                        f"{path.relative_to(site)}: missing anchor {target}"
                    )
    assert not failures, "\n".join(failures)


def test_rendered_python_examples_have_valid_syntax(built_site):
    blocks = []
    for path in built_site.rglob("*.html"):
        page = PageLinks(path.read_text(encoding="utf-8"))
        for source in page.python_blocks:
            ast.parse(source, filename=str(path))
        blocks.extend(page.python_blocks)
    assert blocks, "No rendered Python examples were found"


def test_rendered_api_guide_runs_in_order(built_site, monkeypatch):
    import matplotlib.pyplot as plt

    import sen4cap_client.api

    client = Mock(spec=Client)
    client.execute_process.return_value = JobInfo(jobID="guide-job", status="accepted")
    client.get_job.return_value = JobInfo(jobID="guide-job", status="successful")
    monkeypatch.setattr(sen4cap_client.api, "create_client", lambda: client)
    monkeypatch.setattr(plt, "show", lambda: None)
    monkeypatch.chdir(ROOT)
    page = PageLinks((built_site / "guides/api/index.html").read_text(encoding="utf-8"))
    namespace = {}

    for source in page.python_blocks:
        exec(compile(source, "rendered API guide", "exec"), namespace)

    client.execute_process.assert_called_once()
    client.get_job.assert_called_once_with(job_id="guide-job")
    client.get_job_results.assert_called_once_with(job_id="guide-job")
    client.open_job_result.assert_called_once_with(
        job_id="guide-job", asset_name="SNDVI"
    )
    client.open_job_result.return_value.close.assert_called_once()
    client.close.assert_called_once()
