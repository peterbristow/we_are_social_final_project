from rest_framework import generics
from models import Thread, Posts
from serializers import ThreadSerializer, PostSerializer


# Class based view CBV
# generics.ListAPIView, which is a basic class defined to allow us to render
# a simple list of objects from our models.
class ThreadViewSet(generics.ListAPIView):
    # List polls
    queryset = Thread.objects.all()  # Set the queryset to all of the available poll objects.
    serializer_class = ThreadSerializer


class PostUpdateView(generics.UpdateAPIView):
    # Use this to test i9n the browser:
    # $.ajax({
    #     type: #"PATCH",  ### Remove the '#' from before PATCH ###
    #     url: '/threads/post/update/2',
    #     data: {'id': 2, 'comment': 'foo bar flup!'},
    #     success: function(e) { alert(e); },
    #     dataType: "json",
    #     beforeSend: function (xhr) {
    #         xhr.setRequestHeader("X-CSRFToken", $("input[name='csrfmiddlewaretoken']").val());
    #     },
    # });
    serializer_class = PostSerializer
    queryset = Posts.objects.all()


class PostDeleteView(generics.DestroyAPIView):
    # Use this to test i9n the browser:
    # $.ajax({
    #     type: #"DELETE",  ### Remove the '#' from before DELETE ###
    #     url: '/threads/post/delete/2',
    #     success: function(e) { alert(e); },
    #     dataType: "json",
    #     beforeSend: function (xhr) {
    #         xhr.setRequestHeader("X-CSRFToken", $("input[name='csrfmiddlewaretoken']").val());
    #     },
    # });
    serializer_class = PostSerializer
    queryset = Posts.objects.all()