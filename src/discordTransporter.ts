import Transport, { TransportStreamOptions } from "winston-transport";
import { Client, TextChannel, Guild, RichEmbed } from "discord.js";

export default class DiscordTransporter extends Transport {
  private client: Client;
  private guild!: Guild;
  private channel!: TextChannel;

  private guildName: string;
  private channelName: string;

  constructor(opts: any) {
    super(opts);

    this.client = opts.client;
    this.guildName = opts.guildName;
    this.channelName = opts.channelName;
  }

  private findInfo() {
    if (this.client.readyAt != null) {
      this.findGuild();
      this.findChannel();
    }
  }

  private findGuild() {
    if (!this.guild) {
      const guild: Guild | undefined = this.client.guilds.find(i => i.name === this.guildName);
      if (!guild) {
        console.error("No guild found with name " + this.guildName);
        return;
      }
      this.guild = guild;
    }
  }

  private findChannel() {
    if (!this.channel && this.guild) {
      const channel = this.guild.channels
        .filter(i => i.type === "text")
        .find(i => i.name === this.channelName) as TextChannel | undefined;
      if (!channel) {
        console.error("No channel found with name " + this.channelName);
        return;
      }
      this.channel = channel;
    }
  }

  log(info: IInfo, callback: () => void) {
    setImmediate(() => {
      this.emit('logged', info)
    });

    switch (info.level) {
      case "info":
        this.info(info.message);
        callback();
        break;
      case "warn":
        this.warn(info.message);
        callback();
        break;
    }
  }

  info(info: string) {
    this.findInfo();
    if (this.client.readyAt == null) { return; }

    this.channel.send(info);
  }

  warn(info: string, callback?: () => void) {
    this.findInfo();
    if (this.client.readyAt == null) { return; }

    const embed = new RichEmbed();
    embed.setAuthor("Weeb Bot");
    embed.setColor("RED");
    embed.addField("WARNING", info);

    this.channel.send(embed);
  }
}

interface IInfo {
  message: string;
  level: string;
  timestamp: string;
}
