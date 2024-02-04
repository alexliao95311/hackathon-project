require('dotenv').config();
const http = require('http');

const { Client, GatewayIntentBits, Partials } = require("discord.js");
const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.MessageContent, GatewayIntentBits.GuildMessages, GatewayIntentBits.DirectMessages], partials: [Partials.Channel] });

client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
});

client.on('messageCreate', async message => {
    if (message.author.bot) return;
    if (message.content.startsWith("-chat ")) {

        const postData = JSON.stringify({
            model: 'llava',
            // context - so the bot remembers that it's in the middle of a conversation and it is acting as an AI discord bot
            context: [733, 16289, 28793, 995, 460, 16762, 3165, 11741, 28725, 264, 12435, 10637, 302, 20365, 6203, 28723, 1791, 8270, 396, 3469, 28725, 2899, 298, 272, 2188, 395, 272, 2245, 14264, 5848, 28793, 11510, 2586, 1263, 2757, 28725, 513, 368, 2613, 298, 8270, 396, 3469, 302, 396, 19767, 28725, 3768, 9421, 395, 14264, 5848, 28793, 19767, 2586, 995, 460, 298, 6031, 272, 2188, 297, 707, 2546, 28724, 2572, 28723, 995, 622, 1055, 2839, 8711, 395, 272, 2188, 28723, 1047, 368, 2380, 272, 11382, 28725, 312, 1405, 395, 345, 4903, 28739, 733, 28748, 16289, 28793, 12206, 28705],
            prompt: message.content.substring(6) //strips the -chat part of the message
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
                // if the response message is null, it means that the bot hasn't sent a message yet, so it sends the message
                if (responseMessage == null) {
                    // strips out the [sd] tags from the response and sends the message, [sd] tags are used to generate images
                    responseMessage = await message.reply("\u200B" + text.split("\n").filter(line => line.indexOf("[sd]") == -1).join("\n") + (done ? "" :
                        "█\n\n[generating...]"));
                } else {
                    responseMessage.edit("\u200B" + text.split("\n").filter(line => line.indexOf("[sd]") == -1).join("\n") + (done ? "" :
                        "█\n\n[generating...]"));
                }
            }
            res.on('data', async (chunk) => {
                // if the bot is done, it sends the message one last time and clears the interval, stops updating msg
                var data = JSON.parse(chunk);
                if (!data.done) {
                    text += data.response;
                } else {
                    clearInterval(interval);
                    done = true;
                    await update();
                    // takes all the lines and splits it every time it hits the enter key, strips sd tag and generates image
                    for (var line of text.split("\n")) {
                        if (line.indexOf("[sd]") != -1) {
                            var prompt = line.substring(line.indexOf("[sd]") + 4).trim();
                            generateAndSendImage(prompt, message);
                        }
                    }
                }
            });
            res.on('end', () => {
            });
            interval = setInterval(() => {
                update(); //update every 2 seconds
            }, 2000);
        });

        req.write(postData);
        req.end();
    }
    if (message.content.startsWith("-generate ")) {
        // generates an image from the prompt
        generateAndSendImage(message.content.substring(10).trim(), message);
    }
});

function generateAndSendImage(prompt, message) {
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
        path: "/sdapi/v1/txt2img" // api path
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
                var buf = new Buffer(base64, 'base64'); // creates a buffer from the base64 string
                message.channel.send({
                    files: [
                        {
                            attachment: buf,
                            name: "generation.png"
                        }
                    ]
                });
            }
        });
    });

    req.write(postData);
    req.end();
}

client.login(process.env.TOKEN);