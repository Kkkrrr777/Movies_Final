from .models import User, Movie

# 上下文处理器
def movie_user(request):
    user_id=request.session.get('user_id')
    context={}
    if user_id:
        try:
            user=User.objects.get(pk=user_id)
            context['movie_user']=user
        except:
            pass
    return context

def movie_qs_len(request):
    context={}
    if ('user_id' not in request.session.keys()):
        return context
    cur_user_id = request.session.get('user_id')
    cur_user = User.objects.get(pk=cur_user_id)
    context['movie_qs_len'] = len(Movie.objects.filter(user=cur_user))
    return context
