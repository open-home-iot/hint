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
    console.log("HUME UUID:");
    console.log(this.uuid.value);
    var promise = this.humeService.findHume(this.uuid.value);

    promise.then(
      (hume: Hume) => {
        console.log("Got hume:");
        console.log(hume);
        this.foundHume = hume;
      },
      () => {
        console.log("Find HUME failed!");
      }
    );
  }

  pairHume() {
    this.humeService.pairHume(this.homeId.value, this.foundHume);
  }
}
