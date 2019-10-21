from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import generics
from django.contrib.auth import get_user_model
from utils.Emails import token_confirm
from django.shortcuts import render
import re
from django.db.utils import IntegrityError
from .tasks import random_str, send_register_email
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnlyInfo
from django.contrib.auth import authenticate, login
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    '''
    禁用跨域
    '''
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class YonghuInfo(mixins.UpdateModelMixin, viewsets.ReadOnlyModelViewSet):
    '''
    获取或更新用户信息
    list: http://hostname/auth/yonghu_info/[pk] GET # pk不带获取当前用户，带的话获取指定用户
    update: http://hostname/auth/yonghu_info/pk/ PUT # pk必须带
    '''
    queryset = get_user_model().objects.all()
    lookup_field = 'pk'
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyInfo)
    authentication_classes = [JSONWebTokenAuthentication, CsrfExemptSessionAuthentication]

    def get_queryset(self):
        print(self.kwargs.get('pk'))
        if self.kwargs.get('pk'):
            pk = int(self.kwargs['pk'])
        else:
            pk = self.request.user.id
        return get_user_model().objects.filter(pk=pk)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_active:
            nickname = request.data.get('nickname')
            info = request.data.get('info')
            if user.change_info(nickname, info):
                return Response({'msg': '修改成功', 'code': '0'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': '昵称已存在', 'code': '1'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': '账号未激活，请激活后再试。', 'code': '2'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def yonghu_login(request):
    '''
    用户登录
    :param request:
    :return:
    '''
    from .urls import urlpatterns
    print(urlpatterns)
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'msg': '登陆成功', 'code': '0'}, status=status.HTTP_200_OK)
    else:
        return Response({'msg': '用户名或密码错误', 'code': '1'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT'])
def Yonghu_info(request):
    """
    获取yonghu信息。
    """
    try:
        pk = request.query_params.get('pk')
        yonghu = get_user_model().objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # 获取用户信息
    if request.method == 'GET':
        print(request.session.get('userID'))
        serializer = UserSerializer(yonghu)
        return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def yonghu_create(request):
    """
    注册
    """
    if request.method == 'POST':
        username = request.data.get('username')
        phone = request.data.get('phone')
        email = request.data.get('email')
        password = request.data.get('password')
        ### 账号密码合法性验证
        if password is None or username is None:
            return Response({'msg': '账号或密码为空', 'code': '1'}, status=status.HTTP_400_BAD_REQUEST)
        s = re.match(r"[0-9a-zA-Z]+", username)
        if s is None:
            return Response({'msg': '账号不合法', 'code': '2'}, status=status.HTTP_400_BAD_REQUEST)
        if len(s.group()) != len(username):
            print(s.group())
            return Response({'msg': '账号不合法', 'code': '2'}, status=status.HTTP_400_BAD_REQUEST)
        ### 验证邮箱和手机号是否重复
        if phone is None and email is None:
            return Response({'msg': '邮箱和手机号至少要有一个', 'code': '3'}, status=status.HTTP_400_BAD_REQUEST)
        if email is not None:
            user = get_user_model().objects.filter(email=email)
            if user:
                return Response({'msg': '邮箱已验证过', 'code': '4'}, status=status.HTTP_400_BAD_REQUEST)
        if phone is not None:
            user = get_user_model().objects.filter(phone=phone)
            if user:
                return Response({'msg': '手机号已验证过', 'code': '5'}, status=status.HTTP_400_BAD_REQUEST)
            print(get_user_model().objects.filter(username=username))
        if len(get_user_model().objects.filter(username=username)) == 0:
            try:
                get_user_model().objects.create(
                    username = username,
                    phone = phone,
                    email = email,
                    password = make_password(password),
                    nickname = random_str() ### 创建随机昵称
                )
                token = token_confirm.generate_validate_token(username)
                send_register_email.delay(email=email,username=username,token=token,send_type="register")
                return Response({'msg': '注册成功，', 'code': '0'}, status=status.HTTP_200_OK)
            except IntegrityError as e:
                print(e)
                return Response({'msg': '注册失败,请重新注册', 'code': '7'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': '账号已存在', 'code': '6'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
def email_test(request):
    '''
    邮箱验证测试
    :param request:
    :return:
    '''
    user = get_user_model().objects.get(username='15259695263')
    send_register_email.delay(email=user.email, username=user.username, token=token_confirm.generate_validate_token(user.username), send_type="register")
    return Response({'msg': 'success.'}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def active_email(request):
    '''
    通过邮箱激活验证
    :param request:
    :return:
    '''
    token = request.query_params.get('token')
    try:
        username = token_confirm.confirm_validate_token(token) # 将用户名解析出来
    except Exception:
        username = token_confirm.remove_validate_token(token) # 过期，则将用户名解析出来
        users = get_user_model().objects.filter(username=username)
        for user in users:
            # 验证过期
            if user.is_active == False:
                user.delete() # 删除用户
                # msg = {'message': '验证已过期，请重新注册'}
                return Response('验证已过期')
            # 已经验证过
            else:
                return Response('已经验证过')
    try:
        user = get_user_model().objects.get(username=username)
        if user.is_active == True:
            return Response('已经验证过')
    except Exception as e:
        print(e)
        return Response('您验证过的用户不存在!')
    user.is_active = True
    user.save()
    return Response('验证成功!')


def already_auth(request):
    '''
    是否登录
    :param request:
    :return: 登录状态
    '''
    is_authorized = False
    if request.session.get('is_authorized'):
        is_authorized = True
    print('authorized status:', is_authorized)
    return is_authorized


@csrf_exempt
@api_view(['GET'])
def get_status(request):
    """
    获取登录状态
    :param request:
    :return: 1为已登录，0为未登录
    """
    if already_auth(request):
        data = {"is_authorized": 1}
    else:
        data = {"is_authorized": 0}
    return Response(data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def authorization_by_phone(request):
    '''
    通过手机号码登录
    :param request:
    :return:
    '''
    pass