import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { EventService } from '../event/event.service';

const HOMES_URL = window.location.origin + "/api/homes/"

export class Home {
  id: number;
  name: string;
}

export class Room {
  id: number;
  name: string;

  constructor(id: number, name: string) {
    this.id = id;
    this.name = name;
  }
}

@Injectable()
export class HomeService {

  homes: Home[] = [];
  rooms: Room[] = [];

  constructor(private httpClient: HttpClient,
              private eventService: EventService) {
    this.httpClient.get(HOMES_URL)
      .subscribe(
        (homes: Home[]) => {
          for (let home of homes) {
            this.addHome(home);
          }
        },
        error => {
          console.error(error);
        }
      );
  }

  addHome(home: Home) {
    this.homes.push(home);

    // This ensures that we get dynamic updates for the new homeId
    this.eventService.monitorHome(home.id);
  }

  createHome(name: string) {
    this.httpClient.post(HOMES_URL, {name: name})
      .subscribe(
        (home: Home) => {
          this.addHome(home);
        },
        error => {
          console.error(error);
        }
      );
  }

  private addRoom(room: Room) {
    this.rooms.push(room);
  }

  private addRooms(rooms: Room[]) {
    for (let room of rooms) {
      this.addRoom(room);
    }
  }

  private getHomeRoomsUrl(homeID: number) {
    return HOMES_URL + String(homeID) + "/rooms";
  }

  getHomeRooms(homeID: number): Promise<Room[]> {
    if (this.rooms.length > 0) {
      return Promise.resolve(this.rooms);
    }

    // No rooms gotten yet, getting rooms...
    return new Promise<Room[]>((resolve, reject) => {
      this.httpClient.get(this.getHomeRoomsUrl(homeID))
        .subscribe(
          (rooms: Room[]) => {
            this.addRooms(rooms);
            resolve(this.rooms);
          },
          error => {
            reject(error)
          }
        );
    });
  }

  createRoom(homeID: number, roomName: string): Promise<Room> {
    return new Promise<Room>((resolve, reject) => {
      this.httpClient.post(this.getHomeRoomsUrl(homeID),
                     {"name": roomName})
        .subscribe(
          (room: Room) => {
            this.addRoom(room);
            resolve(room);
          },
          error => {
            reject(error);
          }
        );
    });
  }
}
