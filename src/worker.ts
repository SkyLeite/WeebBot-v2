import { IDBChannel } from "./types";
import { promisify } from "util";
import { readFile, writeFile } from "fs";
import * as Discord from "discord.js";
import * as Knex from "knex";

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

  private async writeCache() {
    const writeFileAsync = promisify(writeFile);
    return writeFileAsync(this.cachePath, this.identifier);
  }

  public async init() {
    await this.fetchData();
    if (!await this.shouldAlert()) { return; }

    await this.fetchChannels();
    const promises = this.channels.map(channel => this.sendAlert(channel));
    Promise.all(promises);
    
    await this.writeCache();
  }
}