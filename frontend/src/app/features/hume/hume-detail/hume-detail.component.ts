import {Component, Input, OnInit} from '@angular/core';
import {Hume, HumeService} from '../hume.service';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {HANDLE_ERROR} from '../../../core/utility';
import {DeviceService} from '../../device/device.service';

@Component({
  selector: 'app-hume-detail',
  templateUrl: './hume-detail.component.html',
  styleUrls: ['./hume-detail.component.scss']
})
export class HumeDetailComponent implements OnInit {

  @Input() hume: Hume;

  changeHumeNameForm: FormGroup;

  constructor(private formBuilder: FormBuilder,
              private humeService: HumeService,
              private deviceService: DeviceService) { }

  ngOnInit(): void {
    this.changeHumeNameForm = this.formBuilder.group({
      name: ['', [Validators.required, Validators.maxLength(50)]]
    });

    // update input field value to current hume's name.
    this.name.setValue(this.hume.name);
  }

  get name() { return this.changeHumeNameForm.get('name'); }

  changeHumeName() {
    this.humeService.changeName(this.hume, this.name.value)
      .then(this.onChangeHumeName.bind(this))
      .catch(HANDLE_ERROR);
  }

  deleteHume() {
    this.humeService.deleteHume(this.hume)
      .then((deletedHume: Hume) => {
        this.deviceService.refreshHomeDevices(deletedHume.home);
      })
      .catch(HANDLE_ERROR);
  }

  private onChangeHumeName(hume: Hume) {
    this.name.setValue(hume.name);
  }
}
