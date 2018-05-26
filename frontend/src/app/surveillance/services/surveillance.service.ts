import { Injectable } from "@angular/core";

import { BehaviorSubject } from "rxjs/BehaviorSubject";

import { Event, EventHandlerService } from "../../events/services/event-handler.service";
import { RequestService } from "../../api-interface/request.service";
import {HttpParams} from "@angular/common/http";
import {ResultSet} from "../../api-interface/result-set.interface";


const BASE_URL = 'http://' + window.location.hostname + ':8000/api/';

const CONFIG_URL = BASE_URL + 'surveillance_configuration/';
const PICTURE_URL = BASE_URL + 'surveillance_pictures/';
const HISTORY_URL = BASE_URL + 'alarm_history/';


@Injectable()
export class SurveillanceService {
  alarmSubject: BehaviorSubject<boolean>;

  date: Date;

  pictures: string[];
  nextPictures: string;
  previousPictures: string;

  alarmHistory: string[];
  nextHistory: string;
  previousHistory: string;


  constructor(private requestService: RequestService,
              private eventListener: EventHandlerService) {
    console.log("Initiated surveillance service");

    this.alarmSubject = new BehaviorSubject<boolean>(false);

    this.date = new Date();

    this.nextPictures = "hi";
    this.nextHistory = "hi";
    this.previousHistory = "hi";
    this.previousPictures = "hi";

    this.pictures = [];
    this.alarmHistory = [];

    this.sendRequest(PICTURE_URL, this.handlePictureResultSet);
    this.sendRequest(HISTORY_URL, this.handleHistoryResultSet);

    eventListener.events.subscribe(
      (event: Event) => {
          switch (event.type) {
            case 'event.alarm':
              this.alarmSubject.next(event.content == 'on');

              // TODO refresh current picture and history lists
              break;
            default:
              break;
          }
      }
    );

  }

  sendRequest(url: string, callback: (resultSet: ResultSet) => void) {
    this.requestService.get(url, { params: this.getQueryParams(url) })
      .subscribe(
        data => {
          callback(data);
        }
      );
  }

  sendRequestWithOptions(url: string, callback: (resultSet: ResultSet) => void, options: {}) {
    this.requestService.get(url, options)
      .subscribe(
        data => {
          callback(data);
        }
      );
  }

  // Arrow function for scope control since I want the initial object and not the subscribe scope.
  handlePictureResultSet = (data: ResultSet): void => {
    this.nextPictures = data.next;
    this.previousPictures = data.previous;

    this.pictures.length = 0;
    for (const item of data.results) {
      this.pictures.push(item);
    }
  };

  // Arrow function for scope control since I want the initial object and not the subscribe scope.
  handleHistoryResultSet = (data: ResultSet): void => {
    this.nextHistory = data.next;
    this.previousHistory = data.previous;

    this.alarmHistory.length = 0; // empties array
    let results = data.results.map(res => res.date); // map to extract strings

    // NOTE THE DIFFERENCE BETWEEN 'OF' AND 'IN'
    for (const item of results) {
      this.alarmHistory.push(item);
    }
  };

  stepDate(newDate: Date) {
    this.date = new Date(newDate);

    // Create month string to be passed as query parameter
    const newMonth = newDate.getMonth() > 8 ? // since months range from 0 to 9 and month needs to be 2 digits
      (newDate.getMonth() + 1).toString() :
      '0' + (newDate.getMonth() + 1).toString(); // starting with 0 if below 10, 01 02 03 etc.

    const queryParams = new HttpParams()
      .set('month', newMonth)
      .set('year', newDate.getFullYear().toString());

    this.sendRequestWithOptions(PICTURE_URL, this.handlePictureResultSet, { params: queryParams });
    this.sendRequestWithOptions(HISTORY_URL, this.handleHistoryResultSet, { params: queryParams });
  }

  stepPictures(forward: boolean) {
    let url = forward ? this.nextPictures : this.previousPictures;
    this.sendRequest(url, this.handlePictureResultSet);
  }

  stepHistory(forward: boolean) {
    let url = forward ? this.nextHistory : this.previousHistory;
    this.sendRequest(url, this.handleHistoryResultSet);
  }

  getQueryParams(url: string) {
    if (url.indexOf('?') == -1) {
      return new HttpParams(); // no params present, this is the case in first query.
    }

    const filteredUrl = url.substr(url.indexOf('?') + 1, url.length);
    const queryParamStrings = filteredUrl.split('&');

    let queryParams = new HttpParams();

    for (let queryParam of queryParamStrings) {
      let keyVal = queryParam.split('=');
      queryParams = queryParams.set(keyVal[0], keyVal[1]);
    }

    return queryParams;
  }
}
