import io
import base64
from odoo import models, fields
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


class BinCardWizard(models.TransientModel):
    _name = 'bin.card.wizard'
    _description = 'BIN Card Report Wizard'

    date_from    = fields.Date(string='Date From', required=True, default=fields.Date.context_today)
    date_to      = fields.Date(string='Date To',   required=True, default=fields.Date.context_today)
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

    def _apply(self, cell, font=None, fill=None, align=None, border=None, number_format=None):
        if font:          cell.font          = font
        if fill:          cell.fill          = fill
        if align:         cell.alignment     = align
        if border:        cell.border        = border
        if number_format: cell.number_format = number_format

    def _style_header(self, cell, bg='1F3864'):
        self._apply(
            cell,
            font=Font(name='Arial', size=9, bold=True, color='FFFFFF'),
            fill=self._fill(bg),
            align=Alignment(horizontal='center', vertical='center', wrap_text=True),
            border=self._thin_border(),
        )

    def _style_data(self, cell, horizontal='center', number_format=None):
        self._apply(
            cell,
            font=Font(name='Arial', size=9),
            align=Alignment(horizontal=horizontal, vertical='center'),
            border=self._thin_border(),
            number_format=number_format,
        )

    def _get_trans_type(self, move):
        if move.picking_type_id:
            return {'incoming': 'GRN', 'outgoing': 'INV', 'internal': 'INT'}.get(
                move.picking_type_id.code, move.picking_type_id.name)
        return 'ADJ'

    def _get_opening_balance(self, product_id, move_date, location_id):
        prior = self.env['stock.move'].search([
            ('product_id', '=', product_id),
            ('state', '=', 'done'),
            ('date', '<', move_date),
        ])
        qty = 0.0
        for m in prior:
            if location_id:
                if m.location_dest_id == location_id:   qty += m.product_qty
                elif m.location_id    == location_id:   qty -= m.product_qty
            else:
                if m.location_dest_id.usage == 'internal': qty += m.product_qty
                if m.location_id.usage      == 'internal': qty -= m.product_qty
        return qty

    # ── main action ──────────────────────────────────────────────────────────
    def action_print_report(self):
        self.ensure_one()
        wb = Workbook()
        ws = wb.active
        ws.title = 'BIN CARD'

        border      = self._thin_border()
        dark_blue   = '1F3864'
        mid_blue    = '2E75B6'
        center_wrap = Alignment(horizontal='center', vertical='center', wrap_text=True)
        center      = Alignment(horizontal='center', vertical='center')
        left        = Alignment(horizontal='left',   vertical='center')
        right       = Alignment(horizontal='right',  vertical='center')
        num_fmt     = '#,##0.00'
        val_fmt     = '#,##0.00'

        # ── column widths ────────────────────────────────────────────────────
        # 18 columns: A(Code), B(Name), C(UOM), D-F(Open), G-I(Recv), J-L(Issue), M-O(Adj), P-R(Closing)
        col_widths = [14, 24, 10, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12]
        for i, w in enumerate(col_widths, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w

        # ── Row 1 — Title ────────────────────────────────────────────────────
        ws.row_dimensions[1].height = 28
        ws.merge_cells('A1:R1')
        title_cell = ws['A1']
        title_cell.value = 'BIN CARD REPORT'
        title_cell.font      = Font(name='Arial', size=14, bold=True)
        title_cell.alignment = center

        # ── Row 2 — Meta ─────────────────────────────────────────────────────
        ws.row_dimensions[2].height = 18
        ws['A2'].value = 'Company:';  ws['A2'].font = Font(name='Arial', size=9, bold=True)
        ws.merge_cells('B2:C2')
        ws['B2'].value = self.env.company.name
        self._style_data(ws['B2'], horizontal='left')

        ws['D2'].value = 'Date From:'; ws['D2'].font = Font(name='Arial', size=9, bold=True)
        ws['E2'].value = self.date_from
        self._style_data(ws['E2'], number_format='DD/MM/YYYY')

        ws['F2'].value = 'Date To:';  ws['F2'].font = Font(name='Arial', size=9, bold=True)
        ws['G2'].value = self.date_to
        self._style_data(ws['G2'], number_format='DD/MM/YYYY')

        # ── Row 4 — Group headers ─────────────────────────────────────────────
        ws.row_dimensions[4].height = 32
        for col in ['A', 'B', 'C']:
            ws.merge_cells(f'{col}4:{col}5')
            self._style_header(ws[f'{col}4'], dark_blue)

        ws['A4'].value = 'Item Code'
        ws['B4'].value = 'Item Name'
        ws['C4'].value = 'UOM'

        merge_groups = [
            ('D4', 'F4', 'Open Balance'),
            ('G4', 'I4', 'Receipts'),
            ('J4', 'L4', 'Issues'),
            ('M4', 'O4', 'Adjustments'),
            ('P4', 'R4', 'Closing Balance'),
        ]
        for start, end, label in merge_groups:
            ws.merge_cells(f'{start}:{end}')
            ws[start].value = label
            self._style_header(ws[start], mid_blue)

        # ── Row 5 — Sub-headers ───────────────────────────────────────────────
        ws.row_dimensions[5].height = 22
        sub_headers = ['Quantity', 'Per Value', 'Value'] * 5
        for i, val in enumerate(sub_headers, start=4):
            cell = ws.cell(row=5, column=i, value=val)
            self._style_header(cell, mid_blue)

        # ── Data Collection ───────────────────────────────────────────────────
        # Determine target locations
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

        # Fetch products
        products = self.env['product.product'].search([('type', '=', 'consu')], order='default_code, name')
        # Wait, usually we want 'product' (storable) in Odoo 18, it's 'consu' with 'is_storable' or similar
        # In Odoo 18, the type for storable is 'consu' but we check if it's storable.
        # Actually, let's just get all products that have stock moves.
        product_ids_with_moves = self.env['stock.move'].search([
            ('state', '=', 'done'),
        ]).mapped('product_id')
        products = product_ids_with_moves.sorted(key=lambda p: (p.default_code or '', p.name or ''))

        data_row = 6
        for product in products:
            # 1. Opening Balance
            # We need qty at date_from 00:00:00
            start_dt = str(self.date_from) + ' 00:00:00'
            end_dt   = str(self.date_to)   + ' 23:59:59'

            # Opening Qty
            prior_moves = self.env['stock.move'].search([
                ('product_id', '=', product.id),
                ('state', '=', 'done'),
                ('date', '<', start_dt),
            ])
            open_qty = 0.0
            for m in prior_moves:
                if m.location_dest_id.id in target_loc_ids: open_qty += m.product_qty
                if m.location_id.id      in target_loc_ids: open_qty -= m.product_qty

            # 2. Period Moves
            period_moves = self.env['stock.move'].search([
                ('product_id', '=', product.id),
                ('state', '=', 'done'),
                ('date', '>=', start_dt),
                ('date', '<=', end_dt),
                '|', ('location_id', 'in', target_loc_ids), ('location_dest_id', 'in', target_loc_ids)
            ])

            qty_receipt = 0.0
            qty_issue   = 0.0
            qty_adj     = 0.0

            for m in period_moves:
                is_in  = m.location_dest_id.id in target_loc_ids
                is_out = m.location_id.id      in target_loc_ids
                
                if is_in and is_out:
                    # Internal transfer within our target set - ignore for total balance
                    continue
                
                if is_in:
                    # Incoming to our target set
                    if m.location_id.usage == 'supplier':
                        qty_receipt += m.product_qty
                    elif m.location_id.usage in ('inventory', 'production'):
                        qty_adj += m.product_qty
                    else:
                        # Other non-internal sources (e.g. transit or other warehouses)
                        qty_receipt += m.product_qty
                elif is_out:
                    # Outgoing from our target set
                    if m.location_dest_id.usage == 'customer':
                        qty_issue += m.product_qty
                    elif m.location_dest_id.usage in ('inventory', 'production'):
                        qty_adj -= m.product_qty
                    else:
                        # Other non-internal destinations
                        qty_issue += m.product_qty

            closing_qty = open_qty + qty_receipt - qty_issue + qty_adj
            per_value   = product.standard_price

            row_data = [
                product.default_code or '',
                product.name,
                product.uom_id.name,
                open_qty, per_value, open_qty * per_value,
                qty_receipt, per_value, qty_receipt * per_value,
                qty_issue, per_value, qty_issue * per_value,
                qty_adj, per_value, qty_adj * per_value,
                closing_qty, per_value, closing_qty * per_value,
            ]

            ws.row_dimensions[data_row].height = 18
            for col_idx, value in enumerate(row_data, start=1):
                cell = ws.cell(row=data_row, column=col_idx, value=value)
                if col_idx <= 3:
                    self._style_data(cell, horizontal='left' if col_idx == 2 else 'center')
                else:
                    self._style_data(cell, horizontal='right', number_format=num_fmt)
            data_row += 1

        # ── Save & return ─────────────────────────────────────────────────────
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        file_data = base64.b64encode(output.read())
        output.close()

        att = self.env['ir.attachment'].create({
            'name':     f'BIN_Card_{self.date_from}_{self.date_to}.xlsx',
            'type':     'binary',
            'datas':    file_data,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })
        return {
            'type':   'ir.actions.act_url',
            'url':    f'/web/content/{att.id}?download=true',
            'target': 'self',
        }