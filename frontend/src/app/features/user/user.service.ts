import { Injectable } from '@angular/core';

@Injectable()
export class UserService {
  id: number = 1;
  users: string[] = ["User " + this.id.toString()];

  addHume(name: string) {
    this.id++;
    this.users.push(name + " " + this.id.toString());
  }

  getAllHumes() {
    return this.users;
  }
}
