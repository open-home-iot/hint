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
    const newMonth = this.currentDisplayDate.getMonth() > 8 ?
      (this.currentDisplayDate.getMonth() + 1).toString() :
      '0' + (this.currentDisplayDate.getMonth() + 1).toString();

    // Important to keep queryparams as constants.
    const queryParams = new HttpParams()
      .set('year', this.currentDisplayDate.getFullYear().toString())
      .set('month', newMonth);

    this.requestPictureList(PICTURE_URL, { params: queryParams })
  }

  showOtherResults(url: string) {

  }

  formatPictureList(pictureResultSet: ResultSet) {
    this.next = pictureResultSet.next;
    this.previous = pictureResultSet.previous;

    this.pictures = pictureResultSet.results.slice();
  }

  requestPictureList(url: string, options: {}) {
    this.requestService.get(PICTURE_URL, options)
      .subscribe(
      data => {
        this.formatPictureList(data);
      }
    );
  }
}
