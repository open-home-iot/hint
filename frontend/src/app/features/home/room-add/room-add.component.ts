import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-room-add',
  templateUrl: './room-add.component.html',
  styleUrls: ['./room-add.component.scss']
})
export class RoomAddComponent implements OnInit {

  createRoomForm: FormGroup;
  apiError: string;

  constructor(private formBuilder: FormBuilder) { }

  ngOnInit(): void {
    this.createRoomForm = this.formBuilder.group({
        name: ['', Validators.required]
    });
  }

  get name() { return this.createRoomForm.get("name"); }

  createRoom() {
    console.log("Chosen room name: " + this.name.value);
  }
}
