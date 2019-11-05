# reflect-slack-app

A simple example of a Slack application to
go along with work-in-progress blog post at
https://lethain.com/creating-reflect-slack-app/

## deployment

To deploy these files

    cd reflect
    gcloud functions deploy reflect_post --runtime python37 --trigger-http
    gcloud functions deploy recall_post --runtime python37 --trigger-http
