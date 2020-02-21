from django.conf.urls import url
from apps.operations.views import AddFavView,CommentView
urlpatterns = [
    #用户收藏
    url(r'^fav/$',AddFavView.as_view(),name="fav"),
    #用户评论
    url(r'^comment/$',CommentView.as_view(),name="comment"),


]