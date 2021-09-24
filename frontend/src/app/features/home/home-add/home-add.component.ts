import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { HomeService, Home } from '../home.service';

@Component({
  selector: 'app-home-add',
  templateUrl: './home-add.component.html',
  styleUrls: ['./home-add.component.scss']
})
export class HomeAddComponent implements OnInit {

  displayAddHomeForm = false;
  addHomeForm: FormGroup;

  @Output() onAddHome = new EventEmitter<Home>();

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
    this.onAddHome.emit(home);
    this.toggleAddHomeForm();
  }

  private onCreateHomeFailed(error) {
    console.error(error);
  }
}
