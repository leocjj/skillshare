var AWS = require('aws-sdk');
const utf8 = require('utf8');

AWS.config.update({region: 'us-east-1'});

var s3 = new AWS.S3();

// Los nombres de buckets deben ser únicos entre todos los usuarios de S3

var myBucket = 'skillshare-terraform-state-017784105438';

var myKey = 'testilasso';
s3.getObject({Bucket: myBucket, Key: myKey,ResponseContentType:'application/json'}, function(err, data) {
   if (err) {
      console.log(err);
    }
    else{
       datas3 = JSON.stringify(data);
       ds3JSON = JSON.parse(datas3);
       //console.log(ds3JSON.Body.data);
       let string = "";
       //console.log(data.toString('utf8'));
       //console.log(utf8.decode(data));
       for (let i=0; i < ds3JSON.Body.data.length; i++){
            //console.log("entre" + String.fromCharCode(ds3JSON.Body.data[i])+'despues');
           string += String.fromCharCode(ds3JSON.Body.data[i]);
       }
       console.log(string);
       var translate = new AWS.Translate({apiVersion: '2017-07-01'});
       translate.translateText({SourceLanguageCode:'en',TargetLanguageCode:'es',Text:string}, function(err,data){
          if (err) console.log(err,err.stack);
          else console.log(data);
      });
    }
});
