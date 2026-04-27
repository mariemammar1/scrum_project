from flask import Blueprint, send_file
from reportlab.pdfgen import canvas
from models import Article, StockOperation
import pandas as pd

export_bp = Blueprint("export", __name__)

# PDF stats
@export_bp.route("/export/stats/pdf")
def export_stats_pdf():
    file = "stats.pdf"
    c = canvas.Canvas(file)

    y = 800

    for a in Article.query.all():
        c.drawString(50, y, f"{a.title} - Stock: {a.stock}")
        y -= 20

    for o in StockOperation.query.all():
        c.drawString(50, y, f"{o.type} - {o.quantity}")
        y -= 20

    c.save()
    return send_file(file, as_attachment=True)


# EXCEL export
@export_bp.route("/export/stats/excel")
def export_excel():
    data = [{
        "title": a.title,
        "stock": a.stock,
        "price": a.price
    } for a in Article.query.all()]

    df = pd.DataFrame(data)
    file = "stats.xlsx"
    df.to_excel(file, index=False)

    return send_file(file, as_attachment=True)
@export_bp.route("/export/kpis/pdf")
def export_kpis():
    from reportlab.pdfgen import canvas

    file = "kpis.pdf"
    c = canvas.Canvas(file)

    c.drawString(50, 800, "Dashboard KPIs")

    c.drawString(50, 780, f"Articles: {Article.query.count()}")
    c.drawString(50, 760, f"Stock: {sum([a.stock for a in Article.query.all()])}")
    c.drawString(50, 740, f"Entries: {StockOperation.query.filter_by(type='ENTRY').count()}")
    c.drawString(50, 720, f"Exits: {StockOperation.query.filter_by(type='EXIT').count()}")

    c.save()
    return send_file(file, as_attachment=True)