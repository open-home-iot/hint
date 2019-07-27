import { Injectable } from '@angular/core';

@Injectable()
export class HomeService {
  id: number = 1;
  homes: string[] = ["Home " + this.id.toString()];

  addHome(name: string) {
    this.id++;
    this.homes.push(name + " " + this.id.toString());
  }

  getAllHomes() {
    return this.homes;
  }
}
