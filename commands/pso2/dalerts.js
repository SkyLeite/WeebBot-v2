const Commando = require('discord.js-commando');

module.exports = class PSO2Commands extends Commando.Command {
    constructor(client) {
        super(client, {
            name: "dalerts",
            group: "pso2",
            memberName: "disablealerts",
            description: "Disables EQ alerts on the current server.",
            examples: ["dalerts"],
            guildOnly: true
        })
    }

    hasPermission(msg) {
        return msg.member.hasPermission('MANAGE_GUILD');
    }

    async run(msg, args, client){
        this.client.provider.set(msg.guild, "alerts");
        return msg.reply(`${msg.author} Alerts successfully disabled on this server.`);
    }
}