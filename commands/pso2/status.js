const Commando = require('discord.js-commando');
const Discord = require('discord.js');
const request = require('request');

module.exports = class PSO2Commands extends Commando.Command {
    constructor(client) {
        super(client, {
            name: "status",
            group: "pso2",
            memberName: "status",
            description: "PSO2 server status."
        })
    }

    async run(msg){
        request('http://kakia.org/pso2_status.json', (error, response, body) => {
            if (!error && response.statusCode == 200) {
                const response = JSON.parse(body);

                let embed = { embed: {
                    color: 3447003,
                    title: `Phantasy Star Online 2`,
                    url: "http://pso2.js",
                    thumbnail: {
                        url: "http://bumped.org/psublog/wp-content/uploads/2011/04/logo_pso2.png"
                    },
                    fields: []
                }}

                for (const ship in response) {
                    if (ship != "20") {
                        embed.embed.fields.push({name: response[ship]['Ship'], value: response[ship]['Status'], inline: true})
                    }
                }

                return msg.reply("", embed)
            }
            else{
                console.log('idk');
            }
        })
    }
}