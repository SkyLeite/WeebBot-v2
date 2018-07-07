import { IModuleParams, IEQData, IDBChannel, IEQ } from "../types";
import fetch from "node-fetch";
import * as fs from "fs";
import * as path from "path";
import { promisify } from "util"
import * as Discord from "discord.js";

export default ({ client, config, db, logger }: IModuleParams) => {
  const readFile = promisify(fs.readFile);
  const writeFile = promisify(fs.writeFile);

  const cachePath = path.join(__dirname, "../../", "cache.json");

  const fetchApi = async () => {
    const response = await fetch(config.apiUrl);
    if (response.status === 200) {
      const data = await response.json();
      return data;
    } else {
      throw new Error("Could not fetch API. Status code: " + response.status);
    }
  }

  const readCache = async () => {
    const cacheData = JSON.parse(await readFile(cachePath, "utf8"));
    return cacheData;
  }

  const buildMessage = (eqs: IEQ[], ships: number[]) => {
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

  const updateCache = async (eq: IEQData) => {
    const cachePath = path.join(__dirname, "../../", "cache.json");
    await writeFile(cachePath, JSON.stringify(eq));
  };
  
  const eqModule = async () => {
    const eqData: IEQData[] = await fetchApi();
    const lastCachedEq = await readCache();
    const lastEq = eqData[0];
    const allChannels: IDBChannel[] = await db("alerts")
      .select("*");

    // Alert has already been sent
    if (lastEq.time === lastCachedEq.time) { return; }

    logger.info("New EQ!");
    await Promise.all(allChannels.map(async (channel) => {
      const ships = channel.ships.split(",").map(Number); // Oh god why
      if (!ships) { return; }

      const guild = client.guilds.find(guild => guild.id === channel.guildId);
      if (!guild) { return; }

      const alertChannel = guild.channels.find(guildChannel => guildChannel.id === channel.channelId) as Discord.TextChannel;

      if (!alertChannel) { return; }

      const embed = buildMessage(lastEq.eqs, ships);

      try {
        logger.info(`Sending alert to channel ${alertChannel.name} from guild ${guild.id} with ships ${ships}`);
        await alertChannel.send(undefined, embed);
      } catch (err) {
        logger.error(err);
        // :D?
      }
    }));

    await updateCache(lastEq);
  }

  client.on("message", (message) => {
    if (message.isMentioned(client.user) && message.content.includes("help")) {
      message.reply("Visit http://wb.rodrigo.li for help!");
    }
  });
  
  client.setInterval(eqModule, 30000);
}