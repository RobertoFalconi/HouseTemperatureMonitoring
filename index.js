// Load the console log
console.log('Loading function');
const https = require('https');
// Load the AWS SDK
var AWS = require("aws-sdk");
    // Set up the code to call when the Lambda function is invoked
    exports.handler = (event, context, callback) => {
    if (event.clickType == "SINGLE") {
        // Load the message passed into the Lambda function into a JSON object 
        var eventText = JSON.stringify(event, null, 2);
        // Log a message to the console, you can view this text in the Monitoring tab in the Lambda console or in the CloudWatch Logs console
        console.log("Received event:", eventText);
        // Individuate the user
        if (event.serialNumber == "G030PT023203RNXB") var user = "Roberto";
        // Create a string extracting the click type and serial number from the message sent by the AWS IoT button
        var messageText = "\nHi everyone, I'm home!\n" + user;
        // Write the string to the console
        console.log("Message to send: " + messageText);
        // Create an SNS object
        var sns = new AWS.SNS();
        // Populate the parameters for the publish operation
        // - Message : the text of the message to send
        // - TopicArn : the ARN of the Amazon SNS topic to which you want to publish 
        var params = {
            Message: messageText,
            TopicArn: "arn:aws:sns:eu-central-1:972603806692:MyIoTButtonSNS"
         };
        sns.publish(params, context.done);
    }
    if (event.clickType == "DOUBLE") {
        /*
        https.get('https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY', (resp) => {
            let data = '';
     
            // A chunk of data has been recieved.
            resp.on('data', (chunk) => {
              data += chunk;
            });
        
            // The whole response has been received. Print out the result.
            resp.on('end', () => {
              console.log(JSON.parse(data).explanation);
            });
     
        }).on("error", (err) => {
             console.log("Error: " + err.message);
        });
        */
    }
    if (event.clickType == "LONG") {
        
    }
};