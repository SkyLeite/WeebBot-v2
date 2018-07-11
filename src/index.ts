import * as Discord from "discord.js";
import * as fs from "fs";
import * as path from "path";
import knex from "knex";
import * as winston from "winston";
import { IModuleParams } from "./types";
import config from "./config";
import DiscordTransporter from "./discordTransporter";

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

modules.forEach(module => {
  try {
    require(path.join(modulesDir, module)).default(moduleParameters);
    logger.info("Loaded module " + module);
  } catch (err) {
    logger.error("Could not load module" + module);
  }
});

// Load workers
const workersDir = path.join(__dirname, "workers");
const workers = fs.readdirSync(workersDir)
  .filter((file: string) => file.endsWith(".js"));

const instanceWorkers = workers.map(async (workerFile) => {
  try {
    const workerClass = (await import(path.join(workersDir, workerFile))).default;
    const worker = new workerClass(db, client, logger);

    client.setInterval(() => worker.init(), 30000);
    logger.info("Loaded worker " + workerFile);
  } catch (err) {
    logger.error(err);
    logger.warn("Could not load worker " + workerFile);
  }
});

Promise.all(instanceWorkers)
  .then(() => client.login(config.token));
