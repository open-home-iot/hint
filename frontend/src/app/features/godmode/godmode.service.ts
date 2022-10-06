import { Injectable } from '@angular/core';
import {Home} from '../home/home.service';
import {HttpClient, HttpParams} from '@angular/common/http';
import {PaginatedResponse} from '../../core/model';
import {Hume} from '../hume/hume.service';

const HOMES_URL = window.location.origin + '/api/godmode/homes';
const TEST_URL = window.location.origin + '/api/godmode/latency-test';

export interface PaginatedHomes extends PaginatedResponse {
  results: Home[];
}

// Only provided in the godmode module scope, not root.
@Injectable()
export class GodmodeService {

  constructor(private httpClient: HttpClient) { }

  public listHomes(): Promise<PaginatedHomes> {
    return this.sendRequest(HOMES_URL);
  }

  public paginate(nextOrPreviousUrl: string): Promise<PaginatedHomes> {
    return this.sendRequest(nextOrPreviousUrl);
  }

  public getHumes(home: Home): Promise<Hume[]> {
    return new Promise<Hume[]>((resolve, reject) => {
      this.httpClient.get(this.getHumesUrl(home))
        .subscribe(
          (humes: Hume[]) => resolve(humes),
          error => reject(error),
        );
    });
  }

  public latencyTest(humes: Hume[]): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.httpClient.get(TEST_URL, { params: this.buildParams(humes) })
        .subscribe(
          (() => resolve()),
          error => reject(error)
        );
    });
  }

  private getHumesUrl(home: Home): string {
    return HOMES_URL + '/' + home.id + '/humes';
  }

  private sendRequest(url: string): Promise<PaginatedHomes> {
    return new Promise<PaginatedHomes>((resolve, reject) => {
      this.httpClient.get(url)
        .subscribe(
          (homes: PaginatedHomes) => resolve(homes),
          error => reject(error),
        );
    });
  }

  private buildParams(humes: Hume[]): HttpParams {
    let humesString = humes[0].uuid;
    for (let hume of humes.slice(1, humes.length-1)) {
      humesString += ',' + hume.uuid;
    }
    return new HttpParams().set("humes", humesString);
  }
}
