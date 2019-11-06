# reflect-slack-app

A simple example of a Slack application to
go along with work-in-progress blog post at
https://lethain.com/creating-reflect-slack-app/

To deploy these files follow the tutorial, update `reflect/env.yaml`
to include your Slack signing secret, and then:

    cd reflect
    gcloud functions deploy reflect_post \
    --env-vars-file env.yaml \
    --runtime python37 --trigger-http
    gcloud functions deploy recall_post \
    --env-vars-file .env.yaml \
    --runtime python37 --trigger-http

