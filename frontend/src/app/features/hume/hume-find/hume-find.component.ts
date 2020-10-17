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
  associateHumeForm: FormGroup;

  foundHume: Hume;

  constructor(private formBuilder: FormBuilder,
              private humeService: HumeService) { }

  ngOnInit() {
    this.findHumeForm = this.formBuilder.group({
      uuid: ['', Validators.required]
    });
    this.associateHumeForm = this.formBuilder.group({
      home_id: ['', Validators.required]
    });
  }

  get uuid() { return this.findHumeForm.get('uuid'); }
  get homeId() { return this.associateHumeForm.get('home_id'); }

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

  associateHume() {
    var promise = this.humeService.associateHume(this.foundHume.id,
                                                 this.homeId.value);

    promise.then(
      () => {
        console.log("Successfully associated HUME!");
      },
      () => {
        console.log("Failed to associate HUME!");
      }
    );
  }
}
