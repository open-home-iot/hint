import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { Room, HomeService } from '../../home.service';

@Component({
  selector: 'app-home-room-overview',
  templateUrl: './home-room-overview.component.html',
  styleUrls: ['./home-room-overview.component.scss']
})
export class HomeRoomOverviewComponent implements OnInit {

  homeID: number;
  rooms: Room[];

  createRoomForm: FormGroup;
  apiError: string;

  constructor(private formBuilder: FormBuilder,
              private route: ActivatedRoute,
              private router: Router,
              private homeService: HomeService) { }

  ngOnInit(): void {
    this.createRoomForm = this.formBuilder.group({
      name: ['', Validators.required]
    });

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
          this.apiError = null;
        },
        error => { this.apiError = error }
      );
  }

  get name() { return this.createRoomForm.get("name"); }

  createRoom() {
    console.log("Chosen room name: " + this.name.value);
  }
}
