import { Injectable } from '@angular/core';

@Injectable()
export class StatisticsService {
  id: number = 1;
  statistics: string[] = ["Stat " + this.id.toString()];

  addHume(name: string) {
    this.id++;
    this.statistics.push(name + " " + this.id.toString());
  }

  getAllHumes() {
    return this.statistics;
  }
}
