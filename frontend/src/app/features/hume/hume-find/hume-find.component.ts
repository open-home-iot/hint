import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { HumeService, Hume } from '../hume.service';

@Component({
  selector: 'app-hume-find',
  templateUrl: './hume-find.component.html',
  styleUrls: ['./hume-find.component.scss']
})
export class HumeFindComponent implements OnInit {

  findHumeForm: FormGroup;
  pairHumeForm: FormGroup;

  foundHume: Hume;

  constructor(private formBuilder: FormBuilder,
              private humeService: HumeService) { }

  ngOnInit() {
    this.findHumeForm = this.formBuilder.group({
      uuid: ['', Validators.required]
    });
    this.pairHumeForm = this.formBuilder.group({
      home_id: ['', Validators.required]
    });
  }

  get uuid() { return this.findHumeForm.get('uuid'); }
  get homeId() { return this.pairHumeForm.get('home_id'); }

  findHume() {
    const PROMISE = this.humeService.findHume(this.uuid.value);

    PROMISE.then(
      (hume: Hume) => {
        this.foundHume = hume;
      },
      error => {
        console.error(error);
      }
    );
  }

  pairHume() {
    this.humeService.pairHume(this.homeId.value, this.foundHume);
  }
}
