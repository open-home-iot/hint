import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HomeService } from '../home/home.service';

export interface Device {
  name: string;
  address: string;
  uuid: string;
  hume: string; // UUID
  is_attached: boolean;
  room: number;
  description: string;
  category_name: string;
  type_name: string;
  parent: number;
  states: DeviceState[];
}

export interface DeviceState {
  device_state_group: DeviceStateGroup;
  state_id: number;
  state_name: string;
}

export interface DeviceStateGroup {
  group_id: number;
  group_name: string;
}

const HUMES_URL = window.location.origin + '/api/humes/';
const HOMES_URL = window.location.origin + '/api/homes/';

@Injectable()
export class DeviceService {

  private homeDevices = new Map();
  private roomDevices = new Map();

  constructor(private homeService: HomeService,
              private httpClient: HttpClient) { }

  getHomeDevicesUrl(homeID: number) {
    return HOMES_URL + String(homeID) + '/devices';
  }

  addHomeDevice(homeID: number, device: Device) {
    this.homeDevices.get(homeID).push(device);
  }

  removeHomeDevice(homeID: number, device: Device) {
    const HOME_DEVICES = this.homeDevices.get(homeID);
    HOME_DEVICES.splice(HOME_DEVICES.indexOf(device), 1);
  }

  replaceHomeDevices(homeID: number, devices: Device[]) {
    if (!this.homeDevices.has(homeID)) {
      this.homeDevices.set(homeID, []);
    }

    // Maintain array reference
    this.homeDevices.get(homeID).length = 0;
    for (const DEVICE of devices) {
      this.addHomeDevice(homeID, DEVICE);
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
            reject(error);
          }
        );
    });
  }

  getRoomDevicesUrl(homeID: number, roomID: number) {
    return HOMES_URL + String(homeID) + '/rooms/' + String(roomID) + '/devices';
  }

  addRoomDevice(roomID: number, device: Device) {
    this.roomDevices.get(roomID).push(device);
  }

  removeRoomDevice(roomID: number, device: Device) {
    const ROOM_DEVICES = this.roomDevices.get(roomID);
    ROOM_DEVICES.splice(ROOM_DEVICES.indexOf(device), 1);
  }

  replaceRoomDevices(roomID: number, devices: Device[]) {
    if (!this.roomDevices.has(roomID)) {
      this.roomDevices.set(roomID, []);
    }

    // Maintain array reference
    this.roomDevices.get(roomID).length = 0;
    for (const DEVICE of devices) {
      this.addRoomDevice(roomID, DEVICE);
    }
  }

  getRoomDevices(homeID:number, roomID: number) {
    if (this.roomDevices.has(roomID)) {
      return Promise.resolve(this.roomDevices.get(roomID));
    }

    return new Promise<Device[]>((resolve, reject) => {
      this.httpClient.get(this.getRoomDevicesUrl(homeID, roomID))
        .subscribe(
          (devices: Device[]) => {
            this.replaceRoomDevices(roomID, devices);
            resolve(this.roomDevices.get(roomID));
          },
          error => {
            reject(error);
          }
        );
    });
  }

  getRoomChangeUrl(homeID: number, device: Device) {
    return HOMES_URL + String(homeID) + '/humes/' + String(device.hume) +
      '/devices/' + device.uuid + '/change-room';
  }

  changeRoom(device: Device, roomID: number | null) {
    // TODO: change method of fetching the home ID
    let homeID
    if (roomID !== null) {
      homeID = this.homeService.getRoom(roomID).home;
    } else {
      homeID = this.homeService.getRoom(device.room).home
    }

    this.httpClient.patch(this.getRoomChangeUrl(homeID, device),
                    {old_id: device.room, new_id: roomID})
      .subscribe(
        success => {
          // Check if device's current room is null (meaning it belongs to the
          // HOME).
          if (typeof device.room !== 'number') {
            // Fetch target room to get access to homeID
            const ROOM = this.homeService.getRoom(roomID);
            this.removeHomeDevice(ROOM.home, device);
          } else {
            this.removeRoomDevice(device.room, device);
          }

          // A device can change from belonging to a room to belonging to the
          // home in general.
          if (typeof roomID !== 'number') {
            const ROOM = this.homeService.getRoom(device.room);
            this.addHomeDevice(ROOM.home, device);
          } else {
            this.addRoomDevice(roomID, device);
          }
          // Set the device room
          device.room = roomID;
        },
        error => {
          console.error(error);
        }
      );
  }

  getDeviceActionUrl(device: Device): string {
    return HUMES_URL + device.hume + '/devices/' + device.uuid + '/action';
  }

  changeState(device: Device, newState: DeviceState) {
    this.httpClient.post(this.getDeviceActionUrl(device), {
      device_state_group_id: newState.device_state_group.group_id,
      device_state_id: newState.state_id,
    })
      .subscribe(
        _success => null,
        error => { console.error(error); }
      );
  }
}
