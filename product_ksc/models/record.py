from odoo import models,fields
class ResProduct(models.Model):
    _name="product.ksc"
    _description="This is data about product"
    _rec_name="product_name"
    product_name=fields.Char(string="Product Name" )
    sku_product=fields.Char(string="SKU Of Product" )
    barcode=fields.Char(string="Barcode" )
    can_this_product_be_sold=fields.Boolean(string="Can this product be sold" )
    product_type=fields.Selection([
        ('storable','Storable'),
        ('consumable','Consumable'),
        ('service','Service')
    ],string="Product Type")
    sale_price=fields.Float(string="Sale price",digits=(6,2))
    cost_price=fields.Float(string="Cost price",digits=(6,2))
    unit_price=fields.Float(string="Unit price",digits=(6,2))
    active_product=fields.Boolean(strings="Active")
    warehouse=fields.Char(string="Warehouse" )
    product_image=fields.Image(String="Product Image")
    website_desc=fields.Html(string="Website Desc." )
    note=fields.Text(string="Internal Note" )
    product_stock=fields.Float(string="Product Stock")
    tax_ids=fields.Many2many('account.tax.ksc',domain=[('tax_use','=','sales')])
    def stock_update1(self):
        return self.env['ir.actions.act_window']._for_xml_id("stock_warehouse.stock_update1_action")



