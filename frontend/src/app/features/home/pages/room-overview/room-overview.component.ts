import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

import { Room, HomeService } from '../../home.service';

@Component({
  selector: 'app-room-overview',
  templateUrl: './room-overview.component.html',
  styleUrls: ['./room-overview.component.scss']
})
export class RoomOverviewComponent implements OnInit {

  homeID: number;
  rooms: Room[];

  constructor(private route: ActivatedRoute,
              private router: Router,
              private homeService: HomeService) { }

  ngOnInit(): void {
    this.homeID = Number(this.route.snapshot.paramMap.get('id'));
    if (isNaN(this.homeID)) {
      console.error('Home ID was NOT A NUMBER');
      this.router.navigate(['/page-not-found']);
      return;
    }

    this.homeService.getHomeRooms(this.homeID)
      .then(this.onGetRooms.bind(this))
      .catch(this.onGetRoomsFailed);
  }

  onRoomCreated(room: Room) {
    //this.rooms.push(room);
  }

  private onGetRooms(rooms: Room[]) {
    this.rooms = rooms;
  }

  private onGetRoomsFailed(error) {
    console.error('Get rooms failed: ', error);
  }
}
