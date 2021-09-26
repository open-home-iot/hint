import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {Home} from '../home.service';

@Component({
  selector: 'app-home-select',
  templateUrl: './home-select.component.html',
  styleUrls: ['./home-select.component.scss']
})
export class HomeSelectComponent implements OnInit {

  @Input() selectedHome: Home;
  @Input() homes: Map<number, Home>;
  @Output() homeSelected = new EventEmitter<Home>();

  constructor() { }

  ngOnInit(): void { }

  selectHome(home: Home) {
    this.homeSelected.emit(home);
  }
}
