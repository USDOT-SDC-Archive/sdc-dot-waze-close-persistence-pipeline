[![Build Status](https://travis-ci.com/usdot-jpo-sdc/sdc-dot-waze-close-persistence-pipeline.svg?branch=develop)](https://travis-ci.com/usdot-jpo-sdc/sdc-dot-waze-close-persistence-pipeline)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=usdot-jpo-sdc_sdc-dot-waze-close-persistence-pipeline&metric=alert_status)](https://sonarcloud.io/dashboard?id=usdot-jpo-sdc_sdc-dot-waze-close-persistence-pipeline)
# sdc-dot-waze-close-persistence-pipeline
This lambda function is responsible for deleting the processed messages from the SQS and publishing the message to SNS about the persistence completion.

<a name="toc"/>

## Table of Contents

[I. Release Notes](#release-notes)

[II. Overview](#overview)

[III. Design Diagram](#design-diagram)

[IV. Getting Started](#getting-started)

[V. Unit Tests](#unit-tests)

[VI. Support](#support)

---

<a name="release-notes"/>


## [I. Release Notes](ReleaseNotes.md)
TO BE UPDATED

<a name="overview"/>

## II. Overview
The primary functions that this lambda function serves:
* **delete_sqs_message** - deletes the processed messages for a particular batch id from the SQS queue.
* **publish_message_to_sns** - publishes a message to SNS topic that the persistence is completed for a particular batch id.

<a name="design-diagram"/>

## III. Design Diagram

![sdc-dot-waze-close-persistence-pipeline](images/waze-data-persistence.png)

<a name="getting-started"/>

## IV. Getting Started

The following instructions describe the procedure to build and deploy the lambda.

### Prerequisites
* NA 

---
### ThirdParty library

*NA

### Licensed softwares

*NA

### Programming tool versions

*Python 3.6


---
### Build and Deploy the Lambda

#### Environment Variables
Below are the environment variables needed :- 

BATCH_NOTIFICATION_SNS - {arn_of_sns_topic_to_send_notification}

SQS_PERSISTENCE_ORCHESTRATION_QUEUE_NAME - {sqs_persistence_orchestration_queue_name}

SQS_PERSISTENCE_ORCHESTRATION_HIS_QUEUE_NAME - {sqs_persistence_orchestration_for_historical_data_queue_name}

#### Build Process

**Step 1**: Setup virtual environment on your system by foloowing below link
https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-deployment-pkg.html#with-s3-example-deployment-pkg-python

**Step 2**: Create a script with below contents e.g(sdc-dot-waze-close-persistence-pipeline.sh)
```#!/bin/sh

cd sdc-dot-waze-close-persistence-pipeline
zipFileName="sdc-dot-waze-close-persistence-pipeline.zip"

zip -r9 $zipFileName common/*
zip -r9 $zipFileName lambdas/*
zip -r9 $zipFileName README.md
zip -r9 $zipFileName persistence_close_statemachine_handler_main.py
zip -r9 $zipFileName root.py
```

**Step 3**: Change the permission of the script file

```
chmod u+x sdc-dot-waze-close-persistence-pipeline.sh
```

**Step 4** Run the script file
./sdc-dot-waze-close-persistence-pipeline.sh

**Step 5**: Upload the sdc-dot-waze-close-persistence-pipeline.zip generated from Step 4 to a lambda function via aws console.

[Back to top](#toc)

---
<a name="unit-tests"/>

## V. Unit Tests

TO BE UPDATED

---
<a name="support"/>

## VI. Support

For any queries you can reach to support@securedatacommons.com
---
[Back to top](#toc)