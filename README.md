[![Build Status](https://travis-ci.com/usdot-jpo-sdc/sdc-dot-waze-close-persistence-pipeline.svg?branch=master)](https://travis-ci.com/usdot-jpo-sdc/sdc-dot-waze-close-persistence-pipeline)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=usdot-jpo-sdc_sdc-dot-waze-close-persistence-pipeline&metric=alert_status)](https://sonarcloud.io/dashboard?id=usdot-jpo-sdc_sdc-dot-waze-close-persistence-pipeline)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=usdot-jpo-sdc_sdc-dot-waze-close-persistence-pipeline&metric=coverage)](https://sonarcloud.io/dashboard?id=usdot-jpo-sdc_sdc-dot-waze-close-persistence-pipeline)

# sdc-dot-waze-close-persistence-pipeline
Lambda function that is triggered at the end of waze persistence step function workflow. The primary function of this lambda function is to delete the message from queue and publish a notification upon successfully processing each message
