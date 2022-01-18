# Peloton Looker

## Motivations
As a data person who's pretty into Peloton, I wanted to see if I could access more detailed data about my workouts than I could get in the Peloton interface. Luckily, Peloton provides a number of undocumented API endpoints that [others](https://github.com/geudrik/peloton-client-library/blob/master/API_DOCS.md) [have](https://coda.io/@atc/analyze-your-peloton-workout-stats-with-real-time-updates) [discovered](https://lgellis.github.io/pelotonR/) and [documented](https://app.swaggerhub.com/apis/DovOps/peloton-unofficial-api/0.2.3#/).

Those resources gave me the information I needed to build a more comprehensive scraper that pulls down all of the accessible data I'm interested in. This included high-level metadata about my (and my friend's) workouts, as well as detailed, second-by-second performance metrics from the bike.

Because the volume of this data was more than I wanted to process locally, I also wrote functions to handle uploading that data to a database. I chose Google BigQuery because it's serverless and has a generous free tier that gives me more than enough capacity to query the ~1Gb of data to my heart's content.

Also, because I spent 5+ years working on Looker, a data exploration tool, I of course wrote a simple LookML model for the data as well, to make it easy to explore the data and share my findings.

## Using Peloton Looker

This is relatively straighforward Python script that's meant to be run from the command line. It's been tested on Python 3.8 and 3.9, but will probably work fine on any current version of Python3.

I tried to encapsulate all the database-facing functions in their own file so that if you want to swap out BigQuery for another database, or just write the outputs locally, it should be relatively straightforward to fork this.

To make the Peloton API bits work, you'll need to set your Peloton username and password as environment variables:
```
USERNAME=myPelotonUsername;PASSWORD=mySecretPassword;
```
The current version will also need you to set up the appropriate pieces in GCP.

To do this, you'll need to enable BigQuery on your GCP account, create a dataset in your project called `peloton`, create a service account, and download the JSON key for that service account so the script can talk to BigQuery.

To make sure BigQuery is enabled and accessible, you can follow [this tutorial](https://cloud.google.com/bigquery/docs/quickstarts/quickstart-cloud-console). It also walks you through creating a dataset.

Then [create a service account here](https://console.cloud.google.com/iam-admin/serviceaccounts/create). Make sure to grant the service account both the BigQuery Data Editor and BigQuery Job User roles. Once the service account is created, you'll need to create a JSON key for it. You can find [instructions here](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating).

Finally, add one more environment variable called `GOOGLE_APPLICATION_CREDENTIALS` in the environment you're going to run the script in that points to the JSON key you've downloaded.

Now you should be all set to run the `scraper.py`. The first run will take the longest, since it needs to fetch your full history (as well as the full history of all the users you follow). Subsequent runs will only fetch the new workouts you've completed since the last time the script was run.

## Looker Model

I'm also including the basic LookML model I wrote to make exploring the data easier. If you happen to have access to a Looker instance (through work?), you can clone the files here and throw them in your dev sandbox. You'll need to give the Looker instance a connection to your BigQuery peloton dataset. If you leave the Python script as-is, the only thing you'll need to set in the Looker model is the connection string.

The LookML files can be found in the Looker directory.

## Next steps

I'll post some analyses of the 7m rows of data I've retrieved soon.

I'll also consider making it easier to write the data locally. Feel free to file other issues if there are other things you'd like to see.

