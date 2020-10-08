import { Component, OnInit } from '@angular/core';

import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-home-add',
  templateUrl: './home-add.component.html',
  styleUrls: ['./home-add.component.scss']
})
export class HomeAddComponent implements OnInit {

  addHomeForm: FormGroup;

  constructor(private formBuilder: FormBuilder) { }

  ngOnInit() {
    this.addHomeForm = this.formBuilder.group({
      name: ['', Validators.required]
    });
  }

  get name() { return this.addHomeForm.get('name') }

  createHome() {
    console.log("HOME name:");
    console.log(this.name.value);
  }

}
