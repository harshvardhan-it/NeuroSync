from datetime import datetime
from pathlib import Path

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


REPORT_DIR = Path("backend/reports")
REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


class PDFReportService:

    @staticmethod
    def generate_executive_pdf(
        report: dict,
        dataset_id: int
    ):

        filename = (
            REPORT_DIR /
            f"executive_{dataset_id}.pdf"
        )

        doc = SimpleDocTemplate(
            str(filename)
        )

        styles = getSampleStyleSheet()

        content = []

        content.append(
            Paragraph(
                "NeuroSync Executive Report",
                styles["Title"]
            )
        )

        content.append(
            Paragraph(
                f"Generated: {datetime.utcnow()}",
                styles["Normal"]
            )
        )

        content.append(
            Spacer(1, 20)
        )

        content.append(
            Paragraph(
                "Executive Summary",
                styles["Heading1"]
            )
        )

        content.append(
            Paragraph(
                str(
                    report.get(
                        "executive_summary",
                        {}
                    )
                ),
                styles["BodyText"]
            )
        )

        content.append(
            Spacer(1, 10)
        )

        content.append(
            Paragraph(
                "Key Findings",
                styles["Heading1"]
            )
        )

        for finding in report.get(
            "key_findings",
            []
        ):

            content.append(
                Paragraph(
                    f"• {finding}",
                    styles["BodyText"]
                )
            )

        content.append(
            PageBreak()
        )

        content.append(
            Paragraph(
                "Recommendations",
                styles["Heading1"]
            )
        )

        for rec in report.get(
            "recommendations",
            []
        ):

            content.append(
                Paragraph(
                    f"• {rec}",
                    styles["BodyText"]
                )
            )

        content.append(
            Spacer(1, 10)
        )

        content.append(
            Paragraph(
                "Action Plan",
                styles["Heading1"]
            )
        )

        for action in report.get(
            "action_plan",
            []
        ):

            content.append(
                Paragraph(
                    f"• {action}",
                    styles["BodyText"]
                )
            )

        doc.build(content)

        return str(filename)