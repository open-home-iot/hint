import {Component, Input, OnInit} from '@angular/core';
import { Room, HomeService } from '../../home/home.service';
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-device-room-selector',
  templateUrl: './device-room-selector.component.html',
  styleUrls: ['./device-room-selector.component.scss']
})
export class DeviceRoomSelectorComponent implements OnInit {

  @Input() roomID: number;
  homeID: number;
  rooms: Room[];

  constructor(private homeService: HomeService,
              private route: ActivatedRoute) { }

  ngOnInit(): void {
    // TODO: this may cause problems in the future, having a nested component
    //  use the paramMap of the route snapshot.
    this.homeID = Number(this.route.snapshot.paramMap.get('id'));

    this.homeService.getHomeRooms(this.homeID)
      .then(this.onGetRooms.bind(this))
      .catch(this.onGetRoomsFailed);
  }

  onGetRooms(rooms: Room[]) {
    this.rooms = rooms;
  }

  onGetRoomsFailed(error) {
    console.error(error)
  }
}
