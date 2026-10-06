"""
Report Generator Service
Produces formal, audit-ready cybersecurity privacy assessment reports
in HTML and direct PDF formats with zero sensitive PII leakage.
"""

import io
import datetime
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def generate_html_report(assessment_data: Dict[str, Any]) -> str:
    """
    Generates a standalone, beautifully styled HTML privacy assessment report
    suitable for immediate browser viewing and PDF printing.
    """
    assessment_id = assessment_data.get("assessment_id", "ASSESS-DEMO")
    created_at = assessment_data.get("created_at", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    overall_score = assessment_data.get("overall_score", 0.0)
    risk_level = assessment_data.get("risk_level", "LOW")
    category_scores = assessment_data.get("category_scores", {})
    findings = assessment_data.get("findings", [])
    recommendations = assessment_data.get("recommendations", [])

    badge_color = {
        "LOW": "#10b981",
        "MODERATE": "#3b82f6",
        "HIGH": "#f59e0b",
        "CRITICAL": "#ef4444"
    }.get(risk_level, "#6b7280")

    cat_rows = ""
    for cat_id, cat_info in category_scores.items():
        name = cat_info.get("name", cat_id)
        score = cat_info.get("score", 0)
        c_level = cat_info.get("risk_level", "LOW")
        c_color = cat_info.get("color", "#10b981")
        cat_rows += f"""
        <tr>
            <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; font-weight: 500;">{name}</td>
            <td style="padding: 10px; border-bottom: 1px solid #e2e8f0;">
                <div style="background: #e2e8f0; border-radius: 9999px; height: 10px; width: 100%; overflow: hidden;">
                    <div style="background: {c_color}; height: 10px; width: {score}%;"></div>
                </div>
            </td>
            <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; text-align: right; font-weight: 600;">{score}/100</td>
            <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; text-align: center;">
                <span style="background: {c_color}20; color: {c_color}; font-weight: 600; font-size: 0.8rem; padding: 2px 8px; border-radius: 6px;">{c_level}</span>
            </td>
        </tr>
        """

    findings_html = ""
    if findings:
        for f in findings:
            sev = f.get("severity", "LOW")
            sev_col = {"CRITICAL": "#ef4444", "HIGH": "#f59e0b", "MODERATE": "#3b82f6", "LOW": "#10b981"}.get(sev, "#6b7280")
            findings_html += f"""
            <div style="margin-bottom: 14px; padding: 14px; border-left: 4px solid {sev_col}; background: #f8fafc; border-radius: 4px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <strong style="color: #0f172a; font-size: 0.95rem;">{f.get('title')}</strong>
                    <span style="background: {sev_col}; color: #fff; font-size: 0.75rem; font-weight: 700; padding: 2px 6px; border-radius: 4px;">{sev}</span>
                </div>
                <p style="margin: 0 0 6px 0; color: #475569; font-size: 0.875rem;">{f.get('description')}</p>
                <div style="font-size: 0.8rem; color: #64748b;"><strong>Security Impact:</strong> {f.get('risk_impact')}</div>
            </div>
            """
    else:
        findings_html = "<p style='color: #10b981;'>No critical vulnerabilities identified. Standard defensive posture maintained.</p>"

    recs_html = ""
    if recommendations:
        for r in recommendations:
            prio = r.get("priority", "IMPORTANT")
            prio_col = {"IMMEDIATE": "#ef4444", "IMPORTANT": "#f59e0b", "GOOD PRACTICE": "#3b82f6"}.get(prio, "#64748b")
            steps_items = "".join([f"<li style='margin-bottom: 4px;'>{s}</li>" for s in r.get("steps", [])])
            recs_html += f"""
            <div style="margin-bottom: 16px; padding: 14px; border: 1px solid #e2e8f0; border-radius: 8px; background: #ffffff;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="font-weight: 700; color: #0f172a; font-size: 0.95rem;">{r.get('action')}</span>
                    <span style="color: {prio_col}; font-weight: 700; font-size: 0.75rem; border: 1px solid {prio_col}; padding: 2px 8px; border-radius: 4px;">{prio} PRIORITY</span>
                </div>
                <p style="margin: 0 0 8px 0; color: #334155; font-size: 0.85rem;"><strong>Rationale:</strong> {r.get('rationale')}</p>
                <ol style="margin: 0; padding-left: 20px; color: #475569; font-size: 0.825rem;">
                    {steps_items}
                </ol>
            </div>
            """
    else:
        recs_html = "<p style='color: #475569;'>No immediate remediation actions required.</p>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Assessment Report - {assessment_id}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #f1f5f9;
            color: #1e293b;
            margin: 0;
            padding: 30px;
        }}
        .report-container {{
            max-width: 900px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #0f172a;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .logo-title h1 {{
            margin: 0;
            font-size: 1.5rem;
            color: #0f172a;
        }}
        .logo-title p {{
            margin: 4px 0 0 0;
            color: #64748b;
            font-size: 0.875rem;
        }}
        .meta-box {{
            text-align: right;
            font-size: 0.85rem;
            color: #64748b;
        }}
        .score-hero {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 24px;
            display: flex;
            justify-content: space-around;
            align-items: center;
            margin-bottom: 30px;
        }}
        .score-circle {{
            text-align: center;
        }}
        .score-value {{
            font-size: 3rem;
            font-weight: 800;
            color: {badge_color};
            line-height: 1;
        }}
        .section-title {{
            font-size: 1.15rem;
            font-weight: 700;
            color: #0f172a;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 8px;
            margin-top: 30px;
            margin-bottom: 16px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .checklist-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 15px;
        }}
        .checklist-item {{
            background: #f8fafc;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.85rem;
            color: #334155;
            border: 1px solid #e2e8f0;
        }}
        .disclaimer-box {{
            margin-top: 40px;
            padding: 16px;
            background: #fef2f2;
            border: 1px solid #fecaca;
            border-radius: 8px;
            font-size: 0.775rem;
            color: #991b1b;
        }}
        .print-btn {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #0f172a;
            color: #ffffff;
            padding: 12px 20px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}
        @media print {{
            body {{ background: #fff; padding: 0; }}
            .report-container {{ box-shadow: none; padding: 0; max-width: 100%; }}
            .print-btn {{ display: none; }}
        }}
    </style>
</head>
<body>
    <button class="print-btn" onclick="window.print()">Print / Save PDF</button>

    <div class="report-container">
        <div class="header">
            <div class="logo-title">
                <h1>Social Media Privacy Risk Assessment Report</h1>
                <p>Industry-Oriented Defensive Exposure & Account Security Evaluation</p>
            </div>
            <div class="meta-box">
                <div><strong>Assessment ID:</strong> {assessment_id}</div>
                <div><strong>Date Generated:</strong> {created_at}</div>
                <div><strong>Assessment Model:</strong> DEFENSIVE v2.4</div>
            </div>
        </div>

        <div class="score-hero">
            <div class="score-circle">
                <div class="score-value">{overall_score}</div>
                <div style="color: #64748b; font-size: 0.85rem; margin-top: 4px;">PRIVACY RISK SCORE (0–100)</div>
            </div>
            <div style="border-left: 1px solid #cbd5e1; height: 60px;"></div>
            <div style="text-align: center;">
                <div style="font-size: 1.8rem; font-weight: 800; color: {badge_color};">{risk_level}</div>
                <div style="color: #64748b; font-size: 0.85rem; margin-top: 4px;">ASSESSED RISK TIER</div>
            </div>
            <div style="border-left: 1px solid #cbd5e1; height: 60px;"></div>
            <div style="text-align: left; max-width: 250px; font-size: 0.85rem; color: #475569;">
                Higher score designates greater digital footprint, exposed personal data, and weaker configuration settings.
            </div>
        </div>

        <div class="section-title">1. Category-Wise Risk Breakdown</div>
        <table>
            <thead>
                <tr style="background: #f8fafc; font-size: 0.8rem; color: #475569; text-transform: uppercase;">
                    <th style="padding: 10px; text-align: left;">Category</th>
                    <th style="padding: 10px; text-align: left; width: 40%;">Risk Visualizer</th>
                    <th style="padding: 10px; text-align: right;">Score</th>
                    <th style="padding: 10px; text-align: center;">Tier</th>
                </tr>
            </thead>
            <tbody>
                {cat_rows}
            </tbody>
        </table>

        <div class="section-title">2. Detected Privacy Weaknesses & Vulnerabilities</div>
        {findings_html}

        <div class="section-title">3. Personalized Actionable Remediation Guidance</div>
        {recs_html}

        <div class="section-title">4. Comprehensive Social Media Privacy Checklist</div>
        <div class="checklist-grid">
            <div class="checklist-item">☑ Restrict main profile visibility to Friends/Connections only</div>
            <div class="checklist-item">☑ Hide personal phone number and personal email address</div>
            <div class="checklist-item">☑ Conceal birth year or hide entire birth date from public view</div>
            <div class="checklist-item">☑ Disable real-time location check-ins and camera geotagging</div>
            <div class="checklist-item">☑ Adopt retrospective travel sharing (post only after departure)</div>
            <div class="checklist-item">☑ Enable Timeline Tag Review to approve tags before display</div>
            <div class="checklist-item">☑ Decline unverified connection requests from unfamiliar profiles</div>
            <div class="checklist-item">☑ Enable Multi-Factor Authentication via TOTP Authenticator App</div>
            <div class="checklist-item">☑ Use a Password Manager for isolated unique 16+ char passwords</div>
            <div class="checklist-item">☑ Activate unrecognized device login alerts</div>
            <div class="checklist-item">☑ Revoke authorizations for stale/unused third-party applications</div>
            <div class="checklist-item">☑ Execute 'Limit Past Posts' to batch-restrict historical public timeline</div>
        </div>

        <div class="disclaimer-box">
            <strong>Defensive Cybersecurity & Educational Disclaimer:</strong><br>
            This assessment is conducted strictly for educational risk awareness and posture evaluation. It analyzes self-reported configuration indicators under privacy-by-design principles and does NOT inspect, access, scrape, or monitor private social media accounts or external profiles. A low risk score indicates adherence to defensive best practices but does not guarantee immunity from sophisticated targeted cyberattacks.
        </div>
    </div>
</body>
</html>
    """
    return html


def generate_pdf_report_bytes(assessment_data: Dict[str, Any]) -> bytes:
    """
    Generates a formal PDF report using ReportLab with tables, styles, and findings.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'RepTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'RepSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=15
    )
    heading2_style = ParagraphStyle(
        'RepH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'RepBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#334155')
    )

    story = []

    # Title & Header
    story.append(Paragraph("Social Media Privacy Risk Assessment Report", title_style))
    story.append(Paragraph("Defensive Exposure & Account Security Framework | Educational Evaluation", subtitle_style))

    # Meta table
    assessment_id = assessment_data.get("assessment_id", "ASSESS-DEMO")
    created_at = assessment_data.get("created_at", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    overall_score = assessment_data.get("overall_score", 0.0)
    risk_level = assessment_data.get("risk_level", "LOW")

    meta_data = [
        [Paragraph(f"<b>Assessment ID:</b> {assessment_id}", body_style), Paragraph(f"<b>Date:</b> {created_at}", body_style)],
        [Paragraph(f"<b>Overall Risk Score:</b> <font size='12' color='#ef4444'><b>{overall_score}/100</b></font>", body_style),
         Paragraph(f"<b>Risk Level:</b> <b>{risk_level}</b>", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[270, 270])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # Category Scores Table
    story.append(Paragraph("1. Category Risk Analysis (0 = Lower Risk, 100 = Higher Risk)", heading2_style))
    cat_data = [["Category", "Risk Score", "Risk Tier"]]
    for cat_id, cat_info in assessment_data.get("category_scores", {}).items():
        cat_data.append([
            cat_info.get("name", cat_id),
            f"{cat_info.get('score', 0)}/100",
            cat_info.get("risk_level", "LOW")
        ])

    cat_table = Table(cat_data, colWidths=[260, 140, 140])
    cat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    story.append(cat_table)
    story.append(Spacer(1, 14))

    # Top Findings
    story.append(Paragraph("2. Top Detected Privacy Weaknesses", heading2_style))
    findings = assessment_data.get("findings", [])
    if findings:
        for f in findings[:6]:  # top 6
            story.append(Paragraph(f"• <b>[{f.get('severity')}] {f.get('title')}</b>", ParagraphStyle('FTitle', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor('#0f172a'))))
            story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;{f.get('description')} <i>(Impact: {f.get('risk_impact')})</i>", body_style))
            story.append(Spacer(1, 4))
    else:
        story.append(Paragraph("No critical weaknesses detected.", body_style))

    story.append(Spacer(1, 10))

    # Recommendations
    story.append(Paragraph("3. Priority Remediation Guidance", heading2_style))
    recs = assessment_data.get("recommendations", [])
    if recs:
        for r in recs[:5]:  # top 5
            story.append(Paragraph(f"• <b>[{r.get('priority')}] {r.get('action')}</b>", ParagraphStyle('RTitle', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor('#1d4ed8'))))
            story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;Rationale: {r.get('rationale')}", body_style))
            story.append(Spacer(1, 4))
    else:
        story.append(Paragraph("Standard privacy practices met.", body_style))

    story.append(Spacer(1, 14))

    # Disclaimer
    disclaimer_text = (
        "<b>Educational & Defensive Disclaimer:</b> This report is generated based on self-reported "
        "configuration responses. It does NOT scrape private profiles, bypass authorization, or monitor live users. "
        "Developed under Privacy-by-Design and Data Minimization principles."
    )
    story.append(Paragraph(disclaimer_text, ParagraphStyle('Disc', parent=body_style, fontSize=7, leading=9, textColor=colors.HexColor('#64748b'))))

    doc.build(story)
    return buffer.getvalue()
