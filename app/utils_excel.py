"""
Excel export utilities.

Functions for generating Excel files from data.
"""
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from typing import List, Dict, Any
from datetime import datetime
from fastapi.responses import Response


def generate_finance_xlsx(entries: List[Dict[str, Any]], target_date: str) -> bytes:
    """
    Generate Excel file for finance entries of a specific date.
    
    Args:
        entries: List of finance entry dictionaries
        target_date: Target date in YYYY-MM-DD format
    
    Returns:
        Excel file as bytes
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Fluxo de Caixa"
    
    # Header style
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=12)
    header_alignment = Alignment(horizontal="center", vertical="center")
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Title
    ws.merge_cells('A1:F1')
    title_cell = ws['A1']
    title_cell.value = f"Relatório de Fluxo de Caixa - {target_date}"
    title_cell.font = Font(bold=True, size=14)
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 25
    
    # Headers
    headers = [
        "Data/Hora",
        "Tipo",
        "Valor",
        "Método de Pagamento",
        "Categoria",
        "Descrição"
    ]
    
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=3, column=col_num)
        cell.value = header
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_alignment
        cell.border = border
    
    # Data rows
    row_num = 4
    total_income = 0.0
    total_expense = 0.0
    
    for entry in entries:
        # Extract date and time
        date_time = entry.get('date_time', '')
        if 'T' in date_time:
            date_part, time_part = date_time.split('T')
            formatted_datetime = f"{date_part} {time_part[:5]}"
        else:
            formatted_datetime = date_time
        
        entry_type = entry.get('type', '').upper()
        amount = float(entry.get('amount', 0))
        payment_method = entry.get('payment_method', '').upper()
        category = entry.get('category', '') or '-'
        description = entry.get('description', '') or '-'
        
        # Calculate totals
        if entry_type.lower() == 'income':
            total_income += amount
        else:
            total_expense += amount
        
        # Write row data
        ws.cell(row=row_num, column=1, value=formatted_datetime).border = border
        ws.cell(row=row_num, column=2, value=entry_type).border = border
        ws.cell(row=row_num, column=3, value=amount).border = border
        ws.cell(row=row_num, column=4, value=payment_method).border = border
        ws.cell(row=row_num, column=5, value=category).border = border
        ws.cell(row=row_num, column=6, value=description).border = border
        
        # Format amount column
        amount_cell = ws.cell(row=row_num, column=3)
        amount_cell.number_format = '#,##0.00'
        amount_cell.alignment = Alignment(horizontal="right")
        
        row_num += 1
    
    # Summary section
    summary_row = row_num + 2
    ws.cell(row=summary_row, column=2, value="TOTAL RECEITAS:").font = Font(bold=True)
    ws.cell(row=summary_row, column=3, value=total_income).font = Font(bold=True)
    ws.cell(row=summary_row, column=3).number_format = '#,##0.00'
    ws.cell(row=summary_row, column=3).alignment = Alignment(horizontal="right")
    
    summary_row += 1
    ws.cell(row=summary_row, column=2, value="TOTAL DESPESAS:").font = Font(bold=True)
    ws.cell(row=summary_row, column=3, value=total_expense).font = Font(bold=True)
    ws.cell(row=summary_row, column=3).number_format = '#,##0.00'
    ws.cell(row=summary_row, column=3).alignment = Alignment(horizontal="right")
    
    summary_row += 1
    balance = total_income - total_expense
    ws.cell(row=summary_row, column=2, value="SALDO:").font = Font(bold=True, size=12)
    ws.cell(row=summary_row, column=3, value=balance).font = Font(bold=True, size=12)
    ws.cell(row=summary_row, column=3).number_format = '#,##0.00'
    ws.cell(row=summary_row, column=3).alignment = Alignment(horizontal="right")
    
    # Color balance cell
    balance_cell = ws.cell(row=summary_row, column=3)
    if balance >= 0:
        balance_cell.fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    else:
        balance_cell.fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    
    # Auto-adjust column widths
    column_widths = [20, 12, 15, 20, 20, 40]
    for col_num, width in enumerate(column_widths, 1):
        ws.column_dimensions[get_column_letter(col_num)].width = width
    
    # Set row heights
    ws.row_dimensions[3].height = 20
    
    # Save to bytes
    from io import BytesIO
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    return output.getvalue()

