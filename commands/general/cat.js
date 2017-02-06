const Commando = require('discord.js-commando');
const request = require('request'); 

module.exports = class GeneralCommands extends Commando.Command {
    constructor(client) {
        super(client, {
            name: "cat",
            group: "general",
            memberName: "cat",
            description: "Posts a random cat gif.",
            examples: ["cat"]
        })
    }

    async run(msg, args, client){
        request('http://edgecats.net/random', function (error, response, body) {
            if (!error && response.statusCode == 200) {
                return msg.reply(body);
            }
        });
    }
}