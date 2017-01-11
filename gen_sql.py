#!/usr/bin/python
# -*- coding: UTF-8 -*-

import copy
import datetime
import json
import re
import sys
import traceback

import math
import tornado.locale

supported_udafs = [
    'max_date',
    'min_date',
    'array_intersect',
    'array_union',
    'collect_set',
    'bol',
    'ltd'
]

def has_udaf(meta):
    if meta.get('formula', ''):
        for udaf in supported_udafs:
            if udaf.lower() in meta['formula'].lower():
                return True
    return False


def use_inner_filter(where):
    if str(where.get('is_inner', '')) == '1':
        if where.get('data_type', '') == 'date':
            return True
        else:
            return where.get('inner_range', [])
    return False

def gen_where(where, gen_for=0):
    """
    :param gen_for:  不同高级计算需要不同的生成规则
    :return:
    """
    wheres = []
    for f in copy.deepcopy(where):
        if not f.get('is_all', False) or use_inner_filter(f):
            if not has_udaf(f):
                filter_factory = field_based_filter_factory.FieldBasedFilterFactory()
                f = filter_factory.create(f, self.work_table, ct_id=self.ct_id)
                expr = f.to_where()
                if expr:
                    wheres.append(expr)
    # for drill operation

    drill_field = self.drill_options.get("drill_field")
    drill_value = self.drill_options.get("drill_value")
    drill_level = self.drill_options.get("drill_level")
    if drill_field and drill_value and drill_level:
        if drill_level <= len(self.ct_meta['level_fields']):
            for i, value in enumerate(drill_value):
                # 过滤掉特殊钻取字段
                if isinstance(value, dict):
                    continue
                drill_where = self._gen_where_for_drill(i, value, gen_for=gen_for)

                if drill_where:
                    wheres.append(drill_where)
                    if gen_for == CALC_MOVING and i == 0:
                        self.data_drill_where_formula = wheres[-1]

    self._filter_out_empty_date(wheres)

    # 当是模板规则分享的图表时，使用全局过滤
    global_where_str = RuleUtil.global_filter_parse(self.global_filter, self.work_table)

    if global_where_str:
        wheres.append(global_where_str)
        self.global_where_str = global_where_str

    # 图表联动筛选
    if self.link_filters_obj is not None:
        link_where_str = self.link_filters_obj.get_where_str()
        if link_where_str:
            wheres.append(link_where_str)
    return wheres