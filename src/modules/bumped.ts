import { IModuleParams } from "../types";
import xml2js from "xml2js";
import fetch from "node-fetch";
import { promisify } from "util";
import fs from "fs";
import path from "path";

export default ({ client, config, db, logger }: IModuleParams) => {
  const bumpedURL = "http://www.bumped.org/psublog/feed/";
  
  const parseXml = (data: string) => {
    return new Promise((resolve, reject) => {
      xml2js.parseString(data, (err, result) => {
        if (err) { return reject(err); }
        return resolve(result);
      });
    });
  }

  const readCache = () => {
    const readFile = promisify(fs.readFile);
    return readFile(path.join(__dirname, "../../", "bumpedCache.json"), "utf8");
  }

  const bumpedModule = async () => {
    const response = await fetch(bumpedURL);
    if (response.status !== 200) { return; }

    const data = await response.text();
    const parsedData: any = await parseXml(data);
    const articles = parsedData.rss.channel[0].item;

    const lastArticle = articles[0];
    const cache = JSON.parse(await readCache());

    if (lastArticle.pubDate === cache.pubDate) { return; }

    logger.info("New Bumped!");
  }

  bumpedModule();
}