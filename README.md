# Reddit Bot for Coronavirus News

Reddit Bot for sending CoronaVirus News by Email.

This is self-hosting application. Please be aware of security implications when you host any application for yourself or for others.

## Why?

I found [reddit coronavirus community](https://www.reddit.com/r/coronavirus) covering news well.
I used [ifttt](https://ifttt.com) to keep track of top news everyday. However,
[ifttt](https://ifttt.com/applets/111819552d/) was not customizable.  I ended up writing this program.

I also packaged it to run it as docker container, and on a kubernetes cluster, even on a raspberry-pi based
kubernetes cluster.

### Hassle Free Service

Do want this news to be delivered to your Inbox? Fill out this form, and your email will be included in hosted version.

* Fill the form: https://forms.gle/YkEAtb1sCKvZqwe77
* You can un-subscribe anytime.
* Your email id will not be shared with anyone and will not be used for any other purpose.

## Using this project.

This is a simple open source application. You can customize it and run it yourself. The simplest way to run it is
using the docker container.
```
docker run --env REDDIT_USERNAME=MY-VALUE \
           --env REDDIT_PASSWORD=MY-VALUE \
           --env REDDIT_API_CLIENT_SECRET=MY-VALUE \
           --env REDDIT_API_CLIENT_ID=MY-VALUE \
           --env SENDER_EMAIL=MY-VALUE \
           --env SENDER_EMAIL_PASSWORD=MY-VALUE \
           --env SENDER_NAME=MY-VALUE \
           --env RECEIVER_EMAIL=MY-VALUE \
           skumaran/redditbot:v0.1
```

### Using Gmail as SMTP

We will use Gmail as SMTP Service. You will have to (turn-on using less-secure apps)[https://hotter.io/docs/email-accounts/secure-app-gmail/] 
in the GMAIL authentication and you could use your username and password for SMTP now.

### Docker Images

Docker Image for x86

```
docker pull skumaran/redditbot:v0.1
```

Docker Image for Arm

```
docker pull skumaran/redditbot:arm-v0.1
```

### Kuberbetes Cron Job.

You could run this application in your Kubernetes Cluster, even on Raspberry Pi cluster, using the configuration files
[cronjob.yaml](cronjob.yaml). Make sure you add the secrets to your cluster as given in the example [redditbot-secrets
.yaml](redditbot-secrets.yaml).


### Required Environment Variables and Values.

The docker image requires the following environment variables.

```
export REDDIT_USERNAME=
export REDDIT_PASSWORD=
export REDDIT_API_CLIENT_SECRET=
export REDDIT_API_CLIENT_ID=
export SENDER_EMAIL=
export SENDER_NAME=
export SENDER_EMAIL_PASSWORD=
export RECEIVER_EMAIL=
```

To get the `REDDIT_API_CLIENT_SECRET` and `REDDIT_API_CLIENT_ID`,
please register an app with reddit: https://www.reddit.com/prefs/apps/

Rest are your email and account information.

## Operational Mechanics

This is a reference information for quick building and deploying.

Building the image.

```
docker build -t skumaran/redditbot:v0.1 .

```

Pushing the image.

```
docker push skumaran/redditbot:v0.1

```

## Setup a Crontab

```
0 7 * * * /usr/bin/docker run --env REDDIT_USERNAME=MY-VALUE \
           --env REDDIT_PASSWORD=MY-VALUE \
           --env REDDIT_API_CLIENT_SECRET=MY-VALUE \
           --env REDDIT_API_CLIENT_ID=MY-VALUE \
           --env SENDER_EMAIL=MY-VALUE \
           --env SENDER_EMAIL_PASSWORD=MY-VALUE \
           --env SENDER_NAME=MY-VALUE \
           --env RECEIVER_EMAIL=MY-VALUE \
           skumaran/redditbot:v0.1
```

### Creating a Kubernetes Secret

```
$ docker login -u username

$ kubectl create secret generic skumaran-docker-login --from-file=.dockerconfigjson=/home/senthil/.docker/config.json --type=kubernetes.io/dockerconfigjson

secret/skumaran-docker-login created
```

Creating Secrets yaml

```$xslt

apiVersion: v1
kind: Secret
metadata:
  name: redditbot-secrets
type: Opaque
data:
  REDDIT_PASSWORD:
  REDDIT_API_CLIENT_SECRET:
  REDDIT_API_CLIENT_ID:
  SENDER_EMAIL_PASSWORD:

```

Create each of the secrets in the base64 encoded format.

```
echo -n aerobic-tram-repulse-ate | base64
```

### Example of an Bot-Email.

![Image of Bot-Email](https://i.imgur.com/u0ihN56.png)

### Where am I running it?

I am running it on my [4-node kubernetes cluster](http://xtoinfinity.com/posts/2020/02/02/kubernetes-cluster-using-raspberry-pi.html).

The master is this.

![Kubernetes Cluster](https://i.imgur.com/zJBFZn9.png)
