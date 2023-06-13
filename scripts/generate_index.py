#!/bin/env python

import logging
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)


def generate_dir_index(curr_dir: Path, parent_link: bool = False):
    logging.info(f"Generate index for {curr_dir.name}")
    filenames = [f for f in curr_dir.iterdir() if not f.name.startswith("index")]

    links_str = '\n'.join(sorted([f"<div><a href='{path.name}'>{path.name}</a></div>" for path in filenames]))
    parent_link = "<div><a href='..'>..</a></div>" if parent_link else ""
    index_html = f"<html><body><h2>{curr_dir.name}</h2>{parent_link}{links_str}</body></html>"

    with open(curr_dir / "index.html", "w") as fp:
        fp.write(index_html)

    for dir in filter(lambda f: f.is_dir(), filenames):
        generate_dir_index(dir, parent_link=True)


if __name__ == "__main__":
    generate_dir_index(Path.cwd())