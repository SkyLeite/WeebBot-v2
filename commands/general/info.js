const Commando = require('discord.js-commando');
const request = require('request'); 

module.exports = class GeneralCommands extends Commando.Command {
    constructor(client) {
        super(client, {
            name: "info",
            group: "general",
            memberName: "info",
            description: "Bot information.",
            examples: ["info"]
        })
    }

    async run(msg, client){
        return msg.reply("", {embed: {
            color: 3447003,
            title: `${this.client.user.username}#${this.client.user.discriminator}`,
            url: "http://rodrigo.li",
            thumbnail: {
                url: this.client.user.avatarURL
            },
            fields: [{
                name: "Information",
                value: `**Servers:** ${this.client.guilds.array().length}\n**Since:** ${this.client.user.createdAt.toDateString()}`,
                inline: true
            }]
        }});
    }
}