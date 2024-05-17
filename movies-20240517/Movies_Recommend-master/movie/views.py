import csv
import time
import os.path
from math import sqrt

import django
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Avg, Count, Max
from django.http import HttpResponse, request, HttpResponseForbidden
from django.shortcuts import render, redirect, reverse
from .forms import RegisterForm, LoginForm, CommentForm, UserInfoForm
from django.views.generic import View, ListView, DetailView
from .models import User, Movie, Genre, Movie_rating, Movie_similarity, Movie_hot, UserType, Statistic

# 别动
BASE = os.path.dirname(os.path.abspath(__file__))

# 加载模型
from sklearn.externals import joblib

model_path = os.path.join(BASE, 'model/model.pkl')
model_pre = joblib.load(model_path)

'''所有注释掉的函数，如果数据库没有出错，不要执行，并且应该在urls中注释掉相应的路径，以免误入'''

'''!!! 导入csv文件用'''
# def get_genre():
#     '''导入所有电影类型'''
#     path=os.path.join(BASE,'static\movie\info\genre.txt')
#     with open(path) as fb:
#         for line in fb:
#             Genre.objects.create(name=line.strip())
#
# def get_movie_info():
#     '''导入所有电影信息，设置它们的类型'''
#     path=os.path.join(BASE,'static\movie\info\info.csv')
#     with open(path) as fb:
#         reader=csv.reader(fb)
#         title=reader.__next__()
#         # 读取title信息 id,name,url,time,genre,release_time,intro,directores,writers,starts
#         # 这里的id是imbd的id，根据它来访问static文件夹下面的poster
#         title_dct=dict(zip(title,range(len(title))))
#         # print(title_dct)
#         # print(path)
#         for i,line in enumerate(reader):
#             m=Movie.objects.create(name=line[title_dct['name']],
#                                  imdb_id=line[title_dct['id']],
#                                  time=line[title_dct['time']],
#                                  release_time=line[title_dct['release_time']],
#                                  intro=line[title_dct['intro']],
#                                  director=line[title_dct['directors']],
#                                  writers=line[title_dct['writers']],
#                                  actors=line[title_dct['starts']])
#             # 必须要先保存才能建立关系
#             m.save()
#             # 建立类型关系
#             for genre in line[title_dct['genre']].split('|'):
#                 # 找到类型 genre_object
#                 go=Genre.objects.filter(name=genre).first()
#                 # print(go)
#                 m.genre.add(go)
#             if i%1000==0:
#                 print(i)    # 控制台查看进度用
#             # pass
#
# def get_user_and_rating():
#     '''
#     获取ratings文件，设置用户信息和对电影的评分
#     由于用户没有独立的信息，默认用这种方式保存用户User: name=userId,password=userId,email=userId@1.com
#     通过imdb_id对电影进行关联，设置用户对电影的评分,comment默认为空
#     '''
#     path = os.path.join(BASE, r'static\movie\info\ratings.csv')
#     with open(path) as fb:
#         reader=csv.reader(fb)
#         # userId,movieId,rating,timestamp,timestamp不用管
#         title=reader.__next__()
#         title_dct=dict(zip(title,range(len(title))))
#         # csv文件中，一条记录就是一个用户对一部电影的评分和时间戳，一个用户可能有多条评论
#         # 所以要先取出用户所有的评分，设置成一个字典,格式为{ user:{movie1:rating, movie2:rating, ...}, ...}
#         user_id_dct=dict()
#         for line in reader:
#             user_id=line[title_dct['userId']]
#             imdb_id=line[title_dct['movieId']]
#             rating=line[title_dct['rating']]
#             user_id_dct.setdefault(user_id,dict())
#             user_id_dct[user_id][imdb_id]=rating
#     # 对所有用户和评分记录
#     for user_id,ratings in user_id_dct.items():
#         u=User.objects.create(name=user_id,password=user_id,email=f'{user_id}@1.com')
#         # 必须先保存
#         u.save()
#         # 开始加入评分记录
#         for imdb_id,rating in ratings.items():
#             # Movie_rating(uid=)
#             movie=Movie.objects.get(imdb_id=imdb_id)
#             relation=Movie_rating(user=u,movie=movie,score=rating,comment='')
#             relation.save()
#             # break
#         print(f'{user_id} process success')
#         # break
#
# def index(request):
#     # 临时的index函数，用来导入数据库
#     # get_genre()
#     # get_movie_info()
#     # get_user_rating()
#     context={'movie':Movie.objects.filter(name="Toy Story (1995) ").first()}
#     # print(Movie.objects.filter(name="Toy Story (1995) ").first())
#     return render(request, 'movie/index.html',context=context)
'''!!! 导入csv文件用'''

'''!!! 恢复评分信息用，如果movie_rating表没有出错，不需要执行下面的函数'''
# def get_ratings():
#     '''这个函数是用来恢复movie_rating表的
#         之前不小心update了所有记录，导致数据库表全部更新成一条了，也就是10万条一样的评分
#         现在要重新导入
#     '''
#     '''
#     获取ratings文件，设置用户信息和对电影的评分
#     由于用户没有独立的信息，默认用这种方式保存用户User: name=userId,password=userId,email=userId@1.com
#     通过imdb_id对电影进行关联，设置用户对电影的评分,comment默认为空
#     '''
#     path = os.path.join(BASE, r'static\movie\info\ratings.csv')
#     with open(path) as fb:
#         reader=csv.reader(fb)
#         # userId,movieId,rating,timestamp,timestamp不用管
#         title=reader.__next__()
#         title_dct=dict(zip(title,range(len(title))))
#         # csv文件中，一条记录就是一个用户对一部电影的评分和时间戳，一个用户可能有多条评论
#         # 所以要先取出用户所有的评分，设置成一个字典,格式为{ user:{movie1:rating, movie2:rating, ...}, ...}
#         user_id_dct=dict()
#         for line in reader:
#             user_id=line[title_dct['userId']]
#             imdb_id=line[title_dct['movieId']]
#             rating=line[title_dct['rating']]
#             user_id_dct.setdefault(user_id,dict())
#             user_id_dct[user_id][imdb_id]=rating
#     # 对所有用户和评分记录
#     for user_id,ratings in user_id_dct.items():
#         # 获取用户
#         u=User.objects.get(name=user_id)
#
#         # 开始加入评分记录
#         for imdb_id,rating in ratings.items():
#             # Movie_rating(uid=)
#             movie=Movie.objects.get(imdb_id=imdb_id)
#             relation=Movie_rating(user=u,movie=movie,score=rating,comment='')
#             relation.save()
#             # break
#         print(f'{user_id} process success')
'''!!! 恢复评分信息用'''

'''!!! 修复数据库用'''
# def fixdb(request):
#     # 修复数据库用
#     # !!!
#     # get_ratings()
#     # !!!
#     print("fix db success")
#     return redirect((reverse('movie:index')))
'''!!! 修复数据库用'''

'''!!! 导入电影相似度用'''

# def calc_movie_similarity(request):
#     path = os.path.join(BASE, r'static\movie\info\movie_similarity.csv')
#     with open(path) as fb:
#         reader=csv.reader(fb)
#         reader.__next__()
#         for line in reader:
#             # 把它们都转换成值
#             line=list(map(eval,line))
#             m1,m2,val=line
#             movie1=Movie.objects.get(imdb_id=m1)
#             movie2=Movie.objects.get(imdb_id=m2)
#             # print(movie1,movie2)
#             # 保存记录到数据库中,因为csv表中存储了每部电影的十条记录，我们保存就行了
#             record=Movie_similarity(movie_source=movie1,movie_target=movie2,similarity=val)
#             record.save()
#
#     print("写入相似度成功")
#     return redirect((reverse('movie:index')))


'''!!! 导入电影相似度用'''


# 用户画像推荐
#逻辑：在外面随机生成的画像虚拟信息（职业、地域、工作），根据虚拟的信息训练的聚类模型
#注册后填写我的画像信息，它调用这个序列模型把我归类到一个用户类别user type
#推荐相近类别user type用户评分喜欢的电影

class PortrayView(ListView):
    model = Movie
    template_name = 'movie/portray.html'
    paginate_by = 15
    context_object_name = 'movies'
    ordering = 'imdb_id'
    page_kwarg = 'p'

    def get_queryset(self):
        try:
            # 根据session获取用户
            user_id = self.request.session.get('user_id')
            # 查询用户
            if user_id:
                user_name = User.objects.get(pk=user_id).name
                user_type = UserType.objects.get(name=user_name)
                # 获取该登录用户的聚类类别
                if user_type:
                    type1 = user_type.type
                    print("用户类型:", type1)
                    # 获取相同类别用户所看电影
                    users = UserType.objects.filter(type=type1)
                    movies = []
                    for user in users:
                        u = User.objects.get(name=user.name)
                        movie_id = Movie_rating.objects.filter(user=u).values_list('movie')
                        movies.extend(movie_id)
                    movies = [i[0] for i in movies]
                    return Movie.objects.filter(id__in=movies)
                else:
                    return redirect(reverse('movie:info'))
        except Exception as e:
            # 如果session过期查不到用户则默认返回前1000部热门电影
            return Movie.objects.filter(imdb_id__lte=1000)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PortrayView, self).get_context_data(*kwargs)
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        pagination_data = self.get_pagination_data(paginator, page_obj)
        context.update(pagination_data)
        # print(context)
        return context

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
            left_has_more = False
        else:
            left_pages = range(current_page - around_count, current_page)
            left_has_more = True

        if current_page >= paginator.num_pages - around_count - 1:
            right_pages = range(current_page + 1, paginator.num_pages + 1)
            right_has_more = False
        else:
            right_pages = range(current_page + 1, current_page + 1 + around_count)
            right_has_more = True
        return {
            'left_pages': left_pages,
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more
        }


class IndexView(ListView):
    model = Movie
    template_name = 'movie/index.html'
    paginate_by = 15
    context_object_name = 'movies'
    ordering = 'imdb_id'
    page_kwarg = 'p'

    def get_queryset(self):
        # 返回前1000部电影
        return Movie.objects.filter(imdb_id__lte=1000)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(*kwargs)
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        pagination_data = self.get_pagination_data(paginator, page_obj)
        context.update(pagination_data)

        # 统计游客人数
        statistic = Statistic.objects.first()
        statistic.guest_count += 1
        statistic.save()
        # print(context)
        return context

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
            left_has_more = False
        else:
            left_pages = range(current_page - around_count, current_page)
            left_has_more = True

        if current_page >= paginator.num_pages - around_count - 1:
            right_pages = range(current_page + 1, paginator.num_pages + 1)
            right_has_more = False
        else:
            right_pages = range(current_page + 1, current_page + 1 + around_count)
            right_has_more = True
        return {
            'left_pages': left_pages,
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more
        }


class PopularMovieView(ListView):
    model = Movie_hot
    template_name = 'movie/hot.html'
    paginate_by = 15
    context_object_name = 'movies'
    # ordering = '-movie_hot__rating_number' # 没有效果
    page_kwarg = 'p'

    def get_queryset(self):
        # 初始化 计算评分人数最多的100部电影，并保存到数据库中
        # ######################
        # movies = Movie.objects.annotate(nums=Count('movie_rating__score')).order_by('-nums')[:100]
        # print(movies)
        # print(movies.values("nums"))
        # for movie in movies:
        # print(movie,movie.nums)
        # record = Movie_hot(movie=movie, rating_number=movie.nums)
        # record.save()
        # ######################

        hot_movies = Movie_hot.objects.all().values("movie_id")
        # print(hot_movies)
        # for movie in hot_movies:
        # print(movie)
        # print(movie.imdb_id,movie.rating_number)
        # Movie.objects.filter(movie_hot__rating_number=)
        # 一个bug!这里filter出来虽然是正确的100部电影，但是会按照imdb_id排序，导致正确的结果被破坏了！也就是得不到100部热门电影的正确顺序！
        # movies=Movie.objects.filter(id__in=hot_movies.values("imdb_id"))
        # 找出100部热门电影，同时按照评分人数排序
        # 因此必须要手动排序一次。
        movies = Movie.objects.filter(id__in=hot_movies).annotate(nums=Max('movie_hot__rating_number')).order_by(
            '-nums')
        return movies

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PopularMovieView, self).get_context_data(*kwargs)
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        pagination_data = self.get_pagination_data(paginator, page_obj)
        context.update(pagination_data)
        # print(context)
        return context

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
            left_has_more = False
        else:
            left_pages = range(current_page - around_count, current_page)
            left_has_more = True

        if current_page >= paginator.num_pages - around_count - 1:
            right_pages = range(current_page + 1, paginator.num_pages + 1)
            right_has_more = False
        else:
            right_pages = range(current_page + 1, current_page + 1 + around_count)
            right_has_more = True
        return {
            'left_pages': left_pages,
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more
        }


class TagView(ListView):
    model = Movie
    template_name = 'movie/tag.html'
    paginate_by = 15
    context_object_name = 'movies'
    # ordering = 'movie_rating__score'
    page_kwarg = 'p'

    def get_queryset(self):
        if 'genre' not in self.request.GET.dict().keys():
            movies = Movie.objects.all()
            return movies[100:200]
        else:
            movies = Movie.objects.filter(genre__name=self.request.GET.dict()['genre'])
            return movies[:100]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TagView, self).get_context_data(*kwargs)
        if 'genre' in self.request.GET.dict().keys():
            genre = self.request.GET.dict()['genre']
            context.update({'genre': genre})
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        pagination_data = self.get_pagination_data(paginator, page_obj)
        context.update(pagination_data)
        return context

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
            left_has_more = False
        else:
            left_pages = range(current_page - around_count, current_page)
            left_has_more = True

        if current_page >= paginator.num_pages - around_count - 1:
            right_pages = range(current_page + 1, paginator.num_pages + 1)
            right_has_more = False
        else:
            right_pages = range(current_page + 1, current_page + 1 + around_count)
            right_has_more = True
        return {
            'left_pages': left_pages,
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more
        }


class SearchView(ListView):
    model = Movie
    template_name = 'movie/search.html'
    paginate_by = 15
    context_object_name = 'movies'
    # ordering = 'movie_rating__score'
    page_kwarg = 'p'

    def get_queryset(self):
        movies = Movie.objects.filter(name__icontains=self.request.GET.dict()['keyword'])
        print(movies)
        return movies

    def get_context_data(self, *, object_list=None, **kwargs):
        # self.genre=self.request.GET.dict()['genre']
        context = super(SearchView, self).get_context_data(*kwargs)
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        pagination_data = self.get_pagination_data(paginator, page_obj)
        context.update(pagination_data)
        context.update({'keyword': self.request.GET.dict()['keyword']})
        return context

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
            left_has_more = False
        else:
            left_pages = range(current_page - around_count, current_page)
            left_has_more = True

        if current_page >= paginator.num_pages - around_count - 1:
            right_pages = range(current_page + 1, paginator.num_pages + 1)
            right_has_more = False
        else:
            right_pages = range(current_page + 1, current_page + 1 + around_count)
            right_has_more = True
        return {
            'left_pages': left_pages,
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more
        }


# 注册视图
class RegisterView(View):
    def get(self, request):
        return render(request, 'movie/register.html')

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 没毛病，保存
            form.save()

            # 创建管理员后台管理的用户模型对象并保存
            admin_user = django.contrib.auth.models.User.objects.create_user(
                username=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            return redirect(reverse('movie:info'))
        else:
            # 表单验证失败，重定向到注册页面
            errors = form.get_errors()
            for error in errors:
                messages.info(request, error)
            print(form.errors.get_json_data())
            return redirect(reverse('movie:register'))


#登录视图
class LoginView(View):
    def get(self, request):
        return render(request, 'movie/login.html')

    def post(self, request):
        print(request.POST)
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            pwd = form.cleaned_data.get('password')
            user = User.objects.filter(name=name, password=pwd).first()
            # username = form.cleaned_data.get('name')
            # print(username)
            # pwd = form.cleaned_data.get('password')
            if user:
                # 登录成功，在session 里面加上当前用户的id，作为标识
                request.session['user_id'] = user.id
                # 统计登录人数
                statistic = Statistic.objects.first()
                statistic.login_count += 1
                statistic.save()

                return redirect(reverse('movie:index'))
                if remember:
                    # 设置为None，则表示使用全局的过期时间
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
            else:
                print('用户名或者密码错误')
                # messages.add_message(request,messages.INFO,'用户名或者密码错误!')
                messages.info(request, '用户名或者密码错误!')
                return redirect(reverse('movie:login'))
        else:
            print("error!!!!!!!!!!!")
            errors = form.get_errors()
            for error in errors:
                messages.info(request, error)
            print(form.errors.get_json_data())
            return redirect(reverse('movie:login'))


def UserLogout(request):
    # 登出，立即停止会话
    request.session.set_expiry(-1)
    return redirect(reverse('movie:index'))


class UserInfo(View):
    def get(self, request):
        return render(request, 'movie/info.html')

    def post(self, request):
        print(request.POST)
        form = UserInfoForm(request.POST)
        if form.is_valid():
            # kmeans做预测分类用户
            name = request.POST.get('name')
            user_type = model_pre.predict(form.get_value_list())
            user = UserType.objects.filter(name=name)
            if user.exists():
                user.delete()
            UserType(name=name, type=user_type).save()
            return redirect(reverse('movie:index'))
        else:
            print("error!!!!!!!!!!!")
            errors = form.get_errors()
            for error in errors:
                messages.info(request, error)
            print(form.errors.get_json_data())
            return redirect(reverse('movie:info'))


class MovieDetailView(DetailView):
    '''电影详情页面'''
    model = Movie
    template_name = 'movie/detail.html'
    # 上下文对象的名称
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        # 重写获取上下文方法，增加评分参数
        context = super().get_context_data(**kwargs)
        # 判断是否登录用
        login = True
        try:
            user_id = self.request.session['user_id']
        except KeyError as e:
            login = False  # 未登录

        # 获得电影的pk
        pk = self.kwargs['pk']
        movie = Movie.objects.get(pk=pk)

        if login:
            # 已经登录，获取当前用户的历史评分数据
            user = User.objects.get(pk=user_id)

            rating = Movie_rating.objects.filter(user=user, movie=movie).first()
            # 默认值
            score = 0
            comment = ''
            if rating:
                score = rating.score
                comment = rating.comment
            context.update({'score': score, 'comment': comment})

        # 获取播放链接
        play_link = movie.play_link
        context.update({'play_link': play_link})

        # 增加观影人数
        statistic = Statistic.objects.first()
        statistic.viewers_count += 1
        statistic.save()

        # 增加观影人数
        movie.viewers_count += 1
        movie.save()

        similarity_movies = movie.get_similarity()
        # 获取与当前电影最相似的电影
        context.update({'similarity_movies': similarity_movies})
        # 判断是否登录，没有登录则不显示评分页面
        context.update({'login': login})

        return context

    # 接受评分表单,pk是当前电影的数据库主键id
    def post(self, request, pk):
        url = request.get_full_path()
        form = CommentForm(request.POST)
        if form.is_valid():
            # 获取分数和评论
            score = form.cleaned_data.get('score')
            comment = form.cleaned_data.get('comment')
            print(score, comment)
            # 获取用户和电影
            user_id = request.session['user_id']
            user = User.objects.get(pk=user_id)
            movie = Movie.objects.get(pk=pk)

            # 更新一条记录
            rating = Movie_rating.objects.filter(user=user, movie=movie).first()
            if rating:
                # 如果存在则更新
                # print(rating)
                rating.score = score
                rating.comment = comment
                rating.save()
                # messages.info(request,"更新评分成功！")
            else:
                print('记录不存在')
                # 如果不存在则添加
                rating = Movie_rating(user=user, movie=movie, score=score, comment=comment)
                rating.save()

            # 增加观影人数
            statistic = Statistic.objects.first()
            statistic.comment_count += 1
            statistic.save()
            messages.info(request, "评论成功!")

        else:
            # 表单没有验证通过
            messages.info(request, "评分不能为空!")
        return redirect(reverse('movie:detail', args=(pk,)))


class RatingHistoryView(DetailView):
    '''用户详情页面'''
    model = User
    template_name = 'movie/history.html'
    # 上下文对象的名称
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        # 这里要增加的对象：当前用户过的电影历史
        context = super().get_context_data(**kwargs)
        user_id = self.request.session['user_id']
        user = User.objects.get(pk=user_id)
        # 获取ratings即可
        ratings = Movie_rating.objects.filter(user=user)

        context.update({'ratings': ratings})
        return context


def delete_recode(request, pk):
    print(pk)
    movie = Movie.objects.get(pk=pk)
    user_id = request.session['user_id']
    print(user_id)
    user = User.objects.get(pk=user_id)
    rating = Movie_rating.objects.get(user=user, movie=movie)
    print(movie, user, rating)
    rating.delete()
    messages.info(request, f"Successfully delete {movie.name}!")
    # 跳转回评分历史
    return redirect(reverse('movie:history', args=(user_id,)))


#For You
class RecommendMovieView(ListView):
    model = Movie
    template_name = 'movie/recommend.html'
    paginate_by = 15
    context_object_name = 'movies'
    ordering = 'movie_rating__score'
    page_kwarg = 'p'

    def __init__(self):
        super().__init__()
        # 最相似的20个用户
        self.K = 20
        # 推荐出10电影
        self.N = 10
        # 存放当前用户评分过的电影querySet
        self.cur_user_movie_qs = None

    def get_user_sim(self):
        # 用户相似度字典，格式为{ user_id1:val , user_id2:val , ... }
        user_sim_dct = dict()
        '''获取用户之间的相似度,存放在user_sim_dct中'''
        # 获取当前用户
        cur_user_id = self.request.session['user_id']
        cur_user = User.objects.get(pk=cur_user_id)
        # 获取其它用户
        other_users = User.objects.exclude(pk=cur_user_id)

        self.cur_user_movie_qs = Movie.objects.filter(user=cur_user)
        
        #逻辑：根据共同评分过的电影的数量来计算用户的相似度，如果没有评分过那和所有的用户的相似度都是0，
        #但就算是0，它也根据前K个用户的偏好推荐N 部电影


        # 计算当前用户与其他用户评分过的电影交集数
        for user in other_users:
            # 记录感兴趣的数量
            user_sim_dct[user.id] = len(Movie.objects.filter(user=user) & self.cur_user_movie_qs)

        # 按照key排序value，返回K个最相近的用户
        print("user similarity calculated!")
        # 格式是 [ (user, value), (user, value), ... ]
        return sorted(user_sim_dct.items(), key=lambda x: -x[1])[:self.K]

    def get_recommend_movie(self, user_lst):
        # 电影兴趣值字典，{ movie:value, movie:value , ...}
        movie_val_dct = dict()
        # print(f'cur_user_movie_qs:{self.cur_user_movie_qs},type:{type(self.cur_user_movie_qs)}')
        # print(Movie.objects.all() & self.cur_user_movie_qs)
        # 用户，相似度
        for user, _ in user_lst:
            # 获取相似用户评分过的电影，并且不在前用户的评分列表中的，再加上score字段，方便计算兴趣值
            movie_set = Movie.objects.filter(user=user).exclude(id__in=self.cur_user_movie_qs).annotate(
                score=Max('movie_rating__score'))
            for movie in movie_set:
                movie_val_dct.setdefault(movie, 0)
                # 累计用户的评分
                movie_val_dct[movie] += movie.score
        print('recommend movie list calculated!')
        return sorted(movie_val_dct.items(), key=lambda x: -x[1])[:self.N]

    def get_queryset(self):
        s = time.time()
        # 获得最相似的K个用户列表
        user_lst = self.get_user_sim()
        # 获得推荐电影的id
        movie_lst = self.get_recommend_movie(user_lst)
        print(movie_lst)
        result_lst = []
        for movie, _ in movie_lst:
            result_lst.append(movie)
        e = time.time()
        print(f"用时:{e - s}")
        return result_lst

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RecommendMovieView, self).get_context_data(*kwargs)
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        pagination_data = self.get_pagination_data(paginator, page_obj)
        return context

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
            left_has_more = False
        else:
            left_pages = range(current_page - around_count, current_page)
            left_has_more = True

        if current_page >= paginator.num_pages - around_count - 1:
            right_pages = range(current_page + 1, paginator.num_pages + 1)
            right_has_more = False
        else:
            right_pages = range(current_page + 1, current_page + 1 + around_count)
            right_has_more = True
        return {
            'left_pages': left_pages,
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more
        }


from django.contrib.auth.models import Group
def stat_movies(request):
    # 查询数据库，获取最受欢迎的电影（假设按照观影人数排序）
    try:
        # 根据session获取用户
        user_id = request.session.get('user_id')
        # 查询用户
        if user_id:
            user_name = User.objects.get(pk=user_id).name
            user = django.contrib.auth.models.User.objects.get(username=user_name)
            # 获取该登录用户的聚类类别
            if user.groups.filter(name='admin').exists():
                popular_movies = Movie.objects.order_by('-viewers_count')[:20]  # 获取前10部观影人数最多的电影
                # 获取统计数据
                statistic = Statistic.objects.first()
                context = {'popular_movies': popular_movies, 'statistic': statistic}
                return render(request, 'movie/popular_movies.html', context)
            else:
                print("else")
                return HttpResponseForbidden("No permission")
    except Exception as e:
        print(e)
        # 如果session过期查不到用户则默认返回前1000部热门电影
        return HttpResponseForbidden("No permission")
        # return redirect(reverse('movie:login'))

