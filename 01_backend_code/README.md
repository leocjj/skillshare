#  Backend code
Backend code created in python within AWS lambda function

## Notes

### General

Function called from an API Gateway (translate-API), receive three parameters inside an array to get a translation.

### List of parameters

```
event: array to receive parameters from API

event['queryStringParameters']['TargetLang']: Target language for translate

event['queryStringParameters']['Bucket']: AWS Bucket (folder) to find transcription S3, MUST BE IN THE SAME LAMBDA SERVER.

event['queryStringParameters']['Bucketkey']: AWS key of S3 object (file) with transcription text
```

### Functionalities

#### Coding notes:
1) If the source language is the same target language, a JSON is also stored
    using the original transcription text.
2) AWS translate_text() allows 5000 bytes per request, so original
    transcription must be split in case its size is bigger.
3) Functionalities:

* Detects if transcription (key) exists in Bucket. If not, returns 400
* Returns translations already stored to improve efficiency
* If no translation found, automatically detects transcription language. If language can't be detected, returns 400.
* If the target language is the same transcription language, converts transcription to JSON, store it and return it
* If the target language is different than transcription language, it translates it, converts transcription to JSON, store it, return it.
Stored file name: key_targetLanguage.srt (e.g: video1_es.srt)
* Translates transcriptions bigger than 5000 bytes (maximum allowed by request), doing split without cutting sentences. Step for split can be 4990 for Unicode-8 general languages, but for very special characters languages, step must be as low as 600.
* Returns 500 in case any error occurs during the translate/store task.

### Return

```
'''Resonse dictionary '''
resp = {    'statusCode': 200,
            'headers': {'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'targetKey': targetkey
                        },
                        'body': json.dumps([])
        }
```


## Testing

...

## Flowchart

...

## Getting Started

...


## Examples

```
...
```

## Built With

* AWS console


## Authors

* **Carlos Andres Garcia Morales** - [Github](https://github.com/agzsoftsi) - [Twitter](https://twitter.com/karlgarmor)
* **Ivan Dario Lasso Gil** - [Github](https://github.com/ilasso) - [Twitter](https://twitter.com/ilasso)
* **Leonardo Calderon Jaramillo** - [Github](https://github.com/leocjj) - [Twitter](https://twitter.com/leocj)

