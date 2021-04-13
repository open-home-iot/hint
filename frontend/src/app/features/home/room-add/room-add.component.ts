import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { Room, HomeService } from '../home.service';

@Component({
  selector: 'app-room-add',
  templateUrl: './room-add.component.html',
  styleUrls: ['./room-add.component.scss']
})
export class RoomAddComponent implements OnInit {

  @Input() homeID: number;
  @Output() newRoomEvent = new EventEmitter<Room>();

  createRoomForm: FormGroup;
  apiError: string;

  constructor(private formBuilder: FormBuilder,
              private homeService: HomeService) { }

  ngOnInit(): void {
    this.createRoomForm = this.formBuilder.group({
        name: ['', Validators.required]
    });
  }

  get name() { return this.createRoomForm.get('name'); }

  createRoom() {
    this.apiError = '';
    this.homeService.createRoom(this.homeID, this.name.value)
      .then(this.onRoomCreated.bind(this))
      .catch(this.onRoomCreateFail.bind(this));
  }

  onRoomCreated(room: Room) {
    this.newRoomEvent.emit(room);
  }

  onRoomCreateFail(error) {
    console.error('Room creation failed: ', error);
    if (error.error.name) {
      this.apiError = error.error.name;
    } else {
      this.apiError = 'Something went wrong.';
    }
  }
}
