import {Component, Input, OnInit} from '@angular/core';
import {Hume} from '../hume.service';

@Component({
  selector: 'app-hume-detail',
  templateUrl: './hume-detail.component.html',
  styleUrls: ['./hume-detail.component.scss']
})
export class HumeDetailComponent implements OnInit {

  @Input() hume: Hume;

  constructor() { }

  ngOnInit(): void {
  }

}
