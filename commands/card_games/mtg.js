const Commando = require('discord.js-commando');
const request = require('request');

module.exports = class SVCommands extends Commando.Command {
    constructor(client) {
        super(client, {
            name: "mtg",
            group: "card_games",
            memberName: "mtg",
            description: "Looks up Magic The Gathering card information.",
            examples: ["mtg Water Fairy"],

            args: [
                {
                    key: 'card',
                    label: 'card',
                    prompt: 'what card do you want to look up?',
                    type: 'string'
                }
            ]
        })
    }

    async run(msg, args, client){
        let card = args.card;

        request(`https://api.magicthegathering.io/v1/cards?name=${encodeURIComponent(card)}`, function(error, response, body) {
            if (!error && response.statusCode == 200) { 
                let data = JSON.parse(body);

                if (data['cards'].length > 0) {
                    let cardInfo = data['cards'][0]

                    let embed = { embed: {
                        color: 3447003,
                        title: `Magic The Gathering`,
                        url: "http://magicthegathering.io",
                        fields: [{
                            name: "Stats",
                            value: `**Name:** ${cardInfo['name']}\n**Cost:** ${cardInfo['manaCost'].replace(/{/g, '').replace(/}/g, '')}\n**Power / Toughness:** ${cardInfo['power']}/${cardInfo['toughness']}\n**Type:** ${cardInfo['type']}`,
                            inline: true
                        },
                        {
                            name: "Text",
                            value: cardInfo['text']
                        }]
                    }}

                    if (cardInfo['imageUrl']){
                        embed.embed.thumbnail = {
                            url: cardInfo['imageUrl']
                        }
                    }

                    msg.reply("", embed)
                }
                else {
                    return msg.reply(`\`${card}\` did not match any cards. Please try again.`)
                }
            }
        })
    }
}