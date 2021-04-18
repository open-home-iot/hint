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
    this.userService.getUser()
      .then(this.onGetUser.bind(this))
      .catch(this.onGetUserFailed);
  }

  private onGetUser(user: User): void {
    this.user = user;
  }

  private onGetUserFailed(error) {
    console.error(error);
  }
}
