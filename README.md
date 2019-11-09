# reflect-slack-app

A simple example of a Slack application to
go along with work-in-progress blog post at
https://lethain.com/creating-reflect-slack-app/

To deploy these files follow the tutorial, update `reflect/env.yaml`
to include your Slack secrets, and then:

    cd reflect
    gcloud functions deploy dispatch \
    --env-vars-file env.yaml \
    --runtime python37 --trigger-http

After which point you're good to go... plus a hundred
other steps in the tutorial tho tbh.