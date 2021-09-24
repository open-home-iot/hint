import {Component, Input, OnInit} from '@angular/core';
import {Home} from '../home.service';

@Component({
  selector: 'app-home-detail',
  templateUrl: './home-detail.component.html',
  styleUrls: ['./home-detail.component.scss']
})
export class HomeDetailComponent implements OnInit {

  @Input() home: Home;

  constructor() { }

  ngOnInit(): void {
  }
}
