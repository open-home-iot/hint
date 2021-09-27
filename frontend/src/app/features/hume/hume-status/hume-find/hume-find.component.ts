import {
  Component,
  Input,
  OnInit,
} from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { HumeService, Hume } from '../../hume.service';
import { Home } from '../../../home/home.service';

@Component({
  selector: 'app-hume-find',
  templateUrl: './hume-find.component.html',
  styleUrls: ['./hume-find.component.scss']
})
export class HumeFindComponent implements OnInit {

  @Input() humes: Hume[];
  @Input() home: Home;

  findHumeForm: FormGroup;

  showAddHumePrompt = false;

  constructor(private formBuilder: FormBuilder,
              private humeService: HumeService) { }

  ngOnInit() {
    this.findHumeForm = this.formBuilder.group({
      uuid: ['', Validators.required]
    });
  }

  get uuid() { return this.findHumeForm.get('uuid'); }

  openFindHumePrompt() {
    this.showAddHumePrompt = true;
  }

  hideFindHumePrompt() {
    this.showAddHumePrompt = false;
    this.findHumeForm.reset();
  }

  findHume() {
    this.humeService.findHume(this.uuid.value)
      .then(this.onHumeFound.bind(this))
      .catch(this.onFailedToFindHume.bind(this));
  }

  private onHumeFound(hume: Hume) {
    this.humeService.pairHume(this.home.id, hume)
      .then(this.onHumePaired.bind(this))
      .catch(this.onFailedToPairHume.bind(this));
  }

  private onFailedToFindHume(error) {
    this.findHumeForm.setErrors(
      {apifind: 'No hub with that ID exists...'}
    );
    console.error(error);
  }

  private onHumePaired(_hume: Hume) {

  }

  private onFailedToPairHume(error) {
    this.findHumeForm.setErrors(
      {apipair: 'Failed to pair hub'}
    );
    console.error(error);
  }
}
