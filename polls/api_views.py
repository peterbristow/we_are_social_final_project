from rest_framework import generics, status
from rest_framework.response import Response
from models import Poll, Vote, Thread, PollSubject
from serializers import PollSerializer, VoteSerializer


# generics.ListAPIView, which is a basic class defined to allow us to render
# a simple list of objects from our models.
class PollViewSet(generics.ListAPIView):
    # List polls
    queryset = Poll.objects.all()  # Set the queryset to all of the available poll objects.
    serializer_class = PollSerializer


# generics.RetrieveAPIView allows you to retrieve a single object.
class PollInstanceView(generics.RetrieveAPIView):
    # Show one single Poll on its own.
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


# generics.ListCreateAPIView, which gives us the ability to add/create new
# objects on an existing list of objects (even if it's a currently empty list
# of objects, we can still start adding to them).
class VoteCreateView(generics.ListCreateAPIView):
    # Can be tested in the browser inspector with:
    # $.ajax({
    #     type: #"POST",  ### Remove the '#' before POST ###
    #     url: '/threads/polls/vote/6/',
    #     data: {'poll': 2, 'subject': 4},
    #     success: function(e) { alert(e); },
    #     dataType: "json",
    #     beforeSend: function (xhr) {
    #      xhr.setRequestHeader("X-CSRFToken", $("input[name='csrfmiddlewaretoken']").val());
    #     },
    # });

    # Creating an object.
    # Register votes from our application using only a small call to our web
    # service with a little bit of JSON.
    serializer_class = VoteSerializer  # specify the serializer class
    queryset = Vote.objects.all()  # source of our objects queryset

    def create(self, request, thread_id):
        # Override this view's create method.

        # Get an instance of the thread to check whether the user has already
        # voted on this poll - and if they have, we simply return an
        # HTTP_400_BAD_REQUEST so that any JavaScript calling this service
        # will know that the call wasn't successful. Then return some JSON with
        # the error inside.
        thread = Thread.objects.get(id=thread_id)
        subject = thread.poll.votes.filter(user=request.user).first()

        if subject:
            return Response({"error": "Already voted!"},
                            status=status.HTTP_400_BAD_REQUEST)

        # If not yet voted, take the JSON stored in the request.data, add in our
        # currently logged in user's id, and pass the request.data into our
        # VoteSerializer - which validates and saves the new Vote object.
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = VoteSerializer(data=data)

        if serializer.is_valid():
            # When using self.perform_create, we're only really calling serializer.save()
            self.perform_create(serializer)
            # When the save process succeeds, DRF keeps a copy of the newly
            # created object in the serializer.instance member variable. We
            # can use that to add it to the poll's votes list, so that we can
            # later use it when counting our vote results.
            thread.poll.votes.add(serializer.instance)

            # Return one of two possible Response objects that will
            # turn into a JSON feedback to the browser with either
            # a HTTP_201_CREATED status or a HTTP_400_BAD_REQUEST.
            # 201 status will be interpreted by JavaScript as a success,
            # so any handlers that are attached to these responses
            # will be triggered.
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
