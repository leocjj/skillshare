#  Backend code
Backend code created in AWS lambda function

## Requirements

### General

Function called from an API Gateway (translate-API), receive three parameters inside an array to get a translation.

### list of parameters

event: array to receive parameters from API
event['queryStringParameters']['TargetLang']: Target language for translate
event['queryStringParameters']['Bucket']: AWS Bucket (folder) to find transcription S3, MUST BE IN THE SAME LAMBDA SERVER.
event['queryStringParameters']['Bucketkey']: AWS key of S3 object (file) with transcription text


### Testing


## Flowchart

![Image of Flowchart](https://i.imgur.com/GUtPTTZ.jpg)

## Getting Started

Use the following command to execute Simple Shell:

    ./hsh
After this, the Simple Shell will be executed and a prompt will appears as follow:

    $_
To exit from Simple Shell just put the following command and press enter key:

    $exit

## Supported Builtin Functions and Variables

| Builtin | Description |
|:-------:| ----------- |
| env | Display the environmental variables |
| exit | Exit the Shimple Shell |
| $?| Enviromental variable to store error exit code for each command|


### Examples

```
example code
```

## Built With

* AWS console


## Authors

* **Carlos Andres Garcia Morales** - [Github](https://github.com/agzsoftsi) - [Twitter](https://twitter.com/karlgarmor)
* **Ivan Dario Lasso Gil** - [Github](https://github.com/ilasso) - [Twitter](https://twitter.com/ilasso)
* **Leonardo Calderon Jaramillo** - [Github](https://github.com/leocjj) - [Twitter](https://twitter.com/leocj)

