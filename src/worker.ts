import { IConfig, IDBChannel, IEQ } from "./types";
import { promisify } from "util";
import { readFile } from "fs";
import path from "path";
import * as Discord from "discord.js";
import * as Knex from "knex";
import config from "./config";
import * as Winston from "winston";
import fetch from "node-fetch";

export default abstract class BaseWorker {
  public data: any;
  public channels!: IDBChannel[];
  public connection: Knex;
  public client: Discord.Client;

  abstract fetchData(): any;
  abstract sendAlert(channel: IDBChannel): Promise<void>;
  abstract cachePath: string;
  abstract identifier: string;

  constructor(connection: Knex, client: Discord.Client) {
    this.connection = connection;
    this.client = client;
  }

  private async readCache() {
    const readFileAsync = promisify(readFile);
    const cache = await readFileAsync(this.cachePath, "utf8");
    return cache;
  }

  private async shouldAlert() {
    const cache = await this.readCache();
    return cache !== this.identifier;
  }

  private async fetchChannels() {
    this.channels = await this.connection("alerts")
      .select("*");
  }

  public async init() {
    await this.fetchData();
    if (!await this.shouldAlert()) { return; }

    await this.fetchChannels();
    const promises = this.channels.map(channel => this.sendAlert(channel));
    await Promise.all(promises);
  }
}

export class EQWorker extends BaseWorker {
  cachePath = path.join(__dirname, "../", "cache.json");
  logger: Winston.Logger;
  identifier = "";

  constructor(connection: Knex, client: Discord.Client, logger: Winston.Logger) {
    super(connection, client);
    this.logger = logger;
  }

  async fetchData() {
    const response = await fetch(config.apiUrl);
    if (response.status === 200) {
      const data = await response.json();
      this.identifier = data[0].time;
      this.data = data;
    } else {
      throw new Error("Could not fetch API. Status code: " + response.status);
    }
  }

  private buildMessage(eqs: IEQ[], ships: number[]) {
    const embed = new Discord.RichEmbed();
    embed.setAuthor("PSO2 Emergency Quest Alert", "https://images.emojiterra.com/mozilla/512px/231a.png");
    embed.setColor("GREEN");
    embed.setFooter("Help: https://bit.ly/2KRb1De");

    eqs
      .filter(eq => ships.includes(eq.ship))
      .forEach(eq => {
        embed.addField(`Ship ${eq.ship}`, eq.name, true);
      });

    return embed;
  }

  async sendAlert(channel: IDBChannel) {
    const ships = channel.ships.split(",").map(Number); // Oh god why
    if (!ships || ships.length === 0) { return; }

    const guild = this.client.guilds.find(guild => guild.id === channel.guildId);
    if (!guild) { return; }

    const alertChannel = guild.channels.find(guildChannel => guildChannel.id === channel.channelId) as Discord.TextChannel;

    if (!alertChannel) { return; }

    const embed = this.buildMessage(this.data[0].eqs, ships);

    try {
      this.logger.info(`Sending alert to channel ${alertChannel.name} from guild ${guild.id} with ships ${ships}`);
      console.log("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
      await alertChannel.send(undefined, embed);
    } catch (err) {
      this.logger.warn(err);
    }
  }
}