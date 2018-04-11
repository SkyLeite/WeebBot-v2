const Commando = require('discord.js-commando');
const fetch = require('node-fetch');

module.exports = class PSO2Commands extends Commando.Command {
    constructor(client) {
        super(client, {
            name: "dailies",
            group: "pso2",
            memberName: "dailies",
            description: "Returns the currently active daily orders",
            examples: ["dailies"],
        })
    }

    async run(msg, args, client) {
        try {
            const data = await (await fetch('http://pso2.rodrigo.li/daily')).json();

            return msg.reply("", {
                embed: {
                    color: 3447003,
                    title: "PSO2 Daily Orders",
                    url: "http://pso2.jp",
                    fields: [{
                        name: "Orders",
                        value: data.join("\n")
                    }]
                }
            })
        } catch (err) {
            console.log(err);
        }
    }
}
