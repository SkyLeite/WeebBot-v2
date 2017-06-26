const Commando = require('discord.js-commando');
const path = require('path');
const sqlite = require('sqlite')
const request = require('request');
const fs = require('fs');

// This code is terrible wtf

if (!fs.existsSync('./config.json')) {
    fs.writeFileSync('./config.json', '{"token" : "", "prefix" : "!"}')
    console.log('WARNING: Config file is missing. Please edit "config.json" and re-run the script.')
    process.exit()
}

if (!fs.existsSync('./cache.json')){
    fs.writeFileSync('./cache.json', '{ "time" : "02-19-2017 19:05:04 +0000" }')
}

const config = require('./config.json')

const client = new Commando.Client({
    owner: '91387943679172608',
    commandPrefix: config.prefix
});

client
    // Events
    .on('error', console.error)
    .on('warn', console.warn)
    //.on('debug', console.log)
    .on('ready', () => {
        console.log(`-> Client ready! \n-> Logged in as ${client.user.username}#${client.user.discriminator} (${client.user.id})`)
        console.log(`-> Servers: ${client.guilds.array().length}`)
    })
    .on('commandError', (cmd, err) => {
        if(err instanceof Commando.FriendlyError) return;
        console.error('Error in command ${cmd.groupID}:${cmd.memberName}', err)
    })

client.registry
    // Custom groups
    .registerGroups([
        ['pso2', 'Phantasy Star Online 2 commmands'],
        ['general', 'General commands'],
        ['card_games', "Card games commands"]
    ])

    // Register default groups, commands and argument types
    .registerDefaults()

    // Register every command in the ./commands/ directory
    .registerCommandsIn(path.join(__dirname, 'commands'))

client.setProvider(
    sqlite.open(path.join(__dirname, 'settings.sqlite3')).then(db => new Commando.SQLiteProvider(db))
).catch(console.error);

// EQ alerts system
client.setInterval(() => {
    request('http://pso2.kaze.rip/eq/', async (error, response, body) => {
        if (!error && response.statusCode === 200) {
            let response = JSON.parse(body);
            let cached = JSON.parse(await fs.readFile("cache.json"));

            if (response[0]['time'] !== cached["time"]){
                client.guilds.forEach((guild) => {
                    if (client.provider.get(guild, "alerts")){
                        let eqs = []
                        let format = []
                        let settings = client.provider.get(guild, "alerts");

                        if (client.channels.get(settings['channel'])){
                            response[0]['eqs'].forEach(function(item) {
                                if (settings['ships'].includes(item['ship'])){
                                    eqs.push(item);
                                }
                            })

                            if (eqs.length > 0){
                                eqs.forEach((eq) => {
                                    format.push(`\`\`SHIP ${eq['ship']}:\`\` ${eq['name']}`);
                                });

                                let string = `:arrow_right: **Emergency Quest Notice**\n\n:watch:**IN 40 MINUTES:**\n${format.join('\n')}`
                                if (client.channels.get(settings['channel']).type === "text" && client.channels.get(settings['channel']).permissionsFor(client.user).hasPermission("SEND_MESSAGES")){
                                    client.channels.get(settings['channel']).sendMessage(string).catch(function(err) { console.log(err) });
                                }
                            }
                        }
                    }
                })

                try {
                    await fs.writeFile('cache.json', JSON.stringify({ time: response[0]['time'] }, null, 2), 'utf-8') // `{ "time" : "${response[0]['time']}" }`
                } catch (err) {
                    return console.log(err);
                }
            }
        }
    })
}, 50000, client)

client.login(config.token);
