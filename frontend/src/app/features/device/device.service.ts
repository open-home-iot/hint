import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {HomeService} from "../home/home.service";


export interface Device {
  hume: string; // UUID
  is_attached: boolean;
  room: number;
  uuid: string;
  name: string;
  description: string;
  category_name: string;
  type_name: string;
  parent: number;
}


const HOMES_URL = window.location.origin + "/api/homes/"
const ROOMS_URL = window.location.origin + "/api/rooms/"


@Injectable()
export class DeviceService {

  homeDevices = new Map();
  roomDevices = new Map();

  constructor(private homeService: HomeService,
              private httpClient: HttpClient) { }

  getHomeDevicesUrl(homeID: number) {
    return HOMES_URL + String(homeID) + "/devices";
  }

  addHomeDevice(homeID: number, device: Device) {
    this.homeDevices.get(homeID).push(device);
  }

  removeHomeDevice(homeID: number, device: Device) {
    let homeDevices = this.homeDevices.get(homeID);
    homeDevices.splice(homeDevices.indexOf(device), 1);
  }

  replaceHomeDevices(homeID: number, devices: Device[]) {
    if (!this.homeDevices.has(homeID)) {
      this.homeDevices.set(homeID, []);
    }

    // Maintain array reference
    this.homeDevices.get(homeID).length = 0;
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
            this.replaceHomeDevices(homeID, devices);
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

  removeRoomDevice(roomID: number, device: Device) {
    let roomDevices = this.roomDevices.get(roomID);
    roomDevices.splice(roomDevices.indexOf(device), 1);
  }

  replaceRoomDevices(roomID: number, devices: Device[]) {
    if (!this.roomDevices.has(roomID)) {
      this.roomDevices.set(roomID, []);
    }

    // Maintain array reference
    this.roomDevices.get(roomID).length = 0;
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
            this.replaceRoomDevices(roomID, devices);
            resolve(this.roomDevices.get(roomID));
          },
          error => {
            reject(error)
          }
        );
    });
  }

  changeRoom(device: Device, roomID: number | undefined) {

    if (device.room == undefined) {
      // Fetch target room to get access to homeID
      let room = this.homeService.getRoom(roomID);
      console.log("Old home devices before: ", this.homeDevices.get(room.home));
      this.removeHomeDevice(room.home, device);
      console.log("Old home devices after: ", this.homeDevices.get(room.home));
    } else {
      console.log("Old room devices before: ", this.roomDevices.get(device.room));
      this.removeRoomDevice(device.room, device);
      console.log("Old room devices after: ", this.roomDevices.get(device.room));
    }

    // A device can change from belonging to a room to belonging to the home in
    // general.
    if (roomID == undefined) {
      console.log("Target room non existent, setting as belonging to home.");
      let room = this.homeService.getRoom(device.room);
      console.log("Home devices before: ", this.homeDevices.get(room.home));
      this.addHomeDevice(room.home, device);
      console.log("Home devices after: ", this.homeDevices.get(room.home));
    } else {
      console.log("New room devices before: ", this.roomDevices.get(roomID));
      this.addRoomDevice(roomID, device);
      console.log("New room devices after: ", this.roomDevices.get(roomID));
    }

    // Set the device room
    console.log("Device before: ", device);
    device.room = roomID;
    console.log("Device after: ", device);
  }
}
