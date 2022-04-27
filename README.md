# Requirements
- A Customer.io account
- A Customer.io segment containing your internal report recipients, and the ID of that segment (found in the URL: https://fly.customer.io/env/<workspace_id>/segments/<segment_id>/overview)
- A Customer.io API Triggered Broadcast and the ID of that Broadcast (https://fly.customer.io/env/<workspace_id>/broadcasts/broadcast/<broadcast_id>/overview)
- Your Workspace ID (found in the URL after `/env/`)
- A way to run the service. The code is currently written as a Dockerized app to be run using Google Cloud Run.
- A way to schedule the execution of the application. We use Google Cloud Scheduler internally.

# What to expect
- If there have been no newsletter or broadcast email sends in the last 7 days, you won't get a report for the respective entity

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

# Triggering the script
The script expects a POST request to the /generate endpoint. The payload only takes the `entity` property and either the `campaigns` or `newsletters` value:

```
{
  "entity":"<campaigns OR newsletters>"
}
```

If you would like reports for both campaigns and newsletters, you'll need to trigger the script twice, one with the `entity` value set to `camnpaigns` and `newsletters` respectively.

# Sample Email Report HTML
There is sample HTML code in the `sample_email` folder. The code already contains the trigger variables that the report expects. You can customize the layout as much as you'd like. Line 133 contains a commented section where you can add a second logo. 

# Set up the Broadcast in Customer.io
### Create the Broadcast
Copy the ID of the Broadcast after you save it. You'll need it for your `.env` configuration.
<img width="1190" alt="Screen Shot 2022-04-27 at 11 33 16 AM" src="https://user-images.githubusercontent.com/3914101/165600584-14e2610f-0c62-4050-9511-35a281100c8e.png">

### Define the Recipient Segment
You will need profiles created in your workspace for everyone you'd like to send the report to. Copy the ID of the segment after you save it. You'll need it for your `.env` configuration.
<img width="1179" alt="Screen Shot 2022-04-27 at 11 34 48 AM" src="https://user-images.githubusercontent.com/3914101/165600655-0f47eb06-c374-4a2b-8ecd-b2b0ad97ba23.png">

### Add and configure the email to your workflow
Use the sample email noted above, or configure your own. If you create your own, you'll need to map the report variables from the script to the trigger variables in the email code. **Tip: you can start this message in Draft Mode to make sure it's all looking good before sending automatically**
<img width="943" alt="Screen Shot 2022-04-27 at 12 06 36 PM" src="https://user-images.githubusercontent.com/3914101/165601389-172d43bd-95c2-4c29-9ba2-f9680feec674.png">

### Start your Broadcast
Follow the remaining steps in the UI to set a goal or simply activate your Broadcast.


