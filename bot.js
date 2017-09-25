const Commando = require('discord.js-commando');
const path = require('path');
const sqlite = require('sqlite')
const request = require('request');
const fetch = require('node-fetch');
const fs = require('mz/fs');
const moment = require('moment');
const handleEQs = require('./eqs.js');
const handleBumped = require('./bumped.js');

if (!fs.existsSync('./config.json')) {
    fs.writeFileSync('./config.json', '{"token" : "", "prefix" : "!"}')
    console.log('WARNING: Config file is missing. Please edit "config.json" and re-run the script.')
    process.exit()
}

if (!fs.existsSync('./cache.json')) {
    fs.writeFileSync('./cache.json', '{ "time" : "02-19-2017 19:05:04 +0000" }')
}

if (!fs.existsSync('./bumped.json')) {
    fs.writeFileSync('./bumped.json', '{ "isoDate" : "2017-09-22T05:58:27.000Z" }')
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
        if (err instanceof Commando.FriendlyError) return;
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

// EQ / Bumped alerts
client.setInterval(handleEQs, 25000, client);
client.setInterval(handleBumped, 25000, client);

client.login(config.token);
