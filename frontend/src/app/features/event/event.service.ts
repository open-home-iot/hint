import { Injectable } from '@angular/core';

@Injectable()
export class EventService {
  id: number = 1;
  events: string[] = ["Event " + this.id.toString()];

  addDevice(name: string) {
    this.id++;
    this.events.push(name + " " + this.id.toString());
  }

  getAllDevices() {
    return this.events;
  }
}
