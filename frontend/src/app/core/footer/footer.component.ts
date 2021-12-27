import { Component, OnInit } from '@angular/core';
import {
  AppInfo,
  AppInfoService,
} from '../app-info/app-info.service';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss']
})
export class FooterComponent implements OnInit {

  appInfo: AppInfo;

  constructor(private appInfoService: AppInfoService) { }

  ngOnInit() {
    this.appInfo = this.appInfoService.appInfo;
  }
}
