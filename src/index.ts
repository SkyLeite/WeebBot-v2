import * as Discord from "discord.js";
import * as fs from "fs";
import * as path from "path";
import knex from "knex";
import * as winston from "winston";
import { IConfig, IModuleParams } from "./types";
import config from "./config";
import DiscordTransporter from "./discordTransporter";
import { EQWorker } from "./worker";

const client = new Discord.Client();
const db = knex(config.database);
const logger = winston.createLogger({
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.printf(info => {
      return `[${info.timestamp}] ${info.level}: ${info.message}`;
    })
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: "WeebBot.log" }),
    new DiscordTransporter({ client, guildName: config.log.guild, channelName: config.log.channel }),
  ]
});

client.on("ready", () => {
  client.user.setPresence(config.presence);
  logger.info("Client ready");
});

logger.info("Starting bot...");
// Load modules
const moduleParameters: IModuleParams = {
  client,
  config,
  db,
  logger
};

const modulesDir = path.join(__dirname, "modules");
const modules = fs.readdirSync(modulesDir)
  .filter((file: string) => file.endsWith(".js"));

// modules.forEach(module => {
//   try {
//     require(path.join(modulesDir, module)).default(moduleParameters);
//     logger.info("Loaded module " + module);
//   } catch (err) {
//     logger.error("Could not load module" + module);
//   }
// });

const eq = new EQWorker(db, client, logger);
client.setInterval(() => eq.init(), 3000);

client.login(config.token);
