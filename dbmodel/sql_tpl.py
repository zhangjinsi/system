#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhangjinsi'


SQL_TPL = {
    'activeacount' : '''
    select fdate, fgamename, SUM(fcount) as activeacount from analysis.gameactive where fdate>='%(sdate)s' and fdate<='%(edate)s' GROUP by fdate, fgamename
    '''
}