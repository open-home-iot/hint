import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HomeService } from '../home/home.service';
import {Hume, HumeService} from '../hume/hume.service';
import {
  EventService,
  ALL_HUMES,
  DEVICE_ATTACHED,
  HumeEvent
} from '../event/event.service';
import {HANDLE_ERROR} from '../../core/utility';

export interface DiscoveredDevice {
  name: string;
  hume: string;
  identifier: string;
}

export interface AttachedDevice {
  identifier: string;
  success: boolean;
}

export interface Device {
  name: string;
  address: string;
  uuid: string;
  hume: string; // UUID
  is_attached: boolean;
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

const HOMES_URL = window.location.origin + '/api/homes/';

@Injectable()
export class DeviceService {

  private homeDevices = new Map<number, Device[]>();

  constructor(private homeService: HomeService,
              private humeService: HumeService,
              private eventService: EventService,
              private httpClient: HttpClient) {
    this.eventService.subscribe(
      ALL_HUMES, DEVICE_ATTACHED, this.onDeviceAttached.bind(this)
    );
  }

  private static getHomeDevicesUrl(homeID: number) {
    return HOMES_URL + String(homeID) + '/devices';
  }

  private static getDeviceActionUrl(hume: Hume, device: Device): string {
    return HOMES_URL + hume.home + '/humes/' + hume.uuid + '/devices/' +
      device.uuid + '/action';
  }

  private static deviceUrl(hume: Hume, device: Device): string {
    return HOMES_URL + String(hume.home) + '/humes/' + hume.uuid + '/devices/' + device.uuid;
  }

  /**
   * Requests devices for the input home if not already gotten and returns
   * the result.
   *
   * @param homeID
   */
  getHomeDevices(homeID: number): Promise<Device[]> {
    if (this.homeDevices.has(homeID)) {
      return Promise.resolve(this.homeDevices.get(homeID));
    }

    return this.requestHomeDevices(homeID);
  }

  /**
   * Requests devices for the input home and returns the result.
   *
   * @param homeID
   */
  refreshHomeDevices(homeID: number): Promise<Device[]> {
    return this.requestHomeDevices(homeID);
  }

  delete(device: Device): Promise<Device> {
    return new Promise<Device>((resolve, reject) => {
      const HUME = this.humeService.getHume(device.hume);
      this.httpClient.delete(DeviceService.deviceUrl(HUME, device))
        .subscribe(
          _success => {
            this.removeHomeDevice(HUME.home, device);
            resolve(device);
          },
          error => {
            reject(error);
          }
        );
    });
  }

  changeState(device: Device, newState: DeviceState) {
    const HUME = this.humeService.getHume(device.hume);

    this.httpClient.post(DeviceService.getDeviceActionUrl(HUME, device), {
      device_state_group_id: newState.device_state_group.group_id,
      device_state_id: newState.state_id,
    })
      .subscribe(
        _success => null,
        error => { HANDLE_ERROR(error); }
      );
  }

  private requestHomeDevices(homeID: number): Promise<Device[]> {
    return new Promise<Device[]>((resolve, reject) => {
      this.httpClient.get(DeviceService.getHomeDevicesUrl(homeID))
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

  private addHomeDevice(homeID: number, device: Device) {
    this.homeDevices.get(homeID).push(device);
  }

  private removeHomeDevice(homeID: number, device: Device) {
    const HOME_DEVICES = this.homeDevices.get(homeID);
    HOME_DEVICES.splice(HOME_DEVICES.indexOf(device), 1);
  }

  private replaceHomeDevices(homeID: number, devices: Device[]) {
    if (!this.homeDevices.has(homeID)) {
      this.homeDevices.set(homeID, []);
    }

    // Maintain array reference
    this.homeDevices.get(homeID).length = 0;
    for (const DEVICE of devices) {
      this.addHomeDevice(homeID, DEVICE);
    }
  }

  private onDeviceAttached(event: HumeEvent) {
    const ATTACH_EVENT = event.content as AttachedDevice;

    if (ATTACH_EVENT.success) {
      const HUME = this.humeService.getHume(event.hume_uuid);
      this.requestHomeDevices(HUME.home);
    } else {
      HANDLE_ERROR("failed to attach " + ATTACH_EVENT.identifier);
    }
  }
}
