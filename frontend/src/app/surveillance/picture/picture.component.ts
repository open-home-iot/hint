import {Component, Input, OnInit} from '@angular/core';
import { ActivatedRoute } from "@angular/router";


@Component({
  selector: 'app-picture',
  templateUrl: './picture.component.html',
  styleUrls: ['./picture.component.css']
})
export class PictureComponent implements OnInit {
  imageSrc: string;
  staticUrl = 'http://' + window.location.hostname + ':8000' + '/static/alarm_pictures/';

  constructor(private route: ActivatedRoute) { }

  ngOnInit() {
    this.route.params.subscribe(params => {
      let month = params['src'].substr(0, 7); // Substring out yyyy_mm

      this.imageSrc = this.staticUrl + month + '/' + params['src'];
    })
  }

}
