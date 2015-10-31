# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time
from openerp.report import report_sxw
from openerp.osv import osv


class add_exam_result(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(add_exam_result, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_result_detail': self._get_result_detail,
        })

    def _get_result_detail(self, subject_ids, result):
        sub_list = []
        result_data = []
        for sub in subject_ids:
            sub_list.append(sub.id)
        sub_obj = self.pool.get('exam.subject')
        subject_exam_ids = sub_obj.search(self.cr, self.uid,
                                          [('id', 'in', sub_list),
                                           ('exam_id', '=', result.id)])
        for subject in sub_obj.browse(self.cr, self.uid, subject_exam_ids):
                result_data.append({
                    'subject': subject.subject_id
                               and subject.subject_id.name or '',
                    'max_mark': subject.maximum_marks or '',
                    'mini_marks': subject.minimum_marks or '',
                    'obt_marks': subject.obtain_marks or '',
                 })
        return result_data


class report_add_exam_result(osv.AbstractModel):

    _name = 'report.exam.exam_result_report'
    _inherit = 'report.abstract_report'
    _template = 'exam.exam_result_report'
    _wrapped_report_class = add_exam_result
