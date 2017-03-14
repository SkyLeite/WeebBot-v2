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

        request(`http://db.kakia.org/item/search?name=${encodeURIComponent(item)}`, function (error, response, body) {
            if (!error && response.statusCode == 200) {
                let js = JSON.parse(body);

                try{
                    if (js.length > 0){
                        let embed = { embed: {
                            color: 3447003,
                            title: "Results",
                            url: "http://kaze.rip",
                            fields: []
                        }}

                        js.slice(0, 4).forEach(function (item) {
                            if (item['PriceInfo'].length > 0){
                                embed['embed']['fields'].push({name: item['EnName'], value: `**Price:** ${item['PriceInfo'].find(x => x['Ship'] === 2)['Price'].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")}\n**JP:** ${item['JpName']}`})
                            }
                            else{
                                embed['embed']['fields'].push({name: item['EnName'], value: `**Price:** Undefined\n**JP:** ${item['JpName']}`})
                            }
                        })

                        msg.reply("", embed)
                    }
                    else{
                        msg.reply("could not find that item. Please try again with a different query.")
                    }
                }
                catch(err){
                    console.log(err);
                }
            }
        });
    }
}