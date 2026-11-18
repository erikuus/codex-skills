#!/usr/bin/env python3
"""Create an initial project-specific dashboard prompt from resolved inputs."""
import argparse
from pathlib import Path
import re


def render(application, page_id, repository, overview, status):
    values = {
        "APPLICATION_NAME": application,
        "DASHBOARD_PAGE_ID": page_id,
        "GITHUB_REPOSITORY": repository,
        "OVERVIEW_TITLE": overview,
        "STATUS_INTERPRETATION": status,
    }
    if any(not isinstance(value, str) or not value.strip() or "{{" in value or "}}" in value for value in values.values()):
        raise ValueError("Resolve all nonempty prompt inputs before rendering")
    if not re.fullmatch("page_[0-9a-f]{32}", page_id):
        raise ValueError("Supply the actual dashboard Page ID")
    if not re.fullmatch("[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise ValueError("Supply the verified GitHub owner/repository")
    if re.search(r"page_[0-9a-f]{32}", status):
        raise ValueError("Status interpretation must not add a second Page destination")
    template = Path(__file__).resolve().parent.parent/"assets/dashboard/refresh-prompt.md.template"
    return re.sub(r"\{\{([A-Z_]+)\}\}", lambda match: values[match[1]], template.read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--application",required=True)
    parser.add_argument("--page-id",required=True)
    parser.add_argument("--repository",required=True)
    parser.add_argument("--overview",required=True)
    parser.add_argument("--status-file",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args = parser.parse_args()
    try:
        result = render(args.application,args.page_id,args.repository,args.overview,args.status_file.read_text())
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open("x") as stream:
            stream.write(result)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1,f"Dashboard prompt creation stopped: {error}\n")


if __name__ == "__main__":
    main()

