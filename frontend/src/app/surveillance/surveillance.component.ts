import { Component, OnInit } from '@angular/core';

import { RequestService } from '../api-interface/request.service';
import { ResultSet } from "../api-interface/result-set.interface";
import {HttpParams} from "@angular/common/http";


const PICTURE_URL = 'http://' + window.location.hostname + ':8000/api/surveillance/pictures/';

@Component({
  selector: 'app-surveillance',
  templateUrl: './surveillance.component.html',
  styleUrls: ['./surveillance.component.css']
})
export class SurveillanceComponent implements OnInit {
  currentDisplayDate: Date;

  pictures: string[];
  next: string;
  previous: string;

  constructor(private requestService: RequestService) {}

  ngOnInit() {
    this.currentDisplayDate = new Date();

    this.requestPictureList(PICTURE_URL, {}); // No extension gets the current dates pictures
  }

  stepPictureList(forward: boolean) {
    const monthChange = forward ? 1 : -1;
    this.currentDisplayDate.setMonth(this.currentDisplayDate.getMonth() + (monthChange));
    // New date creation since pipes do not update on object change but on reassignment (cloning)
    this.currentDisplayDate = new Date(this.currentDisplayDate);

    // All months below 10 must be prepended with 0.
    const newMonth = this.currentDisplayDate.getMonth() > 8 ? // Because months range from 0 to 11
      (this.currentDisplayDate.getMonth() + 1).toString() :
      '0' + (this.currentDisplayDate.getMonth() + 1).toString();

    // Important to keep queryparams as constants.
    const queryParams = new HttpParams()
      .set('year', this.currentDisplayDate.getFullYear().toString())
      .set('month', newMonth);

    this.requestPictureList(PICTURE_URL, { params: queryParams })
  }

  showOtherResults(url: string) {
    // extract query params from URL string
    const filteredUrl = url.substr(url.indexOf('?') + 1, url.length);
    const queryParamStrings = filteredUrl.split('&');

    let queryParams = new HttpParams();

    for (let queryString of queryParamStrings) {
      let keyVal = queryString.split('=');
      queryParams = queryParams.set(keyVal[0], keyVal[1]);
    }
    
    this.requestPictureList(url,{ params: queryParams});
  }

  requestPictureList(url: string, options: {}) {
    this.requestService.get(PICTURE_URL, options)
      .subscribe(
      data => {
        this.handleResultSet(data);
      }
    );
  }

  handleResultSet(pictureResultSet: ResultSet) {
    this.next = pictureResultSet.next;
    this.previous = pictureResultSet.previous;

    this.pictures = pictureResultSet.results.slice();
  }
}
