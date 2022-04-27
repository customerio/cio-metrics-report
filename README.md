# Requirements
- A Customer.io account
- A Customer.io segment containing your internal report recipients, and the ID of that segment (found in the URL: https://fly.customer.io/env/<workspace_id>/segments/<segment_id>/overview)
- A Customer.io API Triggered Broadcast and the ID of that Broadcast (https://fly.customer.io/env/<workspace_id>/broadcasts/broadcast/<broadcast_id>/overview)
- Your Workspace ID (found in the URL after `/env/`)
- A way to run the service. The code is currently written as a Dockerized app to be run using Google Cloud Run.
- A way to schedule the execution of the application. We use Google Cloud Scheduler internally.

# Environment Variables
- If you choose to deploy on GCS Cloud Run, you'll need to follow their instructions for handling env variables. The script expects the format listed here:
```
AppAPITOKEN = "<An App API token created from your Customer.io Workspace Settings under the "App API" tab>"
workspaceID = <Your Workspace ID as an INT (no quotes)>
APITBSegment = <The ID as an INT (no quotes) of the Customer.io segment that defines who should receive the emailed report>
APITBID = <Your API Triggered Broadcast ID as an INT (no quotes)>
```
- To run locally, create a `.env` file with the same format.

# To deploy on GCS
- In the directory of this code, run `pip install -r requirements.txt`
- Log in to your Google Cloud Services account via the CLI
- Run `gcloud app deploy` and select the desired settings

# Sample Email Report HTML
There is sample HTML code in the `sample_email` folder. The code already contains the trigger variables that the report expects. You can customize the layout as much as you'd like. Line 133 contains a commented section where you can add a second logo. 