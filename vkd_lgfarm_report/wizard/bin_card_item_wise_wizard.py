import io
import base64
from odoo import models, fields
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


class BinCardItemWiseWizard(models.TransientModel):
    _name = 'bin.card.item.wise.wizard'
    _description = 'BIN Card Item Wise Report Wizard'

    date_from    = fields.Date(string='Date From', required=True, default=fields.Date.context_today)
    date_to      = fields.Date(string='Date To',   required=True, default=fields.Date.context_today)
    product_ids  = fields.Many2many('product.product', string='Products',
                                    help='Leave empty to include all products')
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')
    location_id  = fields.Many2one(
        'stock.location', string='Location',
        domain=[('usage', '=', 'internal')],
    )

    # ── helpers ──────────────────────────────────────────────────────────────
    def _thin_border(self):
        s = Side(style='thin')
        return Border(left=s, right=s, top=s, bottom=s)

    def _fill(self, hex_color):
        return PatternFill(fill_type='solid', fgColor=hex_color)

    def _style_header(self, cell, bg='1F3864'):
        s = Side(style='thin')
        cell.font      = Font(name='Arial', size=9, bold=True, color='FFFFFF')
        cell.fill      = self._fill(bg)
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border    = Border(left=s, right=s, top=s, bottom=s)

    def _style_data(self, cell, horizontal='center', bold=False,
                    bg=None, number_format=None, font_color='000000'):
        s = Side(style='thin')
        cell.font      = Font(name='Arial', size=9, bold=bold, color=font_color)
        cell.alignment = Alignment(horizontal=horizontal, vertical='center')
        cell.border    = Border(left=s, right=s, top=s, bottom=s)
        if bg:
            cell.fill = self._fill(bg)
        if number_format:
            cell.number_format = number_format

    def _get_trans_type(self, move):
        if move.picking_type_id:
            return {'incoming': 'GRN', 'outgoing': 'INV', 'internal': 'INT'}.get(
                move.picking_type_id.code, move.picking_type_id.name)
        return 'ADJ'

    # ── main action ──────────────────────────────────────────────────────────
    def action_print_report(self):
        self.ensure_one()
        wb = Workbook()
        ws = wb.active
        ws.title = 'BIN CARD Item Wise'

        num_fmt  = '#,##0.00'
        date_fmt = 'DD/MM/YYYY'

        # ── column widths ─────────────────────────────────────────────────────
        # Date, Item Code, Item Name, Transactions, Reference No, QTY, Balance
        for i, w in enumerate([14, 14, 26, 14, 26, 12, 12], start=1):
            ws.column_dimensions[get_column_letter(i)].width = w

        # ── Row 1 — Title ─────────────────────────────────────────────────────
        ws.row_dimensions[1].height = 28
        ws.merge_cells('A1:G1')
        ws['A1'].value     = 'BIN CARD - ITEM WISE REPORT'
        ws['A1'].font      = Font(name='Arial', size=14, bold=True)
        ws['A1'].alignment = Alignment(horizontal='center', vertical='center')

        # ── Row 2 — Meta ──────────────────────────────────────────────────────
        ws.row_dimensions[2].height = 18
        ws['A2'].value = 'Company:';  ws['A2'].font = Font(name='Arial', size=9, bold=True)
        ws.merge_cells('B2:C2')
        ws['B2'].value = self.env.company.name
        self._style_data(ws['B2'], horizontal='left')

        ws['D2'].value = 'Date From:'; ws['D2'].font = Font(name='Arial', size=9, bold=True)
        ws['E2'].value = self.date_from
        self._style_data(ws['E2'], number_format=date_fmt)

        ws['F2'].value = 'Date To:';  ws['F2'].font = Font(name='Arial', size=9, bold=True)
        ws['G2'].value = self.date_to
        self._style_data(ws['G2'], number_format=date_fmt)

        # ── Row 4 — Column headers ────────────────────────────────────────────
        ws.row_dimensions[4].height = 22
        headers = ['Date', 'Item Code', 'Item Name', 'Transactions', 'Reference No', 'QTY', 'Balance']
        for col_idx, header in enumerate(headers, start=1):
            cell = ws.cell(row=4, column=col_idx, value=header)
            self._style_header(cell, '1F3864')

        # ── Fetch Data ────────────────────────────────────────────────────────
        if self.location_id:
            target_loc_ids = [self.location_id.id]
        elif self.warehouse_id:
            target_loc_ids = self.env['stock.location'].search([
                ('id', 'child_of', self.warehouse_id.view_location_id.id),
                ('usage', '=', 'internal')
            ]).ids
        else:
            target_loc_ids = self.env['stock.location'].search([
                ('usage', '=', 'internal')
            ]).ids

        domain = [
            ('state', '=', 'done'),
        ]
        if self.product_ids:
            domain.append(('product_id', 'in', self.product_ids.ids))
        
        start_dt = str(self.date_from) + ' 00:00:00'
        end_dt   = str(self.date_to)   + ' 23:59:59'

        data_row = 5
        # Fetch all products that have moves
        products = self.env['product.product'].search(
            [('id', 'in', self.product_ids.ids)] if self.product_ids else [('type', '=', 'consu')],
            order='default_code, name'
        )

        for product in products:
            # 1. Opening Balance
            prior_moves = self.env['stock.move'].search([
                ('product_id', '=', product.id),
                ('state', '=', 'done'),
                ('date', '<', start_dt),
            ])
            running_bal = 0.0
            for m in prior_moves:
                if m.location_dest_id.id in target_loc_ids: running_bal += m.product_qty
                if m.location_id.id      in target_loc_ids: running_bal -= m.product_qty

            # 2. Period Moves
            period_moves = self.env['stock.move'].search([
                ('product_id', '=', product.id),
                ('state', '=', 'done'),
                ('date', '>=', start_dt),
                ('date', '<=', end_dt),
                '|', ('location_id', 'in', target_loc_ids), ('location_dest_id', 'in', target_loc_ids)
            ], order='date asc')

            if not period_moves:
                continue

            for move in period_moves:
                is_in  = move.location_dest_id.id in target_loc_ids
                is_out = move.location_id.id      in target_loc_ids
                
                if is_in and is_out:
                    # Internal transfer - show but net effect is zero
                    qty_change = 0.0
                elif is_in:
                    qty_change = move.product_qty
                elif is_out:
                    qty_change = -move.product_qty
                else:
                    continue

                running_bal += qty_change
                trans_type   = self._get_trans_type(move)
                ref          = move.reference or move.origin or ''

                row_values = [
                    move.date.date(),
                    product.default_code or '',
                    product.name,
                    trans_type,
                    ref,
                    abs(qty_change) if not (is_in and is_out) else 0.0,
                    running_bal
                ]

                ws.row_dimensions[data_row].height = 18
                for col_idx, val in enumerate(row_values, start=1):
                    cell = ws.cell(row=data_row, column=col_idx, value=val)
                    if col_idx == 1:
                        self._style_data(cell, number_format=date_fmt)
                    elif col_idx in (2, 3, 5):
                        self._style_data(cell, horizontal='left')
                    elif col_idx in (6, 7):
                        self._style_data(cell, horizontal='right', number_format=num_fmt)
                    else:
                        self._style_data(cell)
                data_row += 1

        # ── Save & return ─────────────────────────────────────────────────────
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        file_data = base64.b64encode(output.read())
        output.close()

        att = self.env['ir.attachment'].create({
            'name':     f'BIN_Card_ItemWise_{self.date_from}_{self.date_to}.xlsx',
            'type':     'binary',
            'datas':    file_data,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })
        return {
            'type':   'ir.actions.act_url',
            'url':    f'/web/content/{att.id}?download=true',
            'target': 'self',
        }