import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

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

@Injectable()
export class DeviceService {

  constructor(private httpClient: HttpClient) { }
}
