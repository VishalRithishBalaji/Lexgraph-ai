import gradio as gr
from pathlib import Path
from my_project.crew import MyProject
from my_project.rag import ingest_pdf
from my_project.pdf_export import md_to_pdf
from my_project.knowledge_graph import generate_graph


def run_courtroom(pdf_file):
    if pdf_file is None:
        return (
            "❌ Please upload a PDF.",
            "", "", "", "", None, "",
            None, None, None, None, None
        )

    try:
        # -------------------------
        # PDF -> Text -> ChromaDB
        # -------------------------
        case_text = ingest_pdf(pdf_file.name)

        inputs = {
            "case_text": case_text
        }

        # -------------------------
        # Run CrewAI
        # -------------------------
        MyProject().crew().kickoff(inputs=inputs)

        # -------------------------
        # Generate Knowledge Graph
        # -------------------------
        try:
            generate_graph()
        except Exception as e:
            print(f"Knowledge Graph Error: {e}")

        # -------------------------
        # Generate PDFs
        # -------------------------
        reports_dir = Path("reports")

        report_files = [
            "evidence_report",
            "defense_report",
            "prosecution_report",
            "contradiction_report",
            "judgement"
        ]

        for report in report_files:
            md_file = reports_dir / f"{report}.md"
            pdf_file_path = reports_dir / f"{report}.pdf"

            if md_file.exists():
                md_to_pdf(
                    str(md_file),
                    str(pdf_file_path)
                )

        # -------------------------
        # Read Reports
        # -------------------------
        def read_report(filename):
            try:
                return (reports_dir / filename).read_text(encoding="utf-8")
            except Exception:
                return f"{filename} not found."

        evidence = read_report("evidence_report.md")
        defense = read_report("defense_report.md")
        prosecution = read_report("prosecution_report.md")
        contradiction = read_report("contradiction_report.md")
        judgement = read_report("judgement.md")

        graph_path = reports_dir / "knowledge_graph.png"

        status = """
✅ Investigator Complete
✅ Defense Lawyer Complete
✅ Prosecutor Complete
✅ Contradiction Analysis Complete
✅ Knowledge Graph Generated
✅ Judge Complete
🎉 Analysis Finished
"""
        return (
            status,
            evidence,
            defense,
            prosecution,
            contradiction,
            str(graph_path),
            judgement,
            str(reports_dir / "evidence_report.pdf"),
            str(reports_dir / "defense_report.pdf"),
            str(reports_dir / "prosecution_report.pdf"),
            str(reports_dir / "contradiction_report.pdf"),
            str(reports_dir / "judgement.pdf")
        )

    except Exception as e:
        return (
            f"❌ Error: {str(e)}",
            "", "", "", "", None, "",
            None, None, None, None, None
        )


with gr.Blocks(title="AI Courtroom Simulator") as demo:
    gr.Markdown("# ⚖️ AI Courtroom Simulator")

    gr.Markdown(
        """
Upload a court case PDF.
The AI system will:
🔍 Investigate Evidence
⚖️ Build Defense Case
⚖️ Build Prosecution Case
🔎 Detect Contradictions
🕸️ Build Knowledge Graph
👨‍⚖️ Generate Final Judgement
"""
    )
    
    pdf_input = gr.File(
        label="Upload Case PDF",
        file_types=[".pdf"]
    )

    submit_btn = gr.Button("Submit Case")

    status_output = gr.Textbox(
        label="Agent Activity",
        interactive=False
    )

    evidence_output = gr.Markdown(label="Evidence Report")
    defense_output = gr.Markdown(label="Defense Report")
    prosecution_output = gr.Markdown(label="Prosecution Report")
    contradiction_output = gr.Markdown(label="Contradiction Report")
    graph_output = gr.Image(label="Knowledge Graph")
    judgement_output = gr.Markdown(label="Final Judgement")

    gr.Markdown("## 📄 Download Reports")

    evidence_pdf = gr.File(label="Evidence PDF")
    defense_pdf = gr.File(label="Defense PDF")
    prosecution_pdf = gr.File(label="Prosecution PDF")
    contradiction_pdf = gr.File(label="Contradiction PDF")
    judgement_pdf = gr.File(label="Judgement PDF")

    submit_btn.click(
        fn=run_courtroom,
        inputs=pdf_input,
        outputs=[
            status_output,
            evidence_output,
            defense_output,
            prosecution_output,
            contradiction_output,
            graph_output,
            judgement_output,
            evidence_pdf,
            defense_pdf,
            prosecution_pdf,
            contradiction_pdf,
            judgement_pdf,
        ]
    )

if __name__ == "__main__":
    demo.launch()
