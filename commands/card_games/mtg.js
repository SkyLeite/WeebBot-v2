const Commando = require('discord.js-commando');

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

    async run(msg, args, client) {
        let card = args.card;
        let response = fetch(`https://api.magicthegathering.io/v1/cards?name=${encodeURIComponent(card)}`);

        if (response.statusCode !== 200) return;
        let data = await response.json();

        if (data['cards'].length > 0) {
            for (let i = 0; i < data['cards'].length; i++) {
                if (data['cards'][i]['name'].toLowerCase() == card.toLowerCase()) {
                    var cardInfo = data['cards'][i];
                    break;
                }
            }

            if (typeof cardInfo == 'undefined') {
                var cardInfo = data['cards'][0];
            }

            if (!cardInfo['power'] && !cardInfo['toughness']) {
                cardInfo['power'] = 0;
                cardInfo['toughness'] = 0;
            }

            if (!cardInfo['manaCost']) {
                cardInfo['manaCost'] = 0;
            }
            else {
                cardInfo['manaCost'] = cardInfo['manaCost'].replace(/{/g, '').replace(/}/g, '');
            }

            let embed = {
                embed: {
                    color: 3447003,
                    title: `Magic The Gathering`,
                    url: "http://magicthegathering.io",
                    fields: [{
                        name: "Stats",
                        value: `**Name:** ${cardInfo['name']}\n**Cost:** ${cardInfo['manaCost']}\n**Power / Toughness:** ${cardInfo['power']}/${cardInfo['toughness']}\n**Type:** ${cardInfo['type']}`,
                        inline: true
                    },
                    {
                        name: "Text",
                        value: cardInfo['text']
                    }]
                }
            }

            if (cardInfo['imageUrl']) {
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
}