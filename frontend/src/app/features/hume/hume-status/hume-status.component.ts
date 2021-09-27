import {
  Component,
  Input,
  OnChanges,
  OnInit,
  SimpleChanges
} from '@angular/core';
import {Home} from '../../home/home.service';
import {Hume, HumeService} from '../hume.service';

@Component({
  selector: 'app-hume-status',
  templateUrl: './hume-status.component.html',
  styleUrls: ['./hume-status.component.scss']
})
export class HumeStatusComponent implements OnChanges {

  @Input() home: Home;

  humes: Hume[];

  constructor(private humeService: HumeService) { }

  ngOnChanges(changes: SimpleChanges): void {
    this.home = changes.home.currentValue;
    this.humeService.getHomeHumes(this.home.id)
      .then(this.onGetHomeHumes.bind(this))
      .catch(this.onGetHomeHumesFailed);
  }

  private onGetHomeHumes(humes: Hume[]) {
    this.humes = humes;
  }

  private onGetHomeHumesFailed(error) {
    console.error(error);
  }
}
