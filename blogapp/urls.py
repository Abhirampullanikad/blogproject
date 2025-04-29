from . import views
from django.urls import path
app_name='blogapp'
urlpatterns = [
    path("",views.index,name="index"),
    path("blog",views.blog,name="blog"),

    path("create",views.create,name="create"),
    path("increaselikes/<int:id>",views.increaselikes,name='increaselikes'),
    path("profile/<int:id>",views.profile,name='profile'),
    path("profile/edit/<int:id>",views.profileedit,name='profileedit'),
    path("post/<int:id>",views.post,name="post"),
    path("post/comment/<int:id>",views.savecomment,name="savecomment"),
    path("post/comment/delete/<int:id>",views.deletecomment,name="deletecomment"),
    path("post/edit/<int:id>",views.editpost,name="editpost"),
    path("post/delete/<int:id>",views.deletepost,name="deletepost"),
    path('listblog/',views.listblog,name='listblog'),
    path('detailsview/<int:id>/',views.detailsview,name='detailsview'),
    path('deleteview/<int:id>/',views.deleteview,name='deleteview'),
    path('search_post/',views.search_post,name='search_post'),
    path('base/',views.base,name='base'),
    path('listpost/',views.listpost,name='listpost'),
    path('post/',views.post,name='post'),
    path('news/',views.CreateNews,name='createnews'),
    path('listnews/',views.listNews,name='listnews'),
    path('updateNews/<int:news_id>/',views.updateNews,name='updateview'),
    path('deletenews/<int:news_id>/',views.DeleteView,name='deleteview'),
   

]
