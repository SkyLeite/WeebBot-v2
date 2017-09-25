const Commando = require('discord.js-commando');

module.exports = class PSO2Commands extends Commando.Command {
    constructor(client) {
        super(client, {
            name: "bumped",
            group: "pso2",
            memberName: "bumped",
            description: "Enables Bumped alerts",
            examples: ["alerts #general"],
            guildOnly: true,

            args: [
                {
                    key: 'channel',
                    label: 'channel',
                    prompt: 'on what channel do you want the alerts to be displayed on?',
                    type: 'channel'
                }
            ]
        })
    }

    hasPermission(msg) {
        return msg.member.hasPermission('MANAGE_GUILD');
    }

    async run(msg, args, client){
        let channel = args.channel.id;

        this.client.provider.set(msg.guild, "bumped", channel);
        return msg.reply(`Bumped alerts successfully enabled on channel #${args.channel.name}`);
    }
}