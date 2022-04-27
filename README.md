# Requirements
- A Customer.io account
- A Customer.io segment containing your internal report recipients, and the ID of that segment (found in the URL: https://fly.customer.io/env/<workspace_id>/segments/<segment_id>/overview)
- A Customer.io API Triggered Broadcast and the ID of that Broadcast (https://fly.customer.io/env/<workspace_id>/broadcasts/broadcast/<broadcast_id>/overview)
- Your Workspace ID (found in the URL after `/env/`)
- A way to run the service. The code is currently written as a Dockerized app to be run using Google Cloud Run.
- A way to schedule the execution of the application. We use Google Cloud Scheduler internally.

# To deploy on GCS
- In the directory of this code, run `pip install -r requirements.txt`
- Log in to your Google Cloud Services account via the CLI
- Run `gcloud app deploy` and select the desired settings

