const Commando = require('discord.js-commando');
const Discord = require('discord.js')

module.exports = class PSO2Commands extends Commando.Command {
    constructor(client) {
        super(client, {
            name: "builds",
            group: "pso2",
            memberName: "builds",
            description: "PSO2 meta builds."
        })
    }

    async run(msg){
        return msg.reply("", {embed: {
            color: 3447003,
            title: "Phantasy Star Online 2",
            url: "http://pso2.jp",
            footer: {
                text: "Subject to change."
            },
            fields: [{
                name: "Striking",
                value: "[Hu/Fi](https://goo.gl/DZQb73)\n[Fi/Hu](https://goo.gl/fcJZpV)\n[Br/Hu](https://goo.gl/dZyF9X)\n[Bo/Hu](https://goo.gl/OZOMN7)",
                inline: true
            },
            {
                name: "Ranged",
                value: "[Ra/Hu](https://goo.gl/8O7Wms)\n[Br/Ra](https://goo.gl/SAaSA6)\n[Gu/Ra](https://goo.gl/mdNFR2)",
                inline: true
            },
            {
                name: "Tech",
                value: "[Fo/Te](https://goo.gl/hQthMq)\n[Te/Br](https://goo.gl/bqpYJN)\n[Su/XX](https://goo.gl/AEIBzm)",
                inline: true
            }]
        }});
    }
}