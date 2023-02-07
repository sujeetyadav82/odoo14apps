from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError
import datetime


class PurchaseRequisition(models.Model):
    _name = 'purchase.requisitions'
    _description = 'Product purchase requisition by user/employee'
    _rec_name = 'ref'

    ref = fields.Char(default=lambda self: _('New'))
    employee = fields.Many2one('hr.employee', string="Employee")
    department = fields.Many2one('hr.department', string="Department")
    requi_resp = fields.Many2one('res.users', string='Requisition Responsible')
    requi_date = fields.Date(string='Requisition Date')
    recived_date = fields.Date(string="Recieved Date")
    requi_deadline = fields.Date(string='Requisition Deadline')
    company = fields.Many2one('res.company')
    state = fields.Selection([('new', 'New'),
                              ('waiting department approval', 'Waiting Department Approval'),
                              ('waiting ir approval', 'Waiting IR Approval'),
                              ('approved', 'Approved'),
                              ('purchase order created', 'Purchase Order Created'),
                              ('received', 'Received'),
                              ('rejected', 'Rejected'),
                              ('cancel', 'Cancel'),
                              ], string='state', readonly=True, default='new')
    purchase_line_ids = fields.One2many('purchase.requisitions.line', 'rel')
    confirmed_by = fields.Many2one('res.users', 'Confirmed By')
    department_mng = fields.Many2one('res.users', 'Department Manager')
    approved_by = fields.Many2one('res.users', 'Approved By')
    rejected_by = fields.Many2one('res.users', 'Rejected By')
    confirmed_dt = fields.Date('Confirmed Date')
    department_mng_dt = fields.Date('Department Manager Approval Date')
    approved_dt = fields.Date('Approved Date')
    rejected_dt = fields.Date('Rejected Date')
    purchase_count = fields.Integer(compute="compute_purchase")

    @api.model
    def create(self, vals):
        if vals.get('ref', _('New') == _('New')):
            vals['ref'] = self.env['ir.sequence'].next_by_code('Purchase.Sequence')
        return super(PurchaseRequisition, self).create(vals)

    def state_confirm(self):
        self.state = 'waiting department approval'
        for rec in self:
            rec.confirmed_by = self._uid
        self.confirmed_dt = datetime.date.today()

    def state_cancel(self):
        self.state = 'cancel'
        if self.state == 'cancel':
            self.confirmed_by = None
            self.confirmed_dt = None
            self.department_mng = None
            self.department_mng_dt = None
            self.approved_dt = None
            self.rejected_by = None
            self.rejected_dt = None

    def state_department_approval(self):
        self.state = 'waiting ir approval'
        for rec in self:
            rec.department_mng = self._uid
        self.department_mng_dt = datetime.date.today()

    def state_approval(self):
        self.state = 'approved'
        for rec in self:
            rec.approved_by = self._uid
        self.approved_dt = datetime.date.today()

    def state_reject(self):
        self.state = 'rejected'
        for rec in self:
            rec.rejected_by = self._uid
        self.rejected_dt = datetime.date.today()

    def state_received(self):
        self.state = 'received'

    def unlink(self):
        for order in self:
            if order.state not in ('cancel'):
                raise UserError(
                    _('You can not delete a sent quotation or a confirmed sales order. You must first cancel it.'))
        return super(PurchaseRequisition, self).unlink()

    def create_po(self):
        self.state = 'purchase order created'
        for line in self.purchase_line_ids:
            if line.requisition_action == 'purchase_order':
                dict = {
                    'partner_id': line.vendor_id.id,
                    'date_order': self.requi_deadline,
                    'origin': self.ref,
                    'order_line': [(0, 0, {
                        'product_id': line.order_line.id,  # give id of partner
                        'product_qty': line.product_qty
                    })]}
                self.env['purchase.order'].create(dict)

    def compute_purchase(self):
        for record in self:
            record.purchase_count = self.env['purchase.order'].search_count([('origin', '=', self.ref)])

    def get_vehicles(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
        }


class RequisitionLine(models.Model):
    _name = 'purchase.requisitions.line'

    rel = fields.Many2one('purchase.requisitions')
    order_line = fields.Many2one('product.product', string="Product")
    name = fields.Text(string="Description")
    product_qty = fields.Integer(string="Quantity")

    uom_id = fields.Many2one('uom.uom', string="Unit of Measure")
    vendor_id = fields.Many2many('res.partner', string="Vendor")
    requisition_action = fields.Selection([('purchase_order', 'Purchase order'),
                                           ('picking', 'Picking')], string="Requisition Action")

    @api.onchange('order_line')
    def onchange_product(self):
        if self.order_line:
            self.name = self.order_line.name
            self.product_qty = 1


class Eml(models.Model):
    _inherit = 'hr.employee'

    destination_lo = fields.Many2one('stock.location')


class Dep(models.Model):
    _inherit = 'hr.department'

    destination_location = fields.Many2one('stock.location')
