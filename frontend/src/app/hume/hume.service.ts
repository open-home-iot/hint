import { Injectable } from '@angular/core';

@Injectable()
export class HumeService {
  id: number = 1;
  humes: string[] = ["Hub " + this.id.toString()];

  addHume(name: string) {
    this.id++;
    this.humes.push(name + " " + this.id.toString());
  }

  getAllHumes() {
    return this.humes;
  }
}
