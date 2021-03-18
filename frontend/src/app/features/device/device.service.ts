import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

const DEVICE_TYPE_NAMES = {
  0: "Thermometer"
};

export class Device {
  hume: string; // UUID
  is_attached: boolean;
  room: number;
  uuid: string;
  name: string;
  description: string;
  category: number;
  type: number;
  custom_type_name: string;
  parent: number;
}

const HOMES_URL = window.location.origin + "/api/homes/"
const ROOMS_URL = window.location.origin + "/api/rooms/"

@Injectable()
export class DeviceService {

  homeDevices = new Map();
  roomDevices = new Map();

  constructor(private httpClient: HttpClient) { }

  getHomeDevicesUrl(homeID: number) {
    return HOMES_URL + String(homeID) + "/devices";
  }

  addHomeDevice(homeID: number, device: Device) {
    this.homeDevices.get(homeID).push(device);
  }

  addHomeDevices(homeID: number, devices: Device[]) {
    if (!this.homeDevices.has(homeID)) {
      this.homeDevices.set(homeID, []);
    }

    for (let device of devices) {
      this.addHomeDevice(homeID, device);
    }
  }

  getHomeDevices(homeID: number) {
    if (this.homeDevices.has(homeID)) {
      return Promise.resolve(this.homeDevices.get(homeID));
    }

    return new Promise<Device[]>((resolve, reject) => {
      this.httpClient.get(this.getHomeDevicesUrl(homeID))
        .subscribe(
          (devices: Device[]) => {
            this.addHomeDevices(homeID, devices);
            resolve(this.homeDevices.get(homeID));
          },
          error => {
            reject(error)
          }
        );
    });
  }

  getRoomDevicesUrl(roomID: number) {
    return ROOMS_URL + String(roomID) + "/devices";
  }

  addRoomDevice(roomID: number, device: Device) {
    this.roomDevices.get(roomID).push(device);
  }

  addRoomDevices(roomID: number, devices: Device[]) {
    if (!this.roomDevices.has(roomID)) {
      this.roomDevices.set(roomID, []);
    }

    for (let device of devices) {
      this.addRoomDevice(roomID, device);
    }
  }

  getRoomDevices(roomID: number) {
    if (this.roomDevices.has(roomID)) {
      return Promise.resolve(this.roomDevices.get(roomID));
    }

    return new Promise<Device[]>((resolve, reject) => {
      this.httpClient.get(this.getRoomDevicesUrl(roomID))
        .subscribe(
          (devices: Device[]) => {
            this.addRoomDevices(roomID, devices);
            resolve(this.roomDevices.get(roomID));
          },
          error => {
            reject(error)
          }
        );
    });
  }
}
