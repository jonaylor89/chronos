
# chronos

### Overview

A gcloud function to pull google calendar data and present it as an easily accessible API. The function expects a calendar event as input
and responds with an array of how many hours each day are scheduled for that event this week. 

### Deployment

To deploy this gcloud function on your own account, first enable cloud functions and the google calendar API on the project you 
plan to deploy to. Then from your console, make sure default auth is set up with:

```
gcloud auth application-default login 
```

Next, share your google calendar with the service account email for the cloud function 
(something like whatever@serviceaccount.com in your IAM roles page) and lastly change the CALENDAR\_ID variable in `main.py` 
to your email and you should be set up. To deploy everything you should be able to run:

```
$ ./deploy.sh
```

or if cloudbuild is enabled on the project and is set up with git integration for your gcloud project then just push

---------------------------

### Send Request

```
# Example checking how many hours each day you have "Work" scheduled

curl -s -X POST $YOUR_FUNCTION_URL -H "Content-Type:application/json"  -d '{"name":"Work"}'

# => [0, 0, 0, 0, 0, 0, 0]
```

### Response:

```
  [
    Sunday
    Monday
    Tuesday
    Wednesday
    Thursday
    Friday
    Saturday
  ]
```

Free software: MIT license
