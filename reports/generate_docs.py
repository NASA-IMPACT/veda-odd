#!/usr/bin/env python3
"""
Generate docs/objectives.md from config.py OBJECTIVES.

Usage:
    uv run generate_docs.py
"""

from config import OBJECTIVES
from settings import REPO_URL


def generate_objectives_md() -> str:
    """Generate markdown content for objectives page."""
    lines = [
        "# Quarterly Objectives",
        "",
        "This page tracks quarterly objectives and their related repositories across Program Increments (PIs).",
        "",
    ]

    # Sort PIs reverse chronologically (newest first)
    sorted_pis = sorted(
        OBJECTIVES.keys(), key=lambda x: float(x.split("-")[1]), reverse=True
    )

    for i, pi in enumerate(sorted_pis):
        objectives = OBJECTIVES[pi]
        pi_upper = pi.upper().replace("-", " ")

        if i == 0:
            # Current PI - show full details
            lines.append(f"## Current PI: {pi.split('-')[1]}")
            lines.append("")
            lines.append("| # | Objective | Contributors | Repos |")
            lines.append("|---|-----------|--------------|-------|")

            for obj in sorted(objectives, key=lambda x: x["issue_number"]):
                num = obj["issue_number"]
                # Clean up title (remove PI prefix if present)
                title = obj["title"]
                if "Objective" in title and ":" in title:
                    title = title.split(":", 1)[1].strip()
                title = title[:60] + "..." if len(title) > 60 else title

                contributors = ", ".join(u for _, u in obj["contributors"])
                repos = ", ".join(r for _, r in obj["repos"]) if obj["repos"] else "-"

                lines.append(
                    f"| [#{num}]({REPO_URL}/issues/{num}) | {title} | {contributors} | {repos} |"
                )

            lines.append("")
            lines.append("---")
            lines.append("")
        else:
            # Historical PIs - collapsible
            closed_count = sum(1 for o in objectives if o["state"] == "closed")

            lines.append("<details markdown>")
            lines.append(
                f"<summary>{pi_upper} ({len(objectives)} objectives, {closed_count} closed)</summary>"
            )
            lines.append("")
            lines.append("| # | Objective | State | Contributors |")
            lines.append("|---|-----------|-------|--------------|")

            for obj in sorted(objectives, key=lambda x: x["issue_number"]):
                num = obj["issue_number"]
                title = obj["title"]
                if "Objective" in title and ":" in title:
                    title = title.split(":", 1)[1].strip()
                title = title[:50] + "..." if len(title) > 50 else title

                state = obj["state"]
                contributors = ", ".join(u for _, u in obj["contributors"])

                lines.append(
                    f"| [#{num}]({REPO_URL}/issues/{num}) | {title} | {state} | {contributors} |"
                )

            lines.append("")
            lines.append("</details>")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Visualization")
    lines.append("")
    lines.append(
        "The commits per repository chart uses color-coding to show which objective each repo contributes to. Repos that contribute to multiple objectives are shown with split bars."
    )
    lines.append("")
    # Add image for the current PI
    current_pi = sorted_pis[0]
    lines.append(
        f"![{current_pi.upper()} Commits per Repository](images/{current_pi}.png)"
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Configuration")
    lines.append("")
    lines.append(
        f"Objectives are configured in [`reports/config.py`]({REPO_URL}/blob/main/reports/config.py)."
    )
    lines.append("")
    lines.append("To regenerate this page from config:")
    lines.append("")
    lines.append("```bash")
    lines.append("cd reports")
    lines.append("uv run generate_docs.py")
    lines.append("```")
    lines.append("")
    lines.append(
        "See [FY26 Roadmap](./fy26-roadmap.md) for the broader context of these objectives."
    )

    return "\n".join(lines)


def main():
    content = generate_objectives_md()

    output_file = "../docs/objectives.md"
    with open(output_file, "w") as f:
        f.write(content)

    print(f"Generated {output_file}")

    # Print summary
    total_objectives = sum(len(objs) for objs in OBJECTIVES.values())
    print(f"  {len(OBJECTIVES)} PIs, {total_objectives} total objectives")


if __name__ == "__main__":
    main()
