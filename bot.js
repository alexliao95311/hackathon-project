require('dotenv').config();
const http = require('http');
const fs = require("fs");

var savedContexts = new Map();

const CREATE = 0;
const EDIT = 1;
const REPLY = 2;

const { Client, GatewayIntentBits, Partials } = require("discord.js");
const { fstat } = require('fs');
const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.MessageContent, GatewayIntentBits.GuildMessages, GatewayIntentBits.DirectMessages], partials: [Partials.Channel] });

client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
});

client.on('messageCreate', async message => {
    // context for conversation memory 
    var resuming = false;
    // specific context so the bot knows it's EmeraldAI
    var context = [733,16289,28793,995,460,16762,3165,11741,28725,264,12435,10637,302,20365,6203,28723,1791,8270,396,3469,28725,2899,298,272,2188,395,272,2245,14264,5848,28793,11510,2586,1263,2757,28725,513,368,2613,298,8270,396,3469,302,396,19767,28725,3768,9421,395,14264,5848,28793,19767,2586,995,460,298,6031,272,2188,297,707,2546,28724,2572,28723,995,622,1055,2839,8711,395,272,2188,28723,1047,368,2380,272,11382,28725,312,1405,395,345,4903,28739,733,28748,16289,28793,12206,733,16289,28793,2418,368,8270,396,3469,302,264,5344,19767,28804,733,28748,16289,28793,733,5848,28793,5344,19767,28705];
    if (message.reference) {
        const repliedTo = await message.channel.messages.fetch(message.reference.messageId);
        if (repliedTo && savedContexts.has(repliedTo.id)) {
            context = savedContexts.get(repliedTo.id);
            resuming = true;
        }
    }
    if (message.author.bot) return;
    if (message.content.startsWith("-chat ") || resuming) {
        if (message.author.id == "887131185522806847") {
            return message.reply("You are banned from the AI.")
        }
        const postData = JSON.stringify({
            model: 'llava',
            context,
            prompt: resuming ? message.content : message.content.substring(6) //strips -chat part of msg
        });

        const req = http.request({
            host: '127.0.0.1',
            port: 11434,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(postData),
            },
            path: "/api/generate"
        }, res => {
            res.setEncoding('utf8');
            var text = "";
            var responseMessage = null;
            var interval = null;
            var done = false;
            async function update() {
                if (responseMessage == null) { //if bot hasn't already replied
                    responseMessage = await message.reply("\u200B" + text.split("\n").filter(line => line.indexOf("[sd]") == -1).join("\n") + (done ? "" :
                        "█\n\n[generating...]"));
                } else { //strips out the image generation part of msg
                    responseMessage.edit("\u200B" + text.split("\n").filter(line => line.indexOf("[sd]") == -1).join("\n") + (done ? "" :
                        "█\n\n[generating...]"));
                }
            }
            res.on('data', async (chunk) => {
                var data = JSON.parse(chunk);
                if (!data.done) {
                    text += data.response;
                } else {
                    clearInterval(interval);
                    done = true;
                    await update();
                    if (responseMessage) {
                        savedContexts.set(responseMessage.id, data.context);
                        fs.writeFileSync("contexts.json", JSON.stringify(Object.fromEntries(savedContexts)));
                    }
                    //splits lines
                    for (var line of text.split("\n")) {
                        if (line.indexOf("[sd]") != -1) {
                            var prompt = line.substring(line.indexOf("[sd]") + 4).trim();
                            if (responseMessage) generateAndSendImage(prompt, responseMessage, EDIT);
                            else generateAndSendImage(prompt, message, REPLY);
                        }
                    }
                }
            });
            res.on('end', () => {
            });
            interval = setInterval(() => {
                update();
            }, 2000);
        });

        req.write(postData);
        req.end();
    }
    if (message.content.startsWith("-generate ")) {
        generateAndSendImage(message.content.substring(10).trim(), message);
    }
});

function generateAndSendImage(prompt, message, type = CREATE) {
    const postData = JSON.stringify({
        prompt,
        steps: 10
    });

    const req = http.request({
        host: '127.0.0.1',
        port: 7860,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(postData),
        },
        path: "/sdapi/v1/txt2img"
    }, res => {
        res.setEncoding('utf8');
        var text = "";
        res.on('data', async (chunk) => {
            text += chunk;
        });
        res.on('end', () => {
            const data = JSON.parse(text);
            console.log(data)
            for (var base64 of data.images) {
                var buf = new Buffer(base64, 'base64'); //create buffer convert from base64
                if (type == CREATE) {
                    message.channel.send({
                        files: [
                            {
                                attachment: buf,
                                name: "generation.png"
                            }
                        ]
                    });
                } else if (type == REPLY) {
                    message.reply({
                        files: [
                            {
                                attachment: buf,
                                name: "generation.png"
                            }
                        ]
                    });
                } else if (type == EDIT) {
                    message.edit({
                        files: [
                            {
                                attachment: buf,
                                name: "generation.png"
                            }
                        ]
                    });
                }
            }
        });
    });

    req.write(postData);
    req.end();
}

client.login(token); //enter real token

try {
    var contextsJson = fs.readFileSync("./contexts.json"); // load contexts from file
    savedContexts = new Map(Object.entries(JSON.parse(contextsJson)));
} catch (e) {

}
