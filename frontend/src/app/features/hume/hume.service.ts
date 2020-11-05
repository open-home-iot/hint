import { Injectable } from '@angular/core';

import { HttpService } from '../../core/http/http.service';


const HUME_URL = window.location.origin + "/api/humes/";

const HOME_URL = window.location.origin + "/api/homes/";

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
      this.httpService.get(HUME_URL + uuid)
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

  private humePairUrl(humeId: number): string {
    return HUME_URL + String(humeId) + "/confirm-pairing";
  }

  pairHume(homeId: number, humeId: number) {
    this.httpService.put(this.humePairUrl(humeId), {})
      .subscribe(
        () => {
          this.humePaired(homeId, humeId);
        },
        () => {
          console.log("HUME pairing failed.")
        }
      );
  }

  humePaired(homeId: number, humeId: number) {
    let humes = this.humes[homeId]

    for (let hume of humes) {
      if (hume.id == humeId) {
        hume.is_paired = true;
      }
    }
  }
}
