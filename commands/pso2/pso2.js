const Commando = require('discord.js-commando');
const Discord = require('discord.js')

module.exports = class PSO2Commands extends Commando.Command {
    constructor(client) {
        super(client, {
            name: "pso2",
            group: "pso2",
            memberName: "pso2",
            description: "General information about PSO2."
        })
    }

    async run(msg){
        return msg.reply("", {embed: {
            color: 3447003,
            title: "Phantasy Star Online 2",
            url: "http://pso2.jp",
            description: "General information about PSO2.",
            fields: [{
                name: "Information",
                value: "[News](http://bumped.org/psublog)\n[Reddit](http://reddit.com/r/pso2)\n[Guides](http://fulldive.nu/)\n[PSO-World](http://pso-world.com)\n[Wiki](http://pso2.swiki.jp)",
                inline: true
            },
            {
                name: "Downloads",
                value: "[English Launcher](http://arks-layer.com/)\n[Mods](https://goo.gl/M8PpWh)",
                inline: true
            }]
        }});
    }
}