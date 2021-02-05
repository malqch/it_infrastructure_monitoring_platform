from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandarPagination(PageNumberPagination):
    page_size = 5  # 默认每页显示条数配置
    page_query_param = 'page'  # “页数”的请求参数名称, 默认是page
    page_size_query_param = 'page_size'  # “分页大小”的请求参数名称

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('page', self.page.number),
            ('total_page', self.page.paginator.num_pages),
            ('page_size', self.page.paginator.per_page),
            ('results', data)]))
