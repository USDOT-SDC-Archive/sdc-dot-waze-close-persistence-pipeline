[![Build Status](https://travis-ci.org/usdot-jpo-sdc-projects/sdc-dot-waze-close-persistence-pipeline.svg?branch=develop)](https://travis-ci.org/usdot-jpo-sdc-projects/sdc-dot-waze-close-persistence-pipeline)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=usdot-jpo-sdc-projects_sdc-dot-waze-close-manifest-pipeline&metric=alert_status)](https://sonarcloud.io/dashboard?id=usdot-jpo-sdc-projects_sdc-dot-waze-close-manifest-pipeline)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=usdot-jpo-sdc-projects_sdc-dot-waze-close-manifest-pipeline&metric=coverage)](https://sonarcloud.io/dashboard?id=usdot-jpo-sdc-projects_sdc-dot-waze-close-manifest-pipeline)

# sdc-dot-waze-close-persistence-pipeline
Lambda function that is triggered at the end of waze persistence step function workflow. The primary function of this lambda function is to delete the message from queue and publish a notification upon successfully processing each message
