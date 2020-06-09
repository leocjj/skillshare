import json
import boto3

'''    
Coding notes:
1) If the source language is the same target language, a JSON is also stored
    using the original transcription text.
2) AWS translate_text() allows 5000 bytes per request, so original
    transcription must be split in case its size is bigger.
3) Functionalities:
    *) Detects if transcription (key) exists in Bucket. If not, returns 400
    *) Returns translations already stored to improve efficiency
    *) If no translation found, automatically detects transcription language.
        If language can't be detected, returns 400
    *) If the target language is the same transcription language, converts
        transcription to JSON, store it and return it
    *) If the target language is different than transcription language, it
        translates it, converts transcription to JSON, store it, return it.
        Stored file name: key_targetLanguage.srt (e.g: video1_es.srt)
    *) Translates transcriptions bigger than 5000 bytes (maximum allowed by
        request), doing split without cutting sentences. Step for split can be
        4990 for Unicode-8 general languages, but for very special characters
        languages, step must be as low as 600.
    *) Returns 500 in case any error occurs during the translate/store task.
'''


def lambda_handler(event, context):
    '''
    This function is called from an API Gateway (translate-API), receive three
    parameters inside an array to get a translation.
    event: array to receive parameters from API
    event['queryStringParameters']['TargetLang']:
        Target language for translate
    event['queryStringParameters']['Bucket']:
        AWS Bucket (folder) to find transcription S3,
        MUST BE IN THE SAME LAMBDA SERVER
    event['queryStringParameters']['Bucketkey']:
        AWS key of S3 object (file) with transcription text
    '''
    target_lang = event['queryStringParameters']['TargetLang']
    bucket = event['queryStringParameters']['Bucket']
    key = event['queryStringParameters']['Bucketkey']
    targetkey = key[:key.rfind('.')] + '_' + target_lang + '.srt'

    ''' Resonse dictionary '''
    resp = {    'statusCode': 200,
                'headers': {'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*',
                            'targetKey': targetkey
                            },
                            'body': json.dumps([])
            }

    try:
        ''' TRY TO FIND ORIGINAL TRANSCRIPTION STORED IN S3 '''
        s3 = boto3.client('s3')
        s3.head_object(Bucket=bucket, Key=key)
    except Exception as e:
        resp['statusCode'] = 400
        resp['body'] = json.dumps('Video transcription not found')
        return resp

    try:
        '''GETS ALREADY STORED TRANSLATION, IF NOT, TRANSLATE TRANSCRIPTION'''
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object

        try:
            '''TRY TO FIND IF TRANSLATION IS ALREADY DONE AND STORED IN S3 '''
            s3 = boto3.client('s3')
            s3.head_object(Bucket=bucket, Key=targetkey)
            translation_file = s3.get_object(Bucket=bucket, Key=targetkey)
            resp['body'] = translation_file['Body'].read().decode("utf-8")
            return resp
            
        except Exception as e:
            ''' IF TRANSLATION DOSN'T EXIST, TRANSLATE IT AND STORE IT IN S3'''

            # To get S3 object with original transcrtion
            response = s3.get_object(Bucket=bucket, Key=key)
            text = str(response['Body'].read().decode('utf-8'))

            # Detect source language by sending first 100 characters to check
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html
            source_lang = "auto"
            try:
                client = boto3.client('comprehend')
                responseLanguage = client.detect_dominant_language(Text=text[:100])
                source_lang = responseLanguage['Languages'][0]['LanguageCode']
            except Exception as e:
                resp['statusCode'] = 400
                resp['body'] = json.dumps('Video language not soported')
                return resp

            # Translate text if target language is not the source languaje
            if target_lang != source_lang:
                lenn = len(text)
                # 5000 is the maximum of bytes for AWS translate_text.
                # step can be 4990 for unicode-8 languages, or 600 for all.
                step = 4990
                translate_client = boto3.client('translate')
                if lenn <= step:
                    translated_text = translate_client.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
                    text = translated_text.get('TranslatedText')
                else:
                    srtTemp = ''
                    indexLow = 0
                    indexHigh = text.rfind('\n\n', 0, step)
                    while(indexHigh < lenn and indexHigh != -1):
                        translated_text = translate_client.translate_text(Text=text[indexLow:indexHigh], SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
                        srtTemp += translated_text.get('TranslatedText') + '\n\n'
                        indexLow = indexHigh + 2
                        indexHigh = text.rfind('\n\n', indexLow , indexLow + step)
                    translated_text = translate_client.translate_text(Text=text[indexLow:lenn], SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
                    srtTemp += translated_text.get('TranslatedText')
                    text = srtTemp

            # JSON conversion
            srt_list_translated = []
            for i in text.split('\n\n'):
                phrase = i.split('\n')
                srt_list_translated.append({    'index': phrase[0],
                                                'start': phrase[1][:8],
                                                'content': phrase[2]
                                            })
            
            ########## ALWAYS ACTIVATE THIS IN PRODUCTION ##########
            ##### Store translation in a S3 object for future requests #####
            s3.put_object(  Bucket=bucket, Key=targetkey,
                            Body=json.dumps(srt_list_translated),
                            Metadata={'lang':target_lang,'src_trscpt_file':key})

            resp['body'] = json.dumps(srt_list_translated)
            return resp
            
    except Exception as e:
        resp['statusCode'] = 500
        resp['body'] = json.dumps('An error occurred while translations was in process, please try again later')
        return resp