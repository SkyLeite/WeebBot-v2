import config from "../config";
import * as Winston from "winston";
import fetch from "node-fetch";
import path from "path";
import BaseWorker from "../worker";
import * as Discord from "discord.js";
import * as Knex from "knex";
import { IEQ, IDBChannel } from "../types";

export default class EQWorker extends BaseWorker {
  cachePath = path.join(__dirname, "../../", "cache.json");
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
    const eqs: IEQ[] = this.data[0].eqs;
    const channelEQs = eqs.filter(eq => ships.includes(eq.ship));
    if (channelEQs.length === 0) { return; }

    const embed = this.buildMessage(channelEQs, ships);

    try {
      this.logger.info(`Sending alert to channel ${alertChannel.name} from guild ${guild.id} with ships ${ships}`);
      await alertChannel.send(undefined, embed);
    } catch (err) {
      this.logger.warn(err);
    }
  }
}