const fetch = require('node-fetch');
const fs = require('mz/fs');
const moment = require('moment');

module.exports = async (client) => {
    try {
        const response = await fetch('http://pso2.kaze.rip/eq/');
        if (response.status !== 200) return;

        const data = await response.json();
        const cache = JSON.parse(await fs.readFile("./cache.json"));

        if (data[0]["time"] !== cache["time"]) {
            await fs.writeFile("cache.json", `{ "time" : "${data[0]["time"]}", "i": ${cache["i"] <= 10 ? cache["i"] + 1 : 0} }`);
            const guilds = client.guilds.filter(guild => { return client.provider.get(guild, "alerts") });
            
            for (let guild of guilds) {
                let settings = await client.provider.get(guild[1], "alerts");
                let eqs = data[0]["eqs"].filter(item => { return settings["ships"].includes(item["ship"]) });
                let format = [];
                
                if (!client.channels.get(settings['channel'])) continue;
                let channel = client.channels.get(settings['channel']);

                if (eqs.length <= 0) continue;
                if (eqs.length > 0 && eqs.length !== 10) {
                    for (let eq of eqs) {
                        format.push(`\`SHIP ${eq['ship']}:\` ${eq['name']} (${eq['jpName']})`);
                    }
                }
                else {
                    format.push(`\`ALL SHIPS:\` ${eqs[0]['name']} (${eqs[0]['jpName']})`);
                }

                let donationString = "\nSupport WeebBot on Gratipay! <https://gratipay.com/Weeb-Bot/>";
                let time = moment(data[0]["when"]);
                let string = `:watch:**IN 40 MINUTES:**\n${format.join('\n')}${cache["i"] === 10 ? donationString : ''}`;
                
                if (channel.type == "text" && channel.permissionsFor(client.user).has("SEND_MESSAGES") && channel.permissionsFor(client.user).has("READ_MESSAGES") && guild[1].available) {
                    try {
                        await client.channels.get(settings['channel']).send(string);
                    } catch (err) {
                        continue;
                    }
                }
            }
        }
    } catch (err) {
        console.error(err);
    }
}