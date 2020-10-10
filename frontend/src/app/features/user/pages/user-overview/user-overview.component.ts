import { Component, OnInit } from '@angular/core';

import { UserService, User } from '../../user.service';


@Component({
  selector: 'app-user-overview',
  templateUrl: './user-overview.component.html',
  styleUrls: ['./user-overview.component.scss']
})
export class UserOverviewComponent implements OnInit {

  user: User;

  constructor(private userService: UserService) { }

  ngOnInit() {
    console.log(this.userService.user);
    this.user = this.userService.user;
  }

}
