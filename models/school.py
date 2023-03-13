from datetime import datetime 
from odoo import models,fields, api, _

class StudentStudent(models.Model):
    _name = 'student.student'
    # _description = 'student.student'
    # _rec_name = 'marks'
    _inherit = ['mail.thread','mail.activity.mixin',]


    name = fields.Char(string='Name', tracking=True)
    marks = fields.Integer(string='Marks', tracking=True)
    state = fields.Selection(
        selection=[('in_progress','In Progress'), ('done', 'Done')],
         string='Status', default='in_progress', readonly=True, 
        copy=False, tracking=True)
    child_connection_ids = fields.One2many('student.student.line', 'parent_connection_id', 
    string="Child IDS", )
    # states={'done': [('readonly', True)]}
    reference_no = fields.Char(string='Order Reference', required=True,
                          readonly=True, default=lambda self: _('New'))
    random = fields.Integer(string='R...Number')
    


    def send_message_button(self):
        partner_id = self.env['res.partner'].search([('id', '=' , 3)])
        print('&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        print(partner_id)
        notification_ids = [((0, 0, {
            'res_partner_id': partner_id.id,
            'notification_type': 'inbox'}))]
        user_id = self.env.user.id
        message = ("Untitled #2")
        self.message_post(author_id=user_id,
                            body=(message), 
                            message_type='notification',
                            subtype_xmlid="mail.mt_comment",
                            notification_ids=notification_ids,
                            partner_ids=[user_id],
                            notify_by_email=False,
                            )


    def change_status_button(self):
         self.write({'state': "done"})

    @api.model
    def create(self, vals):
        if vals.get('reference_no', _('New')) == _('New'):
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'student.student') or _('New')
        res = super(StudentStudent, self).create(vals)
        return res

                        
    @api.model    
    def process_demo_scheduler_queue(self):        
        # Contains all records for the model scheduler.demo        
        # scheduler_demo_records = self.env['scheduler.demo'].search([])        
        # # Loop over the records one by one for demo_record in scheduler_demo_records:            
        # number_of_updates = demo_record.number_of_updates + 1            
        # # Update the record with the new number of updates            
        # demo_record.write({               
        #  'number_of_updates': number_of_updates            }) 
        schedule_to_be_rec = self.env['student.student'].search([('name', '=', 'sdf')])
        print('****************************')
        print(schedule_to_be_rec.random)
        schedule_to_be_rec.random = schedule_to_be_rec.random + 1
        print(schedule_to_be_rec.random)




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