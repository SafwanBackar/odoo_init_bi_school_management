from datetime import datetime
from odoo import models,fields, api

class StudentStudent(models.Model):
    _name = 'student.student'
    # _description = 'student.student'
    # _rec_name = 'marks'


    name = fields.Char(string='Name')
    marks = fields.Integer(string='Marks')
    state = fields.Selection(
        selection=[('in_progress','In Progress'), ('done', 'Done')],
         string='Status', default='in_progress', readonly=True, 
        copy=False, tracking=True)
    child_connection_ids = fields.One2many('student.student.line', 'parent_connection_id', 
    string="Child IDS", )
    # states={'done': [('readonly', True)]}

    def change_status_button(self):
         self.write({'state': "done"})



class StudentStudentOrderLine(models.Model):
    _name = 'student.student.line'

    sale_order_id = fields.Many2one('sale.order',)
    parent_connection_id = fields.Many2one('student.student', string="Parent ID")
    date = fields.Datetime('Date', compute='_compute_sale_date', store=True, readonly=False)

    # @api.onchange('sale_order_id')
    # def onchange_sale_order_id(self):
    #     if self.sale_order_id:
    #         self.date = self.sale_order_id.date_order


    @api.depends('sale_order_id')   
    def _compute_sale_date(self):
        for i in self:
            if i.sale_order_id.date_order:
                i.date = i.sale_order_id.date_order
            else:
                i.date = False


class SaleOrder(models.Model):
    _inherit = "sale.order"


    class_division = fields.Char(string='Class Division')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sub_mark = fields.Integer(string='Sub Mark')