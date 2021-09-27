import {Component, Input, OnInit} from '@angular/core';
import {Home} from '../../home/home.service';

@Component({
  selector: 'app-hume-status',
  templateUrl: './hume-status.component.html',
  styleUrls: ['./hume-status.component.scss']
})
export class HumeStatusComponent implements OnInit {

  @Input() home: Home;

  constructor() { }

  ngOnInit(): void {
  }
}
