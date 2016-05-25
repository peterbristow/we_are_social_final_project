/**
 * Created by Peter on 25/05/2016.
 */
var pollApp = angular.module('pollApp', []);

/*
AngularJS has a templating language convention of using {{ and }} to
encapsulate variables in HTML and so does Django, so this collision
needs rectifying:
Using the $interpolateProvider, we can reassign the starting and ending
symbols so that we can then mark our embedded variables like this:
{$ user.name $} earned {$ account.profits $}
 */

pollApp.config(function($interpolateProvider, $httpProvider) {
    $interpolateProvider.startSymbol('{$').endSymbol('$}');
    $httpProvider.defaults.headers.common['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
});

pollApp.factory('pollFactory', function($http) {
    var pollUrl = '/threads/polls/';
    var votingUrl = '/threads/polls/vote/';

    pollFactory = {};

    // The $http.get function takes a URL and and returns the json served at
    // that url.
    // There is an equivalent $http.post method that accepts a URL and some
    // JSON data, and performs a HTTP POST of the json to that url.
    pollFactory.getPoll = function(id) {
        console.log('getPoll ' + id);
        return $http.get(pollUrl + id);
    };

    pollFactory.vote = function(poll, subject) {
        console.log('vote ' + JSON.stringify(poll) + ', subject=' + JSON.stringify(subject));
        var data = {'poll': poll.id, 'subject': subject.id};

        return $http.post(votingUrl + poll.thread + '/', data);  // remember to add the slash for django urls to work!
    };

    return pollFactory;
});

pollApp.controller('PollCtrl', function($scope, pollFactory) {  // include pollFactory
    $scope.poll = "";

    // Sets the poll object in $scope
    function setPoll(response) {
        $scope.poll = response.data;
    }

    // Show errors
    function showError(response) {
        if(response.data.error !== undefined) {
            alert(response.data.error);
        }
    }

    // This method gets the actual data using our poll factory, utilising
    // the variable we created back in our Django template.
    function getPoll() {
        return pollFactory.getPoll(pollID);  // pollID - from our page variable made in our template
    }

    // Call the web service
    // This line calls our getPoll method to get the actual data using our
    // poll factory, utilising the variable created in the Django template.
    // Also append or ‘chain’ what should happen next by adding .then(setPoll),
    // which is passed to the return result of the call from getPoll.
    // setPoll sets the poll object in $scope to be the resulting JSON object
    // from the return result from our web service.
    getPoll().then(setPoll);
    console.log('init: poll=' + JSON.stringify($scope.poll));
    console.log('subject=' + JSON.stringify($scope.subject));

    // send the vote, we take advantage of this chaining of responses by
    // first calling the pollFactory.vote() method and
    // .then(getPoll).then(setPoll)
    // If we have an error, we tell AngularJS to use the showError method.
    $scope.vote = function(poll, subject) {
        pollFactory.vote(poll, subject).then(getPoll).then(setPoll, showError);
    }
});
