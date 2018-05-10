# Copyright 2014 Tecnativa S.L. - Pedro M. Baeza
# Copyright 2015 Tecnativa S.L. - Javier Iniesta
# Copyright 2016 Tecnativa S.L. - Antonio Espinosa
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    event_registration_ids = fields.One2many(
        string="Event registrations", oldname='registrations',
        comodel_name='event.registration', inverse_name="attendee_partner_id")
    registration_count = fields.Integer(
        string='Attendances',
        compute='_compute_registration_count',
        store=False)

    @api.multi
    @api.depends('event_registration_ids')
    def _compute_registration_count(self):
        for partner in self:
            partner.registration_count = len(
                self.env["event.registration"].search([
                    ("attendee_partner_id", "child_of", partner.id),
                    ("state", "not in", ("cancel", "draft")),
                ]).mapped("event_id"))

    @api.multi
    def write(self, data):
        res = super(ResPartner, self).write(data)
        self.mapped('event_registration_ids').partner_data_update(data)
        return res
