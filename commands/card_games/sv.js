const Commando = require('discord.js-commando');
const fetch = require('node-fetch');

module.exports = class SVCommands extends Commando.Command {
    constructor(client) {
        super(client, {
            name: "sv",
            group: "card_games",
            memberName: "sv",
            description: "Looks up Shadowverse card information.",
            examples: ["sv Water Fairy"],

            args: [
                {
                    key: 'card',
                    label: 'card',
                    prompt: 'what card do you want to look up?',
                    type: 'string'
                }
            ]
        })
        this.buildCard = (card) => {
            let obj = {
                embed: {
                    color: 3447003,
                    title: `Shadowverse`,
                    url: "https://shadowverse.com",
                    thumbnail: {
                        url: `https://shadowverse-portal.com/image/card/en/C_${card['card_id']}.png`
                    },
                    fields: [{
                        name: "Info",
                        value: `**Name:** ${card['card_name']}\n**Cost:** ${card['cost']} PP\n**Attack / Defense:** ${card['atk']}/${card['life']}\n**Evo Attack / Defense:** ${card['evo_atk']}/${card['evo_life']}`
                    },
                    {
                        name: "Art",
                        value: `[Classic](https://shadowverse-portal.com/image/card/en/C_${card['card_id']}.png) - [Evolved](https://shadowverse-portal.com/image/card/en/E_${card['card_id']}.png)`
                    }]
                }
            };
            if (card['skill_disc'] || card['evo_skill_disc']) {
                obj.embed.fields.push({
                    name: "Skills",
                    value: `${card['skill_disc'] ? `**Skill:** ${card['skill_disc']}\n`: ''}${card['evo_skill_disc'] ? `**Evo Skill:** ${card['evo_skill_disc']}` : null}`
                });
            }

            return obj;
        }
    }

    async run(msg, args, client) {
        let card = args.card;

        let data = await (await fetch(`http://sv.kaze.rip/cards/${card}`)).json();
        if (data.length === 0) {
            return msg.reply("No matches found. Please try again with a different query.");
        }
        else if (data.length === 1) {
            return msg.reply("", this.buildCard(data[0]));
        }
        else if (data.length > 1) {
            let emojilist = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣"];
            let emojis = emojilist.map((obj, i) => {
                return {emoji: obj, num: i+1}
            });

            let cards = data.slice(0, 9).map((i, index) => {
                return `${index + 1}. ${i.card_name} - ${i.cost}PP - ${i.atk}/${i.life} - ${i.evo_atk}/${i.evo_life}`
            });

            let newMsg = await msg.reply(`Found the following matches:\n\`\`\`${cards.join('\n')}\`\`\``);
            for (let e of emojis) {
                await newMsg.react(e.emoji);
            }

            const collector = newMsg.createReactionCollector(
                (reaction, user) => user.id === msg.author.id && emojilist.includes(reaction.emoji.name),
                { time: 15000 }
            );
            collector.on('collect', async r => {
                await newMsg.edit('', this.buildCard(data[(emojis.filter(i => i.emoji === r.emoji.name))[0].num - 1]));
                newMsg.clearReactions().catch();
            });
        }
    }
}