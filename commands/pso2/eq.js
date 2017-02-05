const Commando = require('discord.js-commando');
const Discord = require('discord.js')

module.exports = class PSO2Commands extends Commando.Command {
    constructor(client) {
        super(client, {
            name: "alerts",
            group: "pso2",
            memberName: "alerts",
            description: "Enables EQ alerts",
            examples: ["enable #general 5, 7, 9"],

            args: [
                {
                    key: 'channel',
                    label: 'channel',
                    prompt: 'on what channel?',
                    type: 'channel'
                },
                {
                    key: 'ships',
                    label: 'ship',
                    prompt: 'what ships do you want to be alerted for?',
                    validate: (args) => {
                        if (args >= 1 && args <= 10){
                            return true;
                        }
                    },
                    type: 'integer',
                    infinite: true
                }
            ]
        })
    }

    hasPermission(msg) {
        return msg.member.hasPermission('MANAGE_GUILD');
    }

    async run(msg, args, client){
        let channel = args.channel;
        let dict = {}
        dict["ships"] = args.ships;
        dict["channel"] = channel.id;

        this.client.provider.set(msg.guild, "alerts", dict);
        return channel.sendMessage(`${msg.author} Alerts successfully enabled for ships ${args.ships.join(', ')} on channel #${args.channel.name}`);
    }
}