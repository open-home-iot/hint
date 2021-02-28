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
      console.log("Home ID was NOT A NUMBER")
      this.router.navigate(['/page-not-found']);
      return
    }

    this.homeService.getHomeRooms(this.homeID)
      .subscribe(
        (result: Room[]) => {
          console.log(result);
        }
      );
  }
}
