const Commando = require('discord.js-commando');
const request = require('request');

module.exports = class PSO2Commands extends Commando.Command {
    constructor(client) {
        super(client, {
            name: "item",
            group: "pso2",
            memberName: "item",
            description: "Looks up Japanese name of items.",
            examples: ["item monomate"],

            args: [
                {
                    key: 'item',
                    label: 'item',
                    prompt: 'what item do you want to look up?',
                    type: 'string'
                }
            ]
        })
    }

    async run(msg, args, client){
        let item = args.item;

        request(`http://db.kakia.org/item/search?name=${item.replace(" ", "%20")}`, function (error, response, body) {
            if (!error && response.statusCode == 200) {
                let resp = []
                JSON.parse(body).forEach(function (item) {
                    resp.push(`\`\`ENGLISH:\`\` ${item['EnName']} \\ \`\`JP:\`\` ${item['JpName']}`)
                })

                if (resp.length > 0)
                    if (resp.length > 6){
                        return msg.reply(resp.slice(0, 6).join("\n"))
                    }
                    else{
                        return msg.reply(resp.join("\n"))
                    }
                else{
                    return msg.reply(`could not find ${args.item}`)
                }
            }
        });
    }
}