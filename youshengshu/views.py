from django.shortcuts import render
from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from .serializers import YoushengshuSerializer
from .models import Youshengshu
from utils import getBook

# Create your views here.

class BookInfo(generics.ListAPIView):
    '''
    有声书信息
    '''
    queryset = Youshengshu.objects.all()
    serializer_class = YoushengshuSerializer

    def get_queryset(self):
        return Youshengshu.objects.filter(pk=self.kwargs.get('pk'))

    def list(self, request, *args, **kwargs):
        youshengshu = self.get_object()
        if youshengshu is not None:

            serializer = YoushengshuSerializer(youshengshu)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'msg': '资源未找到'}, status=status.HTTP_404_NOT_FOUND)


class BookTypeList(generics.ListAPIView):
    '''
    有声书分类列表
    '''
    serializer_class = YoushengshuSerializer
    lookup_field = 'type'

    def get_queryset(self):
        return Youshengshu.objects.filter(type=self.kwargs.get('type'))


class BookVoiceList(generics.ListAPIView):
    '''
    有声书播音列表
    '''
    serializer_class = YoushengshuSerializer
    lookup_field = 'voice'

    def get_queryset(self):
        return Youshengshu.objects.filter(voice=self.kwargs.get('voice'))


class BookAuthorList(generics.ListAPIView):
    '''
    有声书作者分类
    '''
    serializer_class = YoushengshuSerializer
    lookup_field = 'author'

    def get_queryset(self):
        return Youshengshu.objects.filter(author=self.kwargs.get('author'))


@csrf_exempt
@api_view()
def booksound(request):
    '''
    发送有声书资源链接
    :param request:
    :return:
    '''
    pk = request.query_params.get('pk')
    page = request.query_params.get('page')
    User_Agent = request.headers.get('User-Agent')
    headers = {
        'User-Agent': User_Agent
    }
    print(pk)
    url = getBook.getBook(pk, page, headers)
    if url:
        return Response({'url': url, 'code': 0} ,status=status.HTTP_200_OK)
    return Response({'msg': '资源不存在', 'code': 1}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view()
def xmlyTypeList(request):
    '''
    喜马拉雅分类列表
    :param request:
    :return:
    '''
    ft = int(request.query_params.get('ft'))
    st = int(request.query_params.get('st'))
    sort = int(request.query_params.get('sort'))
    page = int(request.query_params.get('page'))
    perPage = int(request.query_params.get('perPage'))
    try:
        if perPage:
            data, pagenum = getBook.getTypeList(ft, st, sort, page, perPage=perPage)
        else:
            data, pagenum = getBook.getTypeList(ft, st, sort, page, perPage=perPage)
        return Response({'data': data, 'pagenum': pagenum, 'code': 0}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'msg': '页数超出', 'code': 1}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view()
def xmlyAllji(request):
    '''
    获取一集或者所有的集数
    :param request:
    :return:
    '''
    ty = request.query_params.get('type')
    albumId = request.query_params.get('albumId')
    page = request.query_params.get('page')
    ji = request.query_params.get('ji')
    if ji:
        return Response(getBook.getDetail1(albumId, ty, ji=ji), status=status.HTTP_200_OK)
    elif page:
        return Response(getBook.getDetail1(albumId, ty, page=page), status=status.HTTP_200_OK)


@csrf_exempt
@api_view()
def xmlySearch(request):
    '''
    查找
    :param request:
    :return:
    '''
    kw = request.query_params.get('kw')
    return Response(getBook.search1(kw), status=status.HTTP_200_OK)