import { Injectable } from '@angular/core';

export class Device {
  uuid: string
  humeUuid: string
}

@Injectable()
export class DeviceService {
  id: number = 1;
  devices: string[] = ["Device " + this.id.toString()];

  addDevice(name: string) {
    this.id++;
    this.devices.push(name + " " + this.id.toString());
  }

  getAllDevices() {
    return this.devices;
  }
}
