import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { HomeService, Home } from '../home.service';

@Component({
  selector: 'app-home-add',
  templateUrl: './home-add.component.html',
  styleUrls: ['./home-add.component.scss']
})
export class HomeAddComponent implements OnInit {

  @Output() homeAdded = new EventEmitter<Home>();

  displayAddHomeForm = false;
  addHomeForm: FormGroup;

  constructor(private formBuilder: FormBuilder,
              private homeService: HomeService) { }

  ngOnInit() {
    this.addHomeForm = this.formBuilder.group({
      name: ['', [Validators.required, Validators.maxLength(50)]]
    });
  }

  get name() { return this.addHomeForm.get('name'); }

  createHome() {
    this.homeService.createHome(this.name.value)
      .then(this.onCreateHomeSuccess.bind(this))
      .catch(this.onCreateHomeFailed);
  }

  toggleAddHomeForm() {this.displayAddHomeForm = !this.displayAddHomeForm;}

  private onCreateHomeSuccess(home: Home) {
    this.addHomeForm.reset();
    this.homeAdded.emit(home);
    this.toggleAddHomeForm();
  }

  private onCreateHomeFailed(error) {
    console.error(error);
  }
}
