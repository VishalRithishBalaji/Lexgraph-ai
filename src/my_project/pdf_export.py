from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet


def md_to_pdf(input_file, output_file):

    doc = SimpleDocTemplate(output_file)

    styles = getSampleStyleSheet()

    story = []

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as f:

        text = f.read()

    # Fix common LLM output issues

    text = text.replace("<br>", "\n")
    text = text.replace("<br/>", "\n")
    text = text.replace("<br />", "\n")

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            story.append(Spacer(1, 6))
            continue

        # Markdown headers

        if line.startswith("# "):

            story.append(
                Paragraph(
                    f"<b>{line[2:]}</b>",
                    styles["Heading1"]
                )
            )

            continue

        elif line.startswith("## "):

            story.append(
                Paragraph(
                    f"<b>{line[3:]}</b>",
                    styles["Heading2"]
                )
            )

            continue

        elif line.startswith("### "):

            story.append(
                Paragraph(
                    f"<b>{line[4:]}</b>",
                    styles["Heading3"]
                )
            )

            continue

        # Convert markdown bold

        line = line.replace("**", "")

        # Skip markdown table separators

        if line.startswith("|---"):
            continue

        try:

            story.append(
                Paragraph(
                    line,
                    styles["BodyText"]
                )
            )

        except Exception:

            # Fallback if paragraph parsing fails

            safe_line = (
                line.replace("<", "")
                    .replace(">", "")
            )

            story.append(
                Paragraph(
                    safe_line,
                    styles["BodyText"]
                )
            )

    doc.build(story)