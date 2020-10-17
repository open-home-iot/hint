import { Injectable } from '@angular/core';

import { HttpService } from '../../core/http/http.service';


const HUME_URL = window.location.origin + "/api/hume/";
const HUME_FIND_URL = HUME_URL + "find";

export class Hume {
  id: number;
  uuid: string;
  name: string;
  heartbeat: string;
  is_paired: boolean;
  ip_address: string;
  home: string;
}

@Injectable()
export class HumeService {

  constructor(private httpService: HttpService) {
    console.log("Constructing HumeService");
  }

  findHume(uuid: string) {
    return new Promise((resolve, reject) => {
      this.httpService.getWithOptions(HUME_FIND_URL,
                                      { params: { "hume_uuid": uuid } })
        .subscribe(
          (hume: Hume) => {
            resolve(hume);
          },
          error => {
            reject();
          }
        );
    });
  }

  humeAssociateUrl(id) {
    return HUME_URL + String(id) + "/associate"
  }

  associateHume(id: number, homeId: number): Promise<{}> {
    return new Promise((resolve, reject) => {
      this.httpService.post(this.humeAssociateUrl(id), { "home_id": homeId })
        .subscribe(
          success => {
            console.log("HUME associate succeeded!");
            resolve();
          },
          error => {
            console.log("HUME associated failed.");
            reject();
          }
        );
    });
  }
}
