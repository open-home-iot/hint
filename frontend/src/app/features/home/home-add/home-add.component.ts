import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { HomeService } from '../home.service';

@Component({
  selector: 'app-home-add',
  templateUrl: './home-add.component.html',
  styleUrls: ['./home-add.component.scss']
})
export class HomeAddComponent implements OnInit {

  displayAddHomeForm = false;
  addHomeForm: FormGroup;

  constructor(private formBuilder: FormBuilder,
              private homeService: HomeService) { }

  ngOnInit() {
    this.addHomeForm = this.formBuilder.group({
      name: ['', Validators.required]
    });
  }

  get name() { return this.addHomeForm.get('name'); }

  createHome() {
    this.homeService.createHome(this.name.value);
    this.toggleAddHomeForm();
  }

  toggleAddHomeForm() {this.displayAddHomeForm = !this.displayAddHomeForm;}
}
