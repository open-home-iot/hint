import {Component, OnDestroy, OnInit} from '@angular/core';
import {
  animate,
  query,
  sequence,
  stagger, style,
  transition,
  trigger
} from '@angular/animations';

@Component({
  selector: 'app-icon',
  templateUrl: './icon.component.html',
  styleUrls: ['./icon.component.scss'],
  animations: [
    trigger('wifiPulse', [
      transition('* => active', [
        query('.wifi', [
          sequence([
            stagger(100,
              animate('0.25s', style({opacity: 0.8}))
            ),
            stagger(100,
              animate('0.25s', style({opacity: 0.2}))
            ),
          ]),
        ]),
      ]),
    ]),
  ],
})
export class IconComponent implements OnInit, OnDestroy {

  intervalTimer: number;
  wifiPulse = false;

  constructor() { }

  ngOnInit(): void {
    this.intervalTimer = setInterval(() => {
      this.wifiPulse = !this.wifiPulse;
    }, 1200);
  }
  ngOnDestroy() {
    clearInterval(this.intervalTimer);
  }
}
