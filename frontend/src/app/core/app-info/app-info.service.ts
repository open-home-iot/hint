import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';

const REVISION_URL = window.location.origin + '/revision';

interface AppInfoInt {
  tag: string;
  commit_id: string;
}

export class AppInfo implements AppInfoInt {
  tag: string;
  commit_id: string;
}

@Injectable({
  providedIn: 'root'
})
export class AppInfoService {

  appInfo = new AppInfo();

  constructor(private httpClient: HttpClient) {
    this.httpClient.get(REVISION_URL)
      .subscribe(
        (appInfo: AppInfoInt) => {
          console.log(appInfo);
          this.appInfo.tag = appInfo.tag;
          this.appInfo.commit_id = appInfo.commit_id;
        },
        error => {
          console.error(error);
        }
      );
  }
}
