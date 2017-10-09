#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhangjinsi'

from basecontrol import BaseControl
from common.response import Response
from dbmodel.datamodel import DataModel
from collections import defaultdict
from dbmodel.userinfomodel import UserInfoModel
from dbmodel.authtablemodel import AuthTableModel

class DataControl(BaseControl):
    def __init__(self, *args, **kwargs):
        super(DataControl, self).__init__(*args, **kwargs)
        self.datamodel = DataModel()
        self.userinfomodel = UserInfoModel()
        self.authtablemodel = AuthTableModel()

    def auth_require(self, dimsname=None):
        '''
        根据用户等级和指标的等级要求来检查用户是否有权限
        :return:
        '''
        #获取用户工号，等级信息
        fworkid = self.session.get('fworkid', None)
        userinfo = self.userinfomodel.get_userinfo(fworkid=fworkid)
        flevel_id = userinfo.get('flevel_id',0)

        #获取指标的等级要求信息
        levelinfo = self.authtablemodel.get_dims_levelinfo(dimsname=dimsname)
        dims_level_id = levelinfo.get('flevel_id',10000)
        #print userinfo
        #print levelinfo

        #比较是否有权限
        if flevel_id<dims_level_id:
            return False
        return True

    def format_data(self,dims=None):
        '''
        格式化数据
        :param dims:
        :return:
        输出数据option = {

             'xAxis': ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"],
             'series': [{
                 'name': '销量',
                 'data': [5, 20, 36, 10, 10, 20]
             }]
         }

        '''
        data = dims.get('data',[])
        name = dims.get('name','')
        type = dims.get('type','bar')

        dict_data = defaultdict(list)

        for item in data: #{'2017-09-16':[144, 56]}
            key = item.get('fdate',None)
            dict_data[key].append(item.get(name))

        axis_x = []
        axis_y = []
        temp = sorted(dict_data.items(),key=lambda x:x[0],reverse=False)
        for key, obj in temp:
            axis_x.append(key) #fdate
            sum_data = sum([num for num in obj if isinstance(num, (float,int,long))])
            axis_y.append(sum_data)

        dims = {
            'xAxis' : axis_x,
            'series' : [{
                'name' : name,
                'data' : axis_y,
                'type' : type
            }]
        }
        #print dims
        return dims


    def user_get_data(self):

        dims = self.args.get('dims',None)
        if not dims:
            return Response.responseJson(Response.INPUT_EMPTY,'输入指标为空')
        #获取数据

        isAuth = self.auth_require(dimsname=dims)  #对应权限检查
        if not isAuth:
            return Response.responseJson(Response.NO_AUTH)

        params = {
            'sdate' : self.args.get('sdate',''),
            'edate' : self.args.get('edate','')
        }
        data = self.datamodel.get_data(dims=dims,args=params)


        #格式化数据
        dims = {
            'name' : dims,
            'type' : 'bar',
            'data' : data
        }
        res_data = self.format_data(dims=dims)
        print 'rese',res_data

        res_data['title'] = '所有游戏活跃度'

        # option = {
        #     'title': 'ECharts 入门示例',
        #     'xAxis': ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"],
        #     'series': [{
        #         'name': '销量',
        #         'type': 'bar',
        #         'data': [5, 20, 36, 10, 10, 20]
        #     }]
        # }
        #print jsonify(Response.responseJson(Response.SUCCESS,data=option,msg='获取数据成功'))

        #返回数据
        return Response.responseJson(Response.SUCCESS,data=res_data,msg='获取数据成功')


