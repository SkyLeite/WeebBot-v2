import { IModuleParams } from "../types";
import fetch from "node-fetch";

export default ({ client, config, db, logger }: IModuleParams) => {
  client.on("message", async (message) => {
    if (message.content === "+cat") {
      const response = await fetch("http://edgecats.net/random");
      if (response.status !== 200) {
        return message.reply("Something went wrong. Please try again later.");
      }

      const data = await response.text();
      message.reply("Here's your :cat:! " + data);
    }
  });
}