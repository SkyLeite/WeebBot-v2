const Commando = require('discord.js-commando');
const config = require('./config.json')
const path = require('path');
const sqlite = require('sqlite')
const request = require('request');
const fs = require('fs');

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
        console.log(`-> Client ready! \nLogged in as ${client.user.username}#${client.user.discriminator} (${client.user.id})`)
    })
    .on('disconnect', () => { console.warn('Disconnected!'); })
    .on('commandError', (cmd, err) => {
        if(err instanceof Commando.FriendlyError) return;
        console.error('Error in command ${cmd.groupID}:${cmd.memberName}', err)
    })

client.registry
    // Custom groups
    .registerGroups([
        ['pso2', 'Phantasy Star Online 2 commmands'],
        ['general', 'General commands']
    ])

    // Register default groups, commands and argument types
    .registerDefaults()

    // Register every command in the ./commands/ directory
    .registerCommandsIn(path.join(__dirname, 'commands'))

client.setProvider(
    sqlite.open(path.join(__dirname, 'settings.sqlite3')).then(db => new Commando.SQLiteProvider(db))
).catch(console.error);

client.setInterval(function() {
    request('http://pso2.kaze.rip/eq/', function (error, response, body) {
        if (!error && response.statusCode == 200) {
            let response = JSON.parse(body);
            let cached = JSON.parse(fs.readFileSync("cache.json"));

            if (response[0]['time'] != cached["time"]){
                client.guilds.forEach(function(guild) {
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
                            eqs.forEach(function(eq) {
                                format.push(`\`\`SHIP ${eq['ship']}:\`\` ${eq['name']}`);
                            });

                            let string = `:arrow_right: **Emergency Quest Notice**\n\n${format.join('\n')}\n\n:love_letter: Support the bot! http://kaze.rip/donate`
                            client.channels.get(settings['channel']).sendMessage(string);
                        }
                    }
                })

                fs.writeFileSync('cache.json', `{ "time" : "${response[0]['time']}" }`, function(err) {
                    if (err) return console.log(err);
                })
            }
        }
    })
}, 10000, client)

client.login(config.token);