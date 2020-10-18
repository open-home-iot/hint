import { Injectable } from '@angular/core';

import { HttpService } from '../../core/http/http.service';


const HUME_URL = window.location.origin + "/api/hume/";
const HUME_FIND_URL = HUME_URL + "find";

const HOME_URL = window.location.origin + "/api/home/";

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

  private humes: { [homeId: number]: Hume[]  } = {};

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

  private humeAssociateUrl(id: number): string {
    return HUME_URL + String(id) + "/associate";
  }

  private pushHume(hume: Hume, homeId: number) {
    console.log("Adding HUME: " + hume.uuid + " to homeId: " + homeId);
    if (homeId in this.humes) {
      this.humes[homeId].push(hume);
    } else {
      this.humes[homeId] = [hume];
    }
  }

  private setHumes(humes: Hume[], homeId: number) {
    this.humes[homeId] = humes;
  }

  associateHume(id: number, homeId: number): Promise<{}> {
    return new Promise((resolve, reject) => {
      this.httpService.post(this.humeAssociateUrl(id), { "home_id": homeId })
        .subscribe(
          (hume: Hume) => {
            console.log("HUME associate succeeded!");
            this.pushHume(hume, homeId);
            resolve();
          },
          error => {
            console.log("HUME associated failed.");
            reject();
          }
        );
    });
  }

  private homeHumesUrl(homeId: number): string {
    return HOME_URL + String(homeId) + "/humes";
  }

  initHomeHumes(homeId: number): Hume[] {
    if (homeId in this.humes) {
      return this.humes[homeId];
    } else {
      this.setHumes([], homeId);

      this.httpService.get(this.homeHumesUrl(homeId))
        .subscribe(
          (humes: Hume[]) => {
            console.log("Get HOME HUMEs succeeded:");
            console.log(humes);
            for (let hume of humes) {
              this.pushHume(hume, homeId);
            }
          },
          error => {
            console.log("Get HOME HUMEs failed.");
          }
        );

      return this.humes[homeId];
    }
  }
}
